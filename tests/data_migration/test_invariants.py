import csv
import hashlib
import json
from dataclasses import replace
from itertools import pairwise

import pytest
import yaml
from django.core.management import call_command

from cargotracker.cargo.domain.delivery import Delivery
from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.cargo.infrastructure.models import CargoRecord
from cargotracker.cargo.infrastructure.repository import DjangoCargoRepository
from cargotracker.handling.infrastructure.models import HandlingEventRecord
from cargotracker.handling.infrastructure.repository import DjangoHandlingEventRepository
from cargotracker.location.infrastructure.models import LocationRecord
from cargotracker.voyage.infrastructure.models import CarrierMovementRecord, VoyageRecord

MAPPING = {
    'defaults': {'timestamp_tz': 'UTC'},
    'tables': [
        {
            'target': 'location',
            'source': 'LOCATION',
            'key': ['id'],
            'columns': {'id': 'ID', 'unlocode': 'UNLOCODE', 'name': 'NAME'},
        },
        {
            'target': 'voyage',
            'source': 'VOYAGE',
            'key': ['id'],
            'columns': {'id': 'ID', 'voyage_number': 'VOYAGE_NUMBER'},
        },
        {
            'target': 'cargo',
            'source': 'CARGO',
            'key': ['id'],
            'columns': {
                'id': 'ID',
                'tracking_id': 'TRACKING_ID',
                'origin_id': 'ORIGIN_ID',
                'spec_origin_id': 'SPEC_ORIGIN_ID',
                'spec_destination_id': 'SPEC_DESTINATION_ID',
                'spec_arrival_deadline': {'from': 'SPEC_ARRIVAL_DEADLINE', 'as': 'date'},
                'transport_status': 'TRANSPORT_STATUS',
                'last_known_location_id': 'LAST_KNOWN_LOCATION_ID',
                'current_voyage_id': 'CURRENT_VOYAGE_ID',
                'misdirected': {'from': 'MISDIRECTED', 'as': 'bool'},
                'eta': {'from': 'ETA', 'as': 'date'},
                'next_expected_handling_event_type': 'NEXT_EXPECTED_HANDLING_EVENT_TYPE',
                'next_expected_location_id': 'NEXT_EXPECTED_LOCATION_ID',
                'next_expected_voyage_id': 'NEXT_EXPECTED_VOYAGE_ID',
                'unloaded_at_dest': {'from': 'UNLOADED_AT_DEST', 'as': 'bool'},
                'routing_status': 'ROUTING_STATUS',
                'calculated_at': {'from': 'CALCULATED_AT', 'as': 'timestamp'},
                'last_event_id': 'LAST_EVENT_ID',
            },
            'refs': {
                'origin_id': 'location.id',
                'spec_origin_id': 'location.id',
                'spec_destination_id': 'location.id',
                'last_known_location_id': 'location.id',
                'current_voyage_id': 'voyage.id',
                'next_expected_location_id': 'location.id',
                'next_expected_voyage_id': 'voyage.id',
                'last_event_id': 'HandlingEvent.id',
            },
        },
        {
            'target': 'HandlingEvent',
            'source': 'HANDLINGEVENT',
            'key': ['id'],
            'columns': {
                'id': 'ID',
                'event_type': 'TYPE',
                'voyage_id': 'VOYAGE_ID',
                'location_id': 'LOCATION_ID',
                'completion_time': {'from': 'COMPLETIONTIME', 'as': 'timestamp'},
                'registration_time': {'from': 'REGISTRATION', 'as': 'timestamp'},
                'cargo_id': 'CARGO_ID',
            },
            'refs': {
                'voyage_id': 'voyage.id',
                'location_id': 'location.id',
                'cargo_id': 'cargo.id',
            },
        },
        {
            'target': 'leg',
            'source': 'LEG',
            'key': ['id'],
            'columns': {
                'id': 'ID',
                'load_time': {'from': 'LOAD_TIME', 'as': 'timestamp'},
                'unload_time': {'from': 'UNLOAD_TIME', 'as': 'timestamp'},
                'load_location_id': 'LOAD_LOCATION_ID',
                'unload_location_id': 'UNLOAD_LOCATION_ID',
                'voyage_id': 'VOYAGE_ID',
                'cargo_id': 'CARGO_ID',
            },
            'refs': {
                'load_location_id': 'location.id',
                'unload_location_id': 'location.id',
                'voyage_id': 'voyage.id',
                'cargo_id': 'cargo.id',
            },
        },
        {
            'target': 'carrier_movement',
            'source': 'CARRIER_MOVEMENT',
            'key': ['id'],
            'columns': {
                'id': 'ID',
                'arrival_time': {'from': 'ARRIVAL_TIME', 'as': 'timestamp'},
                'departure_time': {'from': 'DEPARTURE_TIME', 'as': 'timestamp'},
                'arrival_location_id': 'ARRIVAL_LOCATION_ID',
                'departure_location_id': 'DEPARTURE_LOCATION_ID',
                'voyage_id': 'VOYAGE_ID',
            },
            'refs': {
                'arrival_location_id': 'location.id',
                'departure_location_id': 'location.id',
                'voyage_id': 'voyage.id',
            },
        },
    ],
}

