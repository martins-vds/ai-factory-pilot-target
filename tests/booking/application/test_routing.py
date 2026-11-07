from datetime import UTC, datetime

import pytest

from cargotracker.booking.application.registration import CargoRegistration
from cargotracker.booking.application.routing import CargoRouting
from cargotracker.cargo.domain.itinerary import Itinerary
from cargotracker.cargo.domain.leg import Leg
from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.cargo.infrastructure.repository import DjangoCargoRepository
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
    tracking_id = CargoRegistration(cargo_repository).register(
        ORIGIN, DESTINATION, DEADLINE
    )
    service = CandidateRoutingService(candidates)
    return (
        CargoRouting(
            cargo_repository,
            DjangoLocationRepository(),
            DjangoVoyageRepository(),
            None,
            service,
        ),
        tracking_id,
        service,
    )


@pytest.mark.django_db
def test_route_candidates_convert_paths_and_filter_by_route_specification():
    valid_path = TransitPath(
        (
            _edge('CM001', 'USNYC', 'NLRTM', 1, 2),
            _edge('CM002', 'NLRTM', 'FIHEL', 3, 4),
        )
    )
    missed_deadline = TransitPath((_edge('CM003', 'USNYC', 'FIHEL', 4, 5),))
    wrong_origin = TransitPath((_edge('CM003', 'NLRTM', 'FIHEL', 1, 2),))
    routing, tracking_id, pathfinder = _routing_service(
        (valid_path, missed_deadline, wrong_origin)
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
