import re
from datetime import UTC, datetime, timedelta

import pytest
from django.core.management import call_command

from cargotracker.booking.application.dashboard import CargoDashboard
from cargotracker.booking.application.registration import CargoRegistration
from cargotracker.booking.application.routing import CargoRouting
from cargotracker.booking.interfaces.dashboard.views import create_booking_views
from cargotracker.cargo.domain.itinerary import Itinerary
from cargotracker.cargo.domain.leg import Leg
from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.cargo.infrastructure.models import CargoRecord
from cargotracker.cargo.infrastructure.repository import DjangoCargoRepository
from cargotracker.handling.infrastructure.repository import DjangoHandlingEventRepository
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.location.infrastructure.repository import DjangoLocationRepository
from cargotracker.voyage.domain.voyage_number import VoyageNumber
from cargotracker.voyage.infrastructure.repository import DjangoVoyageRepository


@pytest.mark.django_db
def test_dashboard_fields_match_tier_a_recording(client, booking_recording):
    call_command('seed_sample_data')
    cargo_repository = DjangoCargoRepository()
    cargo = cargo_repository.find(TrackingId('DEF789'))
    assert cargo is not None
    voyage = DjangoVoyageRepository().find(VoyageNumber('0100S'))
    assert voyage is not None
    deadline = cargo.route_specification.arrival_deadline
    CargoRouting(
        cargo_repository,
        DjangoLocationRepository(),
        DjangoVoyageRepository(),
        DjangoHandlingEventRepository(),
        routing_service=None,
    ).assign_route(
        cargo.tracking_id,
        Itinerary(
            (
                Leg(
                    voyage,
                    cargo.route_specification.origin,
                    cargo.route_specification.destination,
                    deadline - timedelta(days=3),
                    deadline - timedelta(days=1),
                ),
            )
        ),
    )
    location_repository = DjangoLocationRepository()
    registration = CargoRegistration(cargo_repository).register(
        location_repository.find(UnLocode('USCHI')),
        location_repository.find(UnLocode('USDAL')),
        datetime(2026, 11, 8, tzinfo=UTC),
    )

    response = client.get('/admin/dashboard/')
    content = response.content.decode()
    recorded_dashboard = booking_recording['cases']['dashboard']['observed']
    routed_table = content.split('id="routed-cargo"', 1)[1].split('</section>', 1)[0]
    not_routed_table = content.split('id="not-routed-cargo"', 1)[1].split('</section>', 1)[0]
    claimed_table = content.split('id="claimed-cargo"', 1)[1].split('</section>', 1)[0]
    expected_routed_ids = set(
        re.search(r'routed rows ([A-Z0-9/]+)', recorded_dashboard)
        .group(1)
        .split('/')
    )

    assert response.status_code == 200
    assert (
        content.index('Routed Cargo')
        < content.index('Not Routed Cargo')
        < content.index('Claimed Cargo')
    )
    assert set(re.findall(r'data-tracking-id="([^"]+)"', routed_table)) == expected_routed_ids
    assert re.findall(r'data-tracking-id="([^"]+)"', not_routed_table) == [registration.value]
    assert re.findall(r'data-tracking-id="([^"]+)"', claimed_table) == ['MNO456']
    for field in ('Origin', 'Destination', 'Last Known Location', 'Status', 'Deadline'):
        assert field in routed_table
    assert 'Hong Kong' in routed_table and 'Melbourne' in routed_table
    assert 'Chicago' in not_routed_table and 'Dallas' in not_routed_table
    assert 'New York' in claimed_table and 'Dallas' in claimed_table
    assert f'href="/admin/cargo/{registration.value}/route/"' in not_routed_table
    assert 'href="/admin/cargo/MNO456/"' in claimed_table
    assert 'title="Click to see details"' in claimed_table
    assert 'Click to see history' not in claimed_table
    assert 'ShowTrackingDialog' not in content
    assert 'Test --&gt;' not in content


@pytest.mark.django_db
def test_claimed_cargo_details_match_tier_a_fields(client, booking_recording):
    call_command('seed_sample_data')
    expected = booking_recording['cases']['cargo-details']['observed']

    response = client.get('/admin/cargo/MNO456/')
    content = response.content.decode()

    assert response.status_code == 200
    assert 'Routing Details for Cargo MNO456' in content
    assert 'New York' in content and 'Dallas' in content
    assert 'Arrival deadline' in content
    assert 'Itinerary' in content
    assert 'Handling Event History' not in content
    assert 'does not show handling-event history' in expected


@pytest.mark.django_db
def test_unknown_cargo_details_match_approved_not_found_behavior(client, booking_recording):
    call_command('seed_sample_data')
    expected = booking_recording['cases']['unknown-cargo-error']['observed']

    response = client.get('/admin/cargo/UNKNOWN/')

    assert 'HTTP 500' in expected
    assert response.status_code == 404


@pytest.mark.django_db
def test_empty_dashboard_matches_tier_a_table_fields(client, booking_recording):
    expected = booking_recording['cases']['dashboard']['observed']
    CargoRecord.objects.all().delete()

    response = client.get('/admin/dashboard/')
    content = response.content.decode()

    assert response.status_code == 200
    assert all(title in expected for title in ('Routed Cargo', 'Not Routed Cargo', 'Claimed Cargo'))
    assert content.index('Routed Cargo') < content.index('Not Routed Cargo') < content.index(
        'Claimed Cargo'
    )
    assert 'data-tracking-id=' not in content
    assert 'No cargo' not in content
