import json
from datetime import UTC, datetime

import pytest
from django.test import Client

from cargotracker.handling.domain.registration_attempt import RegistrationAttemptStatus
from cargotracker.handling.models import RegistrationAttemptRecord

VALID_REPORT = {
    'completionTime': '2026-11-03 10:15',
    'trackingId': 'ABC123',
    'eventType': 'RECEIVE',
    'unLocode': 'USNYC',
}


def _post_report(client, report):
    return client.post(
        '/rest/handling/reports',
        data=json.dumps(report),
        content_type='application/json',
    )


@pytest.mark.django_db
def test_accepted_report_is_persisted_with_completion_time_in_utc(client):
    response = _post_report(client, VALID_REPORT)

    attempt = RegistrationAttemptRecord.objects.get()
    assert response.status_code == 204
    assert response.content == b''
    assert attempt.status == RegistrationAttemptStatus.ACCEPTED
    assert attempt.completion_time == datetime(2026, 11, 3, 10, 15, tzinfo=UTC)
    assert attempt.tracking_id == 'ABC123'
    assert attempt.event_type == 'RECEIVE'
    assert attempt.un_locode == 'USNYC'
    assert attempt.voyage_number is None


@pytest.mark.parametrize('field', ['completionTime', 'trackingId', 'eventType', 'unLocode'])
@pytest.mark.django_db
def test_missing_required_report_field_returns_a_field_error(client, field):
    report = VALID_REPORT.copy()
    report.pop(field)

    response = _post_report(client, report)

    assert response.status_code == 400
    assert response.json()['errors'][field]
    assert not RegistrationAttemptRecord.objects.exists()


@pytest.mark.parametrize(
    ('field', 'value'),
    [
        ('completionTime', '2026-11-03 10:15x'),
        ('completionTime', '2026-11-3 10:15'),
        ('trackingId', 'ABC'),
        ('eventType', 'REC'),
        ('eventType', 'CUSTOMSS'),
        ('unLocode', 'USNY'),
        ('unLocode', 'USNYCZ'),
        ('voyageNumber', 'CM1'),
        ('voyageNumber', 'CM0012'),
    ],
)
@pytest.mark.django_db
def test_report_length_error_is_returned_for_the_field(client, field, value):
    report = VALID_REPORT | {field: value}

    response = _post_report(client, report)

    assert response.status_code == 400
    assert response.json()['errors'][field]
    assert not RegistrationAttemptRecord.objects.exists()


@pytest.mark.django_db
def test_optional_voyage_number_is_persisted(client):
    response = _post_report(client, VALID_REPORT | {'voyageNumber': 'CM001'})

    assert response.status_code == 204
    assert RegistrationAttemptRecord.objects.get().voyage_number == 'CM001'


@pytest.mark.django_db
def test_load_without_voyage_is_accepted_for_worker_validation(client):
    response = _post_report(client, VALID_REPORT | {'eventType': 'LOAD'})

    assert response.status_code == 204
    attempt = RegistrationAttemptRecord.objects.get()
    assert attempt.event_type == 'LOAD'
    assert attempt.voyage_number is None


@pytest.mark.django_db
def test_report_endpoint_is_exempt_from_csrf_checks():
    client = Client(enforce_csrf_checks=True)

    response = _post_report(client, VALID_REPORT)

    assert response.status_code == 204


@pytest.mark.parametrize(
    ('field', 'value'),
    [
        ('completionTime', 202611031015),
        ('trackingId', 12345),
        ('eventType', ['RECEIVE']),
        ('unLocode', {'code': 'USNYC'}),
        ('voyageNumber', 12345),
    ],
)
@pytest.mark.django_db
def test_report_type_error_is_returned_for_the_field(client, field, value):
    report = VALID_REPORT | {field: value}

    response = _post_report(client, report)

    assert response.status_code == 400
    assert response.json()['errors'][field]
    assert not RegistrationAttemptRecord.objects.exists()


@pytest.mark.parametrize(
    ('field', 'value'),
    [
        ('completionTime', '2026-13-03 10:15'),
        ('eventType', 'BOGUS'),
        ('unLocode', 'USN?C'),
    ],
)
@pytest.mark.django_db
def test_invalid_report_value_is_returned_as_a_field_error(client, field, value):
    report = VALID_REPORT | {field: value}

    response = _post_report(client, report)

    assert response.status_code == 400
    assert response.json()['errors'][field]
    assert not RegistrationAttemptRecord.objects.exists()


@pytest.mark.parametrize(
    ('body', 'message'),
    [
        ('not JSON', 'body must be valid JSON'),
        ('[]', 'body must be a JSON object'),
    ],
)
@pytest.mark.django_db
def test_invalid_json_body_returns_a_non_field_error(client, body, message):
    response = client.post(
        '/rest/handling/reports',
        data=body,
        content_type='application/json',
    )

    errors = response.json()['errors']
    assert response.status_code == 400
    assert message in errors['non_field_errors'][0]
    assert not RegistrationAttemptRecord.objects.exists()
