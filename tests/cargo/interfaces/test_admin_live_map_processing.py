import json
from datetime import UTC, datetime, timedelta

import pytest
from django.conf import settings
from django.core.management import call_command
from django.test import override_settings
from django.urls import reverse

from cargotracker.booking.application.routing import CargoRouting
from cargotracker.cargo.domain.itinerary import Itinerary
from cargotracker.cargo.domain.leg import Leg
from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.cargo.infrastructure.repository import DjangoCargoRepository
from cargotracker.handling.application.process_registration_attempt import (
    process_registration_attempt,
)
from cargotracker.handling.infrastructure.attempt_processing_repository import (
    DjangoAttemptProcessingRepository,
)
from cargotracker.handling.infrastructure.repository import DjangoHandlingEventRepository
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.location.infrastructure.repository import DjangoLocationRepository
from cargotracker.pathfinder.application.routing import RoutingService
from cargotracker.voyage.domain.voyage_number import VoyageNumber
from cargotracker.voyage.infrastructure.repository import DjangoVoyageRepository


@pytest.mark.django_db
@override_settings(CARGO_MAP_POLL_SECONDS=17)
def test_processing_receive_updates_admin_live_map_and_page_poll(client):
    call_command('seed_sample_data')
    cargo_repository = DjangoCargoRepository()
    initial_cargo = cargo_repository.find(TrackingId('DEF789'))
    assert initial_cargo.delivery.transport_status.value == 'NOT_RECEIVED'

    locations = DjangoLocationRepository()
    voyages = DjangoVoyageRepository()
    routing = CargoRouting(
        cargo_repository,
        locations,
        voyages,
        DjangoHandlingEventRepository(),
        RoutingService(),
    )
    now = datetime.now(UTC)
    routing.assign_route(
        TrackingId('DEF789'),
        Itinerary(
            (
                Leg(
                    voyages.find(VoyageNumber('0100S')),
                    locations.find(UnLocode('CNHKG')),
                    locations.find(UnLocode('FIHEL')),
                    now + timedelta(days=1),
                    now + timedelta(days=2),
                ),
            )
        ),
    )

    completion_time = now.strftime('%Y-%m-%d %H:%M')
    report_response = client.post(
        '/rest/handling/reports',
        data=json.dumps(
            {
                'completionTime': completion_time,
                'trackingId': 'DEF789',
                'eventType': 'RECEIVE',
                'unLocode': 'CNHKG',
            }
        ),
        content_type='application/json',
    )
    assert report_response.status_code == 204

    assert process_registration_attempt(
        DjangoAttemptProcessingRepository(),
        cargo_repository,
        DjangoHandlingEventRepository(),
    )

    cargo = cargo_repository.find(TrackingId('DEF789'))
    assert cargo.delivery.transport_status.value == 'IN_PORT'
    assert cargo.delivery.last_known_location.unlocode.value == 'CNHKG'
    assert cargo.delivery.routing_status.value == 'MISROUTED'
    assert not cargo.delivery.misdirected

    markers_response = client.get(
        reverse('admin_live_map_markers'),
        HTTP_HX_REQUEST='true',
    )
    assert markers_response.status_code == 200
    markers = markers_response.content.decode()
    def789_marker = next(
        fragment for fragment in markers.split('<template') if 'DEF789' in fragment
    )
    assert 'data-coordinates="22,114"' in def789_marker
    assert 'data-color="red"' in def789_marker
    assert 'Routing Status: Misrouted' in def789_marker
    assert 'Transport Status: In port' in def789_marker
    assert 'Last known location: Hong Kong' in def789_marker

    page_response = client.get(reverse('admin_live_map'))
    assert page_response.status_code == 200
    assert settings.CARGO_MAP_POLL_SECONDS == 17
    assert f'hx-trigger="every {settings.CARGO_MAP_POLL_SECONDS}s"' in (
        page_response.content.decode()
    )
