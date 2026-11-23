import json
import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta

import pytest
from django.core.management import CommandError, call_command
from django.db import OperationalError, close_old_connections, connection

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
    monkeypatch.setattr(
        worker, 'sleep', lambda _: pytest.fail('worker slept with invalid settings')
    )  # afs: allow-mock invalid worker settings must be rejected before sleeping

    with pytest.raises(CommandError):
        worker.Command().handle()


@pytest.mark.parametrize(
    ('poll_setting', 'retry_setting', 'expected_poll', 'expected_retry'),
    [
        ('0.25', '0.5', 0.25, 0.5),
        (None, None, 1.0, 1.0),
    ],
    ids=['configured-settings', 'default-settings'],
)
@pytest.mark.django_db
def test_worker_processes_attempts_before_polling(
    monkeypatch, poll_setting, retry_setting, expected_poll, expected_retry
):
    call_command('seed_sample_data')
    first_attempt = accept_registration(_attempt(), DjangoAttemptSubmissionRepository())
    second_attempt = accept_registration(
        _attempt(completion_time=datetime.now(UTC) + timedelta(days=2)),
        DjangoAttemptSubmissionRepository(),
    )
    events_before = HandlingEventRecord.objects.filter(cargo__tracking_id='ABC123').count()
    retry_delays = []
    sleeps = []

    class StopWorker(Exception):
        pass

    def stop_after_sleep(seconds):
        sleeps.append(seconds)
        raise StopWorker

    if poll_setting is None:
        monkeypatch.delenv('HANDLING_ATTEMPT_POLL_SECONDS', raising=False)
    else:
        monkeypatch.setenv('HANDLING_ATTEMPT_POLL_SECONDS', poll_setting)
    if retry_setting is None:
        monkeypatch.delenv('HANDLING_ATTEMPT_RETRY_BACKOFF_SECONDS', raising=False)
    else:
        monkeypatch.setenv('HANDLING_ATTEMPT_RETRY_BACKOFF_SECONDS', retry_setting)
    monkeypatch.setattr(
        processing, 'sleep', retry_delays.append, raising=False
    )  # afs: allow-mock avoid waiting during a real transient database retry
    monkeypatch.setattr(
        worker, 'sleep', stop_after_sleep
    )  # afs: allow-mock stop the public worker after it drains the queue
    fail_update, registered_updates = _fail_registered_updates(1)

    with connection.execute_wrapper(fail_update):  # afs: allow-mock simulate one transient database write failure
        with pytest.raises(StopWorker):
            call_command('process_handling_attempts')

    first_status = RegistrationAttemptRecord.objects.get(pk=first_attempt.id).status
    second_status = RegistrationAttemptRecord.objects.get(pk=second_attempt.id).status
    assert first_status == second_status == 'registered'
    assert len(registered_updates) == 3
    assert retry_delays == [expected_retry]
    assert sleeps == [expected_poll]
    assert (
        HandlingEventRecord.objects.filter(cargo__tracking_id='ABC123').count()
        == events_before + 2
    )


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


