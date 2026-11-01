from dataclasses import dataclass
from datetime import datetime

from cargotracker.cargo.domain.dates import as_utc
from cargotracker.location.domain.location import Location


@dataclass(frozen=True)
class RouteSpecification:
    origin: Location
    destination: Location
    arrival_deadline: datetime

    def __post_init__(self):
        if not isinstance(self.origin, Location):
            raise TypeError('A route specification requires an origin')
        if not isinstance(self.destination, Location):
            raise TypeError('A route specification requires a destination')
        if self.origin == self.destination:
            raise ValueError("Origin and destination can't be the same")
        object.__setattr__(
            self, 'arrival_deadline', as_utc(self.arrival_deadline, 'arrival deadline')
        )
