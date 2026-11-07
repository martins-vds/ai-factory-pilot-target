from datetime import UTC, datetime

import pytest

from cargotracker.booking.application.specification import CargoSpecification
from cargotracker.cargo.domain.cargo import Cargo
from cargotracker.cargo.domain.delivery import Delivery, RoutingStatus, TransportStatus
from cargotracker.cargo.domain.handling_activity import HandlingActivity
from cargotracker.cargo.domain.itinerary import Itinerary
from cargotracker.cargo.domain.leg import Leg
from cargotracker.cargo.domain.route_specification import RouteSpecification
from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.cargo.infrastructure.models import CargoRecord
from cargotracker.cargo.infrastructure.repository import DjangoCargoRepository
from cargotracker.handling.domain.handling_history import HandlingHistory
from cargotracker.handling.infrastructure.repository import DjangoHandlingEventRepository
from cargotracker.location.domain.location import Location
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.location.infrastructure.models import LocationRecord
from cargotracker.voyage.domain.schedule import Schedule
from cargotracker.voyage.domain.voyage import Voyage
from cargotracker.voyage.domain.voyage_number import VoyageNumber
from cargotracker.voyage.infrastructure.models import VoyageRecord

ORIGIN = Location(UnLocode('USNYC'), 'New York')
DESTINATION = Location(UnLocode('FIHEL'), 'Helsinki')
ARRIVAL = datetime(2030, 11, 11, tzinfo=UTC)
DEADLINE = datetime(2030, 11, 20, tzinfo=UTC)
LOAD = datetime(2030, 11, 10, tzinfo=UTC)


def _persist_routed_cargo():
    LocationRecord.objects.create(unlocode='USNYC', name='New York')
    LocationRecord.objects.create(unlocode='FIHEL', name='Helsinki')
    VoyageRecord.objects.create(voyage_number='CM001')
    voyage = Voyage(VoyageNumber('CM001'), Schedule.EMPTY)
    specification = RouteSpecification(ORIGIN, DESTINATION, DEADLINE)
    itinerary = Itinerary((Leg(voyage, ORIGIN, DESTINATION, LOAD, ARRIVAL),))
    cargo = Cargo(
        TrackingId('ABC12345'),
        specification,
        Delivery.derived_from(specification, itinerary, HandlingHistory.EMPTY),
        itinerary,
    )
    repository = DjangoCargoRepository()
    repository.upsert(cargo)
    return repository, cargo


@pytest.mark.django_db
def test_change_destination_raises_lookup_error_for_unknown_cargo():
    specification = CargoSpecification(
        DjangoCargoRepository(),
        DjangoHandlingEventRepository(),
    )

    with pytest.raises(LookupError, match='Cargo MISSING1 not found'):
        specification.change_destination(TrackingId('MISSING1'), DESTINATION)


@pytest.mark.django_db
def test_change_destination_preserves_other_specification_fields_and_resets_route_state():
    repository, original = _persist_routed_cargo()
    destination = Location(UnLocode('USLAX'), 'Los Angeles')
    LocationRecord.objects.create(unlocode='USLAX', name='Los Angeles')

    CargoSpecification(repository, DjangoHandlingEventRepository()).change_destination(
        original.tracking_id, destination
    )

    cargo = repository.find(original.tracking_id)
    assert cargo is not None
    assert cargo.route_specification.origin == ORIGIN
    assert cargo.route_specification.destination == destination
    assert cargo.route_specification.arrival_deadline == DEADLINE
    assert cargo.itinerary == original.itinerary
    assert cargo.delivery.transport_status is TransportStatus.NOT_RECEIVED
    assert cargo.delivery.last_known_location is None
    assert cargo.delivery.current_voyage is None
    assert not cargo.delivery.misdirected
    assert cargo.delivery.routing_status is RoutingStatus.MISROUTED
    assert cargo.delivery.eta is None
    assert cargo.delivery.next_expected_activity is HandlingActivity.EMPTY
    assert not cargo.delivery.unloaded_at_destination
    record = CargoRecord.objects.get(tracking_id=original.tracking_id.value)
    assert record.spec_destination.unlocode == 'USLAX'
    assert record.transport_status == TransportStatus.NOT_RECEIVED.value
    assert record.last_known_location is None
    assert record.current_voyage is None
    assert not record.misdirected
    assert not record.unloaded_at_dest
    assert record.routing_status == RoutingStatus.MISROUTED.value
    assert record.eta is None
    assert record.next_expected_handling_event_type is None


@pytest.mark.django_db
def test_change_deadline_preserves_other_specification_fields_and_resets_route_state():
    repository, original = _persist_routed_cargo()
    earlier_deadline = datetime(2030, 11, 10, tzinfo=UTC)

    CargoSpecification(repository, DjangoHandlingEventRepository()).change_deadline(
        original.tracking_id, earlier_deadline
    )

    cargo = repository.find(original.tracking_id)
    assert cargo is not None
    assert cargo.route_specification.origin == ORIGIN
    assert cargo.route_specification.destination == DESTINATION
    assert cargo.route_specification.arrival_deadline == earlier_deadline
    assert cargo.itinerary == original.itinerary
    assert cargo.delivery.transport_status is TransportStatus.NOT_RECEIVED
    assert cargo.delivery.last_known_location is None
    assert cargo.delivery.current_voyage is None
    assert not cargo.delivery.misdirected
    assert cargo.delivery.routing_status is RoutingStatus.MISROUTED
    assert cargo.delivery.eta is None
    assert cargo.delivery.next_expected_activity is HandlingActivity.EMPTY
    assert not cargo.delivery.unloaded_at_destination
    record = CargoRecord.objects.get(tracking_id=original.tracking_id.value)
    assert record.spec_origin.unlocode == 'USNYC'
    assert record.spec_destination.unlocode == 'FIHEL'
    assert record.spec_arrival_deadline.isoformat() == '2030-11-10'
    assert record.transport_status == TransportStatus.NOT_RECEIVED.value
    assert record.last_known_location is None
    assert record.current_voyage is None
    assert not record.misdirected
    assert not record.unloaded_at_dest
    assert record.routing_status == RoutingStatus.MISROUTED.value
    assert record.eta is None
    assert record.next_expected_handling_event_type is None
