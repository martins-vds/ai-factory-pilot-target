from types import SimpleNamespace

from cargotracker.booking.application.dashboard import CargoDashboard
from cargotracker.cargo.domain.delivery import TransportStatus
from cargotracker.cargo.domain.tracking_id import TrackingId


class CargoRepository:
    def __init__(self, cargos):
        self.cargos = cargos

    def find(self, tracking_id):
        return self.cargos.get(tracking_id)

    def find_all(self):
        return list(self.cargos.values()) if isinstance(self.cargos, dict) else self.cargos


def _cargo(has_legs, transport_status):
    return SimpleNamespace(
        itinerary=SimpleNamespace(legs=(object(),) if has_legs else ()),
        delivery=SimpleNamespace(transport_status=transport_status),
    )


def test_dashboard_partitions_cargos_in_source_order():
    first_routed = _cargo(True, TransportStatus.IN_PORT)
    not_routed = _cargo(False, TransportStatus.NOT_RECEIVED)
    claimed = _cargo(True, TransportStatus.CLAIMED)
    second_routed = _cargo(True, TransportStatus.ONBOARD_CARRIER)
    dashboard = CargoDashboard(
        CargoRepository([first_routed, not_routed, claimed, second_routed])
    )

    result = dashboard.get_dashboard()

    assert result.routed_cargos == [first_routed, second_routed]
    assert result.not_routed_cargos == [not_routed]
    assert result.claimed_cargos == [claimed]


def test_cargo_details_returns_the_requested_cargo():
    tracking_id = TrackingId('ABC123')
    cargo = SimpleNamespace(tracking_id=tracking_id)
    dashboard = CargoDashboard(CargoRepository({tracking_id: cargo}))

    assert dashboard.get_cargo_details(tracking_id) is cargo
