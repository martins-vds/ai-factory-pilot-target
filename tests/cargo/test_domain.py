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
    with pytest.raises(TypeError) as error:
        TrackingId(None)

    assert str(error.value) == 'A tracking ID must be a string'


def test_route_specification_validates_identity_and_normalizes_deadline_to_utc():
    origin = _location('USNYC', 'New York')
    destination = _location('FIHEL', 'Helsinki')
    deadline = datetime(2026, 11, 12, 12, tzinfo=timezone(timedelta(hours=2)))

    specification = RouteSpecification(origin, destination, deadline)

    assert specification.arrival_deadline == datetime(2026, 11, 12, 10, tzinfo=UTC)
    with pytest.raises(ValueError) as error:
        RouteSpecification(origin, _location('USNYC', 'New York City'), deadline)
    assert str(error.value) == "Origin and destination can't be the same"


@pytest.mark.parametrize(
    ('origin', 'destination', 'deadline', 'message'),
    [
        (
            None,
            _location('FIHEL', 'Helsinki'),
            datetime(2026, 11, 12),
            'A route specification requires an origin',
        ),
        (
            _location('USNYC', 'New York'),
            None,
            datetime(2026, 11, 12),
            'A route specification requires a destination',
        ),
        (
            _location('USNYC', 'New York'),
            _location('FIHEL', 'Helsinki'),
            None,
            'Arrival deadline must be a datetime',
        ),
    ],
)
def test_route_specification_rejects_invalid_fields(origin, destination, deadline, message):
    with pytest.raises((TypeError, ValueError)) as error:
        RouteSpecification(origin, destination, deadline)

    assert str(error.value) == message


def test_route_specification_is_immutable_and_compares_its_value_fields():
    origin = _location('USNYC', 'New York')
    destination = _location('FIHEL', 'Helsinki')
    deadline = datetime(2026, 11, 12, tzinfo=UTC)
    specification = RouteSpecification(origin, destination, deadline)

    assert specification == RouteSpecification(origin, destination, deadline)
    assert hash(specification) == hash(RouteSpecification(origin, destination, deadline))
    with pytest.raises(AttributeError):
        specification.destination = origin


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
        leg.load_time = unload
    with pytest.raises(AttributeError):
        itinerary.legs = ()
    with pytest.raises(ValueError) as error:
        Itinerary([])
    assert str(error.value) == 'An itinerary requires at least one leg'
    with pytest.raises(TypeError) as error:
        Itinerary([object()])
    assert str(error.value) == 'An itinerary requires legs'


@pytest.mark.parametrize(
    ('field', 'value', 'message'),
    [
        ('voyage', None, 'A leg requires a voyage'),
        ('load_location', None, 'A leg requires a load location'),
        ('unload_location', None, 'A leg requires an unload location'),
        ('load_time', None, 'Load time must be a datetime'),
        ('unload_time', None, 'Unload time must be a datetime'),
    ],
)
def test_leg_rejects_invalid_fields(field, value, message):
    arguments = {
        'voyage': Voyage(VoyageNumber('CM001'), Schedule.EMPTY),
        'load_location': _location('USNYC', 'New York'),
        'unload_location': _location('FIHEL', 'Helsinki'),
        'load_time': datetime(2026, 11, 1, tzinfo=UTC),
        'unload_time': datetime(2026, 11, 2, tzinfo=UTC),
    }
    arguments[field] = value

    with pytest.raises(TypeError) as error:
        Leg(**arguments)

    assert str(error.value) == message


def test_naive_leg_times_are_treated_as_utc():
    location = _location('USNYC', 'New York')
    leg = Leg(
        Voyage(VoyageNumber('CM001'), Schedule.EMPTY),
        location,
        _location('FIHEL', 'Helsinki'),
        datetime(2026, 11, 1, 10),
        datetime(2026, 11, 2, 10),
    )

    assert leg.load_time == datetime(2026, 11, 1, 10, tzinfo=UTC)
    assert leg.unload_time == datetime(2026, 11, 2, 10, tzinfo=UTC)


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
    assert first != object()


@pytest.mark.parametrize(
    ('field', 'value', 'message'),
    [
        ('tracking_id', None, 'A cargo requires a tracking ID'),
        ('route_specification', None, 'A cargo requires a route specification'),
        ('delivery', None, 'A cargo requires a delivery'),
        ('itinerary', object(), 'A cargo requires an itinerary'),
        ('origin', object(), 'A cargo origin must be a location'),
    ],
)
def test_cargo_rejects_invalid_components(field, value, message):
    origin = _location('USNYC', 'New York')
    destination = _location('FIHEL', 'Helsinki')
    arguments = {
        'tracking_id': TrackingId('ABC123'),
        'route_specification': RouteSpecification(
            origin, destination, datetime(2026, 11, 12, tzinfo=UTC)
        ),
        'delivery': _delivery(),
        'itinerary': Itinerary.EMPTY,
        'origin': None,
    }
    arguments[field] = value

    with pytest.raises(TypeError) as error:
        Cargo(**arguments)

    assert str(error.value) == message


