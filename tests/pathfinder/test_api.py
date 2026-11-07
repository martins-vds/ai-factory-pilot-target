import random
from datetime import UTC, datetime, timedelta

import pytest
from django.test import override_settings

from cargotracker.pathfinder import api
from cargotracker.pathfinder.routing import RoutingService

NOW = datetime(2026, 11, 7, 12, 0, tzinfo=UTC)
ENDPOINT = '/rest/graph-traversal/shortest-path'


@override_settings(ROOT_URLCONF='cargotracker.pathfinder.urls')
def test_shortest_path_returns_transit_json_and_ignores_deadline(client, monkeypatch):
    monkeypatch.setattr(
        api,
        'routing_service',
        RoutingService(random_source=random.Random(29), clock=lambda: NOW),
    )

    response = client.get(
        ENDPOINT,
        {'origin': 'CNHKG', 'destination': 'USNYC', 'deadline': '2026-11-08'},
    )

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    paths = response.json()
    assert 3 <= len(paths) <= 5
    for path in paths:
        assert set(path) == {'transitEdges'}
        for edge in path['transitEdges']:
            assert set(edge) == {
                'voyageNumber',
                'fromUnLocode',
                'toUnLocode',
                'fromDate',
                'toDate',
            }
            for field in ('fromDate', 'toDate'):
                value = edge[field]
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


@pytest.mark.parametrize(
    ('query', 'field'),
    [
        ({'origin': 'USNY', 'destination': 'USNYC'}, 'origin'),
        ({'origin': 'CNHKG', 'destination': 'NYC'}, 'destination'),
        ({'origin': 'CNHKG'}, 'destination'),
    ],
)
@override_settings(ROOT_URLCONF='cargotracker.pathfinder.urls')
def test_shortest_path_rejects_missing_or_non_five_character_ports(client, query, field):
    response = client.get(ENDPOINT, query)

    assert response.status_code == 400
    assert field in response.json()['errors']