TABLE_ROWS = {
    'LOCATION': (
        ['ID', 'UNLOCODE', 'NAME'],
        [['1', 'USNYC', 'Origin'], ['2', 'NLRTM', 'Transfer'], ['3', 'USLAX', 'Destination']],
    ),
    'VOYAGE': (['ID', 'VOYAGE_NUMBER'], [['10', 'V-001']]),
    'CARGO': (
        [
            'ID',
            'TRACKING_ID',
            'ORIGIN_ID',
            'SPEC_ORIGIN_ID',
            'SPEC_DESTINATION_ID',
            'SPEC_ARRIVAL_DEADLINE',
            'TRANSPORT_STATUS',
            'LAST_KNOWN_LOCATION_ID',
            'CURRENT_VOYAGE_ID',
            'MISDIRECTED',
            'ETA',
            'NEXT_EXPECTED_HANDLING_EVENT_TYPE',
            'NEXT_EXPECTED_LOCATION_ID',
            'NEXT_EXPECTED_VOYAGE_ID',
            'UNLOADED_AT_DEST',
            'ROUTING_STATUS',
            'CALCULATED_AT',
            'LAST_EVENT_ID',
        ],
        [
            [
                '50',
                'TEST-0001',
                '1',
                '1',
                '3',
                '2026-11-10',
                'ONBOARD_CARRIER',
                '1',
                '10',
                'false',
                '2026-11-09',
                'UNLOAD',
                '2',
                '10',
                'false',
                'ROUTED',
                '2026-11-07T01:00:00Z',
                '302',
            ],
            [
                '51',
                'TEST-0002',
                '1',
                '1',
                '2',
                '2026-12-01',
                'NOT_RECEIVED',
                None,
                None,
                'false',
                None,
                None,
                None,
                None,
                'false',
                'NOT_ROUTED',
                '2026-11-07T01:00:00Z',
                None,
            ],
        ],
    ),
    'HANDLINGEVENT': (
        ['ID', 'TYPE', 'VOYAGE_ID', 'LOCATION_ID', 'COMPLETIONTIME', 'REGISTRATION', 'CARGO_ID'],
        [
            ['301', 'RECEIVE', None, '1', '2026-11-07T02:00:00Z', '2026-11-07T02:01:00Z', '50'],
            ['302', 'LOAD', '10', '1', '2026-11-08T08:00:00Z', '2026-11-08T08:01:00Z', '50'],
        ],
    ),
    'LEG': (
        [
            'ID',
            'LOAD_TIME',
            'UNLOAD_TIME',
            'LOAD_LOCATION_ID',
            'UNLOAD_LOCATION_ID',
            'VOYAGE_ID',
            'CARGO_ID',
        ],
        [
            ['401', '2026-11-08T08:00:00Z', '2026-11-08T12:00:00Z', '1', '2', '10', '50'],
            ['402', '2026-11-08T16:00:00Z', '2026-11-09T00:00:00Z', '2', '3', '10', '50'],
        ],
    ),
    'CARRIER_MOVEMENT': (
        [
            'ID',
            'ARRIVAL_TIME',
            'DEPARTURE_TIME',
            'ARRIVAL_LOCATION_ID',
            'DEPARTURE_LOCATION_ID',
            'VOYAGE_ID',
        ],
        [
            ['501', '2026-11-08T12:00:00Z', '2026-11-08T08:00:00Z', '2', '1', '10'],
            ['502', '2026-11-09T00:00:00Z', '2026-11-08T16:00:00Z', '3', '2', '10'],
        ],
    ),
}


