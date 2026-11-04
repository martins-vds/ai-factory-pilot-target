import json
import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta
from math import isfinite

import pytest
from django.core.management import CommandError, call_command
from django.db import OperationalError, close_old_connections

import cargotracker.handling.application.process_registration_attempt as processing
import cargotracker.handling.interfaces.rest as handling_rest
import cargotracker.handling.management.commands.process_handling_attempts as worker
from cargotracker.cargo.application import sample_data
from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.cargo.infrastructure.repository import DjangoCargoRepository
from cargotracker.cargo.management.commands import seed_sample_data
from cargotracker.handling.application.accept_registration import accept_registration
from cargotracker.handling.application.process_registration_attempt import (
    process_registration_attempt,
)
from cargotracker.handling.domain.handling_event import HandlingEventType
from cargotracker.handling.domain.registration_attempt import RegistrationAttempt
from cargotracker.handling.infrastructure.attempt_processing_repository import (
    DjangoAttemptProcessingRepository,
)
from cargotracker.handling.infrastructure.attempt_submission_repository import (
    DjangoAttemptSubmissionRepository,
)
from cargotracker.handling.infrastructure.models import (
    HandlingEventRecord,
    RegistrationAttemptRecord,
)
from cargotracker.handling.infrastructure.repository import DjangoHandlingEventRepository
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.voyage.domain.voyage_number import VoyageNumber


@pytest.mark.parametrize(
    ('setting', 'value'),
    [
        ('HANDLING_ATTEMPT_POLL_SECONDS', '0'),
        ('HANDLING_ATTEMPT_POLL_SECONDS', 'nan'),
        ('HANDLING_ATTEMPT_RETRY_BACKOFF_SECONDS', 'not-a-number'),
        ('HANDLING_ATTEMPT_RETRY_BACKOFF_SECONDS', '0'),
        ('HANDLING_ATTEMPT_RETRY_BACKOFF_SECONDS', 'inf'),
        ('HANDLING_ATTEMPT_RETRY_BACKOFF_SECONDS', 'nan'),
    ],
)
def test_worker_rejects_invalid_settings(monkeypatch, setting, value):
    monkeypatch.setenv(setting, value)
    monkeypatch.setattr(worker, 'process_registration_attempt', lambda *args, **kwargs: False)
    monkeypatch.setattr(
        worker, 'sleep', lambda _: pytest.fail('worker slept with invalid settings')
    )

    with pytest.raises(CommandError):
        worker.Command().handle()


def test_worker_sleeps_when_idle_and_processes_without_sleeping(monkeypatch):
    calls = 0
    sleeps = []

    class StopWorker(Exception):
        pass

    def process_attempt(*repositories, retry_backoff_seconds):
        nonlocal calls
        calls += 1
        if calls == 1:
            assert len(repositories) == 3
            assert retry_backoff_seconds == 0.5
            return False
        if calls == 2:
            return True
        raise StopWorker

    monkeypatch.setenv('HANDLING_ATTEMPT_POLL_SECONDS', '0.25')
    monkeypatch.setenv('HANDLING_ATTEMPT_RETRY_BACKOFF_SECONDS', '0.5')
    monkeypatch.setattr(worker, 'process_registration_attempt', process_attempt)
    monkeypatch.setattr(worker, 'sleep', sleeps.append)

    with pytest.raises(StopWorker):
        worker.Command().handle()

    assert calls == 3
    assert sleeps == [0.25]


def test_worker_processes_and_waits_with_default_settings(monkeypatch):
    monkeypatch.delenv('HANDLING_ATTEMPT_POLL_SECONDS', raising=False)
    monkeypatch.delenv('HANDLING_ATTEMPT_RETRY_BACKOFF_SECONDS', raising=False)
    retry_backoffs = []
    sleeps = []

    class StopWorker(Exception):
        pass

    def process_attempt(*repositories, retry_backoff_seconds):
        assert len(repositories) == 3
        retry_backoffs.append(retry_backoff_seconds)
        return False

    def stop_after_sleep(seconds):
        sleeps.append(seconds)
        raise StopWorker

    monkeypatch.setattr(worker, 'process_registration_attempt', process_attempt)
    monkeypatch.setattr(worker, 'sleep', stop_after_sleep)

    with pytest.raises(StopWorker):
        worker.Command().handle()

    assert len(retry_backoffs) == 1
    assert isfinite(retry_backoffs[0]) and retry_backoffs[0] > 0
    assert len(sleeps) == 1
    assert isfinite(sleeps[0]) and sleeps[0] > 0


