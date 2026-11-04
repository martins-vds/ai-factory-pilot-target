import copy
import json
import re
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import pytest
from django.core.management import call_command
from django.db import OperationalError

import cargotracker.handling.application.process_registration_attempt as processing
from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.cargo.infrastructure.repository import DjangoCargoRepository
from cargotracker.handling.infrastructure.attempt_processing_repository import (
    DjangoAttemptProcessingRepository,
)
from cargotracker.handling.infrastructure.models import (
    HandlingEventRecord,
    RegistrationAttemptRecord,
)
from cargotracker.handling.infrastructure.repository import DjangoHandlingEventRepository

ROOT = Path(__file__).resolve().parents[2]
GOLDEN_DIR = ROOT / 'characterization' / 'handling-registration' / 'golden'
GOLDEN_CASES = sorted(GOLDEN_DIR.glob('*.json'))
TODAY = datetime.now(UTC).date()
UNKNOWN_REFERENCE_CASES = {
    'load_without_voyage',
    'unknown_location',
    'unknown_tracking_id',
    'unknown_voyage',
}
ABC123_EVENT_SEQUENCE = (
    'event_receive',
    'event_customs',
    'event_load',
    'event_unload',
    'event_load_dallas',
    'unload_at_destination',
    'event_claim',
)
DATE_TOKEN = re.compile(r'<TODAY(?P<offset>[+-]\d+)> (?P<clock>\d{2}:\d{2})')


def _target_report(report):
    result = copy.deepcopy(report)
    completion_time = result.get('completionTime')
    if isinstance(completion_time, str):
        match = DATE_TOKEN.fullmatch(completion_time)
        if match:
            offset = int(match.group('offset') or 0)
            day = TODAY + timedelta(days=offset)
            clock = datetime.strptime(match.group('clock'), '%H:%M').time()
            result['completionTime'] = datetime.combine(day, clock).strftime('%Y-%m-%d %H:%M')
    return result


def _completion_time(report):
    return datetime.strptime(report['completionTime'], '%Y-%m-%d %H:%M').replace(tzinfo=UTC)


def _post_report(client, report):
    return client.post(
        '/rest/handling/reports',
        data=json.dumps(report),
        content_type='application/json',
    )


def _process_next_attempt():
    return processing.process_registration_attempt(
        DjangoAttemptProcessingRepository(),
        DjangoCargoRepository(),
        DjangoHandlingEventRepository(),
    )


def _replay_golden_input(client, case_name):
    golden_path = GOLDEN_DIR / f'{case_name}.json'
    golden = json.loads(golden_path.read_text(encoding='utf-8'))
    reports = golden['input'] if isinstance(golden['input'], list) else [golden['input']]
    for report in reports:
        response = _post_report(client, _target_report(report))
        assert response.status_code == 204
        assert _process_next_attempt() is True
        assert RegistrationAttemptRecord.objects.latest('pk').status == 'registered'


def _prime_prior_golden_state(client, case_name):
    if case_name in ABC123_EVENT_SEQUENCE:
        stop = ABC123_EVENT_SEQUENCE.index(case_name)
        prior_cases = ABC123_EVENT_SEQUENCE[:stop]
    elif case_name == 'misdirected_off_itinerary':
        prior_cases = ABC123_EVENT_SEQUENCE
    elif case_name in {'unknown_location', 'unknown_voyage', 'load_without_voyage'}:
        prior_cases = ('two_reports_ordered_by_completion_time',)
    else:
        prior_cases = ()
    for prior_case in prior_cases:
        _replay_golden_input(client, prior_case)


def _cargo_observation(tracking_id):
    cargo = DjangoCargoRepository().find(TrackingId(tracking_id))
    if cargo is None:
        return None

    delivery = cargo.delivery
    return {
        'trackingId': cargo.tracking_id.value,
        'routingStatus': delivery.routing_status.value,
        'misdirected': delivery.misdirected,
        'transportStatus': delivery.transport_status.value,
        'atDestination': delivery.unloaded_at_destination,
        'origin': cargo.origin.unlocode.value,
        'lastKnownLocation': (
            delivery.last_known_location.unlocode.value
            if delivery.last_known_location is not None
            else 'Unknown'
        ),
    }


