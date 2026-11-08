import re
from datetime import UTC, datetime

import pytest
from django.http import Http404
from django.test import RequestFactory, override_settings
from django.urls import path

from cargotracker.booking.application.dashboard import CargoDashboard
from cargotracker.booking.application.registration import CargoRegistration
from cargotracker.booking.application.routing import CargoRouting
from cargotracker.booking.interfaces.dashboard.views import create_booking_views
from cargotracker.booking.interfaces.route_selection.views import create_route_selection_views
from cargotracker.cargo.infrastructure.models import CargoRecord
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


@pytest.mark.django_db
@override_settings(ROOT_URLCONF=__name__)
def test_route_screens_explain_when_no_candidates_satisfy_the_deadline(client):
    tracking_id = _create_cargo(())

    route_response = client.get(f'/admin/cargo/{tracking_id.value}/route/')
    itinerary_response = client.get(f'/admin/cargo/{tracking_id.value}/itineraries/')

    assert route_response.status_code == 200
    assert itinerary_response.status_code == 200
    route_content = route_response.content.decode()
    itinerary_content = itinerary_response.content.decode()
    assert 'No routes found that satisfy the route specification.' in route_content
    assert 'Potential routes:' in route_content
    assert '<dd>0</dd>' in route_content
    assert re.search(
        r'(?<!\w)Try setting an arrival deadline further into the future\.(?!\w)',
        route_content,
    )
    assert 'No routes found that satisfy the route specification.' in itinerary_content
    assert re.search(
        r'(?<!\w)Try setting the arrival deadline further into the future \(a few weeks at least\)\.(?!\w)',
        itinerary_content,
    )
    assert 'Route option #' not in route_content
    assert 'Route option #' not in itinerary_content


@pytest.mark.django_db
@override_settings(ROOT_URLCONF=__name__)
def test_select_itinerary_renders_candidate_routes_when_available(client):
    tracking_id = _create_cargo(_candidate_paths())

    response = client.get(f'/admin/cargo/{tracking_id.value}/itineraries/')
    content = response.content.decode()

    assert response.status_code == 200
    assert 'Route option #1' in content
    assert 'Route option #2' in content
    assert 'CM001' in content
    assert 'USNYC' in content and 'New York' in content
    assert 'FIHEL' in content and 'Helsinki' in content


@pytest.mark.django_db
@override_settings(ROOT_URLCONF=__name__)
def test_assigning_candidate_redirects_to_details_with_the_selected_itinerary(client):
    tracking_id = _create_cargo(_candidate_paths())
    route_url = f'/admin/cargo/{tracking_id.value}/route/'
    route_response = client.get(route_url)
    candidate_tokens = re.findall(
        r'name="candidate" value="([^"]+)"',
        route_response.content.decode(),
    )

    response = client.post(route_url, {'candidate': candidate_tokens[1]}, follow=True)

    assert response.status_code == 200
    assert response.redirect_chain == [(f'/admin/cargo/{tracking_id.value}/', 302)]
    content = response.content.decode()
    assert f'Routing Details for Cargo {tracking_id.value}' in content
    assert 'Itinerary' in content
    assert 'CM003' in content
    assert 'CM001' not in content


@pytest.mark.django_db
@override_settings(ROOT_URLCONF=__name__)
def test_route_assignment_rejects_a_modified_candidate(client):
    tracking_id = _create_cargo(_candidate_paths())
    route_url = f'/admin/cargo/{tracking_id.value}/route/'
    route_content = client.get(route_url).content.decode()
    candidate_token = re.search(
        r'name="candidate" value="([^"]+)"',
        route_content,
    ).group(1)

    response = client.post(route_url, {'candidate': f'{candidate_token}tampered'})

    assert response.status_code == 404
    details = client.get(f'/admin/cargo/{tracking_id.value}/').content.decode()
    assert 'Not routed' in details


@pytest.mark.django_db
@override_settings(ROOT_URLCONF=__name__)
def test_route_screens_reject_unsupported_http_methods(client):
    tracking_id = _create_cargo(())
    route_page = client.get(f'/admin/cargo/{tracking_id.value}/route/')
    itinerary_page = client.get(f'/admin/cargo/{tracking_id.value}/itineraries/')
    route_response = client.put(f'/admin/cargo/{tracking_id.value}/route/')
    itinerary_response = client.post(f'/admin/cargo/{tracking_id.value}/itineraries/')

    assert route_page.status_code == 200
    assert f'Routing Details for Cargo {tracking_id.value}' in route_page.content.decode()
    assert itinerary_page.status_code == 200
    assert f'Select an Itinerary for Cargo {tracking_id.value}' in itinerary_page.content.decode()
    assert route_response.status_code == 405
    assert itinerary_response.status_code == 405


@pytest.mark.django_db
def test_route_selection_raises_not_found_for_unknown_cargo():
    request = RequestFactory().get('/admin/cargo/MISSING1/route/')

    with pytest.raises(Http404, match='Cargo with tracking ID MISSING1 not found\\.'):
        route_view(request, 'MISSING1')


@pytest.mark.django_db
@override_settings(ROOT_URLCONF=__name__)
@pytest.mark.parametrize('screen', ['route', 'itineraries'])
@pytest.mark.parametrize('stale', [False, True])
def test_route_screens_return_not_found_for_unknown_or_stale_cargo(client, screen, stale):
    if stale:
        tracking_id = _create_cargo(())
        CargoRecord.objects.filter(tracking_id=tracking_id.value).delete()
        tracking_id_value = tracking_id.value
    else:
        tracking_id_value = 'MISSING1'

    response = client.get(f'/admin/cargo/{tracking_id_value}/{screen}/')

    assert response.status_code == 404