def _attempt(**overrides):
    fields = {
        'tracking_id': TrackingId('ABC123'),
        'completion_time': datetime.now(UTC) + timedelta(days=1),
        'registration_time': datetime.now(UTC),
        'event_type': HandlingEventType.RECEIVE,
        'location': UnLocode('USNYC'),
    }
    return RegistrationAttempt(**(fields | overrides))


def _process():
    return process_registration_attempt(
        DjangoAttemptProcessingRepository(),
        DjangoCargoRepository(),
        DjangoHandlingEventRepository(),
    )


@pytest.mark.django_db
def test_rest_accepted_report_is_processed_into_handling_event_and_cargo_delivery(
    client, monkeypatch
):
    fixed_now = datetime(2026, 11, 4, 12, tzinfo=UTC)

    class FrozenDateTime(datetime):
        @classmethod
        def now(cls, tz=None):
            return fixed_now.astimezone(tz) if tz else fixed_now

    monkeypatch.setattr(seed_sample_data.timezone, 'now', lambda: fixed_now)
    monkeypatch.setattr(sample_data, 'datetime', FrozenDateTime)
    monkeypatch.setattr(handling_rest, 'datetime', FrozenDateTime)
    call_command('seed_sample_data')

    completion_time = datetime(2026, 11, 5, 12, tzinfo=UTC)
    events_before = HandlingEventRecord.objects.filter(cargo__tracking_id='ABC123').count()
    delivery_before = DjangoCargoRepository().find(TrackingId('ABC123')).delivery
    response = client.post(
        '/rest/handling/reports',
        data=json.dumps(
            {
                'completionTime': completion_time.strftime('%Y-%m-%d %H:%M'),
                'trackingId': 'ABC123',
                'eventType': 'RECEIVE',
                'unLocode': 'USNYC',
            }
        ),
        content_type='application/json',
    )
    attempt = RegistrationAttemptRecord.objects.get()

    assert response.status_code == 204
    assert attempt.status == 'accepted'
    assert HandlingEventRecord.objects.filter(cargo__tracking_id='ABC123').count() == events_before
    assert DjangoCargoRepository().find(TrackingId('ABC123')).delivery == delivery_before
    assert _process() is True

    attempt.refresh_from_db()
    event = HandlingEventRecord.objects.get(
        cargo__tracking_id='ABC123',
        event_type='RECEIVE',
        completion_time=completion_time.date(),
        registration_time=attempt.registration_time.date(),
    )
    cargo = DjangoCargoRepository().find(TrackingId('ABC123'))

    assert attempt.status == 'registered'
    assert (
        HandlingEventRecord.objects.filter(cargo__tracking_id='ABC123').count() == events_before + 1
    )
    assert cargo.delivery.last_event_id == event.pk
    assert cargo.delivery.transport_status == 'IN_PORT'
    assert cargo.delivery.last_known_location.unlocode == UnLocode('USNYC')


