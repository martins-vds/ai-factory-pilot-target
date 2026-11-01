from datetime import UTC, datetime, timedelta, timezone

from cargotracker.cargo.domain.cargo import Cargo
from cargotracker.cargo.domain.delivery import Delivery, RoutingStatus, TransportStatus
from cargotracker.cargo.domain.handling_activity import HandlingActivity
from cargotracker.cargo.domain.itinerary import Itinerary
from cargotracker.cargo.domain.route_specification import RouteSpecification
from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.handling.domain.handling_event import HandlingEvent, HandlingEventType
from cargotracker.handling.domain.handling_history import HandlingHistory
from cargotracker.location.domain.location import Location
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.voyage.domain.schedule import Schedule
from cargotracker.voyage.domain.voyage import Voyage
from cargotracker.voyage.domain.voyage_number import VoyageNumber


def _cargo():
    origin = Location(UnLocode('USNYC'), 'New York')
    destination = Location(UnLocode('FIHEL'), 'Helsinki')
    return Cargo(
        TrackingId('ABC123'),
        RouteSpecification(origin, destination, datetime(2026, 11, 12, tzinfo=UTC)),
        Delivery(
            TransportStatus.NOT_RECEIVED,
            None,
            None,
            False,
            None,
            HandlingActivity.EMPTY,
            False,
            RoutingStatus.NOT_ROUTED,
            datetime(2026, 11, 1, tzinfo=UTC),
        ),
        Itinerary.EMPTY,
        origin,
    )


def test_handling_history_deduplicates_and_orders_events_by_completion_time():
    cargo = _cargo()
    location = Location(UnLocode('USNYC'), 'New York')
    early = HandlingEvent(
        cargo,
        datetime(2026, 11, 1, tzinfo=UTC),
        datetime(2026, 11, 1, 1, tzinfo=UTC),
        HandlingEventType.RECEIVE,
        location,
    )
    duplicate = HandlingEvent(
        cargo,
        datetime(2026, 11, 1, tzinfo=timezone(timedelta(hours=2))),
        datetime(2026, 11, 2, tzinfo=UTC),
        HandlingEventType.RECEIVE,
        location,
    )
    later = HandlingEvent(
        cargo,
        datetime(2026, 11, 3, tzinfo=UTC),
        datetime(2026, 11, 3, tzinfo=UTC),
        HandlingEventType.CLAIM,
        location,
    )

    history = HandlingHistory([later, duplicate, early])

    assert history.events == (early, later)
