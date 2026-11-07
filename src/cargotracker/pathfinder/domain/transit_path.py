from dataclasses import dataclass

from cargotracker.pathfinder.domain.transit_edge import TransitEdge


@dataclass(frozen=True)
class TransitPath:
    transit_edges: tuple[TransitEdge, ...]