def _fail_registered_updates(failure_count):
    registered_updates = []
    table = RegistrationAttemptRecord._meta.db_table

    def fail_update(execute, sql, params, many, context):
        if 'UPDATE' in sql.upper() and table in sql and params and 'registered' in params:
            registered_updates.append(params)
            if len(registered_updates) <= failure_count:
                raise OperationalError('temporary database failure')
        return execute(sql, params, many, context)

    return fail_update, registered_updates


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
    assert response.content == b''
    assert response.headers.get('Content-Type') is None
    assert attempt.status == 'accepted'
    assert HandlingEventRecord.objects.filter(cargo__tracking_id='ABC123').count() == events_before
    assert DjangoCargoRepository().find(TrackingId('ABC123')).delivery == delivery_before
    assert _process() is True

    attempt.refresh_from_db()
    event = HandlingEventRecord.objects.get(
        cargo__tracking_id='ABC123',
        event_type='RECEIVE',
        completion_time=completion_time,
        registration_time=attempt.registration_time,
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
        completion_time=attempt.completion_time,
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
def test_equal_completion_time_uses_registration_order_for_delivered_outcome(caplog, monkeypatch):
    fixed_now = datetime(2026, 11, 4, 12, tzinfo=UTC)

    class FrozenDateTime(datetime):
        @classmethod
        def now(cls, tz=None):
            return fixed_now.astimezone(tz) if tz else fixed_now

    monkeypatch.setattr(seed_sample_data.timezone, 'now', lambda: fixed_now)
    monkeypatch.setattr(sample_data, 'datetime', FrozenDateTime)
    call_command('seed_sample_data')
    completion_time = datetime(2026, 11, 3, 12, 15, 16, 123456, tzinfo=UTC)
    attempts = DjangoAttemptSubmissionRepository()
    earlier_registration_time = datetime(2026, 11, 4, 12, 15, 16, 100000, tzinfo=UTC)
    later_registration_time = datetime(2026, 11, 4, 12, 15, 16, 900000, tzinfo=UTC)
    later_registration = accept_registration(
        _attempt(
            completion_time=completion_time,
            registration_time=later_registration_time,
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
        completion_time=completion_time,
        registration_time=later_registration.registration_time,
    )
    earlier_event = HandlingEventRecord.objects.get(
        cargo__tracking_id='ABC123',
        event_type='RECEIVE',
        completion_time=completion_time,
        registration_time=earlier_registration.registration_time,
    )
    cargo = DjangoCargoRepository().find(TrackingId('ABC123'))

    assert later_event.pk < earlier_event.pk
    assert cargo.delivery.last_event_id == later_event.pk
    history = DjangoHandlingEventRepository().lookup_handling_history_of_cargo(TrackingId('ABC123'))
    assert [event.id for event in history.events[-2:]] == [earlier_event.pk, later_event.pk]
    assert history.events[-1].completion_time == completion_time
    assert history.events[-1].registration_time == later_registration_time
    assert cargo.delivery.unloaded_at_destination is True
    assert 'Cargo ABC123 delivered' in [record.getMessage() for record in caplog.records]


@pytest.mark.django_db
@pytest.mark.parametrize(
    'fixed_now',
    [
        pytest.param(datetime(2026, 11, 5, 12, tzinfo=UTC), id='before-date-boundary'),
        pytest.param(datetime(2026, 11, 6, 12, tzinfo=UTC), id='date-boundary'),
        pytest.param(datetime(2027, 1, 15, 12, tzinfo=UTC), id='later-date'),
    ],
)
def test_equal_completion_and_registration_times_use_event_id_for_delivery(
    caplog, monkeypatch, fixed_now
):
    monkeypatch.setattr(seed_sample_data.timezone, 'now', lambda: fixed_now)
    call_command('seed_sample_data')
    completion_time = fixed_now - timedelta(days=1)
    registration_time = fixed_now - timedelta(days=2)
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
        completion_time=completion_time,
        registration_time=registration_time,
    )
    unload_event = HandlingEventRecord.objects.get(
        cargo__tracking_id='ABC123',
        event_type='UNLOAD',
        completion_time=completion_time,
        registration_time=registration_time,
    )
    cargo = DjangoCargoRepository().find(TrackingId('ABC123'))

    assert receive_event.pk < unload_event.pk
    assert cargo.delivery.last_event_id == unload_event.pk
    assert cargo.delivery.unloaded_at_destination is True
    history = DjangoHandlingEventRepository().lookup_handling_history_of_cargo(TrackingId('ABC123'))
    assert [event.id for event in history.events[-2:]] == [
        receive_event.pk,
        unload_event.pk,
    ]
    assert history.most_recent_event_id == cargo.delivery.last_event_id
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
    clock = [10_000.0]
    retry_delays = []
    retry_observations = []
    fail_update, registered_updates = _fail_registered_updates(25)

    def advance_clock(seconds):
        clock[0] += seconds
        if len(registered_updates) == 20:
            clock[0] = 10_900
        retry_delays.append(seconds)
        retry_observations.append(
            (
                RegistrationAttemptRecord.objects.get(pk=attempt.id).status,
                HandlingEventRecord.objects.filter(cargo__tracking_id='ABC123').count(),
                DjangoCargoRepository().find(TrackingId('ABC123')).delivery,
            )
        )

    monkeypatch.setattr(
        processing, 'monotonic', lambda: clock[0], raising=False
    )  # afs: allow-mock control retry timing without waiting 15 minutes
    monkeypatch.setattr(
        processing, 'sleep', advance_clock, raising=False
    )  # afs: allow-mock control retry timing without waiting 15 minutes

    with caplog.at_level(logging.ERROR, logger=processing.__name__):
        with connection.execute_wrapper(
            fail_update
        ):  # afs: allow-mock simulate transient database write failures
            assert _process() is True

    attempt_record = RegistrationAttemptRecord.objects.get(pk=attempt.id)
    assert attempt_record.status == 'registered'
    assert (
        HandlingEventRecord.objects.filter(cargo__tracking_id='ABC123').count() == events_before + 1
    )
    assert len(registered_updates) == 26
    assert clock[0] >= 10_900
    assert retry_delays[:7] == [1, 2, 4, 8, 16, 32, 60]
    assert set(retry_delays[6:]) == {60}
    assert len(retry_observations) == 25
    assert all(
        status == 'accepted' and count == events_before and delivery == delivery_before
        for status, count, delivery in retry_observations
    )
    assert sum('after 15 minutes' in record.getMessage() for record in caplog.records) == 1


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
