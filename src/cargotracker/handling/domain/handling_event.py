from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum

from cargotracker.cargo.domain.cargo import Cargo
from cargotracker.cargo.domain.dates import as_utc
from cargotracker.location.domain.location import Location
from cargotracker.voyage.domain.voyage import Voyage


class HandlingEventType(StrEnum):
    LOAD = 'LOAD'
    UNLOAD = 'UNLOAD'
    RECEIVE = 'RECEIVE'
    CLAIM = 'CLAIM'
    CUSTOMS = 'CUSTOMS'

    @property
    def requires_voyage(self):
        return self in (HandlingEventType.LOAD, HandlingEventType.UNLOAD)


@dataclass(frozen=True)
class HandlingEvent:
    cargo: Cargo
    completion_time: datetime
    registration_time: datetime = field(compare=False)
    event_type: HandlingEventType
    location: Location
    voyage: Voyage | None = None

    def __post_init__(self):
        if not isinstance(self.cargo, Cargo):
            raise TypeError('A handling event requires a cargo')
        object.__setattr__(self, 'completion_time', as_utc(self.completion_time, 'completion time'))
        object.__setattr__(
            self, 'registration_time', as_utc(self.registration_time, 'registration time')
        )
        if not isinstance(self.event_type, HandlingEventType):
            raise TypeError('A handling event requires an event type')
        if not isinstance(self.location, Location):
            raise TypeError('A handling event requires a location')
        if self.voyage is not None and not isinstance(self.voyage, Voyage):
            raise TypeError('A handling event voyage must be a voyage')
        if self.event_type.requires_voyage and self.voyage is None:
            raise ValueError(f'Voyage is required for event type {self.event_type}')
        if not self.event_type.requires_voyage and self.voyage is not None:
            raise ValueError(f'Voyage is not allowed with event type {self.event_type}')
