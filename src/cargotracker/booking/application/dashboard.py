from dataclasses import dataclass

from cargotracker.cargo.domain.cargo import Cargo
from cargotracker.cargo.domain.delivery import TransportStatus
from cargotracker.cargo.domain.repository import CargoRepository
from cargotracker.cargo.domain.tracking_id import TrackingId


@dataclass
class DashboardCargos:
    routed_cargos: list[Cargo]
    not_routed_cargos: list[Cargo]
    claimed_cargos: list[Cargo]


class CargoDashboard:
    def __init__(self, cargo_repository: CargoRepository):
        self._cargo_repository = cargo_repository

    def get_dashboard(self) -> DashboardCargos:
        cargos = self._cargo_repository.find_all()
        return DashboardCargos(
            routed_cargos=[
                cargo
                for cargo in cargos
                if cargo.itinerary.legs
                and cargo.delivery.transport_status is not TransportStatus.CLAIMED
            ],
            not_routed_cargos=[cargo for cargo in cargos if not cargo.itinerary.legs],
            claimed_cargos=[
                cargo
                for cargo in cargos
                if cargo.delivery.transport_status is TransportStatus.CLAIMED
            ],
        )

    def get_cargo_details(self, tracking_id: TrackingId) -> Cargo | None:
        return self._cargo_repository.find(tracking_id)
