import json
import re
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import pytest
from django.core.management import call_command

ROOT = Path(__file__).resolve().parents[2]
GOLDEN_DIR = ROOT / 'characterization' / 'track-cargo' / 'golden'
GOLDEN_CASES = sorted(GOLDEN_DIR.glob('*.json'))
EXPECTED_COORDINATES = {
    'XXXXX': [38.4667, -28.4],
    'CNHKG': [22, 114],
    'AUMEL': [-38, 145],
    'SESTO': [59, 18],
    'FIHEL': [60, 25],
    'CNHGH': [30, 120],
    'USNYC': [41, -74],
    'USDAL': [33, -97],
}
STATUS_COLORS = {
    'NOT_ROUTED': 'grey',
    'NOT_RECEIVED': 'gold',
    'IN_PORT': 'green',
    'ONBOARD_CARRIER': 'green',
    'MISDIRECTED': 'red',
    'AT_DESTINATION': 'black',
    'CLAIMED': 'black',
}


def _normalize_date(text):
    observed = datetime.strptime(text, '%m/%d/%Y').date()
    offset = (observed - datetime.now(UTC).date()).days
    return '<TODAY>' if offset == 0 else f'<TODAY{offset:+d}>'


def _map_frame_data(client, map_url):
    response = client.get(map_url)
    assert response.status_code == 200
    match = re.search(
        r'<script id="map-data" type="application/json">(.*?)</script>',
        response.content.decode(),
        re.DOTALL,
    )
    assert match is not None, 'map frame did not render its map-data payload'
    return json.loads(match.group(1))


def _observe(client, tracking_id, htmx=False):
    headers = {'HTTP_HX_REQUEST': 'true'} if htmx else {}
    response = client.post('/', {'tracking_id': tracking_id}, **headers)
    assert response.status_code == 200
    context = response.context
    form = context['form']
    cleaned_data = form.cleaned_data if form.is_valid() else {}
    submitted_id = cleaned_data.get('tracking_id', form['tracking_id'].value())
    cargo = context.get('cargo')
    content = response.content.decode()

    result = None
    history_rows = []
    map_query = None
    map_frame = None
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
            result['eta'] = f'{_normalize_date(match.group(1))}{match.group(2)}'
        history_rows = [
            {
                **row,
                'time': f'{_normalize_date(row["time"][:10])}{row["time"][10:]}',
            }
            for row in context['history_rows']
        ]
        if not history_rows:
            empty_label = (
                f'There are no events recorded for the tracking ID {cargo.tracking_id.value}.'
            )
            if empty_label not in content:
                empty_label = None
        map_url = context['map_url']
        parsed_query = parse_qs(urlsplit(map_url).query, keep_blank_values=True)
        map_query = {key: values[0] for key, values in parsed_query.items()}
        map_frame = _map_frame_data(client, map_url)

    return {
        'submitted_id': submitted_id,
        'result': result,
        'history': {'empty_label': empty_label, 'rows': history_rows},
        'map_query': map_query,
        'map_frame': map_frame,
        'message': context.get('message'),
        'cargo_section': 'id="cargo-result"' in content,
        'history_section': 'id="handling-history"' in content,
        'map_frame_element': 'id="tracking-map"' in content,
        'tracking_form': 'id="tracking-form"' in content,
        'alert': 'role="alert"' in content,
    }


def _check_field(mismatches, field, actual, expected):
    if actual != expected:
        mismatches.append(f'{field}: expected {expected!r}, observed {actual!r}')


def _check_map_frame(mismatches, actual, golden_map):
    _check_field(
        mismatches,
        'map_frame.fields',
        sorted(actual),
        ['destination', 'lastKnownLocation', 'markers', 'origin', 'statusCode'],
    )
    _check_field(
        mismatches,
        'map_frame.statusCode',
        actual.get('statusCode'),
        golden_map['statusCode'],
    )
    role_keys = {
        'origin': ('originCode', 'originName'),
        'destination': ('destinationCode', 'destinationName'),
        'lastKnownLocation': ('lastKnownLocationCode', 'lastKnownLocationName'),
    }
    for role, (code_key, name_key) in role_keys.items():
        observed_location = actual.get(role, {})
        _check_field(
            mismatches,
            f'map_frame.{role}.fields',
            sorted(observed_location),
            ['code', 'name'],
        )
        _check_field(
            mismatches,
            f'map_frame.{role}.code',
            observed_location.get('code'),
            golden_map[code_key],
        )
        _check_field(
            mismatches,
            f'map_frame.{role}.name',
            observed_location.get('name'),
            golden_map[name_key],
        )

    expected_markers = [
        {
            'role': role,
            'code': golden_map[code_key],
            'name': golden_map[name_key],
            'coordinates': EXPECTED_COORDINATES[golden_map[code_key]],
            'color': (
                STATUS_COLORS[golden_map['statusCode']] if role == 'lastKnownLocation' else 'black'
            ),
        }
        for role, (code_key, name_key) in role_keys.items()
        if golden_map[code_key] in EXPECTED_COORDINATES
    ]
    actual_markers = {marker.get('role'): marker for marker in actual.get('markers', [])}
    _check_field(
        mismatches,
        'map_frame.markers.roles',
        list(actual_markers),
        [marker['role'] for marker in expected_markers],
    )
    for expected_marker in expected_markers:
        role = expected_marker['role']
        actual_marker = actual_markers.get(role, {})
        _check_field(
            mismatches,
            f'map_frame.markers[{role}].fields',
            sorted(actual_marker),
            ['code', 'color', 'coordinates', 'name', 'role'],
        )
        for field in ('code', 'name', 'color'):
            _check_field(
                mismatches,
                f'map_frame.markers[{role}].{field}',
                actual_marker.get(field),
                expected_marker[field],
            )
        _check_field(
            mismatches,
            f'ruling #14: map_frame.markers[{role}].coordinates',
            actual_marker.get('coordinates'),
            expected_marker['coordinates'],
        )


