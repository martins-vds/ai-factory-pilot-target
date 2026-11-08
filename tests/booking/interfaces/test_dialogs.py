import re
from datetime import UTC, date, datetime

import pytest
from django.core.management import call_command
from django.http import Http404
from django.test import RequestFactory
from django.urls import path

from cargotracker.booking.application.dashboard import CargoDashboard
from cargotracker.booking.application.specification import CargoSpecification
from cargotracker.booking.interfaces.dashboard.views import create_booking_views
from cargotracker.booking.interfaces.dialogs.views import create_dialog_views
from cargotracker.cargo.domain.cargo import Cargo
from cargotracker.cargo.domain.delivery import Delivery, RoutingStatus
from cargotracker.cargo.domain.itinerary import Itinerary
from cargotracker.cargo.domain.leg import Leg
from cargotracker.cargo.domain.route_specification import RouteSpecification
from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.cargo.infrastructure.repository import DjangoCargoRepository
from cargotracker.handling.domain.handling_history import HandlingHistory
from cargotracker.handling.infrastructure.repository import DjangoHandlingEventRepository
from cargotracker.location.infrastructure.repository import DjangoLocationRepository
from cargotracker.voyage.domain.voyage_number import VoyageNumber
from cargotracker.voyage.infrastructure.repository import DjangoVoyageRepository

pytestmark = pytest.mark.django_db

cargo_repository = DjangoCargoRepository()
location_repository = DjangoLocationRepository()
shipping_locations = []
cargo_dashboard = CargoDashboard(cargo_repository)
specification = CargoSpecification(cargo_repository, DjangoHandlingEventRepository())


def _shipping_locations():
    return shipping_locations


def _persist_routed_cargo():
    cargo = cargo_repository.find(TrackingId('DEF789'))
    assert cargo is not None
    voyage = DjangoVoyageRepository().find(VoyageNumber('0100S'))
    assert voyage is not None
    route_specification = RouteSpecification(
        cargo.route_specification.origin,
        cargo.route_specification.destination,
        datetime(2030, 11, 20, tzinfo=UTC),
    )
    itinerary = Itinerary(
        (
            Leg(
                voyage,
                route_specification.origin,
                route_specification.destination,
                datetime(2030, 11, 10, tzinfo=UTC),
                datetime(2030, 11, 15, tzinfo=UTC),
            ),
        )
    )
    routed_cargo = Cargo(
        cargo.tracking_id,
        route_specification,
        Delivery.derived_from(route_specification, itinerary, HandlingHistory.EMPTY),
        itinerary,
        cargo.origin,
    )
    cargo_repository.upsert(routed_cargo)
    return routed_cargo


dashboard_view, _ = create_booking_views(cargo_dashboard)
destination_dialog_view, deadline_dialog_view = create_dialog_views(
    cargo_dashboard,
    specification,
    _shipping_locations,
)

urlpatterns = [
    path('admin/dashboard/', dashboard_view),
    path('admin/cargo/<str:tracking_id>/destination/', destination_dialog_view),
    path('admin/cargo/<str:tracking_id>/deadline/', deadline_dialog_view),
]


@pytest.fixture(autouse=True)
def seed_data(settings):
    settings.ROOT_URLCONF = __name__
    call_command('seed_sample_data')
    shipping_locations[:] = location_repository.find_all()


def test_not_routed_table_exposes_destination_and_deadline_dialogs(client):
    response = client.get('/admin/dashboard/')
    not_routed_table = (
        response.content.decode().split('id="not-routed-cargo"', 1)[1].split('</section>', 1)[0]
    )

    assert response.status_code == 200
    assert 'id="cargo-edit-dialog"' in not_routed_table
    assert 'aria-labelledby="cargo-edit-dialog-title"' in not_routed_table
    assert 'id="cargo-edit-dialog-title">Edit cargo</h2>' in not_routed_table
    assert 'aria-haspopup="dialog"' in not_routed_table
    assert 'hx-get="/admin/cargo/DEF789/destination/"' in not_routed_table
    assert 'hx-get="/admin/cargo/DEF789/deadline/"' in not_routed_table
    assert 'href="/admin/cargo/DEF789/route/"' in not_routed_table


