from dataclasses import dataclass
from datetime import datetime

from cargotracker.cargo.domain.dates import as_utc
from cargotracker.location.domain.location import Location
from cargotracker.voyage.domain.voyage import Voyage


@dataclass(frozen=True)
class Leg:
    voyage: Voyage
    load_location: Location
    unload_location: Location
    load_time: datetime
    unload_time: datetime

    def __post_init__(self):
        if not isinstance(self.voyage, Voyage):
            raise TypeError('A leg requires a voyage')
        if not isinstance(self.load_location, Location):
            raise TypeError('A leg requires a load location')
        if not isinstance(self.unload_location, Location):
            raise TypeError('A leg requires an unload location')
        object.__setattr__(self, 'load_time', as_utc(self.load_time, 'load time'))
        object.__setattr__(self, 'unload_time', as_utc(self.unload_time, 'unload time'))
