import pytest
from django.template.loader import render_to_string
from django.urls import reverse


def _cargo(**overrides):
    cargo = {
        'tracking_id': 'ABC123',
        'routing_status': 'ROUTED',
        'misdirected': False,
        'transport_status': 'IN_PORT',
        'at_destination': False,
        'origin': {'code': 'CNHKG', 'name': 'Hong Kong'},
        'last_known_location': {'code': 'USNYC', 'name': 'New York'},
        'location': {'code': 'USNYC', 'name': 'New York'},
        'coordinates': [41, -74],
    }
    cargo.update(overrides)
    return cargo


@pytest.mark.parametrize(
    ('overrides', 'expected_color'),
    [
        (
            {
                'routing_status': 'NOT_ROUTED',
                'misdirected': True,
                'at_destination': True,
            },
            'grey',
        ),
        ({'misdirected': True, 'at_destination': True}, 'red'),
        ({'routing_status': 'MISROUTED'}, 'red'),
        ({'at_destination': True}, 'black'),
        ({'transport_status': 'NOT_RECEIVED'}, 'gold'),
        ({'transport_status': 'IN_PORT'}, 'green'),
        ({'transport_status': 'ONBOARD_CARRIER'}, 'green'),
        ({'transport_status': 'CLAIMED'}, 'black'),
        ({'transport_status': 'UNKNOWN'}, 'red'),
    ],
)
def test_admin_live_map_marker_color_preserves_status_precedence(overrides, expected_color):
    content = render_to_string(
        'admin/_live_map_markers.html',
        {'map_data': [_cargo(**overrides)]},
    )

    assert f'data-color="{expected_color}"' in content


def test_admin_live_map_marker_uses_exact_coordinates_and_source_tooltip_fields():
    content = render_to_string(
        'admin/_live_map_markers.html',
        {'map_data': [_cargo()]},
    )

    assert 'data-coordinates="41,-74"' in content
    expected_url = reverse('booking:cargo-details', args=['ABC123'])
    assert f'Tracking ID: <a href="{expected_url}">ABC123</a>' in content
    assert 'Routing Status: Routed' in content
    assert 'Misdirected: No' in content
    assert 'Transport Status: In port' in content
    assert 'At Destination: No' in content
    assert 'Origin: Hong Kong' in content
    assert 'Last known location: New York' in content
    assert 'window.liveMapMarkers.add' in content


def test_admin_live_map_lists_unmapped_cargo_without_creating_a_marker():
    known_cargo = _cargo()
    unmapped_cargo = _cargo(
        tracking_id='XYZ789',
        location={'code': 'ZZZZZ', 'name': 'Unmapped'},
        coordinates=None,
    )
    content = render_to_string(
        'admin/_live_map_markers.html',
        {'map_data': [known_cargo, unmapped_cargo]},
    )

    assert content.count('<template') == 1
    assert 'href="/admin/cargo/XYZ789/"' in content
    assert 'XYZ789' in content
    assert 'Unmapped' in content
    assert reverse('booking:cargo-details', args=['XYZ789']) in content


def test_admin_live_map_keeps_not_received_unknown_at_its_origin():
    cargo = _cargo(
        tracking_id='DEF789',
        transport_status='NOT_RECEIVED',
        origin={'code': 'CNHKG', 'name': 'Hong Kong'},
        last_known_location={'code': 'XXXXX', 'name': 'Unknown'},
        location={'code': 'CNHKG', 'name': 'Hong Kong'},
        coordinates=[22, 114],
    )
    content = render_to_string(
        'admin/_live_map_markers.html',
        {'map_data': [cargo]},
    )

    assert 'data-coordinates="22,114"' in content
    assert 'Last known location: Unknown' in content
    assert 'undefined' not in content


def test_admin_live_map_has_no_marker_content_for_empty_data():
    assert not render_to_string(
        'admin/_live_map_markers.html',
        {'map_data': []},
    ).strip()
