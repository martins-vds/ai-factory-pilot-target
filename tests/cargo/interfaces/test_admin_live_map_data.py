import pytest
from django.core.management import call_command

from cargotracker.cargo.application.admin_map import build_admin_map_data
from cargotracker.cargo.infrastructure.repository import DjangoCargoRepository
from cargotracker.cargo.interfaces.tracking.map.coordinates import LOCATION_COORDINATES


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
