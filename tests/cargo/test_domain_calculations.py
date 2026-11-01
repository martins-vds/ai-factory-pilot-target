from datetime import UTC, datetime, timedelta

import pytest

from cargotracker.cargo.domain.cargo import Cargo
from cargotracker.cargo.domain.delivery import Delivery, RoutingStatus, TransportStatus
from cargotracker.cargo.domain.handling_activity import HandlingActivity
from cargotracker.cargo.domain.itinerary import Itinerary
from cargotracker.cargo.domain.leg import Leg
from cargotracker.cargo.domain.route_specification import RouteSpecification
from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.handling.domain.handling_event import HandlingEvent, HandlingEventType
from cargotracker.handling.domain.handling_history import HandlingHistory
from cargotracker.location.domain.location import Location
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.voyage.domain.schedule import Schedule
from cargotracker.voyage.domain.voyage import Voyage
from cargotracker.voyage.domain.voyage_number import VoyageNumber

ORIGIN = Location(UnLocode('USNYC'), 'New York')
TRANSFER = Location(UnLocode('NLRTM'), 'Rotterdam')
DESTINATION = Location(UnLocode('FIHEL'), 'Helsinki')
FIRST_VOYAGE = Voyage(VoyageNumber('CM001'), Schedule.EMPTY)
SECOND_VOYAGE = Voyage(VoyageNumber('CM002'), Schedule.EMPTY)
CALCULATED_AT = datetime(2026, 11, 1, tzinfo=UTC)
DEADLINE = datetime(2026, 12, 1, tzinfo=UTC)


def _two_leg_route():
    legs = (
        Leg(
            FIRST_VOYAGE,
            ORIGIN,
            TRANSFER,
            datetime(2026, 10, 1, tzinfo=UTC),
            datetime(2026, 10, 5, tzinfo=UTC),
        ),
        Leg(
            SECOND_VOYAGE,
            TRANSFER,
            DESTINATION,
            datetime(2026, 10, 7, tzinfo=UTC),
            datetime(2026, 10, 12, tzinfo=UTC),
        ),
    )
    return RouteSpecification(ORIGIN, DESTINATION, DEADLINE), Itinerary(legs)


def _cargo(route_specification, itinerary):
    delivery = Delivery(
        TransportStatus.NOT_RECEIVED,
        None,
        None,
        False,
        None,
        HandlingActivity.EMPTY,
        False,
        RoutingStatus.NOT_ROUTED,
        CALCULATED_AT,
    )
    return Cargo(TrackingId('TC08'), route_specification, delivery, itinerary)


def _event(cargo, event_type, location, voyage=None, days_ago=1):
    completed = CALCULATED_AT - timedelta(days=days_ago)
    return HandlingEvent(
        cargo,
        completed,
        completed,
        event_type,
        location,
        voyage,
    )


def _derive_delivery(route_specification, itinerary, event_data=None):
    cargo = _cargo(route_specification, itinerary)
    events = ()
    if event_data is not None:
        events = (_event(cargo, *event_data),)
    return Delivery.derived_from(
        route_specification,
        itinerary,
        HandlingHistory(events),
        CALCULATED_AT,
    )


@pytest.mark.parametrize('event_type', tuple(HandlingEventType))
def test_empty_itinerary_accepts_every_declared_handling_type(event_type):
    route_specification, _ = _two_leg_route()
    cargo = _cargo(route_specification, Itinerary.EMPTY)
    voyage = FIRST_VOYAGE if event_type.requires_voyage else None
    event = _event(cargo, event_type, ORIGIN, voyage)

    assert Itinerary.EMPTY.is_expected(event)


