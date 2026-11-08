from django.urls import get_resolver, resolve, reverse
from django.urls.resolvers import URLPattern, URLResolver


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


def test_booking_routes_enforce_their_supported_http_methods(client):
    assert client.put('/admin/cargo/BK05H123/route/').status_code == 405
    assert client.post('/admin/cargo/BK05H123/itineraries/').status_code == 405
    assert client.post('/rest/graph-traversal/shortest-path').status_code == 405


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
    assert resolve(path).url_name == 'pathfinder-shortest-path'
    assert list(_route_paths(get_resolver().url_patterns)).count(path.lstrip('/')) == 1
    assert client.get(path).status_code == 400