def _write_snapshot(snapshot, mapping_path):
    snapshot.mkdir()
    tables = {}
    for source, (header, rows) in TABLE_ROWS.items():
        path = snapshot / f'{source}.csv'
        with path.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.writer(stream)
            writer.writerow(header)
            writer.writerows([['\\N' if value is None else value for value in row] for row in rows])
        tables[source] = {
            'rows': len(rows),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        }
    (snapshot / 'manifest.json').write_text(
        json.dumps({'null': '\\N', 'tables': tables}),
        encoding='utf-8',
    )
    mapping_path.write_text(yaml.safe_dump(MAPPING), encoding='utf-8')


@pytest.fixture
def loaded_snapshot(tmp_path):
    snapshot = tmp_path / 'snapshot'
    mapping_path = tmp_path / 'mapping.yaml'
    _write_snapshot(snapshot, mapping_path)
    call_command('load_data_snapshot', snapshot=str(snapshot), mapping=str(mapping_path))


@pytest.mark.django_db(transaction=True)
def test_loaded_cargo_delivery_matches_its_handling_history(loaded_snapshot):
    cargo_repository = DjangoCargoRepository()
    handling_repository = DjangoHandlingEventRepository()

    cargos = cargo_repository.find_all()
    assert len(cargos) == CargoRecord.objects.count() == 2
    for cargo in cargos:
        history = handling_repository.lookup_handling_history_of_cargo(cargo.tracking_id)
        expected = Delivery.derived_from(
            cargo.route_specification,
            cargo.itinerary,
            history,
            cargo.delivery.calculated_at,
        )

        assert replace(expected, last_event_id=history.most_recent_event_id) == cargo.delivery


@pytest.mark.django_db(transaction=True)
def test_loaded_itinerary_legs_connect(loaded_snapshot):
    cargos = DjangoCargoRepository().find_all()
    routed_cargo = next(cargo for cargo in cargos if cargo.tracking_id == TrackingId('TEST-0001'))
    assert len(routed_cargo.itinerary.legs) == 2

    for previous, following in pairwise(routed_cargo.itinerary.legs):
        assert previous.unload_location == following.load_location


@pytest.mark.django_db(transaction=True)
def test_loaded_handling_events_reference_existing_voyages_and_locations(loaded_snapshot):
    location_ids = set(LocationRecord.objects.values_list('pk', flat=True))
    voyage_ids = set(VoyageRecord.objects.values_list('pk', flat=True))

    events = HandlingEventRecord.objects.all()
    assert events.count() == 2
    for event in events:
        assert event.location_id in location_ids
        if event.voyage_id is not None:
            assert event.voyage_id in voyage_ids


@pytest.mark.django_db(transaction=True)
def test_loaded_voyage_carrier_movements_are_in_schedule_order(loaded_snapshot):
    voyages = VoyageRecord.objects.all()
    assert voyages.count() == 1
    for voyage in voyages:
        movements = list(
            CarrierMovementRecord.objects.filter(voyage=voyage)
            .select_related('departure_location', 'arrival_location')
            .order_by('departure_time', 'pk')
        )
        assert len(movements) == 2
        for previous, following in pairwise(movements):
            assert previous.arrival_time <= following.departure_time
            assert previous.arrival_location == following.departure_location