def test_destination_dialog_filters_options_without_mutating_locations(client):
    cargo = cargo_repository.find(TrackingId('DEF789'))
    assert cargo is not None
    original_locations = tuple(shipping_locations)

    first_response = client.get('/admin/cargo/DEF789/destination/', HTTP_HX_REQUEST='true')
    second_response = client.get('/admin/cargo/DEF789/destination/', HTTP_HX_REQUEST='true')
    first_content = first_response.content.decode()
    second_content = second_response.content.decode()
    first_options = re.findall(r'<option\b[^>]*value="([^"]+)"', first_content)
    second_options = re.findall(r'<option\b[^>]*value="([^"]+)"', second_content)
    excluded_codes = {
        cargo.route_specification.origin.unlocode.value,
        cargo.route_specification.destination.unlocode.value,
    }

    assert first_response.status_code == second_response.status_code == 200
    assert cargo.route_specification.origin.name in first_content
    assert cargo.route_specification.destination.name in first_content
    assert len(first_options) == len(original_locations) - 2
    assert not excluded_codes.intersection(first_options)
    assert f'value="{first_options[0]}" selected' in first_content
    assert 'role="alert"' not in first_content
    assert first_options == second_options
    assert tuple(shipping_locations) == original_locations


@pytest.mark.parametrize(
    ('dialog', 'tracking_id'),
    [
        ('destination', 'UNKNOWN'),
        ('destination', 'STALE1'),
        ('deadline', 'UNKNOWN'),
        ('deadline', 'STALE1'),
    ],
)
def test_unknown_or_stale_cargo_dialog_returns_cargo_not_found(client, dialog, tracking_id):
    response = client.get(
        f'/admin/cargo/{tracking_id}/{dialog}/',
        HTTP_HX_REQUEST='true',
    )
    view = destination_dialog_view if dialog == 'destination' else deadline_dialog_view

    assert response.status_code == 404
    with pytest.raises(
        Http404,
        match=f'^Cargo with tracking ID {tracking_id} not found\\.$',
    ):
        view(
            RequestFactory().get(f'/admin/cargo/{tracking_id}/{dialog}/'),
            tracking_id,
        )


def test_deadline_dialog_shows_current_route_and_deadline(client):
    cargo = cargo_repository.find(TrackingId('DEF789'))
    assert cargo is not None

    response = client.get('/admin/cargo/DEF789/deadline/', HTTP_HX_REQUEST='true')
    content = response.content.decode()

    assert response.status_code == 200
    assert cargo.route_specification.origin.name in content
    assert cargo.route_specification.destination.name in content
    assert f'value="{cargo.route_specification.arrival_deadline.date().isoformat()}"' in content
    assert 'role="alert"' not in content


def test_invalid_deadline_shows_field_error_and_keeps_dialog_open(client):
    response = client.post(
        '/admin/cargo/DEF789/deadline/',
        {'deadline': 'not-a-date'},
        HTTP_HX_REQUEST='true',
    )
    content = response.content.decode()

    assert response.status_code == 200
    assert 'Enter a valid arrival deadline.' in content
    assert 'role="alert"' in content
    assert 'aria-invalid="true"' in content


def test_missing_deadline_shows_error_without_fabricating_a_value(client):
    response = client.post(
        '/admin/cargo/DEF789/deadline/',
        {},
        HTTP_HX_REQUEST='true',
    )
    content = response.content.decode()

    assert response.status_code == 200
    assert 'Enter a valid arrival deadline.' in content
    assert 'value=""' in content


