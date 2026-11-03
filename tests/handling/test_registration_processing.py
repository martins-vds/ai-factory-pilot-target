from concurrent.futures import ThreadPoolExecutor
import logging
from datetime import UTC, datetime, timedelta

import pytest
from django.core.management import call_command
from django.db import OperationalError, close_old_connections

import cargotracker.handling.application.process_registration_attempt as processing
from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.cargo.infrastructure.repository import DjangoCargoRepository
from cargotracker.handling.application.accept_registration import accept_registration
from cargotracker.handling.application.process_registration_attempt import (
    process_registration_attempt,
)
from cargotracker.handling.domain.handling_event import HandlingEventType
from cargotracker.handling.domain.registration_attempt import RegistrationAttempt
from cargotracker.handling.infrastructure.attempt_submission_repository import (
    DjangoAttemptSubmissionRepository,
)
from cargotracker.handling.infrastructure.models import HandlingEventRecord, RegistrationAttemptRecord
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.voyage.domain.voyage_number import VoyageNumber


def _attempt(**overrides):
    fields = {
        'tracking_id': TrackingId('ABC123'),
        'completion_time': datetime.now(UTC) + timedelta(days=1),
        'registration_time': datetime.now(UTC),
        'event_type': HandlingEventType.RECEIVE,
        'location': UnLocode('USNYC'),
    }
    return RegistrationAttempt(**(fields | overrides))


@pytest.mark.django_db
def test_processing_registers_attempt_once_and_rederives_cargo_delivery():
    call_command('seed_sample_data')
    attempt = accept_registration(_attempt(), DjangoAttemptSubmissionRepository())
    events_before = HandlingEventRecord.objects.filter(cargo__tracking_id='ABC123').count()

    assert process_registration_attempt() is True
    assert process_registration_attempt() is False

    attempt_record = RegistrationAttemptRecord.objects.get(pk=attempt.id)
    event = HandlingEventRecord.objects.get(
        cargo__tracking_id='ABC123', event_type='RECEIVE', completion_time=attempt.completion_time.date()
    )
    cargo = DjangoCargoRepository().find(TrackingId('ABC123'))

    assert attempt_record.status == 'registered'
    assert HandlingEventRecord.objects.filter(cargo__tracking_id='ABC123').count() == events_before + 1
    assert cargo.delivery.last_event_id == event.pk
    assert cargo.delivery.transport_status == 'IN_PORT'


@pytest.mark.django_db
@pytest.mark.parametrize(
    ('attempt_changes', 'reason_code'),
    [
        ({'tracking_id': TrackingId('MISSING')}, 'UNKNOWN_CARGO'),
        ({'location': UnLocode('ZZXXX')}, 'UNKNOWN_LOCATION'),
        (
            {
                'event_type': HandlingEventType.LOAD,
                'voyage_number': VoyageNumber('CM999'),
            },
            'UNKNOWN_VOYAGE',
        ),
        ({'event_type': HandlingEventType.LOAD}, 'INVALID_EVENT'),
    ],
)
def test_unknown_references_reject_attempt_without_storing_event(attempt_changes, reason_code):
    call_command('seed_sample_data')
    attempt = accept_registration(
        _attempt(**attempt_changes),
        DjangoAttemptSubmissionRepository(),
    )
    existing_events = HandlingEventRecord.objects.count()

    assert process_registration_attempt() is True

    attempt_record = RegistrationAttemptRecord.objects.get(pk=attempt.id)
    assert attempt_record.status == 'rejected'
    assert attempt_record.rejection_reason.startswith(f'{reason_code}:')
    assert HandlingEventRecord.objects.count() == existing_events


