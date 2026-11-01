from typing import Protocol

from cargotracker.cargo.domain.cargo import Cargo
from cargotracker.cargo.domain.tracking_id import TrackingId


class CargoRepository(Protocol):
    def upsert(self, cargo: Cargo) -> None: ...

    def find(self, tracking_id: TrackingId) -> Cargo | None: ...

    def find_all(self) -> list[Cargo]: ...
