import csv
import hashlib
import json
from datetime import UTC, date, datetime

import pytest
import yaml
from django.core.management import call_command

from cargotracker.cargo.infrastructure.models import CargoRecord, LegRecord
from cargotracker.handling.infrastructure.models import HandlingEventRecord
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
                'transport_status': {
                    'from': 'TRANSPORT_STATUS',
                    'as': {'map': {'0': 'NOT_RECEIVED'}},
                },
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
                'type': 'TYPE',
                'voyage_id': 'VOYAGE_ID',
                'location_id': 'LOCATION_ID',
                'completionTime': 'COMPLETIONTIME',
                'registration': 'REGISTRATION',
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
                'load_time': 'LOAD_TIME',
                'unload_time': 'UNLOAD_TIME',
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
                'arrival_time': 'ARRIVAL_TIME',
                'departure_time': 'DEPARTURE_TIME',
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
        [['4', 'USNYC', 'New York']],
    ),
    'VOYAGE': (
        ['ID', 'VOYAGE_NUMBER'],
        [['9', 'V001']],
    ),
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
                '15',
                'ABC123',
                '4',
                '4',
                '4',
                '2026-11-15',
                '0',
                '4',
                '9',
                'false',
                None,
                None,
                None,
                None,
                'false',
                'NOT_ROUTED',
                '2026-11-07T04:05:06Z',
                '35',
            ]
        ],
    ),
    'HANDLINGEVENT': (
        [
            'ID',
            'TYPE',
            'VOYAGE_ID',
            'LOCATION_ID',
            'COMPLETIONTIME',
            'REGISTRATION',
            'CARGO_ID',
        ],
        [['35', 'RECEIVE', '9', '4', '2026-11-06T10:00:00Z', '2026-11-06T10:01:00Z', '15']],
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
        [['50', '2026-11-07T10:00:00Z', '2026-11-08T10:00:00Z', '4', '4', '9', '15']],
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
        [['55', '2026-11-08T10:00:00Z', '2026-11-07T10:00:00Z', '4', '4', '9']],
    ),
}


def _snapshot(directory):
    directory.mkdir()
    tables = {}
    for table, (header, rows) in TABLE_ROWS.items():
        path = directory / f'{table}.csv'
        with path.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.writer(stream)
            writer.writerow(header)
            writer.writerows([['\\N' if value is None else value for value in row] for row in rows])
        tables[table] = {
            'rows': len(rows),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        }
    (directory / 'manifest.json').write_text(
        json.dumps({'null': '\\N', 'tables': tables}),
        encoding='utf-8',
    )


def _rows(model):
    return list(model.objects.order_by('pk').values())


@pytest.mark.django_db(transaction=True)
def test_load_snapshot_is_idempotent_restores_cycle_and_realigns_sequences(tmp_path):
    snapshot = tmp_path / 'snapshot'
    _snapshot(snapshot)
    mapping = tmp_path / 'mapping.yaml'
    mapping.write_text(yaml.safe_dump(MAPPING), encoding='utf-8')

    call_command('load_data_snapshot', snapshot=str(snapshot), mapping=str(mapping))

    imported_cargo = CargoRecord.objects.get(pk=15)
    imported_event = HandlingEventRecord.objects.get(pk=35)
    assert imported_cargo.last_event_id == imported_event.pk
    assert imported_event.cargo_id == imported_cargo.pk
    assert imported_cargo.spec_arrival_deadline == date(2026, 11, 15)
    assert imported_cargo.calculated_at == datetime(2026, 11, 7, 4, 5, 6, tzinfo=UTC)
    assert imported_cargo.transport_status == 'NOT_RECEIVED'

    before = {
        model: _rows(model)
        for model in (
            LocationRecord,
            VoyageRecord,
            CargoRecord,
            HandlingEventRecord,
            LegRecord,
            CarrierMovementRecord,
        )
    }
    call_command('load_data_snapshot', snapshot=str(snapshot), mapping=str(mapping))
    assert {model: _rows(model) for model in before} == before

    new_location = LocationRecord.objects.create(unlocode='TST01', name='Test location')
    new_voyage = VoyageRecord.objects.create(voyage_number='V002')
    new_cargo = CargoRecord.objects.create(
        tracking_id='XYZ789',
        origin=new_location,
        spec_origin=new_location,
        spec_destination=new_location,
        spec_arrival_deadline=date(2026, 11, 15),
        transport_status='NOT_RECEIVED',
        misdirected=False,
        unloaded_at_dest=False,
        routing_status='NOT_ROUTED',
        calculated_at=datetime(2026, 11, 7, tzinfo=UTC),
    )
    new_event = HandlingEventRecord.objects.create(
        event_type='RECEIVE',
        location=new_location,
        completion_time=datetime(2026, 11, 6, 10, tzinfo=UTC),
        registration_time=datetime(2026, 11, 6, 10, 1, tzinfo=UTC),
        cargo=new_cargo,
    )
    new_leg = LegRecord.objects.create(
        cargo=new_cargo,
        voyage=new_voyage,
        load_location=new_location,
        unload_location=new_location,
        load_time=datetime(2026, 11, 7, 10, tzinfo=UTC),
        unload_time=datetime(2026, 11, 8, 10, tzinfo=UTC),
    )
    new_movement = CarrierMovementRecord.objects.create(
        arrival_time=datetime(2026, 11, 8, 10, tzinfo=UTC),
        departure_time=datetime(2026, 11, 7, 10, tzinfo=UTC),
        arrival_location=new_location,
        departure_location=new_location,
        voyage=new_voyage,
    )

    assert new_location.pk > 4
    assert new_voyage.pk > 9
    assert new_cargo.pk > 15
    assert new_event.pk > 35
    assert new_leg.pk > 50
    assert new_movement.pk > 55
