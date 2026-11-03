from datetime import UTC, datetime, timedelta

import pytest
from django.core.management import call_command

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
