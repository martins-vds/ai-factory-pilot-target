import re
from dataclasses import replace
from datetime import UTC, datetime, timedelta

import pytest
from django.core.management import call_command
from django.test import override_settings
from django.urls import path

from cargotracker.booking.application.routing import CargoRouting
from cargotracker.booking.interfaces.dashboard.views import create_booking_views
from cargotracker.cargo.domain.itinerary import Itinerary
from cargotracker.cargo.domain.leg import Leg
from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.cargo.infrastructure.repository import DjangoCargoRepository
from cargotracker.handling.infrastructure.repository import DjangoHandlingEventRepository
from cargotracker.location.domain.location import Location
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.location.infrastructure.repository import DjangoLocationRepository
from cargotracker.voyage.domain.voyage_number import VoyageNumber
from cargotracker.voyage.infrastructure.repository import DjangoVoyageRepository


class DashboardRepository:
    def __init__(self):
        self._repository = DjangoCargoRepository()
        self.ordered_cargos = None

    def find(self, tracking_id):
        return self._repository.find(tracking_id)

    def find_all(self):
        return (
            self.ordered_cargos
            if self.ordered_cargos is not None
            else self._repository.find_all()
        )


repository = DashboardRepository()
dashboard_view, cargo_details_view = create_booking_views(repository)
urlpatterns = [
    path('admin/dashboard/', dashboard_view),
    path('admin/cargo/<str:tracking_id>/', cargo_details_view),
]


@pytest.fixture(autouse=True)
def reset_repository():
    repository.ordered_cargos = None


@pytest.mark.django_db
@override_settings(ROOT_URLCONF=__name__)
def test_dashboard_partitions_cargo_in_source_order_and_renders_claimed_details_link(client):
    call_command('seed_sample_data')
    routed_cargo = repository.find(TrackingId('ABC123'))
    assert routed_cargo is not None
    cargo_with_unknown_last_location = replace(
        routed_cargo,
        delivery=replace(
            routed_cargo.delivery,
            last_known_location=Location(UnLocode('XXXXX'), 'Unknown'),
        ),
    )
    repository.ordered_cargos = [
        repository.find(TrackingId(tracking_id))
        for tracking_id in ('JKL567', 'DEF789')
    ]
    repository.ordered_cargos.extend((cargo_with_unknown_last_location, repository.find(TrackingId('MNO456'))))

    response = client.get('/admin/dashboard/')
    content = response.content.decode()
    routed_table = content.split('id="routed-cargo"', 1)[1].split('</section>', 1)[0]
    not_routed_table = content.split('id="not-routed-cargo"', 1)[1].split('</section>', 1)[0]
    claimed_table = content.split('id="claimed-cargo"', 1)[1].split('</section>', 1)[0]

    assert response.status_code == 200
    assert content.index('Routed Cargo') < content.index('Not Routed Cargo') < content.index(
        'Claimed Cargo'
    )
    assert re.findall(r'data-tracking-id="([^"]+)"', routed_table) == ['JKL567', 'ABC123']
    assert re.findall(r'data-tracking-id="([^"]+)"', not_routed_table) == ['DEF789']
    assert re.findall(r'data-tracking-id="([^"]+)"', claimed_table) == ['MNO456']
    assert routed_table.index('JKL567') < routed_table.index('ABC123')
    assert 'Origin' in routed_table and 'CNHKG' in routed_table
    assert 'Destination' in routed_table and 'FIHEL' in routed_table
    assert 'Last Known Location' in routed_table and 'Unknown' in routed_table
    assert 'XXXXX' not in routed_table
    assert 'Status' in routed_table and 'IN_PORT' in routed_table
    assert 'Deadline' in routed_table and re.search(r'\d{2}/\d{2}/\d{4}', routed_table)
    assert 'Hong Kong' in not_routed_table and 'Melbourne' in not_routed_table
    assert 'AUMEL' in not_routed_table and 'Deadline' in not_routed_table
    assert 'New York' in claimed_table and 'Dallas' in claimed_table
    assert 'href="/admin/cargo/DEF789/route/"' in not_routed_table
    assert 'href="/admin/cargo/MNO456/"' in claimed_table
    assert 'title="Click to see details"' in claimed_table
    assert 'Click to see history' not in claimed_table
    assert 'ShowTrackingDialog' not in content
    assert 'Test --&gt;' not in content


@pytest.mark.django_db
@override_settings(ROOT_URLCONF=__name__)
def test_dashboard_renders_empty_tables_without_custom_empty_state(client):
    repository.ordered_cargos = []

    response = client.get('/admin/dashboard/')
    content = response.content.decode()

    assert response.status_code == 200
    assert 'Routed Cargo' in content
    assert 'Not Routed Cargo' in content
    assert 'Claimed Cargo' in content
    assert 'data-tracking-id=' not in content
    assert 'No cargo' not in content


@pytest.mark.django_db
@override_settings(ROOT_URLCONF=__name__)
def test_cargo_moves_from_not_routed_to_routed_after_assignment(client):
    call_command('seed_sample_data')
    cargo_repository = DjangoCargoRepository()
    tracking_id = TrackingId('DEF789')
    cargo = cargo_repository.find(tracking_id)
    assert cargo is not None

    before = client.get('/admin/dashboard/').content.decode()
    not_routed_table = before.split('id="not-routed-cargo"', 1)[1].split('</section>', 1)[0]
    assert 'data-tracking-id="DEF789"' in not_routed_table

    voyage = DjangoVoyageRepository().find(VoyageNumber('0100S'))
    assert voyage is not None
    itinerary = Itinerary(
        (
            Leg(
                voyage,
                cargo.route_specification.origin,
                cargo.route_specification.destination,
                datetime.now(UTC),
                datetime.now(UTC) + timedelta(days=1),
            ),
        )
    )
    CargoRouting(
        cargo_repository,
        DjangoLocationRepository(),
        DjangoVoyageRepository(),
        DjangoHandlingEventRepository(),
        routing_service=None,
    ).assign_route(tracking_id, itinerary)

    after = client.get('/admin/dashboard/').content.decode()
    routed_table = after.split('id="routed-cargo"', 1)[1].split('</section>', 1)[0]
    not_routed_table = after.split('id="not-routed-cargo"', 1)[1].split('</section>', 1)[0]

    assert 'data-tracking-id="DEF789"' in routed_table
    assert 'data-tracking-id="DEF789"' not in not_routed_table