@pytest.mark.parametrize(
    ('event_type', 'location', 'voyage', 'expected'),
    [
        (HandlingEventType.RECEIVE, ORIGIN, None, True),
        (HandlingEventType.RECEIVE, TRANSFER, None, False),
        (HandlingEventType.LOAD, ORIGIN, FIRST_VOYAGE, True),
        (HandlingEventType.LOAD, ORIGIN, SECOND_VOYAGE, False),
        (HandlingEventType.LOAD, TRANSFER, FIRST_VOYAGE, False),
        (HandlingEventType.UNLOAD, TRANSFER, FIRST_VOYAGE, True),
        (HandlingEventType.UNLOAD, TRANSFER, SECOND_VOYAGE, False),
        (HandlingEventType.UNLOAD, ORIGIN, FIRST_VOYAGE, False),
        (HandlingEventType.CLAIM, DESTINATION, None, True),
        (HandlingEventType.CLAIM, TRANSFER, None, False),
        (HandlingEventType.CUSTOMS, TRANSFER, None, True),
    ],
)
def test_itinerary_matches_only_expected_event_location_and_voyage(
    event_type, location, voyage, expected
):
    route_specification, itinerary = _two_leg_route()
    cargo = _cargo(route_specification, itinerary)

    assert itinerary.is_expected(_event(cargo, event_type, location, voyage)) is expected


def test_route_specification_requires_matching_endpoints_and_strictly_early_arrival():
    route_specification, itinerary = _two_leg_route()
    arrival = itinerary.legs[-1].unload_time

    assert route_specification.is_satisfied_by(itinerary)
    assert not route_specification.is_satisfied_by(Itinerary.EMPTY)
    assert not RouteSpecification(TRANSFER, DESTINATION, DEADLINE).is_satisfied_by(itinerary)
    assert not RouteSpecification(ORIGIN, TRANSFER, DEADLINE).is_satisfied_by(itinerary)
    assert not RouteSpecification(ORIGIN, DESTINATION, arrival).is_satisfied_by(itinerary)
    assert not RouteSpecification(
        ORIGIN, DESTINATION, arrival - timedelta(seconds=1)
    ).is_satisfied_by(itinerary)


@pytest.mark.parametrize(
    ('event_type', 'location', 'voyage', 'expected'),
    [
        (None, None, None, TransportStatus.NOT_RECEIVED),
        (HandlingEventType.LOAD, ORIGIN, FIRST_VOYAGE, TransportStatus.ONBOARD_CARRIER),
        (HandlingEventType.UNLOAD, TRANSFER, FIRST_VOYAGE, TransportStatus.IN_PORT),
        (HandlingEventType.RECEIVE, ORIGIN, None, TransportStatus.IN_PORT),
        (HandlingEventType.CUSTOMS, TRANSFER, None, TransportStatus.IN_PORT),
        (HandlingEventType.CLAIM, DESTINATION, None, TransportStatus.CLAIMED),
    ],
)
def test_delivery_derives_transport_status_from_latest_event(
    event_type, location, voyage, expected
):
    route_specification, itinerary = _two_leg_route()
    event_data = (event_type, location, voyage) if event_type is not None else None

    assert _derive_delivery(route_specification, itinerary, event_data).transport_status is expected


def test_delivery_derives_routing_eta_and_first_activity_without_events():
    route_specification, itinerary = _two_leg_route()

    delivery = _derive_delivery(route_specification, itinerary)

    assert delivery.routing_status is RoutingStatus.ROUTED
    assert not delivery.misdirected
    assert delivery.transport_status is TransportStatus.NOT_RECEIVED
    assert delivery.last_known_location is None
    assert delivery.current_voyage is None
    assert delivery.eta == itinerary.legs[-1].unload_time
    assert delivery.next_expected_activity == HandlingActivity('RECEIVE', ORIGIN)
    assert not delivery.unloaded_at_destination
    assert delivery.calculated_at == CALCULATED_AT


@pytest.mark.parametrize(
    ('route_specification', 'itinerary', 'expected_status'),
    [
        (
            RouteSpecification(ORIGIN, DESTINATION, DEADLINE),
            Itinerary.EMPTY,
            RoutingStatus.NOT_ROUTED,
        ),
        (
            RouteSpecification(TRANSFER, DESTINATION, DEADLINE),
            _two_leg_route()[1],
            RoutingStatus.MISROUTED,
        ),
    ],
)
def test_delivery_has_no_eta_or_activity_when_unrouted_or_route_misses_specification(
    route_specification, itinerary, expected_status
):
    delivery = _derive_delivery(route_specification, itinerary)

    assert delivery.routing_status is expected_status
    assert delivery.eta is None
    assert delivery.next_expected_activity is HandlingActivity.EMPTY


