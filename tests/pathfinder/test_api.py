import random
import re
from datetime import UTC, datetime, timedelta

import pytest
from django.test import override_settings

from cargotracker.pathfinder import api
from cargotracker.pathfinder.routing import RoutingService

NOW = datetime(2026, 11, 7, 12, 0, tzinfo=UTC)
ENDPOINT = '/rest/graph-traversal/shortest-path'


def test_shortest_path_is_registered_in_project_urlconf(client):
    response = client.get(ENDPOINT, {'origin': 'CNHKG', 'destination': 'USNYC'})

    assert response.status_code == 200


@override_settings(ROOT_URLCONF='cargotracker.pathfinder.urls')
def test_shortest_path_returns_transit_json_and_ignores_deadline(client, monkeypatch):
    monkeypatch.setattr(
        api,
        'routing_service',
        RoutingService(random_source=random.Random(29), clock=lambda: NOW),
    )

    response = client.get(
        ENDPOINT,
        {
            'origin': 'CNHKG',
            'destination': 'USNYC',
            'deadline': '2030-01-01T00:00:00Z',
        },
    )

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    paths = response.json()
    assert 3 <= len(paths) <= 5
    for path in paths:
        assert set(path) == {'transitEdges'}
        for edge in path['transitEdges']:
            assert list(edge) == [
                'fromDate',
                'fromUnLocode',
                'toDate',
                'toUnLocode',
                'voyageNumber',
            ]
            for field in ('fromDate', 'toDate'):
                value = edge[field]
                assert re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z', value)
                parsed = datetime.fromisoformat(value)
                assert parsed.utcoffset() == timedelta(0)

    first_result = response.json()
    monkeypatch.setattr(
        api,
        'routing_service',
        RoutingService(random_source=random.Random(29), clock=lambda: NOW),
    )
    second_response = client.get(ENDPOINT, {'origin': 'CNHKG', 'destination': 'USNYC'})

    assert second_response.json() == first_result


@override_settings(ROOT_URLCONF='cargotracker.pathfinder.urls')
def test_shortest_path_uses_the_default_in_process_service(client):
    response = client.get(ENDPOINT, {'origin': 'CNHKG', 'destination': 'USNYC'})

    assert response.status_code == 200
    assert 3 <= len(response.json()) <= 5


@override_settings(ROOT_URLCONF='cargotracker.pathfinder.urls')
def test_shortest_path_accepts_get_only(client):
    response = client.post(ENDPOINT)

    assert response.status_code == 405


@pytest.mark.parametrize(
    ('query', 'expected_body'),
    [
        (
            {'origin': 'CNHK', 'destination': 'USNYC'},
            (
                'size must be between 5 and 5 (path = '
                '__EJB31_Generated__GraphTraversalService__Intf____Bean__.'
                'findShortestPath.arg0, invalidValue = CNHK)\n'
            ),
        ),
        (
            {'origin': 'CNHKG'},
            (
                'may not be null (path = '
                '__EJB31_Generated__GraphTraversalService__Intf____Bean__.'
                'findShortestPath.arg1, invalidValue = null)\n'
            ),
        ),
    ],
)
@override_settings(ROOT_URLCONF='cargotracker.pathfinder.urls')
def test_shortest_path_validation_matches_characterized_goldens(client, query, expected_body):
    response = client.get(ENDPOINT, query)

    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'text/plain'
    assert response.content.decode() == expected_body


@pytest.mark.parametrize(
    ('query', 'parameter', 'value'),
    [
        ({'origin': 'USNYC1', 'destination': 'USNYC'}, 'arg0', 'USNYC1'),
        ({'origin': ' CNHKG', 'destination': 'USNYC'}, 'arg0', ' CNHKG'),
        ({'origin': 'CNHKG', 'destination': 'USNY'}, 'arg1', 'USNY'),
        ({'origin': 'CNHKG', 'destination': 'NYC'}, 'arg1', 'NYC'),
        ({'origin': 'CNHKG', 'destination': 'USNYC1'}, 'arg1', 'USNYC1'),
        ({'origin': 'CNHKG', 'destination': 'USNYC '}, 'arg1', 'USNYC '),
    ],
)
@override_settings(ROOT_URLCONF='cargotracker.pathfinder.urls')
def test_shortest_path_rejects_non_five_character_ports(client, query, parameter, value):
    response = client.get(ENDPOINT, query)
    expected_body = (
        'size must be between 5 and 5 (path = '
        f'__EJB31_Generated__GraphTraversalService__Intf____Bean__.findShortestPath.{parameter}, '
        f'invalidValue = {value})\n'
    )

    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'text/plain'
    assert response.content.decode() == expected_body
