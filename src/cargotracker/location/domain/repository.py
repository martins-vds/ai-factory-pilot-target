from typing import Protocol

from cargotracker.location.domain.location import Location
from cargotracker.location.domain.un_locode import UnLocode


class LocationRepository(Protocol):
    def find(self, unlocode: UnLocode) -> Location: ...

    def find_all(self) -> list[Location]: ...