@pytest.mark.django_db
def test_processing_registers_attempt_once_and_rederives_cargo_delivery():
    call_command('seed_sample_data')
    attempt = accept_registration(_attempt(), DjangoAttemptSubmissionRepository())
    events_before = HandlingEventRecord.objects.filter(cargo__tracking_id='ABC123').count()

    assert _process() is True
    assert _process() is False

    attempt_record = RegistrationAttemptRecord.objects.get(pk=attempt.id)
    event = HandlingEventRecord.objects.get(
        cargo__tracking_id='ABC123',
        event_type='RECEIVE',
        completion_time=attempt.completion_time.date(),
    )
    cargo = DjangoCargoRepository().find(TrackingId('ABC123'))

    assert attempt_record.status == 'registered'
    assert (
        HandlingEventRecord.objects.filter(cargo__tracking_id='ABC123').count() == events_before + 1
    )
    assert cargo.delivery.last_event_id == event.pk
    assert cargo.delivery.transport_status == 'IN_PORT'
    history = DjangoHandlingEventRepository().lookup_handling_history_of_cargo(TrackingId('ABC123'))
    assert all(event.cargo.tracking_id == TrackingId('ABC123') for event in history.events)


@pytest.mark.django_db
@pytest.mark.parametrize(
    ('attempt_changes', 'reason_code', 'message'),
    [
        (
            {'tracking_id': TrackingId('MISSING')},
            'UNKNOWN_CARGO',
            'cargo MISSING does not exist',
        ),
        (
            {'location': UnLocode('ZZXXX')},
            'UNKNOWN_LOCATION',
            'location ZZXXX does not exist',
        ),
        (
            {
                'event_type': HandlingEventType.LOAD,
                'voyage_number': VoyageNumber('CM999'),
            },
            'UNKNOWN_VOYAGE',
            'voyage CM999 does not exist',
        ),
        (
            {'event_type': HandlingEventType.LOAD},
            'INVALID_EVENT',
            'Voyage is required for event type LOAD',
        ),
    ],
)
def test_unknown_references_reject_attempt_without_storing_event(
    attempt_changes, reason_code, message, caplog
):
    call_command('seed_sample_data')
    attempt = accept_registration(
        _attempt(**attempt_changes),
        DjangoAttemptSubmissionRepository(),
    )
    existing_events = HandlingEventRecord.objects.count()

    with caplog.at_level(logging.WARNING, logger=processing.__name__):
        assert _process() is True

    attempt_record = RegistrationAttemptRecord.objects.get(pk=attempt.id)
    assert attempt_record.status == 'rejected'
    assert attempt_record.rejection_reason == f'{reason_code}: {message}'
    assert HandlingEventRecord.objects.count() == existing_events
    assert [record.getMessage() for record in caplog.records] == [
        f'Registration attempt {attempt.id} rejected: {message}'
    ]


@pytest.mark.django_db
@pytest.mark.parametrize('earlier_registration_day', [4, 5])
def test_equal_completion_time_uses_registration_order_for_delivered_outcome(
    caplog, monkeypatch, earlier_registration_day
):
    fixed_now = datetime(2026, 11, 4, 12, tzinfo=UTC)

    class FrozenDateTime(datetime):
        @classmethod
        def now(cls, tz=None):
            return fixed_now.astimezone(tz) if tz else fixed_now

    monkeypatch.setattr(seed_sample_data.timezone, 'now', lambda: fixed_now)
    monkeypatch.setattr(sample_data, 'datetime', FrozenDateTime)
    call_command('seed_sample_data')
    completion_time = datetime(2026, 11, 3, 12, tzinfo=UTC)
    attempts = DjangoAttemptSubmissionRepository()
    earlier_registration_time = datetime(2026, 11, earlier_registration_day, 12, tzinfo=UTC)
    later_registration = accept_registration(
        _attempt(
            completion_time=completion_time,
            registration_time=earlier_registration_time + timedelta(days=1),
            event_type=HandlingEventType.UNLOAD,
            location=UnLocode('FIHEL'),
            voyage_number=VoyageNumber('0300A'),
        ),
        attempts,
    )
    earlier_registration = accept_registration(
        _attempt(
            completion_time=completion_time,
            registration_time=earlier_registration_time,
            event_type=HandlingEventType.RECEIVE,
            location=UnLocode('USNYC'),
        ),
        attempts,
    )

    with caplog.at_level(logging.INFO):
        assert _process() is True
        assert _process() is True

    later_event = HandlingEventRecord.objects.get(
        cargo__tracking_id='ABC123',
        event_type='UNLOAD',
        completion_time=completion_time.date(),
        registration_time=later_registration.registration_time.date(),
    )
    earlier_event = HandlingEventRecord.objects.get(
        cargo__tracking_id='ABC123',
        event_type='RECEIVE',
        completion_time=completion_time.date(),
        registration_time=earlier_registration.registration_time.date(),
    )
    cargo = DjangoCargoRepository().find(TrackingId('ABC123'))

    assert later_event.pk < earlier_event.pk
    assert cargo.delivery.last_event_id == later_event.pk
    assert cargo.delivery.unloaded_at_destination is True
    assert 'Cargo ABC123 delivered' in [record.getMessage() for record in caplog.records]


