from concurrent.futures import ThreadPoolExecutor, TimeoutError
from dataclasses import FrozenInstanceError, replace
from datetime import UTC, datetime

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, close_old_connections, connection, transaction

from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.handling.application.accept_registration import accept_registration
from cargotracker.handling.domain.handling_event import HandlingEventType
from cargotracker.handling.domain.registration_attempt import (
    RegistrationAttempt,
    RegistrationAttemptStatus,
)
from cargotracker.handling.infrastructure.attempt_submission_repository import (
    DjangoAttemptSubmissionRepository,
)
from cargotracker.handling.models import HandlingEventRecord, RegistrationAttemptRecord
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.voyage.domain.voyage_number import VoyageNumber


def _attempt(voyage_number='CM001'):
    voyage_number = VoyageNumber(voyage_number) if voyage_number is not None else None
    return RegistrationAttempt(
        tracking_id=TrackingId('ABC123'),
        completion_time=datetime(2026, 11, 3, 10, tzinfo=UTC),
        registration_time=datetime(2026, 11, 3, 11, tzinfo=UTC),
        event_type=HandlingEventType.LOAD,
        location=UnLocode('USNYC'),
        voyage_number=voyage_number,
    )


def _record_fields(**overrides):
    fields = {
        'tracking_id': 'ABC123',
        'completion_time': datetime(2026, 11, 3, 10, tzinfo=UTC),
        'registration_time': datetime(2026, 11, 3, 11, tzinfo=UTC),
        'event_type': 'LOAD',
        'un_locode': 'USNYC',
        'voyage_number': 'CM001',
        'status': 'accepted',
        'rejection_reason': None,
    }
    return fields | overrides


@pytest.mark.django_db
def test_accept_registration_persists_attempt_without_expiry():
    accepted = accept_registration(_attempt(), DjangoAttemptSubmissionRepository())
    record = RegistrationAttemptRecord.objects.get()

    with connection.cursor() as cursor:
        columns = {
            column.name
            for column in connection.introspection.get_table_description(
                cursor, RegistrationAttemptRecord._meta.db_table
            )
        }

    assert accepted.id == record.pk
    assert accepted.status is RegistrationAttemptStatus.ACCEPTED
    assert accepted.tracking_id == TrackingId('ABC123')
    assert accepted.completion_time == datetime(2026, 11, 3, 10, tzinfo=UTC)
    assert accepted.registration_time == datetime(2026, 11, 3, 11, tzinfo=UTC)
    assert accepted.event_type is HandlingEventType.LOAD
    assert accepted.location == UnLocode('USNYC')
    assert accepted.voyage_number == VoyageNumber('CM001')
    assert accepted.rejection_reason is None
    assert record.tracking_id == 'ABC123'
    assert record.completion_time == datetime(2026, 11, 3, 10, tzinfo=UTC)
    assert record.registration_time == datetime(2026, 11, 3, 11, tzinfo=UTC)
    assert record.event_type == 'LOAD'
    assert record.un_locode == 'USNYC'
    assert record.voyage_number == 'CM001'
    assert record.status == 'accepted'
    assert record.rejection_reason is None
    assert columns == {
        'id',
        'tracking_id',
        'completion_time',
        'registration_time',
        'event_type',
        'un_locode',
        'voyage_number',
        'status',
        'rejection_reason',
    }
    assert RegistrationAttemptRecord._meta.db_table == 'handling_registration_attempt'
    assert RegistrationAttemptRecord._meta.get_field('tracking_id').max_length == 255
    assert (
        RegistrationAttemptRecord._meta.get_field('completion_time').get_internal_type()
        == 'DateTimeField'
    )
    assert (
        RegistrationAttemptRecord._meta.get_field('registration_time').get_internal_type()
        == 'DateTimeField'
    )
    assert RegistrationAttemptRecord._meta.get_field('event_type').max_length == 255
    assert RegistrationAttemptRecord._meta.get_field('un_locode').max_length == 5
    assert RegistrationAttemptRecord._meta.get_field('voyage_number').null
    assert RegistrationAttemptRecord._meta.get_field('status').max_length == 10
    assert RegistrationAttemptRecord._meta.get_field('status').db_index
    assert RegistrationAttemptRecord._meta.get_field('status').choices == [
        ('accepted', 'accepted'),
        ('registered', 'registered'),
        ('rejected', 'rejected'),
    ]
    assert RegistrationAttemptRecord._meta.get_field('rejection_reason').null
    assert RegistrationAttemptRecord._meta.get_field('rejection_reason').blank
    for field_name in ('cargo', 'location', 'voyage'):
        assert HandlingEventRecord._meta.get_field(field_name).remote_field.related_name == '+'


@pytest.mark.django_db
def test_repository_persists_an_attempt_without_a_voyage():
    accepted = DjangoAttemptSubmissionRepository().submit(_attempt(voyage_number=None))
    record = RegistrationAttemptRecord.objects.get()

    assert accepted.voyage_number is None
    assert record.voyage_number is None


@pytest.mark.django_db
def test_registration_attempt_defaults_to_no_voyage_and_normalizes_times():
    attempt = RegistrationAttempt(
        tracking_id=TrackingId('ABC123'),
        completion_time=datetime(2026, 11, 3, 10),
        registration_time=datetime(2026, 11, 3, 11),
        event_type=HandlingEventType.RECEIVE,
        location=UnLocode('USNYC'),
    )

    assert attempt.voyage_number is None
    assert attempt.completion_time == datetime(2026, 11, 3, 10, tzinfo=UTC)
    assert attempt.registration_time == datetime(2026, 11, 3, 11, tzinfo=UTC)
    with pytest.raises(FrozenInstanceError):
        attempt.id = 1


