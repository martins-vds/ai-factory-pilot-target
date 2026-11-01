from datetime import UTC, datetime, timedelta, timezone

import pytest

from cargotracker.cargo.domain.cargo import Cargo
from cargotracker.cargo.domain.delivery import Delivery, RoutingStatus, TransportStatus
from cargotracker.cargo.domain.handling_activity import HandlingActivity
from cargotracker.cargo.domain.itinerary import Itinerary
from cargotracker.cargo.domain.leg import Leg
from cargotracker.cargo.domain.route_specification import RouteSpecification
from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.location.domain.location import Location
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.voyage.domain.schedule import Schedule
from cargotracker.voyage.domain.voyage import Voyage
from cargotracker.voyage.domain.voyage_number import VoyageNumber


def _location(code, name):
    return Location(UnLocode(code), name)


def test_tracking_id_is_an_immutable_value_object():
    tracking_id = TrackingId('ABC123')

    assert tracking_id == TrackingId('ABC123')
    assert hash(tracking_id) == hash(TrackingId('ABC123'))
    assert tracking_id.value == 'ABC123'
    assert str(tracking_id) == 'ABC123'

    with pytest.raises(AttributeError):
        tracking_id.value = 'DEF789'


def test_tracking_id_rejects_non_string_values():
    with pytest.raises(TypeError, match='A tracking ID must be a string'):
        TrackingId(None)


def test_route_specification_validates_identity_and_normalizes_deadline_to_utc():
    origin = _location('USNYC', 'New York')
    destination = _location('FIHEL', 'Helsinki')
    deadline = datetime(2026, 11, 12, 12, tzinfo=timezone(timedelta(hours=2)))

    specification = RouteSpecification(origin, destination, deadline)

    assert specification.arrival_deadline == datetime(2026, 11, 12, 10, tzinfo=UTC)
    with pytest.raises(ValueError, match="Origin and destination can't be the same"):
        RouteSpecification(origin, _location('USNYC', 'New York City'), deadline)


def test_leg_normalizes_times_to_utc_and_itinerary_copies_ordered_legs():
    new_york = _location('USNYC', 'New York')
    helsinki = _location('FIHEL', 'Helsinki')
    voyage = Voyage(VoyageNumber('CM001'), Schedule.EMPTY)
    load = datetime(2026, 11, 1, 12, tzinfo=timezone(timedelta(hours=2)))
    unload = datetime(2026, 11, 2, 8, tzinfo=UTC)
    leg = Leg(voyage, new_york, helsinki, load, unload)
    legs = [leg]

    itinerary = Itinerary(legs)
    legs.clear()

    assert itinerary.legs == (leg,)
    assert leg.load_time == datetime(2026, 11, 1, 10, tzinfo=UTC)
    assert leg.unload_time == unload
    with pytest.raises(AttributeError):
        itinerary.legs = ()
    with pytest.raises(ValueError, match='An itinerary requires at least one leg'):
        Itinerary([])


def test_cargo_identity_is_its_tracking_id_and_origin_defaults_from_route():
    origin = _location('USNYC', 'New York')
    destination = _location('FIHEL', 'Helsinki')
    specification = RouteSpecification(origin, destination, datetime(2026, 11, 12, tzinfo=UTC))
    delivery = Delivery(
        transport_status=TransportStatus.NOT_RECEIVED,
        last_known_location=None,
        current_voyage=None,
        misdirected=False,
        eta=None,
        next_expected_activity=HandlingActivity.EMPTY,
        unloaded_at_destination=False,
        routing_status=RoutingStatus.NOT_ROUTED,
        calculated_at=datetime(2026, 11, 1, tzinfo=UTC),
    )

    first = Cargo(TrackingId('ABC123'), specification, delivery)
    same_identity = Cargo(
        TrackingId('ABC123'),
        RouteSpecification(origin, destination, datetime(2026, 11, 13, tzinfo=UTC)),
        delivery,
    )

    assert first.origin == origin
    assert first.itinerary == Itinerary.EMPTY
    assert first == same_identity
    assert hash(first) == hash(same_identity)


def test_delivery_preserves_source_status_and_date_fields():
    delivery = Delivery(
        transport_status=TransportStatus.ONBOARD_CARRIER,
        last_known_location=_location('NLRTM', 'Rotterdam'),
        current_voyage=Voyage(VoyageNumber('CM001'), Schedule.EMPTY),
        misdirected=True,
        eta=datetime(2026, 11, 12, tzinfo=UTC),
        next_expected_activity=HandlingActivity('UNLOAD', _location('FIHEL', 'Helsinki')),
        unloaded_at_destination=False,
        routing_status=RoutingStatus.MISROUTED,
        calculated_at=datetime(2026, 11, 1, 10, tzinfo=UTC),
        last_event_id=42,
    )

    assert delivery.transport_status is TransportStatus.ONBOARD_CARRIER
    assert delivery.eta == datetime(2026, 11, 12, tzinfo=UTC)
    assert delivery.next_expected_activity.event_type == 'UNLOAD'
    assert delivery.calculated_at == datetime(2026, 11, 1, 10, tzinfo=UTC)
    assert delivery.last_event_id == 42
