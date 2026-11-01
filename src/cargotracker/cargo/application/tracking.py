from cargotracker.cargo.domain.cargo import Cargo
from cargotracker.cargo.domain.repository import CargoRepository
from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.handling.domain.handling_history import HandlingHistory
from cargotracker.handling.domain.repository import HandlingEventRepository


class TrackingLookup:
    def __init__(self, cargos: CargoRepository, handling_events: HandlingEventRepository):
        self._cargos = cargos
        self._handling_events = handling_events

    def find_cargo(self, tracking_id: str) -> Cargo | None:
        return self._cargos.find(TrackingId(tracking_id))

    def find_handling_history(self, cargo: Cargo) -> HandlingHistory:
        return self._handling_events.lookup_handling_history_of_cargo(cargo.tracking_id)