@pytest.mark.django_db
@pytest.mark.parametrize('golden_path', GOLDEN_CASES, ids=lambda path: path.stem)
def test_tracking_page_matches_each_normalized_golden_case(client, golden_path):
    call_command('seed_sample_data')
    golden = json.loads(golden_path.read_text(encoding='utf-8'))
    tracking_id = golden['input']
    regular = _observe(client, tracking_id)
    htmx = _observe(client, tracking_id, htmx=True)
    case_name = golden_path.stem
    expected = deepcopy(golden['observed'])
    mismatches = []

    if expected['result'] is None:
        _check_field(
            mismatches,
            'ruling #12: history.empty_label',
            regular['history']['empty_label'],
            None,
        )
        expected['history']['empty_label'] = None
        expected_message = (
            'tracking ID is required'
            if not tracking_id
            else f'Cargo with tracking ID {tracking_id} not found.'
        )
        _check_field(
            mismatches,
            'ruling #12: visible message',
            regular['message'],
            expected_message,
        )
        _check_field(mismatches, 'ruling #12: visible alert', regular['alert'], True)
        _check_field(mismatches, 'ruling #12: no cargo result', regular['cargo_section'], False)
        _check_field(
            mismatches,
            'ruling #12: no history section',
            regular['history_section'],
            False,
        )
        _check_field(
            mismatches,
            'ruling #12: no map frame',
            regular['map_frame_element'],
            False,
        )
        _check_field(mismatches, 'ruling #12: no map query', regular['map_query'], None)
        _check_field(
            mismatches,
            'ruling #12: regular form remains usable',
            regular['tracking_form'],
            True,
        )
        _check_field(
            mismatches,
            'htmx result has no full form',
            htmx['tracking_form'],
            False,
        )
    elif tracking_id.strip() == 'ABC123':
        _check_field(
            mismatches,
            'ruling #13: result.status_text',
            regular['result']['status_text'],
            'In port New York',
        )
        expected['result']['status_text'] = 'In port New York'
    elif tracking_id == 'MNO456':
        _check_field(
            mismatches,
            'ruling #17: result.eta',
            regular['result']['eta'],
            None,
        )
        expected['result']['eta'] = None

    for field in (
        'submitted_id',
        'result',
        'history',
        'map_query',
        'map_frame',
        'message',
        'cargo_section',
        'history_section',
        'map_frame_element',
        'alert',
    ):
        _check_field(
            mismatches,
            f'htmx and regular form {field}',
            htmx[field],
            regular[field],
        )
    _check_field(mismatches, 'submitted_id', regular['submitted_id'], expected['submitted_id'])
    _check_field(mismatches, 'result', regular['result'], expected['result'])

    if expected['result'] is not None:
        for field, expected_value in expected['result'].items():
            _check_field(
                mismatches,
                f'result.{field}',
                regular['result'].get(field),
                expected_value,
            )
        _check_field(mismatches, 'cargo result section', regular['cargo_section'], True)
        _check_field(mismatches, 'history section', regular['history_section'], True)
        _check_field(mismatches, 'map frame element', regular['map_frame_element'], True)

    _check_field(
        mismatches,
        'history.empty_label',
        regular['history']['empty_label'],
        expected['history']['empty_label'],
    )
    expected_rows = expected['history']['rows']
    actual_rows = regular['history']['rows']
    _check_field(
        mismatches,
        'history.rows.length',
        len(actual_rows),
        len(expected_rows),
    )
    for index in range(max(len(actual_rows), len(expected_rows))):
        actual_row = actual_rows[index] if index < len(actual_rows) else {}
        expected_row = expected_rows[index] if index < len(expected_rows) else {}
        _check_field(
            mismatches,
            f'history.rows[{index}].fields',
            sorted(actual_row),
            sorted(expected_row),
        )
        for field, expected_value in expected_row.items():
            _check_field(
                mismatches,
                f'history.rows[{index}].{field}',
                actual_row.get(field),
                expected_value,
            )

    expected_map = expected['map_query']
    actual_map = regular['map_query']
    _check_field(mismatches, 'map_query.present', actual_map is not None, expected_map is not None)
    if expected_map is not None and actual_map is not None:
        for field in sorted(set(actual_map) | set(expected_map)):
            _check_field(
                mismatches,
                f'map_query.{field}',
                actual_map.get(field),
                expected_map.get(field),
            )
    if expected['map_query'] is not None:
        if regular['map_frame'] is None:
            mismatches.append('map_frame: expected data, observed None')
        else:
            _check_map_frame(mismatches, regular['map_frame'], expected['map_query'])
    assert not mismatches, f'{case_name} field-level differences:\n' + '\n'.join(mismatches)