def test_invalid_destination_shows_field_error_without_updating_cargo(client):
    cargo = cargo_repository.find(TrackingId('DEF789'))
    assert cargo is not None

    response = client.post(
        '/admin/cargo/DEF789/destination/',
        {'destination': cargo.route_specification.origin.unlocode.value},
        HTTP_HX_REQUEST='true',
    )
    updated = cargo_repository.find(TrackingId('DEF789'))
    content = response.content.decode()

    assert response.status_code == 200
    assert 'Select a valid destination.' in content
    assert 'role="alert"' in content
    assert 'aria-invalid="true"' in content
    assert updated is not None
    assert updated.route_specification.destination == cargo.route_specification.destination


def test_destination_update_redirects_and_refreshes_not_routed_row(client):
    cargo = cargo_repository.find(TrackingId('DEF789'))
    assert cargo is not None
    destinations = [
        location
        for location in shipping_locations
        if location not in (cargo.route_specification.origin, cargo.route_specification.destination)
    ]
    destination = destinations[1]

    response = client.post(
        '/admin/cargo/DEF789/destination/',
        {'destination': destination.unlocode.value},
        HTTP_HX_REQUEST='true',
    )
    updated = cargo_repository.find(TrackingId('DEF789'))
    dashboard = client.get('/admin/dashboard/').content.decode()
    not_routed_table = dashboard.split('id="not-routed-cargo"', 1)[1].split('</section>', 1)[0]

    assert response.status_code == 204
    assert response['HX-Redirect'] == '/admin/dashboard/'
    assert updated is not None
    assert updated.route_specification.origin == cargo.route_specification.origin
    assert updated.route_specification.destination == destination
    assert (
        updated.route_specification.arrival_deadline == cargo.route_specification.arrival_deadline
    )
    assert updated.itinerary == cargo.itinerary
    assert destination.name in not_routed_table
    assert 'Widget for var' not in response.content.decode()


def test_deadline_update_preserves_route_and_refreshes_not_routed_row(client):
    cargo = cargo_repository.find(TrackingId('DEF789'))
    assert cargo is not None
    updated_date = date(2027, 1, 15)

    response = client.post(
        '/admin/cargo/DEF789/deadline/',
        {'deadline': updated_date.isoformat()},
    )
    updated = cargo_repository.find(TrackingId('DEF789'))
    dashboard = client.get('/admin/dashboard/').content.decode()
    not_routed_table = dashboard.split('id="not-routed-cargo"', 1)[1].split('</section>', 1)[0]

    assert response.status_code == 302
    assert response.url == '/admin/dashboard/'
    assert updated is not None
    assert updated.route_specification.origin == cargo.route_specification.origin
    assert updated.route_specification.destination == cargo.route_specification.destination
    assert updated.route_specification.arrival_deadline.date() == updated_date
    assert updated.itinerary == cargo.itinerary
    assert '01/15/2027' in not_routed_table
    assert 'Widget for var' not in response.content.decode()


@pytest.mark.parametrize('dialog', ['destination', 'deadline'])
def test_dialog_update_recalculates_route_state(client, dialog):
    cargo = _persist_routed_cargo()
    assert cargo.delivery.routing_status is RoutingStatus.ROUTED

    if dialog == 'destination':
        destination = next(
            location
            for location in shipping_locations
            if location
            not in (cargo.route_specification.origin, cargo.route_specification.destination)
        )
        data = {'destination': destination.unlocode.value}
    else:
        data = {'deadline': date(2030, 11, 14).isoformat()}

    response = client.post(
        f'/admin/cargo/{cargo.tracking_id.value}/{dialog}/',
        data,
        HTTP_HX_REQUEST='true',
    )
    updated = cargo_repository.find(cargo.tracking_id)

    assert response.status_code == 204
    assert updated is not None
    assert updated.delivery.routing_status is RoutingStatus.MISROUTED
    assert updated.itinerary == cargo.itinerary
