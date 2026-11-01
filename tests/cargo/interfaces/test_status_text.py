from datetime import UTC, datetime

from cargotracker.cargo.domain.cargo import Cargo
from cargotracker.cargo.domain.delivery import Delivery, RoutingStatus, TransportStatus
from cargotracker.cargo.domain.handling_activity import HandlingActivity
from cargotracker.cargo.domain.route_specification import RouteSpecification
from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.cargo.interfaces.tracking.status_text import get_status_text
from cargotracker.location.domain.location import Location
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.voyage.domain.schedule import Schedule
from cargotracker.voyage.domain.voyage import Voyage
from cargotracker.voyage.domain.voyage_number import VoyageNumber

ORIGIN = Location(UnLocode('CNHKG'), 'Hong Kong')
NEW_YORK = Location(UnLocode('USNYC'), 'New York')
HELSINKI = Location(UnLocode('FIHEL'), 'Helsinki')
DALLAS = Location(UnLocode('USDAL'), 'Dallas')
CALCULATED_AT = datetime(2026, 11, 1, tzinfo=UTC)
DEADLINE = datetime(2026, 12, 1, tzinfo=UTC)
VOYAGE = Voyage(VoyageNumber('0100S'), Schedule.EMPTY)


def _cargo(status, last_known_location=None, current_voyage=None):
    return Cargo(
        tracking_id=TrackingId('ABC123'),
        route_specification=RouteSpecification(ORIGIN, HELSINKI, DEADLINE),
        delivery=Delivery(
            transport_status=status,
            last_known_location=last_known_location,
            current_voyage=current_voyage,
            misdirected=False,
            eta=None,
            next_expected_activity=HandlingActivity.EMPTY,
            unloaded_at_destination=False,
            routing_status=RoutingStatus.ROUTED,
            calculated_at=CALCULATED_AT,
        ),
    )


def test_in_port_status_names_last_known_location():
    cargo = _cargo(TransportStatus.IN_PORT, NEW_YORK)

    assert cargo.tracking_id.value == 'ABC123'
    assert get_status_text(cargo) == 'In port New York'
    assert cargo.route_specification.destination == HELSINKI
    assert cargo.route_specification.destination.unlocode.value == 'FIHEL'


def test_onboard_status_names_current_voyage():
    cargo = _cargo(TransportStatus.ONBOARD_CARRIER, NEW_YORK, VOYAGE)

    assert get_status_text(cargo) == 'Onboard voyage 0100S'


def test_not_received_status_text():
    cargo = _cargo(TransportStatus.NOT_RECEIVED)

    assert get_status_text(cargo) == 'Not received'


def test_claimed_status_text():
    cargo = _cargo(TransportStatus.CLAIMED, DALLAS)

    assert get_status_text(cargo) == 'Claimed'


def test_unknown_status_text():
    cargo = _cargo(TransportStatus.UNKNOWN)

    assert get_status_text(cargo) == '[Unknown status]'
