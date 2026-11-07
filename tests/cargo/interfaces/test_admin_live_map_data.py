from dataclasses import replace

import pytest
from django.conf import settings
from django.core.management import call_command
from django.urls import resolve, reverse

from cargotracker.cargo.application.admin_map import build_admin_map_data
from cargotracker.cargo.domain.delivery import TransportStatus
from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.cargo.infrastructure.repository import DjangoCargoRepository
from cargotracker.cargo.interfaces.tracking.map.coordinates import LOCATION_COORDINATES
from cargotracker.location.domain.location import Location
from cargotracker.location.domain.un_locode import UnLocode


class _CargoRepository:
    def __init__(self, cargos):
        self._cargos = cargos

    def find_all(self):
        return self._cargos


@pytest.mark.django_db
def test_admin_map_data_includes_every_cargo_and_maps_status_and_location():
    call_command('seed_sample_data')

    map_data = build_admin_map_data(DjangoCargoRepository(), LOCATION_COORDINATES)
    cargos = {cargo['tracking_id']: cargo for cargo in map_data}

    assert set(cargos) == {'ABC123', 'DEF789', 'JKL567', 'MNO456'}
    assert cargos['ABC123'] == {
        'tracking_id': 'ABC123',
        'routing_status': 'ROUTED',
        'misdirected': False,
        'transport_status': 'IN_PORT',
        'at_destination': False,
        'origin': {'code': 'CNHKG', 'name': 'Hong Kong'},
        'last_known_location': {'code': 'USNYC', 'name': 'New York'},
        'location': {'code': 'USNYC', 'name': 'New York'},
        'coordinates': [41, -74],
    }
    assert cargos['DEF789'] == {
        'tracking_id': 'DEF789',
        'routing_status': 'NOT_ROUTED',
        'misdirected': False,
        'transport_status': 'NOT_RECEIVED',
        'at_destination': False,
        'origin': {'code': 'CNHKG', 'name': 'Hong Kong'},
        'last_known_location': {'code': 'XXXXX', 'name': 'Unknown'},
        'location': {'code': 'CNHKG', 'name': 'Hong Kong'},
        'coordinates': [22, 114],
    }


@pytest.mark.django_db
def test_unknown_and_unmapped_locations_never_receive_coordinates():
    call_command('seed_sample_data')
    cargo_repository = DjangoCargoRepository()
    not_received = cargo_repository.find(TrackingId('DEF789'))
    not_received.origin = Location.UNKNOWN
    in_transit = cargo_repository.find(TrackingId('ABC123'))
    in_transit.delivery = replace(
        in_transit.delivery,
        transport_status=TransportStatus.IN_PORT,
        last_known_location=Location(UnLocode('ZZZZZ'), 'Unmapped'),
    )

    cargos = build_admin_map_data(
        _CargoRepository([not_received, in_transit]), LOCATION_COORDINATES
    )

    assert cargos[0]['location'] == {'code': 'XXXXX', 'name': 'Unknown'}
    assert cargos[0]['coordinates'] is None
    assert cargos[1]['location'] == {'code': 'ZZZZZ', 'name': 'Unmapped'}
    assert cargos[1]['coordinates'] is None


def test_admin_live_map_routes_are_registered():
    assert reverse('admin_live_map') == '/admin/live-map/'
    assert reverse('admin_live_map_markers') == '/admin/live-map/markers/'
    assert resolve('/admin/live-map/').url_name == 'admin_live_map'
    assert resolve('/admin/live-map/markers/').url_name == 'admin_live_map_markers'


def test_admin_map_polling_interval_defaults_to_ten_seconds():
    assert settings.CARGO_MAP_POLL_SECONDS == 10
