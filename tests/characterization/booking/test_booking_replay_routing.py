import itertools
import json
import random
import re
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from django.core.management import call_command
from django.test import override_settings
from django.urls import path

from cargotracker.booking.application.dashboard import CargoDashboard
from cargotracker.booking.application.registration import CargoRegistration
from cargotracker.booking.application.routing import CargoRouting
from cargotracker.booking.interfaces.dashboard.views import create_booking_views
from cargotracker.booking.interfaces.route_selection.views import create_route_selection_views
from cargotracker.cargo.infrastructure.repository import DjangoCargoRepository
from cargotracker.handling.infrastructure.repository import DjangoHandlingEventRepository
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.location.infrastructure.repository import DjangoLocationRepository
from cargotracker.pathfinder.application.routing import RoutingService
from cargotracker.pathfinder.domain.transit_edge import TransitEdge
from cargotracker.pathfinder.domain.transit_path import TransitPath
from cargotracker.pathfinder.interfaces import api
from cargotracker.voyage.infrastructure.repository import DjangoVoyageRepository

ROOT = Path(__file__).resolve().parents[3]
PATHFINDER_RECORDINGS = ROOT / '.migration' / 'characterization' / 'booking' / 'pathfinder'
NOW = datetime(2026, 11, 7, 12, 0, tzinfo=UTC)
ENDPOINT = '/rest/graph-traversal/shortest-path'


class RecordedCandidatePaths:
    def __init__(self):
        self.paths = ()

    def find_shortest_paths(self, origin, destination):
        assert (origin, destination) == ('CNHKG', 'AUMEL')
        return self.paths


repository = DjangoCargoRepository()
dashboard = CargoDashboard(repository)
candidate_paths = RecordedCandidatePaths()
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


def _recorded_candidate(recording):
    source_candidate = recording['cases']['route-candidates']['example_candidate']
    first_departure = datetime(2026, 11, 8, tzinfo=UTC)
    edges = []
    for index, edge in enumerate(source_candidate['legs']):
        departure = first_departure + timedelta(days=index * 4)
        arrival = departure + timedelta(days=1)
        edges.append(
            TransitEdge(
                edge['voyage'],
                edge['load'],
                edge['unload'],
                departure,
                arrival,
            )
        )
    return TransitPath(tuple(edges))


def _recorded_cargo(deadline):
    locations = DjangoLocationRepository()
    return CargoRegistration(repository).register(
        locations.find(UnLocode('CNHKG')),
        locations.find(UnLocode('AUMEL')),
        deadline,
    )


def _late_candidate(valid_candidate):
    edges = list(valid_candidate.transit_edges)
    last_edge = edges[-1]
    edges[-1] = TransitEdge(
        last_edge.voyage_number,
        last_edge.from_port,
        last_edge.to_port,
        datetime(2026, 12, 10, tzinfo=UTC),
        datetime(2026, 12, 11, tzinfo=UTC),
    )
    return TransitPath(tuple(edges))


@pytest.mark.django_db
@override_settings(ROOT_URLCONF=__name__)
def test_route_candidates_and_assignment_match_recorded_fields_and_ruling(
    client, booking_recording
):
    call_command('seed_sample_data')
    expected = booking_recording['cases']['route-candidates']
    assignment = booking_recording['cases']['route-assignment']
    valid_candidate = _recorded_candidate(booking_recording)
    candidate_paths.paths = (valid_candidate, _late_candidate(valid_candidate))
    tracking_id = _recorded_cargo(datetime(2026, 12, 1, tzinfo=UTC))
    route_url = f'/admin/cargo/{tracking_id.value}/route/'
    itinerary_url = f'/admin/cargo/{tracking_id.value}/itineraries/'

    route_response = client.get(route_url)
    route_content = route_response.content.decode()
    itinerary_response = client.get(itinerary_url)
    itinerary_content = itinerary_response.content.decode()
    candidate_tokens = re.findall(r'name="candidate" value="([^"]+)"', route_content)

    assert route_response.status_code == 200
    assert expected['example_candidate']['origin'] in route_content
    assert expected['example_candidate']['destination'] in route_content
    assert 'Potential routes:' in route_content
    assert '<dd>1</dd>' in route_content
    assert 'Route option #1' in route_content
    assert 'Route option #2' not in route_content
    assert len(candidate_tokens) == 1
    for edge in expected['example_candidate']['legs']:
        assert edge['voyage'] in route_content
        assert edge['load'] in route_content
        assert edge['unload'] in route_content
    assert itinerary_response.status_code == 200
    assert 'Route option #1' in itinerary_content
    assert expected['example_candidate']['destination'] in itinerary_content

    assigned = client.post(route_url, {'candidate': candidate_tokens[0]}, follow=True)
    content = assigned.content.decode()

    assert assigned.status_code == 200
    assert assigned.redirect_chain == [(f'/admin/cargo/{tracking_id.value}/', 302)]
    assert f'Routing Details for Cargo {tracking_id.value}' in content
    assert 'Itinerary' in content
    assert 'AUMEL' in content
    assert 'JNTKO' in content
    assert 'SESTO' in content
    assert '0300A' in content and '0400S' in content and '0200T' in content
    assert (
        'The browser reaches /admin/show.xhtml' in assignment['observed']
        or 'renders the itinerary legs' in assignment['observed']
    )


