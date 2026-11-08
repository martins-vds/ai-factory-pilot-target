import re
from datetime import UTC, date, datetime

import pytest
from django.core.management import call_command

from cargotracker.booking.application.registration import CargoRegistration
from cargotracker.cargo.infrastructure.repository import DjangoCargoRepository
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.location.infrastructure.repository import DjangoLocationRepository


@pytest.fixture
def recorded_unrouted_cargo():
    call_command('seed_sample_data')
    locations = DjangoLocationRepository()
    return CargoRegistration(DjangoCargoRepository()).register(
        locations.find(UnLocode('USCHI')),
        locations.find(UnLocode('USDAL')),
        datetime(2026, 11, 8, tzinfo=UTC),
    )


@pytest.mark.django_db
def test_destination_dialog_fields_match_recording_and_apply_approved_rulings(
    client, booking_recording, recorded_unrouted_cargo
):
    expected = booking_recording['cases']['destination-dialog']['observed']
    tracking_id = recorded_unrouted_cargo.value
    location_repository = DjangoLocationRepository()
    locations_before = tuple(location_repository.find_all())
    excluded = {'USCHI', 'USDAL'}

    first = client.get(
        f'/admin/cargo/{tracking_id}/destination/',
        HTTP_HX_REQUEST='true',
    )
    second = client.get(
        f'/admin/cargo/{tracking_id}/destination/',
        HTTP_HX_REQUEST='true',
    )
    first_content = first.content.decode()
    first_options = re.findall(r'<option\b[^>]*value="([^"]+)"', first_content)
    second_options = re.findall(r'<option\b[^>]*value="([^"]+)"', second.content.decode())

    assert first.status_code == second.status_code == 200
    assert 'Chicago' in first_content and 'Dallas' in first_content
    assert len(first_options) == len(locations_before) - len(excluded)
    assert not excluded.intersection(first_options)
    assert first_options == second_options
    assert locations_before == tuple(location_repository.find_all())
    assert 'initial option was Gothenburg' in expected
    assert 'Gothenburg' in first_content

    updated = client.post(
        f'/admin/cargo/{tracking_id}/destination/',
        {'destination': 'USNYC'},
        HTTP_HX_REQUEST='true',
    )
    cargo = DjangoCargoRepository().find(recorded_unrouted_cargo)
    dashboard = client.get('/admin/dashboard/').content.decode()
    not_routed_table = dashboard.split('id="not-routed-cargo"', 1)[1].split('</section>', 1)[0]

    assert updated.status_code == 204
    assert updated['HX-Redirect'] == '/admin/dashboard/'
    assert cargo is not None
    assert cargo.route_specification.origin.unlocode.value == 'USCHI'
    assert cargo.route_specification.destination.unlocode.value == 'USNYC'
    assert cargo.route_specification.arrival_deadline.date() == date(2026, 11, 8)
    assert 'New York' in not_routed_table
    assert 'Widget for var' not in updated.content.decode()


@pytest.mark.django_db
def test_deadline_dialog_fields_match_recording_and_preserve_successful_update(
    client, booking_recording, recorded_unrouted_cargo
):
    expected = booking_recording['cases']['deadline-dialog']['observed']
    tracking_id = recorded_unrouted_cargo.value

    opened = client.get(f'/admin/cargo/{tracking_id}/deadline/', HTTP_HX_REQUEST='true')
    content = opened.content.decode()
    assert opened.status_code == 200
    assert 'Chicago' in content and 'Dallas' in content
    assert 'value="2026-11-08"' in content
    assert '11/8/26' in expected

    invalid = client.post(
        f'/admin/cargo/{tracking_id}/deadline/',
        {'deadline': 'not-a-date'},
        HTTP_HX_REQUEST='true',
    )
    assert invalid.status_code == 200
    assert 'Enter a valid arrival deadline.' in invalid.content.decode()
    assert 'aria-invalid="true"' in invalid.content.decode()

    updated = client.post(
        f'/admin/cargo/{tracking_id}/deadline/',
        {'deadline': '2027-01-15'},
        HTTP_HX_REQUEST='true',
    )
    cargo = DjangoCargoRepository().find(recorded_unrouted_cargo)
    dashboard = client.get('/admin/dashboard/').content.decode()
    not_routed_table = dashboard.split('id="not-routed-cargo"', 1)[1].split('</section>', 1)[0]

    assert updated.status_code == 204
    assert updated['HX-Redirect'] == '/admin/dashboard/'
    assert cargo is not None
    assert cargo.route_specification.origin.unlocode.value == 'USCHI'
    assert cargo.route_specification.destination.unlocode.value == 'USDAL'
    assert cargo.route_specification.arrival_deadline.date() == date(2027, 1, 15)
    assert '01/15/2027' in not_routed_table
    assert 'Widget for var' not in updated.content.decode()


@pytest.mark.parametrize('dialog', ['destination', 'deadline'])
@pytest.mark.django_db
def test_unknown_dialog_updates_return_approved_not_found(dialog, client):
    call_command('seed_sample_data')

    response = client.post(
        f'/admin/cargo/UNKNOWN/{dialog}/',
        {'destination': 'USNYC', 'deadline': '2027-01-15'},
        HTTP_HX_REQUEST='true',
    )

    assert response.status_code == 404
