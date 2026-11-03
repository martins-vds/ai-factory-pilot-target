import json
from datetime import UTC, datetime

import pytest

from cargotracker.handling.domain.registration_attempt import RegistrationAttemptStatus
from cargotracker.handling.models import RegistrationAttemptRecord


@pytest.mark.django_db
def test_accepted_report_is_persisted_with_completion_time_in_utc(client):
    report = {
        'completionTime': '2026-11-03 10:15',
        'trackingId': 'ABC123',
        'eventType': 'RECEIVE',
        'unLocode': 'USNYC',
    }

    response = client.post(
        '/rest/handling/reports',
        data=json.dumps(report),
        content_type='application/json',
    )

    attempt = RegistrationAttemptRecord.objects.get()
    assert response.status_code == 204
    assert response.content == b''
    assert attempt.status == RegistrationAttemptStatus.ACCEPTED
    assert attempt.completion_time == datetime(2026, 11, 3, 10, 15, tzinfo=UTC)
    assert attempt.tracking_id == 'ABC123'
    assert attempt.event_type == 'RECEIVE'
    assert attempt.un_locode == 'USNYC'
    assert attempt.voyage_number is None