def _normalize_display_date(value):
    observed = datetime.strptime(value, '%m/%d/%Y').date()
    offset = (observed - datetime.now(UTC).date()).days
    return '<TODAY>' if offset == 0 else f'<TODAY{offset:+d}>'


def _tracking_observation(client, tracking_id):
    response = client.post('/', {'tracking_id': tracking_id})
    assert response.status_code == 200
    context = response.context
    form = context['form']
    cleaned_data = form.cleaned_data if form.is_valid() else {}
    submitted_id = cleaned_data.get('tracking_id', form['tracking_id'].value())
    cargo = context.get('cargo')

    result = None
    history_rows = []
    map_query = None
    empty_label = None
    if cargo is not None:
        result = {
            'tracking_id': cargo.tracking_id.value,
            'status_text': context['status_text'],
            'destination': cargo.route_specification.destination.name,
            'eta': context['eta'],
            'next_activity': context['next_activity_text'],
            'misdirected': context['misdirected'],
        }
        if result['eta'] not in (None, '?'):
            match = re.match(r'(\d{2}/\d{2}/\d{4})(.*)', result['eta'])
            assert match is not None
            result['eta'] = f'{_normalize_display_date(match.group(1))}{match.group(2)}'
        history_rows = [
            {
                **row,
                'time': (f'{_normalize_display_date(row["time"][:10])}{row["time"][10:]}'),
            }
            for row in context['history_rows']
        ]
        if not history_rows:
            empty_label = (
                f'There are no events recorded for the tracking ID {cargo.tracking_id.value}.'
            )
            if empty_label not in response.content.decode():
                empty_label = None
        query = parse_qs(urlsplit(context['map_url']).query, keep_blank_values=True)
        map_query = {key: values[0] for key, values in query.items()}

    return {
        'submitted_id': submitted_id,
        'result': result,
        'history': {'empty_label': empty_label, 'rows': history_rows},
        'map_query': map_query,
    }


def _field_mismatches(actual, expected, path=''):
    if isinstance(actual, dict) and isinstance(expected, dict):
        mismatches = []
        if set(actual) != set(expected):
            mismatches.append(
                f'{path or "<root>"} fields: expected {sorted(expected)!r}, '
                f'observed {sorted(actual)!r}'
            )
        for field in sorted(set(actual) & set(expected)):
            field_path = f'{path}.{field}' if path else field
            mismatches.extend(_field_mismatches(actual[field], expected[field], field_path))
        return mismatches

    if isinstance(actual, list) and isinstance(expected, list):
        mismatches = []
        if len(actual) != len(expected):
            mismatches.append(
                f'{path}.length: expected {len(expected)!r}, observed {len(actual)!r}'
            )
        for index, (observed, wanted) in enumerate(zip(actual, expected)):
            mismatches.extend(_field_mismatches(observed, wanted, f'{path}[{index}]'))
        return mismatches

    if type(actual) is not type(expected) or actual != expected:
        return [f'{path}: expected {expected!r}, observed {actual!r}']
    return []


def _assert_persisted_event(report, tracking_id, previous_count):
    events = HandlingEventRecord.objects.filter(cargo__tracking_id=tracking_id).order_by('pk')
    assert events.count() == previous_count + 1
    event = events.last()
    assert event.event_type == report['eventType']
    assert event.completion_time == _completion_time(report).date()
    assert event.location.unlocode == report['unLocode']
    if report.get('voyageNumber'):
        assert event.voyage.voyage_number == report['voyageNumber']
    else:
        assert event.voyage is None


