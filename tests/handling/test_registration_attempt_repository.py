from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime

import pytest
from django.db import close_old_connections, connection, transaction

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
from cargotracker.handling.models import RegistrationAttemptRecord
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.voyage.domain.voyage_number import VoyageNumber


def _attempt():
    return RegistrationAttempt(
        tracking_id=TrackingId('ABC123'),
        completion_time=datetime(2026, 11, 3, 10, tzinfo=UTC),
        registration_time=datetime(2026, 11, 3, 11, tzinfo=UTC),
        event_type=HandlingEventType.LOAD,
        location=UnLocode('USNYC'),
        voyage_number=VoyageNumber('CM001'),
    )


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
def test_repository_does_not_reject_an_attempt_without_a_reason():
    repository = DjangoAttemptSubmissionRepository()
    accepted = repository.submit(_attempt())

    with pytest.raises(ValueError, match='requires a reason'):
        repository.mark_rejected(accepted.id, '  ')

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

    with transaction.atomic():
        claimed = repository.claim_next()
        with ThreadPoolExecutor(max_workers=1) as executor:
            skipped = executor.submit(claim_in_another_transaction).result(timeout=5)

    assert claimed.id == accepted.id
    assert skipped is None
