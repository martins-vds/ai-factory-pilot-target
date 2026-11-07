import random
from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta, timezone
from itertools import pairwise

import pytest

from cargotracker.pathfinder.routing import RoutingService

NOW = datetime(2026, 11, 7, 12, 0, tzinfo=UTC)
SAMPLE_PORTS = (
    'CNHKG',
    'AUMEL',
    'SESTO',
    'FIHEL',
    'USCHI',
    'JNTKO',
    'DEHAM',
    'CNSHA',
    'NLRTM',
    'SEGOT',
    'CNHGH',
    'USNYC',
    'USDAL',
)
SAMPLE_VOYAGES = {'0100S', '0200T', '0300A', '0400S', '0301S'}


def test_seeded_paths_have_random_candidates_and_connected_increasing_legs():
    service = RoutingService(random_source=random.Random(29), clock=lambda: NOW)

    paths = service.find_shortest_paths('CNHKG', 'USNYC')

    assert 3 <= len(paths) <= 5
    sample_order = {port: index for index, port in enumerate(SAMPLE_PORTS)}
    for path in paths:
        edges = path.transit_edges
        assert 1 <= len(edges) - 1 <= 5
        assert edges[0].from_port == 'CNHKG'
        assert edges[-1].to_port == 'USNYC'
        intermediate_ports = [edge.from_port for edge in edges[1:]]
        assert len(set(intermediate_ports)) == len(intermediate_ports)
        assert all(edge.voyage_number in SAMPLE_VOYAGES for edge in edges)
        assert all(edge.from_date < edge.to_date for edge in edges)
        assert all(
            previous.to_port == current.from_port and previous.to_date < current.from_date
            for previous, current in pairwise(edges)
        )
    assert any(
        [sample_order[edge.from_port] for edge in path.transit_edges[1:]]
        != sorted(sample_order[edge.from_port] for edge in path.transit_edges[1:])
        for path in paths
    )


def test_seeded_random_source_is_repeatable_and_changes_candidate_paths():
    first = RoutingService(random.Random(29), lambda: NOW).find_shortest_paths('CNHKG', 'USNYC')
    repeated = RoutingService(random.Random(29), lambda: NOW).find_shortest_paths('CNHKG', 'USNYC')
    different_seed = RoutingService(random.Random(30), lambda: NOW).find_shortest_paths(
        'CNHKG', 'USNYC'
    )

    assert first == repeated
    assert first != different_seed


def test_seeded_routes_cover_sample_ports_voyages_and_all_random_bounds():
    candidate_counts = set()
    intermediate_counts = set()
    intermediate_ports = set()
    voyage_numbers = set()
    for seed in range(100):
        paths = RoutingService(random.Random(seed), lambda: NOW).find_shortest_paths(
            'CNHKG', 'USNYC'
        )
        candidate_counts.add(len(paths))
        for path in paths:
            intermediate_counts.add(len(path.transit_edges) - 1)
            intermediate_ports.update(edge.from_port for edge in path.transit_edges[1:])
            voyage_numbers.update(edge.voyage_number for edge in path.transit_edges)

    assert candidate_counts == {3, 4, 5}
    assert intermediate_counts == {1, 2, 3, 4, 5}
    assert intermediate_ports == set(SAMPLE_PORTS) - {'CNHKG', 'USNYC'}
    assert voyage_numbers == SAMPLE_VOYAGES


def test_service_normalizes_clock_and_keeps_leg_dates_in_order():
    local_now = datetime(2026, 11, 7, 12, 0, tzinfo=timezone(timedelta(hours=5)))
    paths = RoutingService(random.Random(29), lambda: local_now).find_shortest_paths(
        'CNHKG', 'USNYC'
    )

    for path in paths:
        edges = path.transit_edges
        assert (
            timedelta(hours=16)
            <= edges[0].from_date - local_now.astimezone(UTC)
            <= timedelta(hours=32)
        )
        assert all(edge.from_date.utcoffset() == timedelta(0) for edge in edges)
        assert all(
            timedelta(hours=16) <= edge.to_date - edge.from_date <= timedelta(hours=32)
            for edge in edges
        )
        assert (
            timedelta(hours=16)
            <= edges[0].from_date - local_now.astimezone(UTC)
            <= timedelta(hours=32)
        )
        assert all(
            timedelta(hours=16) <= current.from_date - previous.to_date <= timedelta(hours=32)
            for previous, current in pairwise(edges)
        )


def test_service_assumes_naive_clock_values_are_utc():
    naive_now = datetime(2026, 11, 7, 12, 0)
    paths = RoutingService(random.Random(29), lambda: naive_now).find_shortest_paths(
        'CNHKG', 'USNYC'
    )

    first_departure = paths[0].transit_edges[0].from_date
    assert first_departure.utcoffset() == timedelta(0)
    assert timedelta(hours=16) <= first_departure - NOW <= timedelta(hours=32)


def test_transit_path_and_edges_are_immutable():
    path = RoutingService(random.Random(29), lambda: NOW).find_shortest_paths('CNHKG', 'USNYC')[0]

    with pytest.raises(FrozenInstanceError):
        path.transit_edges[0].from_port = 'AUMEL'
    with pytest.raises(FrozenInstanceError):
        path.transit_edges = ()


def test_default_service_generates_candidate_paths():
    paths = RoutingService().find_shortest_paths('CNHKG', 'USNYC')

    assert 3 <= len(paths) <= 5
    assert paths[0].transit_edges[0].from_date.tzinfo == UTC
