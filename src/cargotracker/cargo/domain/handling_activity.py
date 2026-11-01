from dataclasses import dataclass
from typing import ClassVar

from cargotracker.location.domain.location import Location
from cargotracker.voyage.domain.voyage import Voyage


@dataclass(frozen=True)
class HandlingActivity:
    event_type: str | None = None
    location: Location | None = None
    voyage: Voyage | None = None

    EMPTY: ClassVar['HandlingActivity']

    def __post_init__(self):
        if self.event_type is None and self.location is None and self.voyage is None:
            return
        if not isinstance(self.event_type, str):
            raise TypeError('A handling activity requires an event type')
        if not isinstance(self.location, Location):
            raise TypeError('A handling activity requires a location')
        if self.voyage is not None and not isinstance(self.voyage, Voyage):
            raise TypeError('A handling activity voyage must be a voyage')


HandlingActivity.EMPTY = HandlingActivity()
