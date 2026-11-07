import random
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from itertools import pairwise

from cargotracker.pathfinder.domain.transit_edge import TransitEdge
from cargotracker.pathfinder.domain.transit_path import TransitPath

SAMPLE_PORT_CODES = (
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
SAMPLE_VOYAGE_NUMBERS = ('0100S', '0200T', '0300A', '0400S', '0301S')


class RoutingService:
    def __init__(
        self,
        random_source: random.Random | None = None,
        clock: Callable[[], datetime] | None = None,
    ):
        self._random_source = random_source if random_source is not None else random.Random()
        self._clock = clock if clock is not None else lambda: datetime.now(UTC)

    def find_shortest_paths(self, origin: str, destination: str) -> tuple[TransitPath, ...]:
        candidates = self._random_source.randint(3, 5)
        available_ports = [port for port in SAMPLE_PORT_CODES if port not in {origin, destination}]
        paths = []
        for _ in range(candidates):
            self._random_source.shuffle(available_ports)
            intermediate_count = (
                self._random_source.randint(1, 5)
                if len(available_ports) > 4
                else len(available_ports)
            )
            available_ports = available_ports[:intermediate_count]
            route = (
                origin,
                *available_ports,
                destination,
            )
            edges = []
            previous_date = _as_utc(self._clock())
            for from_port, to_port in pairwise(route):
                departure = self._next_date(previous_date)
                arrival = self._next_date(departure)
                edges.append(
                    TransitEdge(
                        voyage_number=self._random_source.choice(SAMPLE_VOYAGE_NUMBERS),
                        from_port=from_port,
                        to_port=to_port,
                        from_date=departure,
                        to_date=arrival,
                    )
                )
                previous_date = arrival
            paths.append(TransitPath(tuple(edges)))
        return tuple(paths)

    def _next_date(self, value: datetime) -> datetime:
        return value + timedelta(days=1, hours=self._random_source.randint(-8, 8))


def _as_utc(value: datetime) -> datetime:
    if value.utcoffset() is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)
