import random
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from itertools import pairwise

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


@dataclass(frozen=True)
class TransitEdge:
    voyage_number: str
    from_port: str
    to_port: str
    from_date: datetime
    to_date: datetime


@dataclass(frozen=True)
class TransitPath:
    transit_edges: tuple[TransitEdge, ...]


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
        available_ports = tuple(
            port for port in SAMPLE_PORT_CODES if port not in {origin, destination}
        )
        paths = []
        for _ in range(candidates):
            intermediate_count = self._random_source.randint(1, 5)
            route = (
                origin,
                *self._random_source.sample(available_ports, intermediate_count),
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
