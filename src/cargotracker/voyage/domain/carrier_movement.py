from dataclasses import dataclass
from datetime import UTC, datetime

from cargotracker.location.domain.location import Location


@dataclass(frozen=True)
class CarrierMovement:
    departure_location: Location
    arrival_location: Location
    departure_time: datetime
    arrival_time: datetime

    def __post_init__(self):
        if not isinstance(self.departure_location, Location) or not isinstance(
            self.arrival_location, Location
        ):
            raise TypeError('A carrier movement requires departure and arrival locations')

        for field in ('departure_time', 'arrival_time'):
            value = getattr(self, field)
            if not isinstance(value, datetime):
                raise TypeError('A carrier movement time must be a datetime')
            if value.utcoffset() is None:
                value = value.replace(tzinfo=UTC)
            else:
                value = value.astimezone(UTC)
            object.__setattr__(self, field, value)
