import random
from datetime import UTC, datetime
from itertools import pairwise

from cargotracker.pathfinder.routing import SAMPLE_PORT_CODES, RoutingService

NOW = datetime(2026, 11, 7, 12, 0, tzinfo=UTC)
SAMPLE_VOYAGES = {'0100S', '0200T', '0300A', '0400S', '0301S'}


def test_seeded_paths_have_random_candidates_and_connected_increasing_legs():
    service = RoutingService(random_source=random.Random(29), clock=lambda: NOW)

    paths = service.find_shortest_paths('CNHKG', 'USNYC')

    assert 3 <= len(paths) <= 5
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
    sample_order = {port: index for index, port in enumerate(SAMPLE_PORT_CODES)}
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
