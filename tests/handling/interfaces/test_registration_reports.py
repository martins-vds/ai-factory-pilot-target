import json
from datetime import UTC, datetime

import pytest
from django.test import Client
from django.urls import reverse

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


@pytest.mark.django_db
def test_accepts_zero_padded_year_in_completion_time(client):
    report = VALID_REPORT | {'completionTime': '0001-01-01 00:00'}

    response = _post_report(client, report)

    assert response.status_code == 204
    assert RegistrationAttemptRecord.objects.get().completion_time == datetime(
        1, 1, 1, 0, 0, tzinfo=UTC
    )


def test_handling_report_url_is_registered_without_changing_tracking_root():
    assert reverse('handling-report') == '/rest/handling/reports'
    assert reverse('track') == '/'


@pytest.mark.parametrize('field', ['completionTime', 'trackingId', 'eventType', 'unLocode'])
@pytest.mark.django_db
def test_missing_required_report_field_returns_a_field_error(client, field):
    report = VALID_REPORT.copy()
    report.pop(field)

    response = _post_report(client, report)

    assert response.status_code == 400
    assert response.json()['errors'][field] == ['This field is required.']
    assert not RegistrationAttemptRecord.objects.exists()


@pytest.mark.parametrize(
    ('field', 'value', 'error'),
    [
        ('completionTime', ' 2026-11-03 10:15', 'at most 16 characters'),
        ('completionTime', '2026-11-03 10:15x', 'at most 16 characters'),
        ('completionTime', '2026-11-3 10:15', 'at least 16 characters'),
        ('trackingId', 'ABC', 'at least 4 characters'),
        ('eventType', 'REC', 'at least 4 characters'),
        ('eventType', ' RECEIVE', 'at most 7 characters'),
        ('eventType', 'CUSTOMSS', 'at most 7 characters'),
        ('unLocode', 'USNY', 'at least 5 characters'),
        ('unLocode', ' USNYC', 'at most 5 characters'),
        ('unLocode', 'USNYCZ', 'at most 5 characters'),
        ('voyageNumber', '', 'at least 4 characters'),
        ('voyageNumber', 'CM1', 'at least 4 characters'),
        ('voyageNumber', ' CM001', 'at most 5 characters'),
        ('voyageNumber', 'CM0012', 'at most 5 characters'),
    ],
)
@pytest.mark.django_db
def test_report_length_error_is_returned_for_the_field(client, field, value, error):
    report = VALID_REPORT | {field: value}

    response = _post_report(client, report)

    assert response.status_code == 400
    assert error in response.json()['errors'][field][0]
    assert not RegistrationAttemptRecord.objects.exists()


@pytest.mark.django_db
def test_optional_voyage_number_is_persisted(client):
    response = _post_report(client, VALID_REPORT | {'voyageNumber': 'CM001'})

    assert response.status_code == 204
    assert RegistrationAttemptRecord.objects.get().voyage_number == 'CM001'


@pytest.mark.django_db
def test_tracking_id_minimum_length_counts_leading_whitespace(client):
    response = _post_report(client, VALID_REPORT | {'trackingId': ' ABC'})

    assert response.status_code == 204
    assert RegistrationAttemptRecord.objects.get().tracking_id == ' ABC'


@pytest.mark.django_db
def test_null_voyage_number_is_accepted_as_optional(client):
    response = _post_report(client, VALID_REPORT | {'voyageNumber': None})

    assert response.status_code == 204
    assert RegistrationAttemptRecord.objects.get().voyage_number is None


@pytest.mark.django_db
def test_load_without_voyage_is_accepted_for_worker_validation(client):
    response = _post_report(
        client,
        VALID_REPORT | {'eventType': 'LOAD', 'unLocode': 'ZZZZZ'},
    )

    assert response.status_code == 204
    attempt = RegistrationAttemptRecord.objects.get()
    assert attempt.event_type == 'LOAD'
    assert attempt.un_locode == 'ZZZZZ'
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
    assert response.json()['errors'][field] == ['Enter a valid string.']
    assert not RegistrationAttemptRecord.objects.exists()


@pytest.mark.parametrize(
    ('field', 'value', 'error'),
    [
        ('completionTime', '2026-13-03 10:15', 'Enter a valid completion time.'),
        ('completionTime', '2026-11-03  1:15', 'Enter a valid completion time.'),
        ('eventType', 'BOGUS', 'Select a valid event type.'),
        ('unLocode', 'USN?C', 'Enter a valid UN/LOCODE.'),
    ],
)
@pytest.mark.django_db
def test_invalid_report_value_is_returned_as_a_field_error(client, field, value, error):
    report = VALID_REPORT | {field: value}

    response = _post_report(client, report)

    assert response.status_code == 400
    assert response.json()['errors'][field] == [error]
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
    assert errors['non_field_errors'] == [f'Request {message}.']
    assert not RegistrationAttemptRecord.objects.exists()


@pytest.mark.django_db
def test_non_post_request_is_not_accepted(client):
    response = client.get('/rest/handling/reports')

    assert response.status_code == 405
    assert not RegistrationAttemptRecord.objects.exists()
