import itertools
import json
from datetime import UTC, datetime
from pathlib import Path

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

ROOT = Path(__file__).resolve().parents[2]
OBSERVATIONS = json.loads(
    (ROOT / '.migration' / 'characterization' / 'booking' / 'observations.json').read_text()
)
SOURCE_TESTS = json.loads(
    (ROOT / '.migration' / 'characterization' / 'booking' / 'source-tests.json').read_text()
)
BOOKING_LEDGER_IDS = sorted(
    path.stem for path in (ROOT / '.migration' / 'ledger').glob('booking.*.yaml')
)

HONG_KONG = Location(UnLocode('CNHKG'), 'Hong Kong')
ROTTERDAM = Location(UnLocode('NLRTM'), 'Rotterdam')
CHICAGO = Location(UnLocode('USCHI'), 'Chicago')
HELSINKI = Location(UnLocode('FIHEL'), 'Helsinki')
CALCULATED_AT = datetime(2026, 11, 7, tzinfo=UTC)
DEADLINE = datetime(2026, 12, 1, tzinfo=UTC)


@pytest.mark.parametrize('capability_id', BOOKING_LEDGER_IDS)
def test_booking_observation_is_recorded(capability_id):
    capability = OBSERVATIONS['capabilities'][capability_id]

    assert capability['cases']
    assert capability['observed']
    assert capability['predicted']
    assert isinstance(capability['match'], bool)
    assert all(case in OBSERVATIONS['cases'] for case in capability['cases'])


def test_route_specification_matches_source_junit_examples():
    first_voyage = Voyage(VoyageNumber('BK301'), Schedule.EMPTY)
    second_voyage = Voyage(VoyageNumber('BK302'), Schedule.EMPTY)
    itinerary = Itinerary(
        [
            Leg(
                first_voyage,
                HONG_KONG,
                ROTTERDAM,
                datetime(2026, 10, 1, tzinfo=UTC),
                datetime(2026, 10, 5, tzinfo=UTC),
            ),
            Leg(
                second_voyage,
                ROTTERDAM,
                CHICAGO,
                datetime(2026, 10, 7, tzinfo=UTC),
                datetime(2026, 10, 12, tzinfo=UTC),
            ),
        ]
    )

    assert RouteSpecification(HONG_KONG, CHICAGO, DEADLINE).is_satisfied_by(itinerary)
    assert not RouteSpecification(ROTTERDAM, CHICAGO, DEADLINE).is_satisfied_by(itinerary)
    assert not RouteSpecification(HONG_KONG, ROTTERDAM, DEADLINE).is_satisfied_by(itinerary)
    assert not RouteSpecification(
        HONG_KONG, CHICAGO, datetime(2026, 10, 12, tzinfo=UTC)
    ).is_satisfied_by(itinerary)


def test_itinerary_matches_source_event_and_construction_examples():
    voyage = Voyage(VoyageNumber('BK303'), Schedule.EMPTY)
    itinerary = Itinerary(
        [
            Leg(
                voyage,
                HONG_KONG,
                ROTTERDAM,
                datetime(2026, 10, 1, tzinfo=UTC),
                datetime(2026, 10, 5, tzinfo=UTC),
            ),
            Leg(
                voyage,
                ROTTERDAM,
                HELSINKI,
                datetime(2026, 10, 7, tzinfo=UTC),
                datetime(2026, 10, 12, tzinfo=UTC),
            ),
        ]
    )
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
    cargo = Cargo(
        TrackingId('BK-ITIN'),
        RouteSpecification(HONG_KONG, HELSINKI, DEADLINE),
        delivery,
        itinerary,
    )

    def event(event_type, location, event_voyage=None):
        return HandlingEvent(
            cargo,
            CALCULATED_AT,
            CALCULATED_AT,
            event_type,
            location,
            event_voyage,
        )

    assert itinerary.is_expected(event(HandlingEventType.RECEIVE, HONG_KONG))
    assert itinerary.is_expected(event(HandlingEventType.LOAD, HONG_KONG, voyage))
    assert itinerary.is_expected(event(HandlingEventType.UNLOAD, ROTTERDAM, voyage))
    assert itinerary.is_expected(event(HandlingEventType.CLAIM, HELSINKI))
    assert itinerary.is_expected(event(HandlingEventType.CUSTOMS, HELSINKI))
    assert not itinerary.is_expected(event(HandlingEventType.RECEIVE, ROTTERDAM))
    assert not itinerary.is_expected(event(HandlingEventType.CLAIM, ROTTERDAM))

    with pytest.raises(ValueError, match='at least one leg'):
        Itinerary([])


