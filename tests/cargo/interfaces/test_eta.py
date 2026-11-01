from datetime import UTC, datetime, timedelta, timezone

from cargotracker.cargo.domain.cargo import Cargo
from cargotracker.cargo.domain.delivery import Delivery, RoutingStatus, TransportStatus
from cargotracker.cargo.domain.handling_activity import HandlingActivity
from cargotracker.cargo.domain.route_specification import RouteSpecification
from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.location.domain.location import Location
from cargotracker.location.domain.un_locode import UnLocode

from cargotracker.cargo.interfaces.tracking.eta import format_eta


ORIGIN = Location(UnLocode('USNYC'), 'New York')
DESTINATION = Location(UnLocode('USDAL'), 'Dallas')
CALCULATED_AT = datetime(2026, 11, 1, tzinfo=UTC)


def _cargo(tracking_id, transport_status, eta):
    delivery = Delivery(
        transport_status=transport_status,
        last_known_location=DESTINATION if transport_status is TransportStatus.CLAIMED else None,
        current_voyage=None,
        misdirected=False,
        eta=eta,
        next_expected_activity=HandlingActivity.EMPTY,
        unloaded_at_destination=transport_status is TransportStatus.CLAIMED,
        routing_status=RoutingStatus.ROUTED,
        calculated_at=CALCULATED_AT,
    )
    return Cargo(
        tracking_id=TrackingId(tracking_id),
        route_specification=RouteSpecification(ORIGIN, DESTINATION, CALCULATED_AT),
        delivery=delivery,
    )


def test_claimed_cargo_hides_eta():
    cargo = _cargo(
        'MNO456',
        TransportStatus.CLAIMED,
        datetime(2026, 10, 4, tzinfo=UTC),
    )

    assert cargo.tracking_id.value == 'MNO456'
    assert format_eta(cargo) is None


def test_eta_uses_utc_and_source_format():
    cargo = _cargo(
        'ABC123',
        TransportStatus.IN_PORT,
        datetime(2026, 11, 2, 14, 5, tzinfo=timezone(timedelta(hours=2))),
    )

    assert format_eta(cargo) == '11/02/2026 12:05 PM UTC'


def test_unknown_eta_uses_existing_question_mark():
    cargo = _cargo('DEF789', TransportStatus.NOT_RECEIVED, None)

    assert format_eta(cargo) == '?'