@pytest.mark.django_db
def test_equal_completion_time_uses_registration_order_for_delivered_outcome(caplog):
    call_command('seed_sample_data')
    completion_time = datetime(2026, 11, 3, 12, tzinfo=UTC)
    attempts = DjangoAttemptSubmissionRepository()
    later_registration = accept_registration(
        _attempt(
            completion_time=completion_time,
            registration_time=datetime(2026, 11, 5, 12, tzinfo=UTC),
            event_type=HandlingEventType.UNLOAD,
            location=UnLocode('FIHEL'),
            voyage_number=VoyageNumber('0300A'),
        ),
        attempts,
    )
    earlier_registration = accept_registration(
        _attempt(
            completion_time=completion_time,
            registration_time=datetime(2026, 11, 4, 12, tzinfo=UTC),
            event_type=HandlingEventType.RECEIVE,
            location=UnLocode('USNYC'),
        ),
        attempts,
    )

    with caplog.at_level(logging.INFO):
        assert process_registration_attempt() is True
        assert process_registration_attempt() is True

    later_event = HandlingEventRecord.objects.get(
        cargo__tracking_id='ABC123',
        event_type='UNLOAD',
        registration_time=later_registration.registration_time.date(),
    )
    earlier_event = HandlingEventRecord.objects.get(
        cargo__tracking_id='ABC123',
        event_type='RECEIVE',
        registration_time=earlier_registration.registration_time.date(),
    )
    cargo = DjangoCargoRepository().find(TrackingId('ABC123'))

    assert later_event.pk < earlier_event.pk
    assert cargo.delivery.last_event_id == later_event.pk
    assert cargo.delivery.unloaded_at_destination is True
    assert 'Cargo ABC123 delivered' in [record.getMessage() for record in caplog.records]


@pytest.mark.django_db
def test_temporary_database_failure_retries_atomically_and_logs_after_fifteen_minutes(
    caplog, monkeypatch
):
    call_command('seed_sample_data')
    attempt = accept_registration(_attempt(), DjangoAttemptSubmissionRepository())
    events_before = HandlingEventRecord.objects.filter(cargo__tracking_id='ABC123').count()
    original_upsert = DjangoCargoRepository.upsert
    upsert_calls = 0
    clock = [0.0]
    retry_observations = []

    def fail_before_upsert(self, cargo):
        nonlocal upsert_calls
        upsert_calls += 1
        if upsert_calls <= 25:
            raise OperationalError('temporary database failure')
        return original_upsert(self, cargo)

    def advance_clock(seconds):
        clock[0] += seconds
        retry_observations.append(
            (
                RegistrationAttemptRecord.objects.get(pk=attempt.id).status,
                HandlingEventRecord.objects.filter(cargo__tracking_id='ABC123').count(),
            )
        )

    monkeypatch.setattr(DjangoCargoRepository, 'upsert', fail_before_upsert)
    monkeypatch.setattr(processing, 'monotonic', lambda: clock[0], raising=False)
    monkeypatch.setattr(processing, 'sleep', advance_clock, raising=False)

    with caplog.at_level(logging.ERROR, logger=processing.__name__):
        assert process_registration_attempt() is True

    attempt_record = RegistrationAttemptRecord.objects.get(pk=attempt.id)
    assert attempt_record.status == 'registered'
    assert HandlingEventRecord.objects.filter(cargo__tracking_id='ABC123').count() == events_before + 1
    assert upsert_calls == 26
    assert clock[0] >= 900
    assert retry_observations
    assert set(retry_observations) == {('accepted', events_before)}
    assert any('after 15 minutes' in record.getMessage() for record in caplog.records)


@pytest.mark.django_db(transaction=True)
def test_concurrent_processing_claims_an_attempt_only_once():
    call_command('seed_sample_data')
    attempt = accept_registration(_attempt(), DjangoAttemptSubmissionRepository())
    events_before = HandlingEventRecord.objects.filter(cargo__tracking_id='ABC123').count()

    def process_in_thread():
        close_old_connections()
        try:
            return process_registration_attempt()
        finally:
            close_old_connections()

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(lambda _: process_in_thread(), range(2)))

    assert results.count(True) == 1
    assert RegistrationAttemptRecord.objects.get(pk=attempt.id).status == 'registered'
    assert HandlingEventRecord.objects.filter(cargo__tracking_id='ABC123').count() == events_before + 1
