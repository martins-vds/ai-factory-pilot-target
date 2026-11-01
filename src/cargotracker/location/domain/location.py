from dataclasses import dataclass, field
from typing import ClassVar

from cargotracker.location.domain.un_locode import UnLocode


@dataclass(frozen=True)
class Location:
    unlocode: UnLocode
    name: str = field(compare=False)

    UNKNOWN: ClassVar['Location']

    def __post_init__(self):
        if not isinstance(self.unlocode, UnLocode):
            raise TypeError('A location requires a UN/LOCODE')
        if not isinstance(self.name, str):
            raise TypeError('A location name must be a string')

    def __str__(self):
        return f'{self.name} [{self.unlocode}]'


Location.UNKNOWN = Location(UnLocode('XXXXX'), 'Unknown location')