def test_cargo_initial_and_routing_statuses_match_source_examples():
    specification = RouteSpecification(HONG_KONG, HELSINKI, DEADLINE)
    empty_delivery = Delivery.derived_from(
        specification, Itinerary.EMPTY, HandlingHistory(()), CALCULATED_AT
    )
    assert empty_delivery.transport_status is TransportStatus.NOT_RECEIVED
    assert empty_delivery.routing_status is RoutingStatus.NOT_ROUTED
    assert empty_delivery.last_known_location is None

    voyage = Voyage(VoyageNumber('BK304'), Schedule.EMPTY)
    valid_itinerary = Itinerary(
        [
            Leg(
                voyage,
                HONG_KONG,
                HELSINKI,
                datetime(2026, 11, 8, tzinfo=UTC),
                datetime(2026, 11, 12, tzinfo=UTC),
            )
        ]
    )
    routed_delivery = Delivery.derived_from(
        specification, valid_itinerary, HandlingHistory(()), CALCULATED_AT
    )
    assert routed_delivery.routing_status is RoutingStatus.ROUTED

    wrong_itinerary = Itinerary(
        [
            Leg(
                voyage,
                ROTTERDAM,
                HELSINKI,
                datetime(2026, 11, 8, tzinfo=UTC),
                datetime(2026, 11, 12, tzinfo=UTC),
            )
        ]
    )
    misrouted_delivery = Delivery.derived_from(
        specification, wrong_itinerary, HandlingHistory(()), CALCULATED_AT
    )
    assert misrouted_delivery.routing_status is RoutingStatus.MISROUTED


def test_source_test_inventory_records_executed_and_unexecuted_contracts():
    executed = SOURCE_TESTS['executed_source_tests']
    assert sum(group['count'] for group in executed.values() if 'count' in group) == 16
    assert executed['ItineraryTest']['methods'] == [
        'testCargoOnTrack',
        'testNextExpectedEvent',
        'testCreateItinerary',
    ]
    assert 'empty TODO' in executed['ItineraryTest']['note']

    unexecuted = {test['method']: test for test in SOURCE_TESTS['unexecuted_test_methods']}
    assert unexecuted['testCalculatePossibleRoutes']['junit_test_annotation'] is False
    assert unexecuted['testCalculatePossibleRoutes']['executed'] is False
    assert unexecuted['testCargoFromHongkongToStockholm']['junit_test_annotation'] is False
    assert unexecuted['testCargoFromHongkongToStockholm']['executed'] is False
    assert len(unexecuted['testCalculatePossibleRoutes']['would_assert']) == 4
    assert SOURCE_TESTS['domain_test_contracts']['ItineraryTest']['testCreateItinerary'] == [
        'An empty leg list throws IllegalArgumentException.',
        'A null leg list throws NullPointerException.',
    ]


def test_booking_service_junit_contracts_are_transcribed():
    contracts = SOURCE_TESTS['booking_service_contracts']

    assert set(contracts) == {
        'testRegisterNew',
        'testRouteCandidates',
        'testAssignRoute',
        'testChangeDestination',
        'testChangeDeadline',
    }
    assert any('empty itinerary' in rule for rule in contracts['testRegisterNew'])
    assert any('non-empty' in rule for rule in contracts['testRouteCandidates'])
    assert any('MISROUTED' in rule for rule in contracts['testChangeDestination'])
    assert any('MISROUTED' in rule for rule in contracts['testChangeDeadline'])


def test_unannotated_external_routing_assertions_match_observed_candidate():
    candidate = OBSERVATIONS['cases']['route-candidates']['example_candidate']
    legs = candidate['legs']

    assert legs
    assert legs[0]['load'] == candidate['origin']
    assert legs[-1]['unload'] == candidate['destination']
    assert all(
        previous['unload'] == following['load'] for previous, following in itertools.pairwise(legs)
    )