def test_delivery_keeps_transport_status_when_latest_event_is_misdirected():
    route_specification, itinerary = _two_leg_route()

    delivery = _derive_delivery(
        route_specification,
        itinerary,
        (HandlingEventType.LOAD, TRANSFER, FIRST_VOYAGE),
    )

    assert delivery.transport_status is TransportStatus.ONBOARD_CARRIER
    assert delivery.current_voyage == FIRST_VOYAGE
    assert delivery.misdirected
    assert delivery.routing_status is RoutingStatus.ROUTED
    assert delivery.eta is None
    assert delivery.next_expected_activity is HandlingActivity.EMPTY


@pytest.mark.parametrize(
    ('event_type', 'location', 'voyage', 'expected_activity', 'unloaded'),
    [
        (
            HandlingEventType.RECEIVE,
            ORIGIN,
            None,
            HandlingActivity('LOAD', ORIGIN, FIRST_VOYAGE),
            False,
        ),
        (
            HandlingEventType.LOAD,
            ORIGIN,
            FIRST_VOYAGE,
            HandlingActivity('UNLOAD', TRANSFER, FIRST_VOYAGE),
            False,
        ),
        (
            HandlingEventType.UNLOAD,
            TRANSFER,
            FIRST_VOYAGE,
            HandlingActivity('LOAD', TRANSFER, SECOND_VOYAGE),
            False,
        ),
        (
            HandlingEventType.UNLOAD,
            DESTINATION,
            SECOND_VOYAGE,
            HandlingActivity('CLAIM', DESTINATION),
            True,
        ),
        (
            HandlingEventType.CLAIM,
            DESTINATION,
            None,
            HandlingActivity.EMPTY,
            False,
        ),
    ],
)
def test_delivery_calculates_next_activity_after_latest_event(
    event_type, location, voyage, expected_activity, unloaded
):
    route_specification, itinerary = _two_leg_route()

    delivery = _derive_delivery(
        route_specification,
        itinerary,
        (event_type, location, voyage),
    )

    assert delivery.next_expected_activity == expected_activity
    assert delivery.unloaded_at_destination is unloaded
    assert delivery.eta == itinerary.legs[-1].unload_time


def test_quirk52_next_activity_uses_first_matching_location():
    voyage_1 = Voyage(VoyageNumber('V1'), Schedule.EMPTY)
    voyage_2 = Voyage(VoyageNumber('V2'), Schedule.EMPTY)
    voyage_3 = Voyage(VoyageNumber('V3'), Schedule.EMPTY)
    location_a = Location(UnLocode('USNYC'), 'A')
    location_b = Location(UnLocode('NLRTM'), 'B')
    location_c = Location(UnLocode('FIHEL'), 'C')
    itinerary = Itinerary(
        (
            Leg(voyage_1, location_a, location_b, CALCULATED_AT, CALCULATED_AT + timedelta(days=1)),
            Leg(
                voyage_2,
                location_b,
                location_a,
                CALCULATED_AT + timedelta(days=2),
                CALCULATED_AT + timedelta(days=3),
            ),
            Leg(
                voyage_3,
                location_a,
                location_c,
                CALCULATED_AT + timedelta(days=4),
                CALCULATED_AT + timedelta(days=5),
            ),
        )
    )
    route_specification = RouteSpecification(
        location_a, location_c, CALCULATED_AT + timedelta(days=6)
    )

    delivery = _derive_delivery(
        route_specification,
        itinerary,
        (HandlingEventType.LOAD, location_a, voyage_3),
    )

    assert not delivery.misdirected
    assert delivery.next_expected_activity == HandlingActivity('UNLOAD', location_b, voyage_1)