@pytest.mark.django_db
def test_repository_claims_and_marks_registered_attempt_as_terminal():
    repository = DjangoAttemptSubmissionRepository()
    accepted = repository.submit(_attempt())

    claimed = repository.claim_next()

    assert claimed.id == accepted.id
    assert claimed.status is RegistrationAttemptStatus.ACCEPTED

    repository.mark_registered(claimed.id)

    record = RegistrationAttemptRecord.objects.get(pk=accepted.id)
    assert record.status == RegistrationAttemptStatus.REGISTERED
    assert record.rejection_reason is None
    assert repository.claim_next() is None
    with pytest.raises(ValueError, match='is not accepted'):
        repository.mark_registered(accepted.id)


@pytest.mark.django_db
def test_repository_marks_rejected_attempt_with_its_reason():
    repository = DjangoAttemptSubmissionRepository()
    accepted = repository.submit(_attempt())
    reason = 'unknown location: ZZXXX'

    repository.mark_rejected(accepted.id, reason)

    record = RegistrationAttemptRecord.objects.get(pk=accepted.id)
    assert record.status == RegistrationAttemptStatus.REJECTED
    assert record.rejection_reason == reason
    assert repository.claim_next() is None


@pytest.mark.django_db
@pytest.mark.parametrize('reason', [None, '', '  '])
def test_repository_does_not_reject_an_attempt_without_a_reason(reason):
    repository = DjangoAttemptSubmissionRepository()
    accepted = repository.submit(_attempt())

    with pytest.raises(ValueError, match='requires a reason'):
        repository.mark_rejected(accepted.id, reason)

    record = RegistrationAttemptRecord.objects.get(pk=accepted.id)
    assert record.status == RegistrationAttemptStatus.ACCEPTED


@pytest.mark.django_db(transaction=True)
def test_repository_claim_skips_an_attempt_locked_by_another_transaction():
    repository = DjangoAttemptSubmissionRepository()
    accepted = repository.submit(_attempt())

    def claim_in_another_transaction():
        close_old_connections()
        try:
            with transaction.atomic():
                return repository.claim_next()
        finally:
            close_old_connections()

    executor = ThreadPoolExecutor(max_workers=1)
    with transaction.atomic():
        claimed = repository.claim_next()
        future = executor.submit(claim_in_another_transaction)
        try:
            skipped = future.result(timeout=1)
        except TimeoutError:
            skipped = 'blocked'
    executor.shutdown(wait=True)

    assert claimed.id == accepted.id
    assert skipped is None


@pytest.mark.parametrize(
    ('changes', 'exception', 'message'),
    [
        ({'tracking_id': 'ABC123'}, TypeError, 'requires a tracking ID'),
        ({'completion_time': '2026-11-03'}, TypeError, 'Completion time must be a datetime'),
        ({'registration_time': None}, TypeError, 'Registration time must be a datetime'),
        ({'event_type': 'LOAD'}, TypeError, 'requires an event type'),
        ({'location': 'USNYC'}, TypeError, 'requires a UN/LOCODE'),
        ({'voyage_number': 'CM001'}, TypeError, 'voyage number must be a voyage number'),
        ({'id': 0}, ValueError, 'ID must be a positive integer'),
        ({'id': True}, ValueError, 'ID must be a positive integer'),
        ({'status': 'accepted'}, TypeError, 'requires a status'),
        ({'status': RegistrationAttemptStatus.REJECTED}, ValueError, 'requires a reason'),
        (
            {
                'status': RegistrationAttemptStatus.REJECTED,
                'rejection_reason': '  ',
            },
            ValueError,
            'requires a reason',
        ),
        ({'rejection_reason': 'not rejected'}, ValueError, 'may have a reason'),
    ],
)
def test_registration_attempt_rejects_invalid_values(changes, exception, message):
    with pytest.raises(exception, match=message):
        replace(_attempt(), **changes)


@pytest.mark.parametrize(
    'changes',
    [
        {'id': 1},
        {'status': RegistrationAttemptStatus.REGISTERED},
    ],
)
def test_accept_registration_only_accepts_new_attempts(changes):
    with pytest.raises(ValueError, match='Only a new registration attempt can be accepted'):
        accept_registration(replace(_attempt(), **changes), DjangoAttemptSubmissionRepository())


@pytest.mark.parametrize(
    'changes',
    [
        {'id': 1},
        {'status': RegistrationAttemptStatus.REGISTERED},
    ],
)
def test_repository_only_submits_new_attempts(changes):
    with pytest.raises(ValueError, match='Only a new registration attempt can be submitted'):
        DjangoAttemptSubmissionRepository().submit(replace(_attempt(), **changes))


@pytest.mark.parametrize(
    ('status', 'reason'),
    [
        ('rejected', None),
        ('rejected', ''),
        ('registered', 'not rejected'),
        ('unknown', None),
    ],
)
@pytest.mark.django_db
def test_database_rejects_inconsistent_terminal_state(status, reason):
    with pytest.raises(ValidationError):
        RegistrationAttemptRecord(
            **_record_fields(status=status, rejection_reason=reason)
        ).full_clean()

    with pytest.raises(IntegrityError), transaction.atomic():
        RegistrationAttemptRecord.objects.create(
            **_record_fields(status=status, rejection_reason=reason)
        )
