from typing import Protocol

from cargotracker.voyage.domain.voyage import Voyage
from cargotracker.voyage.domain.voyage_number import VoyageNumber


class VoyageRepository(Protocol):
    def find(self, voyage_number: VoyageNumber) -> Voyage: ...

    def find_all(self) -> list[Voyage]: ...