def test_delivery_matches_golden_states_for_abc_jkl_def_and_mno():
    hong_kong = Location(UnLocode('CNHKG'), 'Hong Kong')
    new_york = Location(UnLocode('USNYC'), 'New York')
    helsinki = Location(UnLocode('FIHEL'), 'Helsinki')
    hangzhou = Location(UnLocode('CNHGH'), 'Hangzhou')
    stockholm = Location(UnLocode('SESTO'), 'Stockholm')
    dallas = Location(UnLocode('USDAL'), 'Dallas')
    melbourne = Location(UnLocode('AUMEL'), 'Melbourne')
    voyage_0100s = Voyage(VoyageNumber('0100S'), Schedule.EMPTY)
    voyage_0200t = Voyage(VoyageNumber('0200T'), Schedule.EMPTY)
    abc_arrival = CALCULATED_AT + timedelta(days=14)
    abc_specification = RouteSpecification(hong_kong, helsinki, abc_arrival + timedelta(days=1))
    abc_itinerary = Itinerary(
        (
            Leg(
                voyage_0100s,
                hong_kong,
                new_york,
                CALCULATED_AT,
                CALCULATED_AT + timedelta(days=9),
            ),
            Leg(
                voyage_0200t,
                new_york,
                helsinki,
                CALCULATED_AT + timedelta(days=10),
                abc_arrival,
            ),
        )
    )
    abc = _derive_delivery(
        abc_specification,
        abc_itinerary,
        (HandlingEventType.UNLOAD, new_york, voyage_0100s),
    )
    jkl_arrival = CALCULATED_AT + timedelta(days=20)
    jkl_specification = RouteSpecification(hangzhou, stockholm, jkl_arrival + timedelta(days=1))
    jkl_itinerary = Itinerary(
        (
            Leg(
                voyage_0100s,
                hangzhou,
                new_york,
                CALCULATED_AT,
                CALCULATED_AT + timedelta(days=12),
            ),
            Leg(
                voyage_0200t,
                new_york,
                stockholm,
                CALCULATED_AT + timedelta(days=13),
                jkl_arrival,
            ),
        )
    )
    jkl = _derive_delivery(
        jkl_specification,
        jkl_itinerary,
        (HandlingEventType.LOAD, new_york, voyage_0100s),
    )
    def_specification = RouteSpecification(hong_kong, melbourne, CALCULATED_AT + timedelta(days=30))
    def_delivery = _derive_delivery(def_specification, Itinerary.EMPTY)
    mno_arrival = CALCULATED_AT - timedelta(days=28)
    mno_specification = RouteSpecification(new_york, dallas, CALCULATED_AT + timedelta(days=1))
    mno_itinerary = Itinerary(
        (
            Leg(
                voyage_0200t,
                new_york,
                dallas,
                mno_arrival - timedelta(days=5),
                mno_arrival,
            ),
        )
    )
    mno = _derive_delivery(
        mno_specification,
        mno_itinerary,
        (HandlingEventType.CLAIM, dallas, None, 26),
    )

    assert abc.transport_status is TransportStatus.IN_PORT
    assert abc.last_known_location == new_york
    assert not abc.misdirected
    assert abc.next_expected_activity == HandlingActivity('LOAD', new_york, voyage_0200t)
    assert abc.eta == abc_arrival

    assert jkl.transport_status is TransportStatus.ONBOARD_CARRIER
    assert jkl.current_voyage == voyage_0100s
    assert jkl.misdirected
    assert jkl.eta is None
    assert jkl.next_expected_activity is HandlingActivity.EMPTY

    assert def_delivery.transport_status is TransportStatus.NOT_RECEIVED
    assert def_delivery.routing_status is RoutingStatus.NOT_ROUTED
    assert def_delivery.eta is None
    assert def_delivery.next_expected_activity is HandlingActivity.EMPTY

    assert mno.transport_status is TransportStatus.CLAIMED
    assert not mno.misdirected
    assert mno.eta == mno_arrival
    assert mno.eta < mno.calculated_at
    assert mno.next_expected_activity is HandlingActivity.EMPTY
