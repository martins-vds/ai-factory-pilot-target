from datetime import UTC, datetime, timedelta, timezone

import pytest

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


def _event(**overrides):
    fields = {
        'cargo': _cargo(),
        'completion_time': datetime(2026, 11, 1, tzinfo=UTC),
        'registration_time': datetime(2026, 11, 1, tzinfo=UTC),
        'event_type': HandlingEventType.RECEIVE,
        'location': Location(UnLocode('USNYC'), 'New York'),
        'voyage': None,
    }
    fields.update(overrides)
    return HandlingEvent(**fields)


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
        datetime(2026, 11, 1, 2, tzinfo=timezone(timedelta(hours=2))),
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
    assert history.most_recent_event == later


def test_handling_history_is_immutable_and_requires_handling_events():
    history = HandlingHistory([_event()])

    with pytest.raises(AttributeError):
        history.events = ()
    with pytest.raises(TypeError, match='Handling events are required'):
        HandlingHistory(None)
    with pytest.raises(TypeError, match='Handling history requires handling events'):
        HandlingHistory([object()])


def test_handling_event_types_match_source_voyage_rules():
    assert {event_type.value for event_type in HandlingEventType} == {
        'LOAD',
        'UNLOAD',
        'RECEIVE',
        'CLAIM',
        'CUSTOMS',
    }
    assert {event_type for event_type in HandlingEventType if event_type.requires_voyage} == {
        HandlingEventType.LOAD,
        HandlingEventType.UNLOAD,
    }


def test_handling_event_normalizes_completion_and_registration_times_to_utc():
    event = _event(
        completion_time=datetime(2026, 11, 1, 2, tzinfo=timezone(timedelta(hours=2))),
        registration_time=datetime(2026, 11, 1, 4, tzinfo=timezone(timedelta(hours=2))),
    )

    assert event.completion_time == datetime(2026, 11, 1, tzinfo=UTC)
    assert event.registration_time == datetime(2026, 11, 1, 2, tzinfo=UTC)


@pytest.mark.parametrize(
    ('field', 'value', 'message'),
    [
        ('cargo', None, 'A handling event requires a cargo'),
        ('event_type', 'RECEIVE', 'A handling event requires an event type'),
        ('location', None, 'A handling event requires a location'),
        ('voyage', object(), 'A handling event voyage must be a voyage'),
    ],
)
def test_handling_event_rejects_invalid_fields(field, value, message):
    with pytest.raises(TypeError, match=message):
        _event(**{field: value})


@pytest.mark.parametrize(
    ('field', 'message'),
    [
        ('completion_time', 'Completion time must be a datetime'),
        ('registration_time', 'Registration time must be a datetime'),
    ],
)
def test_handling_event_requires_datetime_fields(field, message):
    with pytest.raises(TypeError, match=message):
        _event(**{field: None})


@pytest.mark.parametrize('event_type', [HandlingEventType.LOAD, HandlingEventType.UNLOAD])
def test_load_and_unload_events_require_a_voyage(event_type):
    with pytest.raises(ValueError, match=f'Voyage is required for event type {event_type}'):
        _event(event_type=event_type)


@pytest.mark.parametrize(
    'event_type',
    [HandlingEventType.RECEIVE, HandlingEventType.CLAIM, HandlingEventType.CUSTOMS],
)
def test_non_carrier_events_prohibit_a_voyage(event_type):
    voyage = Voyage(VoyageNumber('CM001'), Schedule.EMPTY)

    with pytest.raises(ValueError, match=f'Voyage is not allowed with event type {event_type}'):
        _event(event_type=event_type, voyage=voyage)
