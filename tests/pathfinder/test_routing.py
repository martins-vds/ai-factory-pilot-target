import random
from datetime import UTC, datetime

from cargotracker.pathfinder.routing import RoutingService

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
            previous.to_port == current.from_port
            and previous.to_date < current.from_date
            for previous, current in zip(edges, edges[1:])
        )
