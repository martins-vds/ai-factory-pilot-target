from datetime import UTC, datetime

import pytest
from django.test import override_settings
from django.urls import path

from cargotracker.booking.application.dashboard import CargoDashboard
from cargotracker.booking.application.registration import CargoRegistration
from cargotracker.booking.application.routing import CargoRouting
from cargotracker.booking.interfaces.dashboard.views import create_booking_views
from cargotracker.booking.interfaces.route_selection.views import create_route_selection_views
from cargotracker.cargo.infrastructure.repository import DjangoCargoRepository
from cargotracker.handling.infrastructure.repository import DjangoHandlingEventRepository
from cargotracker.location.domain.location import Location
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.location.infrastructure.models import LocationRecord
from cargotracker.location.infrastructure.repository import DjangoLocationRepository
from cargotracker.pathfinder.domain.transit_edge import TransitEdge
from cargotracker.pathfinder.domain.transit_path import TransitPath
from cargotracker.voyage.infrastructure.models import VoyageRecord
from cargotracker.voyage.infrastructure.repository import DjangoVoyageRepository

ORIGIN = Location(UnLocode('USNYC'), 'New York')
TRANSFER = Location(UnLocode('NLRTM'), 'Rotterdam')
DESTINATION = Location(UnLocode('FIHEL'), 'Helsinki')
DEADLINE = datetime(2030, 11, 5, tzinfo=UTC)


class CandidatePaths:
    def __init__(self):
        self.paths = ()

    def find_shortest_paths(self, origin, destination):
        assert (origin, destination) == ('USNYC', 'FIHEL')
        return self.paths


repository = DjangoCargoRepository()
dashboard = CargoDashboard(repository)
candidate_paths = CandidatePaths()
routing = CargoRouting(
    repository,
    DjangoLocationRepository(),
    DjangoVoyageRepository(),
    DjangoHandlingEventRepository(),
    candidate_paths,
)
route_view, itinerary_view = create_route_selection_views(routing, dashboard)
_, cargo_details_view = create_booking_views(dashboard)
urlpatterns = [
    path('admin/cargo/<str:tracking_id>/route/', route_view),
    path('admin/cargo/<str:tracking_id>/itineraries/', itinerary_view),
    path('admin/cargo/<str:tracking_id>/', cargo_details_view),
]


def _edge(voyage_number, from_port, to_port, departure, arrival):
    return TransitEdge(
        voyage_number,
        from_port,
        to_port,
        datetime(2030, 11, departure, tzinfo=UTC),
        datetime(2030, 11, arrival, tzinfo=UTC),
    )


def _candidate_paths():
    return (
        TransitPath(
            (
                _edge('CM001', 'USNYC', 'NLRTM', 1, 2),
                _edge('CM002', 'NLRTM', 'FIHEL', 3, 4),
            )
        ),
        TransitPath((_edge('CM003', 'USNYC', 'FIHEL', 1, 4),)),
    )


def _create_cargo(paths):
    for location in (ORIGIN, TRANSFER, DESTINATION):
        LocationRecord.objects.create(
            unlocode=location.unlocode.value,
            name=location.name,
        )
    for voyage_number in ('CM001', 'CM002', 'CM003'):
        VoyageRecord.objects.create(voyage_number=voyage_number)
    candidate_paths.paths = paths
    return CargoRegistration(repository).register(ORIGIN, DESTINATION, DEADLINE)


@pytest.mark.django_db
@override_settings(ROOT_URLCONF=__name__)
def test_route_selection_renders_populated_candidates_and_numbered_legs(client):
    tracking_id = _create_cargo(_candidate_paths())

    response = client.get(f'/admin/cargo/{tracking_id.value}/route/')
    content = response.content.decode()

    assert response.status_code == 200
    assert f'Routing Details for Cargo {tracking_id.value}' in content
    assert 'Potential routes:' in content
    assert '<dd>2</dd>' in content
    assert 'Route option #1' in content
    assert 'Route option #2' in content
    assert 'Leg 1' in content
    assert 'Leg 2' in content
    assert 'CM001' in content
    assert 'New York' in content and 'USNYC' in content
    assert 'Rotterdam' in content and 'NLRTM' in content
    assert 'Helsinki' in content and 'FIHEL' in content
    assert '11/03/2030' in content and '11/04/2030' in content