@pytest.mark.django_db
@override_settings(ROOT_URLCONF=__name__)
def test_short_deadline_and_unknown_cargo_fields_match_recordings(client, booking_recording):
    call_command('seed_sample_data')
    candidate_paths.paths = (_recorded_candidate(booking_recording),)
    short_deadline = _recorded_cargo(datetime(2026, 11, 8, tzinfo=UTC))

    route = client.get(f'/admin/cargo/{short_deadline.value}/route/')
    itineraries = client.get(f'/admin/cargo/{short_deadline.value}/itineraries/')
    route_content = route.content.decode()
    itineraries_content = itineraries.content.decode()
    unknown_route = client.get('/admin/cargo/UNKNOWN/route/')
    unknown_itineraries = client.get('/admin/cargo/UNKNOWN/itineraries/')

    assert route.status_code == itineraries.status_code == 200
    assert '<dd>0</dd>' in route_content
    assert 'No routes found that satisfy the route specification.' in route_content
    assert 'No routes found that satisfy the route specification.' in itineraries_content
    assert 'Potential routes: 0' in booking_recording['cases']['route-candidates']['observed']
    assert unknown_route.status_code == unknown_itineraries.status_code == 404


@override_settings(ROOT_URLCONF='cargotracker.pathfinder.interfaces.urls')
def test_pathfinder_fields_match_tier_a_recordings_and_ignore_deadline(client, monkeypatch):
    expected = json.loads((PATHFINDER_RECORDINGS / 'normal-1.body').read_text())
    deadline_expected = json.loads((PATHFINDER_RECORDINGS / 'deadline.body').read_text())

    monkeypatch.setattr(
        api,
        'routing_service',
        RoutingService(random_source=random.Random(29), clock=lambda: NOW),
    )
    response = client.get(
        ENDPOINT,
        {'origin': 'CNHKG', 'destination': 'USNYC', 'deadline': '2030-01-01T00:00:00Z'},
    )
    actual = response.json()

    assert response.status_code == int((PATHFINDER_RECORDINGS / 'deadline.status').read_text())
    assert (
        response['Content-Type']
        == (PATHFINDER_RECORDINGS / 'deadline.content-type').read_text().strip()
    )
    assert 3 <= len(actual) <= 5
    assert len(deadline_expected) == 3
    assert set(actual[0]) == set(expected[0]) == {'transitEdges'}
    assert list(actual[0]['transitEdges'][0]) == list(expected[0]['transitEdges'][0])
    for path_value in actual:
        edges = path_value['transitEdges']
        assert edges
        assert edges[0]['fromUnLocode'] == 'CNHKG'
        assert edges[-1]['toUnLocode'] == 'USNYC'
        for previous, following in itertools.pairwise(edges):
            assert previous['toUnLocode'] == following['fromUnLocode']
            assert datetime.fromisoformat(previous['toDate']) < datetime.fromisoformat(
                following['fromDate']
            )

    monkeypatch.setattr(
        api,
        'routing_service',
        RoutingService(random_source=random.Random(29), clock=lambda: NOW),
    )
    no_deadline = client.get(ENDPOINT, {'origin': 'CNHKG', 'destination': 'USNYC'})
    assert no_deadline.json() == actual


@pytest.mark.parametrize(
    ('case', 'query'),
    [
        ('four-character-origin', {'origin': 'CNHK', 'destination': 'USNYC'}),
        ('missing-destination', {'origin': 'CNHKG'}),
    ],
)
@override_settings(ROOT_URLCONF='cargotracker.pathfinder.interfaces.urls')
def test_pathfinder_validation_matches_exact_recorded_fields(client, case, query):
    response = client.get(ENDPOINT, query)
    expected_body = (PATHFINDER_RECORDINGS / f'{case}.body').read_bytes()
    expected_status = int((PATHFINDER_RECORDINGS / f'{case}.status').read_text())
    expected_content_type = (PATHFINDER_RECORDINGS / f'{case}.content-type').read_text().strip()

    assert response.status_code == expected_status == 400
    assert response['Content-Type'] == expected_content_type
    assert response.content == expected_body