def test_delivery_preserves_source_status_and_date_fields():
    eta = datetime(2026, 11, 12, 12, tzinfo=timezone(timedelta(hours=2)))
    calculated_at = datetime(2026, 11, 1, 12, tzinfo=timezone(timedelta(hours=2)))
    delivery = Delivery(
        transport_status=TransportStatus.ONBOARD_CARRIER,
        last_known_location=_location('NLRTM', 'Rotterdam'),
        current_voyage=Voyage(VoyageNumber('CM001'), Schedule.EMPTY),
        misdirected=True,
        eta=eta,
        next_expected_activity=HandlingActivity('UNLOAD', _location('FIHEL', 'Helsinki')),
        unloaded_at_destination=False,
        routing_status=RoutingStatus.MISROUTED,
        calculated_at=calculated_at,
        last_event_id=42,
    )

    assert delivery.transport_status is TransportStatus.ONBOARD_CARRIER
    assert delivery.eta == datetime(2026, 11, 12, 10, tzinfo=UTC)
    assert delivery.next_expected_activity.event_type == 'UNLOAD'
    assert delivery.calculated_at == datetime(2026, 11, 1, 10, tzinfo=UTC)
    assert delivery.last_event_id == 42
    with pytest.raises(AttributeError):
        delivery.misdirected = False


def _delivery(**overrides):
    fields = {
        'transport_status': TransportStatus.NOT_RECEIVED,
        'last_known_location': None,
        'current_voyage': None,
        'misdirected': False,
        'eta': None,
        'next_expected_activity': HandlingActivity.EMPTY,
        'unloaded_at_destination': False,
        'routing_status': RoutingStatus.NOT_ROUTED,
        'calculated_at': datetime(2026, 11, 1, tzinfo=UTC),
        'last_event_id': None,
    }
    fields.update(overrides)
    return Delivery(**fields)


@pytest.mark.parametrize(
    ('field', 'value', 'message'),
    [
        ('transport_status', 'NOT_RECEIVED', 'A delivery requires a transport status'),
        ('last_known_location', object(), 'A delivery last-known location must be a location'),
        ('current_voyage', object(), 'A delivery current voyage must be a voyage'),
        ('misdirected', 1, 'A delivery misdirected flag must be a boolean'),
        ('eta', 'tomorrow', 'ETA must be a datetime'),
        ('next_expected_activity', object(), 'A delivery requires a next expected activity'),
        ('unloaded_at_destination', 0, 'A delivery unloaded-at-destination flag must be a boolean'),
        ('routing_status', 'NOT_ROUTED', 'A delivery requires a routing status'),
        ('calculated_at', None, 'Calculated time must be a datetime'),
        ('last_event_id', True, 'A delivery last event ID must be an integer'),
    ],
)
def test_delivery_rejects_invalid_fields(field, value, message):
    with pytest.raises(TypeError) as error:
        _delivery(**{field: value})

    assert str(error.value) == message


def test_delivery_status_values_match_source_enums():
    assert {status.value for status in TransportStatus} == {
        'NOT_RECEIVED',
        'IN_PORT',
        'ONBOARD_CARRIER',
        'CLAIMED',
        'UNKNOWN',
    }
    assert {status.value for status in RoutingStatus} == {'NOT_ROUTED', 'ROUTED', 'MISROUTED'}


@pytest.mark.parametrize(
    ('event_type', 'location', 'voyage', 'message'),
    [
        (None, _location('FIHEL', 'Helsinki'), None, 'A handling activity requires an event type'),
        ('UNLOAD', None, None, 'A handling activity requires a location'),
        (
            'UNLOAD',
            _location('FIHEL', 'Helsinki'),
            object(),
            'A handling activity voyage must be a voyage',
        ),
    ],
)
def test_handling_activity_rejects_incomplete_fields(event_type, location, voyage, message):
    with pytest.raises(TypeError) as error:
        HandlingActivity(event_type, location, voyage)

    assert str(error.value) == message


def test_empty_handling_activity_is_a_shared_immutable_value_object():
    assert HandlingActivity() == HandlingActivity.EMPTY

    with pytest.raises(AttributeError):
        HandlingActivity.EMPTY.event_type = 'UNLOAD'
