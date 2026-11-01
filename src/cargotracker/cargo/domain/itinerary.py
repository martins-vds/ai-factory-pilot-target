from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from cargotracker.cargo.domain.leg import Leg

if TYPE_CHECKING:
    from cargotracker.handling.domain.handling_event import HandlingEvent


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

    def is_expected(self, event: 'HandlingEvent') -> bool:
        if not self.legs:
            return True
        if event.event_type == 'CUSTOMS':
            return True
        checkers = {
            'RECEIVE': self._receive_matches_first_leg,
            'LOAD': self._load_matches_leg,
            'UNLOAD': self._unload_matches_leg,
            'CLAIM': self._claim_matches_destination,
        }
        checker = checkers.get(event.event_type)
        return checker(event) if checker is not None else False

    def _receive_matches_first_leg(self, event: 'HandlingEvent') -> bool:
        return self.legs[0].load_location == event.location

    def _load_matches_leg(self, event: 'HandlingEvent') -> bool:
        return any(
            leg.load_location == event.location and leg.voyage == event.voyage
            for leg in self.legs
        )

    def _unload_matches_leg(self, event: 'HandlingEvent') -> bool:
        return any(
            leg.unload_location == event.location and leg.voyage == event.voyage
            for leg in self.legs
        )

    def _claim_matches_destination(self, event: 'HandlingEvent') -> bool:
        return self.legs[-1].unload_location == event.location


Itinerary.EMPTY = Itinerary()
