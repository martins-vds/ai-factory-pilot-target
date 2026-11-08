import importlib

import pytest
from django.core.management import call_command
from django.urls import get_resolver, resolve, reverse
from django.urls.resolvers import URLPattern, URLResolver

import cargotracker.booking.urls
import cargotracker.urls


@pytest.fixture(autouse=True)
def reload_urlconfs():
    from django.urls import clear_url_caches

    clear_url_caches()
    importlib.reload(cargotracker.booking.urls)
    importlib.reload(cargotracker.urls)
    clear_url_caches()


def test_booking_routes_have_stable_names_and_paths():
    routes = {
        'wizard': ('/booking/', {}),
        'dashboard': ('/admin/dashboard/', {}),
        'cargo-details': ('/admin/cargo/BK05H123/', {'tracking_id': 'BK05H123'}),
        'route-selection': (
            '/admin/cargo/BK05H123/route/',
            {'tracking_id': 'BK05H123'},
        ),
        'select-itinerary': (
            '/admin/cargo/BK05H123/itineraries/',
            {'tracking_id': 'BK05H123'},
        ),
        'destination-dialog': (
            '/admin/cargo/BK05H123/destination/',
            {'tracking_id': 'BK05H123'},
        ),
        'deadline-dialog': (
            '/admin/cargo/BK05H123/deadline/',
            {'tracking_id': 'BK05H123'},
        ),
    }

    for name, (expected_path, kwargs) in routes.items():
        url = reverse(f'booking:{name}', kwargs=kwargs or None)
        match = resolve(expected_path)

        assert url == expected_path
        assert match.url_name == name
        assert match.namespace == 'booking'
        assert match.kwargs == kwargs
        assert callable(match.func)

    for name, expected_path in (
        ('track', '/'),
        ('handling-report', '/rest/handling/reports'),
        ('cargo_map_frame', '/tracking/map/'),
        ('admin_live_map', '/admin/live-map/'),
    ):
        match = resolve(expected_path)

        assert reverse(name) == expected_path
        assert match.url_name == name
        assert callable(match.func)


def test_booking_routes_enforce_their_supported_http_methods(client):
    assert client.put('/admin/cargo/BK05H123/route/').status_code == 405
    assert client.post('/admin/cargo/BK05H123/itineraries/').status_code == 405
    assert client.post('/rest/graph-traversal/shortest-path').status_code == 405


@pytest.mark.django_db
def test_booking_urls_dispatch_to_the_composed_views(client):
    call_command('seed_sample_data')

    assert client.get('/booking/').status_code == 200
    assert client.get('/admin/dashboard/').status_code == 200
    assert client.get('/admin/cargo/DEF789/').status_code == 200
    assert client.get('/admin/cargo/DEF789/route/').status_code == 200
    assert client.get('/admin/cargo/DEF789/itineraries/').status_code == 200
    assert client.get('/admin/cargo/DEF789/destination/').status_code == 200
    assert client.get('/admin/cargo/DEF789/deadline/').status_code == 200

    response = client.post(
        '/admin/cargo/DEF789/deadline/',
        {'deadline': '2030-11-20'},
    )

    assert response.status_code == 302
    assert response.url == '/admin/dashboard/'


def _route_paths(patterns, prefix=''):
    for pattern in patterns:
        route = f'{prefix}{pattern.pattern}'
        if isinstance(pattern, URLResolver):
            yield from _route_paths(pattern.url_patterns, route)
        elif isinstance(pattern, URLPattern):
            yield route


def test_pathfinder_keeps_its_exact_public_path_without_duplicate_routes(client):
    path = '/rest/graph-traversal/shortest-path'

    assert reverse('pathfinder-shortest-path') == path
    match = resolve(path)

    assert match.url_name == 'pathfinder-shortest-path'
    assert callable(match.func)
    assert list(_route_paths(get_resolver().url_patterns)).count(path.lstrip('/')) == 1
    assert client.get(path).status_code == 400
