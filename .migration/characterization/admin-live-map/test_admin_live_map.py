import json
from pathlib import Path

FIXTURES = Path(__file__).parent


def load(name):
    return json.loads((FIXTURES / name).read_text(encoding='utf-8'))


def test_cargo_source_shape_and_baseline_sentinel():
    cargos = load('cargo-before-handling.json')
    assert [cargo['trackingId'] for cargo in cargos] == [
        'ABC123',
        'JKL567',
        'DEF789',
        'MNO456',
    ]
    assert all(
        set(cargo)
        == {
            'trackingId',
            'routingStatus',
            'misdirected',
            'transportStatus',
            'atDestination',
            'origin',
            'lastKnownLocation',
        }
        for cargo in cargos
    )
    assert cargos[2]['lastKnownLocation'] == 'Unknown'


def test_handling_registration_acceptance_golden():
    before = next(
        cargo for cargo in load('cargo-before-handling.json') if cargo['trackingId'] == 'DEF789'
    )
    after = next(
        cargo for cargo in load('cargo-after-handling.json') if cargo['trackingId'] == 'DEF789'
    )
    assert (before['transportStatus'], before['lastKnownLocation']) == (
        'NOT_RECEIVED',
        'Unknown',
    )
    assert (after['transportStatus'], after['lastKnownLocation']) == (
        'IN_PORT',
        'CNHKG',
    )
    assert after['routingStatus'] == 'MISROUTED'


def test_marker_coordinate_selection_and_source_offsets():
    cargos = load('cargo-after-handling.json')
    markers = load('browser-observations.json')['markers_after_receive']
    configured = {'USNYC': (41, -74), 'CNHKG': (22, 114), 'USDAL': (33, -97)}
    assert [marker['trackingId'] for marker in markers] == [cargo['trackingId'] for cargo in cargos]
    for cargo, marker in zip(cargos, markers):
        location = (
            cargo['origin']
            if cargo['transportStatus'] == 'NOT_RECEIVED'
            else cargo['lastKnownLocation']
        )
        base_lat, base_lon = configured[location]
        assert marker['location'] == location
        assert -3 <= marker['position']['lat'] - base_lat <= -1
        assert -3 <= marker['position']['lon'] - base_lon <= -1


def test_marker_status_precedence_and_colors():
    cases = load('edge-cases.json')['status_precedence_and_colors']
    assert [case['color'] for case in cases] == [
        'grey',
        'red',
        'red',
        'black',
        'green',
        'green',
        'black',
        'red',
    ]


def test_tooltip_fields_and_unknown_sentinel_label():
    observations = load('browser-observations.json')
    assert 'Transport Status:  In port' in observations['markers_after_receive'][0]['tooltip_html']
    sentinel = load('edge-cases.json')['unknown_sentinel_not_received']
    assert sentinel['selected_marker_location'] == 'CNHKG'
    assert sentinel['tooltip_html'].endswith('Last known location: undefined')


def test_marker_navigation_opens_cargo_admin_page():
    navigation = load('browser-observations.json')['navigation']
    assert navigation['url'].endswith('/admin/show.xhtml?trackingId=DEF789')
    assert navigation['target'] == 'winMap'
    assert navigation['window_features'].startswith('height=')


def test_empty_and_http_error_responses():
    cases = load('edge-cases.json')
    for name in ('empty_response', 'http_500_with_json_array'):
        case = cases[name]
        assert case['markers'] == 0
        assert case['scale_control'] is True
        assert case['user_message'] is None


def test_network_failure_is_only_logged():
    failure = load('edge-cases.json')['network_failure']
    assert failure['console'] == 'cannot fetch cargos'
    assert failure['user_message'] is None
    assert failure['scale_control'] is False


def test_non_not_received_unknown_location_fails_marker_creation():
    failure = load('edge-cases.json')['unknown_sentinel_on_in_port_controlled_input']
    assert failure['marker_count'] == 0
    assert failure['error'] == 'Invalid LatLng object: (NaN, NaN)'


def test_page_frame_provider_and_connection_status():
    observations = load('browser-observations.json')
    page = observations['page']
    assert page['title'] == 'Live Map'
    assert page['frame_height_px'] == 960
    assert page['map_height_px'] == 600
    assert page['initial_zoom'] == 2
    assert page['connection_status'] == 'online'
    assert observations['providers']['leaflet_assets_and_tiles_loaded'] is True


def test_handling_notification_reloads_map_frame():
    notification = load('browser-observations.json')['handling_event_reload']
    assert notification['post_status'] == 204
    assert notification['map_frame_get_count_before_and_after_event'] == 2
    assert notification['status_after_reconnect'] == 'online'
