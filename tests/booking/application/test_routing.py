from datetime import UTC, datetime

import pytest
from django.http import Http404

from cargotracker.booking.application.registration import CargoRegistration
from cargotracker.booking.application.routing import CargoRouting
from cargotracker.cargo.domain.delivery import RoutingStatus, TransportStatus
from cargotracker.cargo.domain.handling_activity import HandlingActivity
from cargotracker.cargo.domain.itinerary import Itinerary
from cargotracker.cargo.domain.leg import Leg
from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.cargo.infrastructure.models import CargoRecord, LegRecord
from cargotracker.cargo.infrastructure.repository import DjangoCargoRepository
from cargotracker.handling.infrastructure.repository import DjangoHandlingEventRepository
from cargotracker.location.domain.location import Location
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.location.infrastructure.models import LocationRecord
from cargotracker.location.infrastructure.repository import DjangoLocationRepository
from cargotracker.pathfinder.domain.transit_edge import TransitEdge
from cargotracker.pathfinder.domain.transit_path import TransitPath
from cargotracker.voyage.domain.voyage_number import VoyageNumber
from cargotracker.voyage.infrastructure.models import VoyageRecord
from cargotracker.voyage.infrastructure.repository import DjangoVoyageRepository

ORIGIN = Location(UnLocode('USNYC'), 'New York')
TRANSFER = Location(UnLocode('NLRTM'), 'Rotterdam')
DESTINATION = Location(UnLocode('FIHEL'), 'Helsinki')
DEADLINE = datetime(2030, 11, 5, tzinfo=UTC)


class CandidateRoutingService:
    def __init__(self, candidates):
        self.candidates = candidates
        self.requested_route = None

    def find_shortest_paths(self, origin, destination):
        self.requested_route = (origin, destination)
        return self.candidates


def _edge(voyage, from_port, to_port, departure, arrival):
    return TransitEdge(
        voyage,
        from_port,
        to_port,
        datetime(2030, 11, departure, tzinfo=UTC),
        datetime(2030, 11, arrival, tzinfo=UTC),
    )


def _routing_service(candidates):
    for location in (ORIGIN, TRANSFER, DESTINATION):
        LocationRecord.objects.create(
            unlocode=location.unlocode.value,
            name=location.name,
        )
    for voyage_number in ('CM001', 'CM002', 'CM003'):
        VoyageRecord.objects.create(voyage_number=voyage_number)

    cargo_repository = DjangoCargoRepository()
    tracking_id = CargoRegistration(cargo_repository).register(ORIGIN, DESTINATION, DEADLINE)
    service = CandidateRoutingService(candidates)
    return (
        CargoRouting(
            cargo_repository,
            DjangoLocationRepository(),
            DjangoVoyageRepository(),
            DjangoHandlingEventRepository(),
            service,
        ),
        tracking_id,
        service,
    )


@pytest.mark.django_db
def test_assign_route_persists_itinerary_and_recalculates_delivery():
    routing, tracking_id, _ = _routing_service(())
    itinerary = Itinerary(
        (
            Leg(
                DjangoVoyageRepository().find(VoyageNumber('CM001')),
                ORIGIN,
                TRANSFER,
                datetime(2030, 11, 1, tzinfo=UTC),
                datetime(2030, 11, 2, tzinfo=UTC),
            ),
            Leg(
                DjangoVoyageRepository().find(VoyageNumber('CM002')),
                TRANSFER,
                DESTINATION,
                datetime(2030, 11, 3, tzinfo=UTC),
                datetime(2030, 11, 4, tzinfo=UTC),
            ),
        )
    )

    assigned = routing.assign_route(tracking_id, itinerary)

    assert assigned.itinerary == itinerary
    assert assigned.delivery.transport_status is TransportStatus.NOT_RECEIVED
    assert assigned.delivery.routing_status is RoutingStatus.ROUTED
    assert assigned.delivery.eta == datetime(2030, 11, 4, tzinfo=UTC)
    assert assigned.delivery.next_expected_activity == HandlingActivity('RECEIVE', ORIGIN)
    stored = DjangoCargoRepository().find(tracking_id)
    assert stored is not None
    assert stored.itinerary == itinerary
    assert stored.delivery.routing_status is RoutingStatus.ROUTED
    assert stored.delivery.eta == datetime(2030, 11, 4, tzinfo=UTC)
    assert stored.delivery.next_expected_activity == HandlingActivity('RECEIVE', ORIGIN)
    assert CargoRecord.objects.get(tracking_id=tracking_id.value).routing_status == 'ROUTED'
    assert LegRecord.objects.filter(cargo__tracking_id=tracking_id.value).count() == 2


@pytest.mark.django_db
@pytest.mark.parametrize(
    ('operation', 'stale'),
    [
        ('route_candidates', False),
        ('route_candidates', True),
        ('assign_route', False),
        ('assign_route', True),
    ],
)
def test_unknown_or_stale_routing_updates_raise_cargo_not_found(operation, stale):
    routing, tracking_id, _ = _routing_service(())
    if stale:
        CargoRecord.objects.filter(tracking_id=tracking_id.value).delete()
    else:
        tracking_id = TrackingId('MISSING1')

    with pytest.raises(Http404, match=f'Cargo with tracking ID {tracking_id} not found'):
        if operation == 'route_candidates':
            routing.route_candidates(tracking_id)
        else:
            routing.assign_route(tracking_id, Itinerary.EMPTY)


@pytest.mark.django_db
def test_route_candidates_convert_paths_and_filter_by_route_specification():
    valid_path = TransitPath(
        (
            _edge('CM001', 'USNYC', 'NLRTM', 1, 2),
            _edge('CM002', 'NLRTM', 'FIHEL', 3, 4),
        )
    )
    arrival_at_deadline = TransitPath((_edge('CM003', 'USNYC', 'FIHEL', 4, 5),))
    missed_deadline = TransitPath((_edge('CM003', 'USNYC', 'FIHEL', 4, 6),))
    wrong_origin = TransitPath((_edge('CM003', 'NLRTM', 'FIHEL', 1, 2),))
    wrong_destination = TransitPath((_edge('CM003', 'USNYC', 'NLRTM', 1, 2),))
    routing, tracking_id, pathfinder = _routing_service(
        (valid_path, arrival_at_deadline, missed_deadline, wrong_origin, wrong_destination)
    )

    candidates = routing.route_candidates(tracking_id)

    assert pathfinder.requested_route == ('USNYC', 'FIHEL')
    assert len(candidates) == 1
    itinerary = candidates[0]
    assert itinerary == Itinerary(
        (
            Leg(
                DjangoVoyageRepository().find(VoyageNumber('CM001')),
                ORIGIN,
                TRANSFER,
                datetime(2030, 11, 1, tzinfo=UTC),
                datetime(2030, 11, 2, tzinfo=UTC),
            ),
            Leg(
                DjangoVoyageRepository().find(VoyageNumber('CM002')),
                TRANSFER,
                DESTINATION,
                datetime(2030, 11, 3, tzinfo=UTC),
                datetime(2030, 11, 4, tzinfo=UTC),
            ),
        )
    )
