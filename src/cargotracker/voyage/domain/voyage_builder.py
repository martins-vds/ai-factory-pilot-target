from datetime import datetime

from cargotracker.location.domain.location import Location
from cargotracker.voyage.domain.carrier_movement import CarrierMovement
from cargotracker.voyage.domain.schedule import Schedule
from cargotracker.voyage.domain.voyage import Voyage
from cargotracker.voyage.domain.voyage_number import VoyageNumber


class VoyageBuilder:
    def __init__(self, voyage_number: VoyageNumber, departure_location: Location):
        if not isinstance(voyage_number, VoyageNumber):
            raise TypeError('A voyage requires a voyage number')
        if not isinstance(departure_location, Location):
            raise TypeError('A voyage requires a departure location')
        self._voyage_number = voyage_number
        self._departure_location = departure_location
        self._carrier_movements = []

    def add_movement(
        self, arrival_location: Location, departure_time: datetime, arrival_time: datetime
    ):
        self._carrier_movements.append(
            CarrierMovement(
                self._departure_location,
                arrival_location,
                departure_time,
                arrival_time,
            )
        )
        self._departure_location = arrival_location
        return self

    def build(self) -> Voyage:
        if not self._carrier_movements:
            raise ValueError('A voyage schedule must contain at least one movement')
        return Voyage(self._voyage_number, Schedule(tuple(self._carrier_movements)))
