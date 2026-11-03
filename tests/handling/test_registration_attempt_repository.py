from datetime import UTC, datetime

import pytest
from django.db import connection

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