@pytest.mark.django_db
def test_equal_completion_and_registration_times_use_event_id_for_delivery(caplog):
    call_command('seed_sample_data')
    completion_time = datetime(2026, 11, 4, 12, tzinfo=UTC)
    registration_time = datetime(2026, 11, 3, 12, tzinfo=UTC)
    attempts = DjangoAttemptSubmissionRepository()
    accept_registration(
        _attempt(
            completion_time=completion_time,
            registration_time=registration_time,
            event_type=HandlingEventType.RECEIVE,
            location=UnLocode('USNYC'),
        ),
        attempts,
    )
    accept_registration(
        _attempt(
            completion_time=completion_time,
            registration_time=registration_time,
            event_type=HandlingEventType.UNLOAD,
            location=UnLocode('FIHEL'),
            voyage_number=VoyageNumber('0300A'),
        ),
        attempts,
    )

    with caplog.at_level(logging.INFO):
        assert _process() is True
        assert _process() is True

    receive_event = HandlingEventRecord.objects.get(
        cargo__tracking_id='ABC123',
        event_type='RECEIVE',
        completion_time=completion_time.date(),
        registration_time=registration_time.date(),
    )
    unload_event = HandlingEventRecord.objects.get(
        cargo__tracking_id='ABC123',
        event_type='UNLOAD',
        completion_time=completion_time.date(),
        registration_time=registration_time.date(),
    )
    cargo = DjangoCargoRepository().find(TrackingId('ABC123'))

    assert receive_event.pk < unload_event.pk
    assert cargo.delivery.last_event_id == unload_event.pk
    assert cargo.delivery.unloaded_at_destination is True
    assert 'Cargo ABC123 delivered' in [record.getMessage() for record in caplog.records]


@pytest.mark.django_db
def test_misdirected_outcome_is_logged(caplog):
    call_command('seed_sample_data')
    attempt = accept_registration(
        _attempt(
            completion_time=datetime.now(UTC) + timedelta(days=2),
            event_type=HandlingEventType.CLAIM,
            location=UnLocode('USNYC'),
        ),
        DjangoAttemptSubmissionRepository(),
    )

    with caplog.at_level(logging.INFO):
        assert _process() is True

    cargo = DjangoCargoRepository().find(TrackingId('ABC123'))

    assert RegistrationAttemptRecord.objects.get(pk=attempt.id).status == 'registered'
    assert cargo.delivery.misdirected is True
    assert 'Cargo ABC123 is misdirected' in [record.getMessage() for record in caplog.records]


@pytest.mark.django_db
def test_misdirected_and_delivered_outcomes_are_logged_independently(caplog):
    call_command('seed_sample_data')
    attempt = accept_registration(
        _attempt(
            completion_time=datetime.now(UTC) + timedelta(days=2),
            event_type=HandlingEventType.UNLOAD,
            location=UnLocode('FIHEL'),
            voyage_number=VoyageNumber('0400S'),
        ),
        DjangoAttemptSubmissionRepository(),
    )

    with caplog.at_level(logging.INFO):
        assert _process() is True

    cargo = DjangoCargoRepository().find(TrackingId('ABC123'))
    messages = [record.getMessage() for record in caplog.records]

    assert RegistrationAttemptRecord.objects.get(pk=attempt.id).status == 'registered'
    assert cargo.delivery.misdirected is True
    assert cargo.delivery.unloaded_at_destination is True
    assert 'Cargo ABC123 is misdirected' in messages
    assert 'Cargo ABC123 delivered' in messages


