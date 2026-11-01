from dataclasses import dataclass
from typing import ClassVar

from cargotracker.cargo.domain.leg import Leg


@dataclass(frozen=True, init=False)
class Itinerary:
    legs: tuple[Leg, ...]

    EMPTY: ClassVar['Itinerary']

    def __init__(self, legs=None):
        if legs is None:
            normalized = ()
        else:
            normalized = tuple(legs)
            if not normalized:
                raise ValueError('An itinerary requires at least one leg')
            if any(not isinstance(leg, Leg) for leg in normalized):
                raise TypeError('An itinerary requires legs')
        object.__setattr__(self, 'legs', normalized)


Itinerary.EMPTY = Itinerary()
