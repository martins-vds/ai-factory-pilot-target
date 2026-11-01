from cargotracker.cargo.domain.cargo import Cargo
from cargotracker.cargo.domain.repository import CargoRepository
from cargotracker.cargo.domain.tracking_id import TrackingId


class TrackingLookup:
    def __init__(self, cargos: CargoRepository):
        self._cargos = cargos

    def find_cargo(self, tracking_id: str) -> Cargo | None:
        return self._cargos.find(TrackingId(tracking_id))