@pytest.mark.django_db
def test_temporary_database_failure_retries_atomically_and_logs_after_fifteen_minutes(
    caplog, monkeypatch
):
    call_command('seed_sample_data')
    attempt = accept_registration(_attempt(), DjangoAttemptSubmissionRepository())
    events_before = HandlingEventRecord.objects.filter(cargo__tracking_id='ABC123').count()
    delivery_before = DjangoCargoRepository().find(TrackingId('ABC123')).delivery
    original_mark_registered = DjangoAttemptProcessingRepository.mark_registered
    mark_calls = 0
    clock = [10_000.0]
    retry_delays = []
    retry_observations = []
    error_times = []
    original_error = processing.logger.error

    def fail_before_marking_registered(self, attempt_id):
        nonlocal mark_calls
        mark_calls += 1
        if mark_calls <= 25:
            raise OperationalError('temporary database failure')
        return original_mark_registered(self, attempt_id)

    def advance_clock(seconds):
        clock[0] += seconds
        if mark_calls == 20:
            clock[0] = 10_900
        retry_delays.append(seconds)
        retry_observations.append(
            (
                RegistrationAttemptRecord.objects.get(pk=attempt.id).status,
                HandlingEventRecord.objects.filter(cargo__tracking_id='ABC123').count(),
                DjangoCargoRepository().find(TrackingId('ABC123')).delivery,
            )
        )

    def record_error(*args, **kwargs):
        error_times.append(clock[0])
        return original_error(*args, **kwargs)

    monkeypatch.setattr(
        DjangoAttemptProcessingRepository,
        'mark_registered',
        fail_before_marking_registered,
    )
    monkeypatch.setattr(processing.logger, 'error', record_error)
    monkeypatch.setattr(processing, 'monotonic', lambda: clock[0], raising=False)
    monkeypatch.setattr(processing, 'sleep', advance_clock, raising=False)

    with caplog.at_level(logging.ERROR, logger=processing.__name__):
        assert _process() is True

    attempt_record = RegistrationAttemptRecord.objects.get(pk=attempt.id)
    assert attempt_record.status == 'registered'
    assert (
        HandlingEventRecord.objects.filter(cargo__tracking_id='ABC123').count() == events_before + 1
    )
    assert mark_calls == 26
    assert clock[0] >= 10_900
    assert retry_delays[:7] == [1, 2, 4, 8, 16, 32, 60]
    assert set(retry_delays[6:]) == {60}
    assert len(retry_observations) == 25
    assert all(
        status == 'accepted' and count == events_before and delivery == delivery_before
        for status, count, delivery in retry_observations
    )
    assert sum('after 15 minutes' in record.getMessage() for record in caplog.records) == 1
    assert error_times == [10_900]


@pytest.mark.parametrize('backoff', [0, -1, float('inf'), float('nan')])
def test_processing_rejects_nonpositive_or_nonfinite_retry_backoff(backoff):
    with pytest.raises(ValueError, match='Retry backoff must be greater than zero'):
        process_registration_attempt(None, None, None, retry_backoff_seconds=backoff)


@pytest.mark.django_db(transaction=True)
def test_concurrent_processing_claims_an_attempt_only_once():
    call_command('seed_sample_data')
    attempt = accept_registration(_attempt(), DjangoAttemptSubmissionRepository())
    events_before = HandlingEventRecord.objects.filter(cargo__tracking_id='ABC123').count()

    def process_in_thread():
        close_old_connections()
        try:
            return _process()
        finally:
            close_old_connections()

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(lambda _: process_in_thread(), range(2)))

    assert results.count(True) == 1
    assert RegistrationAttemptRecord.objects.get(pk=attempt.id).status == 'registered'
    assert (
        HandlingEventRecord.objects.filter(cargo__tracking_id='ABC123').count() == events_before + 1
    )