@pytest.mark.parametrize(
    'golden_path',
    GOLDEN_CASES,
    ids=lambda golden_path: golden_path.stem,
)
@pytest.mark.django_db
def test_each_handling_registration_golden_matches_target(golden_path, client):
    call_command('seed_sample_data')
    case_name = golden_path.stem
    golden = json.loads(golden_path.read_text(encoding='utf-8'))
    reports = golden['input'] if isinstance(golden['input'], list) else [golden['input']]
    expected = copy.deepcopy(golden['observed'])
    _prime_prior_golden_state(client, case_name)

    malformed = 'post' in expected and expected['post']['status'] != 204
    if malformed:
        expected['post'] = {'status': 400, 'content_type': 'application/json'}
    elif 'posts' in expected:
        expected['posts'] = [{'status': status, 'content_type': ''} for status in expected['posts']]
    if case_name == 'unknown_tracking_id':
        # Ruling #12 removes the legacy empty-history label for unknown cargo.
        expected['tracking']['history']['empty_label'] = None

    actual = {'posts': [], 'cargo': None, 'tracking': None}
    if malformed:
        for report in reports:
            attempt_count = RegistrationAttemptRecord.objects.count()
            response = _post_report(client, _target_report(report))
            actual['posts'].append(
                {
                    'status': response.status_code,
                    'content_type': response.headers.get('Content-Type', '').split(';')[0],
                }
            )
            assert response.status_code == 400
            assert response.headers.get('Content-Type', '').split(';')[0] == 'application/json'
            assert RegistrationAttemptRecord.objects.count() == attempt_count
    else:
        for report in reports:
            target_report = _target_report(report)
            tracking_id = target_report['trackingId']
            response = _post_report(client, target_report)
            actual['posts'].append(
                {
                    'status': response.status_code,
                    'content_type': response.headers.get('Content-Type', '').split(';')[0],
                }
            )
            assert response.status_code == 204
            attempt = RegistrationAttemptRecord.objects.latest('pk')
            assert attempt.status == 'accepted'
            event_count = HandlingEventRecord.objects.filter(cargo__tracking_id=tracking_id).count()

            assert _process_next_attempt() is True
            attempt.refresh_from_db()
            if case_name in UNKNOWN_REFERENCE_CASES:
                assert attempt.status == 'rejected'
                assert attempt.rejection_reason
                assert (
                    HandlingEventRecord.objects.filter(cargo__tracking_id=tracking_id).count()
                    == event_count
                )
            else:
                assert attempt.status == 'registered'
                _assert_persisted_event(target_report, tracking_id, event_count)

        tracking_id = reports[-1]['trackingId']
        actual['cargo'] = _cargo_observation(tracking_id)
        actual['tracking'] = _tracking_observation(client, tracking_id)

    posts = actual.pop('posts')
    if 'post' in expected:
        actual['post'] = posts[0]
    else:
        actual['posts'] = posts

    mismatches = _field_mismatches(actual, expected)
    assert not mismatches, f'{case_name} field-level differences:\n' + '\n'.join(mismatches)


@pytest.mark.django_db
def test_accepted_handling_attempt_is_processed_after_one_second(client):
    call_command('seed_sample_data')
    report = {
        'completionTime': (TODAY + timedelta(days=1)).strftime('%Y-%m-%d 12:00'),
        'trackingId': 'ABC123',
        'eventType': 'RECEIVE',
        'unLocode': 'USNYC',
    }

    response = _post_report(client, report)
    attempt = RegistrationAttemptRecord.objects.latest('pk')

    assert response.status_code == 204
    time.sleep(1.1)
    assert _process_next_attempt() is True
    attempt.refresh_from_db()
    assert attempt.status == 'registered'


@pytest.mark.django_db
def test_registration_and_inspection_updates_roll_back_together(client, monkeypatch):
    call_command('seed_sample_data')
    report = {
        'completionTime': (TODAY + timedelta(days=1)).strftime('%Y-%m-%d 12:00'),
        'trackingId': 'ABC123',
        'eventType': 'RECEIVE',
        'unLocode': 'USNYC',
    }
    response = _post_report(client, report)
    attempt = RegistrationAttemptRecord.objects.latest('pk')
    events_before = HandlingEventRecord.objects.filter(cargo__tracking_id='ABC123').count()
    delivery_before = DjangoCargoRepository().find(TrackingId('ABC123')).delivery

    def fail_marking_registered(self, attempt_id):
        raise OperationalError('force rollback after inspection update')

    monkeypatch.setattr(
        DjangoAttemptProcessingRepository,
        'mark_registered',
        fail_marking_registered,
    )
    with pytest.raises(processing.TemporaryProcessingFailure):
        processing._process_registration_attempt_once(
            DjangoAttemptProcessingRepository(),
            DjangoCargoRepository(),
            DjangoHandlingEventRepository(),
        )

    attempt.refresh_from_db()
    assert response.status_code == 204
    assert attempt.status == 'accepted'
    assert HandlingEventRecord.objects.filter(cargo__tracking_id='ABC123').count() == events_before
    assert DjangoCargoRepository().find(TrackingId('ABC123')).delivery == delivery_before
