import json
import re
from urllib.parse import parse_qs, urlsplit

import pytest
from django.core.management import call_command
from django.test import Client
from django.urls import reverse

from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.cargo.infrastructure.repository import DjangoCargoRepository
from cargotracker.cargo.interfaces.tracking.map.adapter import map_frame_url, map_status_code
from cargotracker.location.infrastructure.models import LocationRecord

EXPECTED_COORDINATES = {
    'CNHKG': [22, 114],
    'AUMEL': [-38, 145],
    'SESTO': [59, 18],
    'FIHEL': [60, 25],
    'USCHI': [42, -88],
    'JNTKO': [36, 140],
    'DEHAM': [54, 10],
    'CNSHA': [31, 121],
    'NLRTM': [52, 5],
    'SEGOT': [58, 12],
    'CNHGH': [30, 120],
    'USNYC': [41, -74],
    'USDAL': [33, -97],
}


def _rendered_map_data(response):
    match = re.search(
        r'<script id="map-data" type="application/json">(.*?)</script>',
        response.content.decode(),
        re.DOTALL,
    )
    assert match is not None
    return json.loads(match.group(1))


@pytest.mark.django_db
def test_map_markers_use_exact_configured_coordinates():
    call_command('seed_sample_data')
    client = Client()

    seeded_locations = LocationRecord.objects.values_list('unlocode', 'name')
    assert {code for code, _ in seeded_locations} == set(EXPECTED_COORDINATES)

    for code, name in seeded_locations:
        response = client.get(
            reverse('cargo_map_frame'),
            {'statusCode': 'IN_PORT', 'originCode': code, 'originName': name},
        )

        assert response.status_code == 200
        assert _rendered_map_data(response)['markers'] == [
            {
                'role': 'origin',
                'code': code,
                'name': name,
                'coordinates': EXPECTED_COORDINATES[code],
                'color': 'black',
            }
        ]


@pytest.mark.django_db
def test_map_frame_url_carries_status_and_cargo_locations():
    call_command('seed_sample_data')
    cargo = DjangoCargoRepository().find(TrackingId('ABC123'))

    map_url = map_frame_url(cargo)
    query = parse_qs(urlsplit(map_url).query, keep_blank_values=True)
    assert query == {
        'statusCode': ['IN_PORT'],
        'lastKnownLocationCode': ['USNYC'],
        'lastKnownLocationName': ['New York'],
        'originCode': ['CNHKG'],
        'originName': ['Hong Kong'],
        'destinationCode': ['FIHEL'],
        'destinationName': ['Helsinki'],
    }

    response = Client().get(map_url)
    assert response.status_code == 200
    map_data = _rendered_map_data(response)
    assert map_data['statusCode'] == 'IN_PORT'
    assert map_data['origin'] == {'code': 'CNHKG', 'name': 'Hong Kong'}
    assert map_data['destination'] == {'code': 'FIHEL', 'name': 'Helsinki'}
    assert map_data['lastKnownLocation'] == {'code': 'USNYC', 'name': 'New York'}
    assert 'apiKey' not in response.content.decode()


@pytest.mark.django_db
@pytest.mark.parametrize(
    ('tracking_id', 'expected_status'),
    [
        ('DEF789', 'NOT_ROUTED'),
        ('MNO456', 'AT_DESTINATION'),
        ('JKL567', 'MISDIRECTED'),
        ('ABC123', 'IN_PORT'),
    ],
)
def test_map_status_code_preserves_source_branch_precedence(tracking_id, expected_status):
    call_command('seed_sample_data')
    cargo = DjangoCargoRepository().find(TrackingId(tracking_id))

    assert map_status_code(cargo) == expected_status
