import copy
import csv
import hashlib
import json
import shutil
from datetime import UTC, date, datetime
from io import StringIO
from pathlib import Path

import pytest
import yaml
from django.core.management import call_command
from django.core.management.base import CommandError

from cargotracker.cargo.infrastructure.models import CargoRecord, LegRecord
from cargotracker.data_migration import loader
from cargotracker.handling.infrastructure.models import HandlingEventRecord
from cargotracker.location.infrastructure.models import LocationRecord
from cargotracker.voyage.infrastructure.models import CarrierMovementRecord, VoyageRecord

FIXTURE_SNAPSHOT = Path(__file__).parent / 'fixtures' / 'DM-05C'

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
                    'as': {
                        'map': {
                            'NOT_RECEIVED': 'NOT_RECEIVED',
                            'IN_PORT': 'IN_PORT',
                            'ONBOARD_CARRIER': 'ONBOARD_CARRIER',
                            'CLAIMED': 'CLAIMED',
                            'UNKNOWN': 'UNKNOWN',
                        }
                    },
                },
                'last_known_location_id': 'LAST_KNOWN_LOCATION_ID',
                'current_voyage_id': 'CURRENT_VOYAGE_ID',
                'misdirected': {'from': 'MISDIRECTED', 'as': 'bool'},
                'eta': {'from': 'ETA', 'as': 'date'},
                'next_expected_handling_event_type': {
                    'from': 'NEXT_EXPECTED_HANDLING_EVENT_TYPE',
                    'as': {
                        'map': {
                            'LOAD': 'LOAD',
                            'UNLOAD': 'UNLOAD',
                            'RECEIVE': 'RECEIVE',
                            'CLAIM': 'CLAIM',
                            'CUSTOMS': 'CUSTOMS',
                        }
                    },
                },
                'next_expected_location_id': 'NEXT_EXPECTED_LOCATION_ID',
                'next_expected_voyage_id': 'NEXT_EXPECTED_VOYAGE_ID',
                'unloaded_at_dest': {'from': 'UNLOADED_AT_DEST', 'as': 'bool'},
                'routing_status': {
                    'from': 'ROUTING_STATUS',
                    'as': {
                        'map': {
                            'NOT_ROUTED': 'NOT_ROUTED',
                            'ROUTED': 'ROUTED',
                            'MISROUTED': 'MISROUTED',
                        }
                    },
                },
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
                'type': {
                    'from': 'TYPE',
                    'as': {
                        'map': {
                            'LOAD': 'LOAD',
                            'UNLOAD': 'UNLOAD',
                            'RECEIVE': 'RECEIVE',
                            'CLAIM': 'CLAIM',
                            'CUSTOMS': 'CUSTOMS',
                        }
                    },
                },
                'voyage_id': 'VOYAGE_ID',
                'location_id': 'LOCATION_ID',
                'completionTime': {'from': 'COMPLETIONTIME', 'as': 'timestamp'},
                'registration': {'from': 'REGISTRATION', 'as': 'timestamp'},
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
                'NOT_RECEIVED',
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


def _snapshot(directory, table_rows=TABLE_ROWS):
    directory.mkdir()
    tables = {}
    for table, (header, rows) in table_rows.items():
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


def _load_fixture(tmp_path):
    mapping = tmp_path / 'mapping.yaml'
    mapping.write_text(yaml.safe_dump(MAPPING), encoding='utf-8')
    call_command(
        'load_data_snapshot',
        snapshot=str(FIXTURE_SNAPSHOT),
        mapping=str(mapping),
    )


def _refresh_manifest(snapshot, source, row_count):
    manifest_path = snapshot / 'manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    source_path = snapshot / f'{source}.csv'
    manifest['tables'][source].update(
        rows=row_count,
        sha256=hashlib.sha256(source_path.read_bytes()).hexdigest(),
    )
    manifest_path.write_text(json.dumps(manifest), encoding='utf-8')


@pytest.mark.django_db(transaction=True)
def test_load_snapshot_persists_every_mapped_value(tmp_path):
    _load_fixture(tmp_path)

    assert _rows(LocationRecord) == [
        {'id': 101, 'unlocode': 'USNYC', 'name': 'New York'},
        {'id': 102, 'unlocode': 'NLRTM', 'name': 'Rotterdam'},
    ]
    assert _rows(VoyageRecord) == [{'id': 900, 'voyage_number': ''}]
    assert _rows(CargoRecord) == [
        {
            'id': 13,
            'tracking_id': 'FIDELITY-0001',
            'origin_id': 101,
            'spec_origin_id': 101,
            'spec_destination_id': 102,
            'spec_arrival_deadline': date(2026, 12, 30),
            'transport_status': 'NOT_RECEIVED',
            'last_known_location_id': None,
            'current_voyage_id': 900,
            'misdirected': True,
            'eta': date(2026, 12, 29),
            'next_expected_handling_event_type': 'LOAD',
            'next_expected_location_id': None,
            'next_expected_voyage_id': None,
            'unloaded_at_dest': False,
            'routing_status': 'ROUTED',
            'calculated_at': datetime(2026, 11, 7, 10, 11, 12, tzinfo=UTC),
            'last_event_id': 71,
        }
    ]
    assert _rows(HandlingEventRecord) == [
        {
            'id': 71,
            'event_type': 'RECEIVE',
            'voyage_id': 900,
            'location_id': 102,
            'completion_time': datetime(2026, 11, 7, 8, 12, 13, tzinfo=UTC),
            'registration_time': datetime(2026, 11, 7, 10, 13, 14, tzinfo=UTC),
            'cargo_id': 13,
        }
    ]
    assert _rows(LegRecord) == [
        {
            'id': 81,
            'load_time': datetime(2026, 11, 8, 8, tzinfo=UTC),
            'unload_time': datetime(2026, 11, 9, 11, tzinfo=UTC),
            'load_location_id': 101,
            'unload_location_id': 102,
            'voyage_id': 900,
            'cargo_id': 13,
        }
    ]
    assert _rows(CarrierMovementRecord) == [
        {
            'id': 91,
            'arrival_time': datetime(2026, 11, 9, 10, tzinfo=UTC),
            'departure_time': datetime(2026, 11, 8, 12, tzinfo=UTC),
            'arrival_location_id': 102,
            'departure_location_id': 101,
            'voyage_id': 900,
        }
    ]


@pytest.mark.django_db(transaction=True)
def test_load_snapshot_clears_and_reloads_identical_rows(tmp_path):
    _load_fixture(tmp_path)
    models = (
        LocationRecord,
        VoyageRecord,
        CargoRecord,
        HandlingEventRecord,
        LegRecord,
        CarrierMovementRecord,
    )
    before = {model: _rows(model) for model in models}

    _load_fixture(tmp_path)

    assert {model: _rows(model) for model in models} == before


@pytest.mark.django_db(transaction=True)
def test_load_snapshot_defers_and_restores_cargo_event_cycle(tmp_path, monkeypatch):
    restore_references = loader._set_deferred_references

    def observe_two_phase_cycle(pending):
        assert CargoRecord.objects.get(pk=13).last_event_id is None
        assert HandlingEventRecord.objects.get(pk=71).cargo_id == 13
        restore_references(pending)
        assert CargoRecord.objects.get(pk=13).last_event_id == 71

    monkeypatch.setattr(loader, '_set_deferred_references', observe_two_phase_cycle)
    _load_fixture(tmp_path)


@pytest.mark.django_db(transaction=True)
def test_load_snapshot_realigns_each_sequence_to_max_plus_one(tmp_path):
    _load_fixture(tmp_path)

    location = LocationRecord.objects.create(unlocode='TST01', name='Test location')
    voyage = VoyageRecord.objects.create(voyage_number='V-901')
    cargo = CargoRecord.objects.create(
        tracking_id='FIDELITY-0002',
        origin=location,
        spec_origin=location,
        spec_destination=location,
        spec_arrival_deadline=date(2026, 12, 31),
        transport_status='NOT_RECEIVED',
        misdirected=False,
        unloaded_at_dest=False,
        routing_status='NOT_ROUTED',
        calculated_at=datetime(2026, 11, 7, tzinfo=UTC),
    )
    event = HandlingEventRecord.objects.create(
        event_type='RECEIVE',
        location=location,
        completion_time=datetime(2026, 11, 7, 10, tzinfo=UTC),
        registration_time=datetime(2026, 11, 7, 11, tzinfo=UTC),
        cargo=cargo,
    )
    leg = LegRecord.objects.create(
        cargo=cargo,
        voyage=voyage,
        load_location=location,
        unload_location=location,
        load_time=datetime(2026, 11, 8, 10, tzinfo=UTC),
        unload_time=datetime(2026, 11, 9, 10, tzinfo=UTC),
    )
    movement = CarrierMovementRecord.objects.create(
        arrival_time=datetime(2026, 11, 9, 10, tzinfo=UTC),
        departure_time=datetime(2026, 11, 8, 10, tzinfo=UTC),
        arrival_location=location,
        departure_location=location,
        voyage=voyage,
    )

    assert location.pk == 103
    assert voyage.pk == 901
    assert cargo.pk == 14
    assert event.pk == 72
    assert leg.pk == 82
    assert movement.pk == 92


@pytest.mark.django_db(transaction=True)
def test_load_snapshot_includes_carrier_movement_row(tmp_path):
    _load_fixture(tmp_path)

    assert _rows(CarrierMovementRecord) == [
        {
            'id': 91,
            'arrival_time': datetime(2026, 11, 9, 10, tzinfo=UTC),
            'departure_time': datetime(2026, 11, 8, 12, tzinfo=UTC),
            'arrival_location_id': 102,
            'departure_location_id': 101,
            'voyage_id': 900,
        }
    ]


@pytest.mark.django_db(transaction=True)
def test_load_snapshot_rejects_malformed_snapshot_inputs(tmp_path):
    cases = (
        'missing_manifest',
        'invalid_manifest',
        'invalid_table_list',
        'missing_table_entry',
        'missing_csv',
        'hash_mismatch',
        'empty_file',
        'duplicate_header',
        'wrong_field_count',
        'row_count_mismatch',
        'missing_mapped_column',
        'missing_multiple_mapped_columns',
        'null_primary_key',
    )
    for case in cases:
        case_dir = tmp_path / case
        case_dir.mkdir()
        snapshot = case_dir / 'snapshot'
        shutil.copytree(FIXTURE_SNAPSHOT, snapshot)
        mapping = copy.deepcopy(MAPPING)
        manifest_path = snapshot / 'manifest.json'
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))

        if case == 'missing_manifest':
            manifest_path.unlink()
        elif case == 'invalid_manifest':
            manifest_path.write_text('{', encoding='utf-8')
        elif case == 'invalid_table_list':
            manifest['tables'] = []
            manifest_path.write_text(json.dumps(manifest), encoding='utf-8')
        elif case == 'missing_table_entry':
            manifest['tables'].pop('CARGO')
            manifest_path.write_text(json.dumps(manifest), encoding='utf-8')
        elif case == 'missing_csv':
            (snapshot / 'LEG.csv').unlink()
        elif case == 'hash_mismatch':
            (snapshot / 'LOCATION.csv').write_text(
                'ID,UNLOCODE,NAME\n101,USNYC,Changed\n102,NLRTM,Rotterdam\n',
                encoding='utf-8',
            )
        elif case == 'empty_file':
            (snapshot / 'LOCATION.csv').write_text('', encoding='utf-8')
            _refresh_manifest(snapshot, 'LOCATION', 0)
        elif case == 'duplicate_header':
            (snapshot / 'LOCATION.csv').write_text(
                'ID,ID,NAME\n101,USNYC,New York\n',
                encoding='utf-8',
            )
            _refresh_manifest(snapshot, 'LOCATION', 1)
        elif case == 'wrong_field_count':
            (snapshot / 'LOCATION.csv').write_text(
                'ID,UNLOCODE,NAME\n101,USNYC\n',
                encoding='utf-8',
            )
            _refresh_manifest(snapshot, 'LOCATION', 1)
        elif case == 'row_count_mismatch':
            manifest['tables']['CARGO']['rows'] = 2
            manifest_path.write_text(json.dumps(manifest), encoding='utf-8')
        elif case == 'missing_mapped_column':
            mapping['tables'][0]['columns']['name'] = 'MISSING'
        elif case == 'missing_multiple_mapped_columns':
            mapping['tables'][0]['columns']['unlocode'] = 'MISSING_B'
            mapping['tables'][0]['columns']['name'] = 'MISSING_A'
        elif case == 'null_primary_key':
            (snapshot / 'LOCATION.csv').write_text(
                'ID,UNLOCODE,NAME\n\\N,USNYC,New York\n',
                encoding='utf-8',
            )
            _refresh_manifest(snapshot, 'LOCATION', 1)

        mapping_path = case_dir / 'mapping.yaml'
        mapping_path.write_text(yaml.safe_dump(mapping), encoding='utf-8')
        with pytest.raises(CommandError) as error:
            call_command(
                'load_data_snapshot',
                snapshot=str(snapshot),
                mapping=str(mapping_path),
            )
        expected = {
            'missing_manifest': f'{snapshot}/manifest.json: no manifest.json',
            'invalid_manifest': (
                f'{snapshot}/manifest.json: invalid manifest: '
                'Expecting property name enclosed in double quotes: line 1 column 2 (char 1)'
            ),
            'invalid_table_list': f'{snapshot}/manifest.json: tables must be an object',
            'missing_table_entry': 'CARGO: table is not listed in the snapshot manifest',
            'missing_csv': f'{snapshot}/LEG.csv: missing',
            'hash_mismatch': 'LOCATION: sha256 differs from the snapshot manifest',
            'empty_file': f'{snapshot}/LOCATION.csv: empty file (a header row is required)',
            'duplicate_header': f'{snapshot}/LOCATION.csv: duplicate columns in header',
            'wrong_field_count': f'{snapshot}/LOCATION.csv:2: 2 fields, header has 3',
            'row_count_mismatch': 'CARGO: 1 rows, manifest says 2',
            'missing_mapped_column': 'LOCATION: no column(s) MISSING in its CSV header',
            'missing_multiple_mapped_columns': (
                'LOCATION: no column(s) MISSING_A, MISSING_B in its CSV header'
            ),
            'null_primary_key': 'LOCATION: primary key cannot be NULL',
        }[case]
        assert str(error.value) == expected


@pytest.mark.django_db(transaction=True)
def test_load_snapshot_uses_utc_when_mapping_has_no_timestamp_default(tmp_path):
    mapping = copy.deepcopy(MAPPING)
    mapping.pop('defaults')
    mapping_path = tmp_path / 'mapping.yaml'
    mapping_path.write_text(yaml.safe_dump(mapping), encoding='utf-8')

    call_command(
        'load_data_snapshot',
        snapshot=str(FIXTURE_SNAPSHOT),
        mapping=str(mapping_path),
    )

    assert CargoRecord.objects.get(pk=13).calculated_at == datetime(
        2026, 11, 7, 10, 11, 12, tzinfo=UTC
    )


@pytest.mark.django_db(transaction=True)
def test_load_snapshot_defaults_to_identity_when_as_is_omitted(tmp_path):
    mapping = copy.deepcopy(MAPPING)
    mapping['tables'][0]['columns']['name'] = {'from': 'NAME'}
    mapping_path = tmp_path / 'mapping.yaml'
    mapping_path.write_text(yaml.safe_dump(mapping), encoding='utf-8')

    call_command(
        'load_data_snapshot',
        snapshot=str(FIXTURE_SNAPSHOT),
        mapping=str(mapping_path),
    )

    assert LocationRecord.objects.get(pk=101).name == 'New York'


@pytest.mark.django_db(transaction=True)
def test_load_snapshot_rejects_unknown_timestamp_timezone(tmp_path):
    mapping = copy.deepcopy(MAPPING)
    mapping['defaults']['timestamp_tz'] = 'Not/A_Timezone'
    mapping_path = tmp_path / 'mapping.yaml'
    mapping_path.write_text(yaml.safe_dump(mapping), encoding='utf-8')

    with pytest.raises(CommandError) as error:
        call_command(
            'load_data_snapshot',
            snapshot=str(FIXTURE_SNAPSHOT),
            mapping=str(mapping_path),
        )
    assert str(error.value) == "unknown timestamp timezone 'Not/A_Timezone'"


@pytest.mark.django_db(transaction=True)
def test_load_snapshot_uses_every_supported_boolean_spelling(tmp_path):
    aliases = (
        ('t', 'f'),
        ('yes', 'no'),
        ('y', 'n'),
    )
    for index, (true_value, false_value) in enumerate(aliases, start=1):
        case_dir = tmp_path / str(index)
        case_dir.mkdir()
        snapshot = case_dir / 'snapshot'
        table_rows = {
            table: (header.copy(), [row.copy() for row in rows])
            for table, (header, rows) in TABLE_ROWS.items()
        }
        cargo = table_rows['CARGO'][1][0].copy()
        cargo[0] = str(15 + index)
        cargo[1] = f'ALIAS-{index}'
        cargo[9] = true_value
        cargo[14] = false_value
        table_rows['CARGO'][1].append(cargo)
        _snapshot(snapshot, table_rows)
        mapping_path = case_dir / 'mapping.yaml'
        mapping_path.write_text(yaml.safe_dump(MAPPING), encoding='utf-8')

        call_command(
            'load_data_snapshot',
            snapshot=str(snapshot),
            mapping=str(mapping_path),
        )

        loaded = CargoRecord.objects.get(pk=15 + index)
        assert loaded.misdirected
        assert not loaded.unloaded_at_dest


@pytest.mark.django_db(transaction=True)
def test_load_snapshot_applies_mapping_transforms(tmp_path):
    snapshot = tmp_path / 'snapshot'
    table_rows = {
        table: (header.copy(), [row.copy() for row in rows])
        for table, (header, rows) in TABLE_ROWS.items()
    }
    table_rows['LOCATION'][1][0][1:3] = [' USNYC ', ' New York ']
    table_rows['CARGO'][1][0][1] = '17.25'
    table_rows['CARGO'][1][0][6] = '0'
    table_rows['CARGO'][1][0][9] = '1'
    table_rows['CARGO'][1][0][10] = ''
    table_rows['CARGO'][1][0][16] = '2026-11-07 00:40:40.322'
    table_rows['CARGO'][1][0][14] = '0'
    _snapshot(snapshot, table_rows)

    mapping = copy.deepcopy(MAPPING)
    tables = {table['target']: table for table in mapping['tables']}
    tables['location']['columns']['id'] = {'from': 'ID', 'as': 'int'}
    tables['location']['columns']['unlocode'] = {'from': 'UNLOCODE', 'as': 'trim'}
    tables['location']['columns']['name'] = {'from': 'NAME', 'as': 'trim'}
    tables['cargo']['columns']['tracking_id'] = {'from': 'TRACKING_ID', 'as': 'decimal'}
    tables['cargo']['columns']['transport_status'] = {
        'from': 'TRANSPORT_STATUS',
        'as': {'map': {'0': 'NOT_RECEIVED'}},
    }
    tables['cargo']['columns']['eta'] = {'from': 'ETA', 'as': 'null_if_empty'}
    mapping_file = tmp_path / 'mapping.yaml'
    mapping_file.write_text(yaml.safe_dump(mapping), encoding='utf-8')

    call_command('load_data_snapshot', snapshot=str(snapshot), mapping=str(mapping_file))

    location = LocationRecord.objects.get(pk=4)
    cargo = CargoRecord.objects.get(pk=15)
    assert location.unlocode == 'USNYC'
    assert location.name == 'New York'
    assert cargo.tracking_id == '17.25'
    assert cargo.transport_status == 'NOT_RECEIVED'
    assert cargo.misdirected
    assert not cargo.unloaded_at_dest
    assert cargo.eta is None
    assert cargo.calculated_at == datetime(2026, 11, 7, 0, 40, 40, 322000, tzinfo=UTC)


@pytest.mark.django_db(transaction=True)
def test_load_snapshot_rejects_invalid_boolean_transform(tmp_path):
    snapshot = tmp_path / 'snapshot'
    table_rows = {
        table: (header.copy(), [row.copy() for row in rows])
        for table, (header, rows) in TABLE_ROWS.items()
    }
    table_rows['CARGO'][1][0][9] = 'sometimes'
    _snapshot(snapshot, table_rows)
    mapping = tmp_path / 'mapping.yaml'
    mapping.write_text(yaml.safe_dump(MAPPING), encoding='utf-8')

    with pytest.raises(CommandError) as error:
        call_command('load_data_snapshot', snapshot=str(snapshot), mapping=str(mapping))
    assert str(error.value) == "not a boolean: 'sometimes'"


@pytest.mark.django_db(transaction=True)
def test_load_snapshot_rejects_unmapped_enum_value_and_rolls_back(tmp_path):
    snapshot = tmp_path / 'snapshot'
    table_rows = {
        table: (header.copy(), [row.copy() for row in rows])
        for table, (header, rows) in TABLE_ROWS.items()
    }
    table_rows['CARGO'][1][0][6] = '1'
    _snapshot(snapshot, table_rows)
    mapping = tmp_path / 'mapping.yaml'
    mapping.write_text(yaml.safe_dump(MAPPING), encoding='utf-8')

    with pytest.raises(CommandError) as error:
        call_command('load_data_snapshot', snapshot=str(snapshot), mapping=str(mapping))
    assert str(error.value) == "no mapping for value '1'"

    assert not LocationRecord.objects.exists()


@pytest.mark.django_db(transaction=True)
def test_load_snapshot_rejects_invalid_mapping_references(tmp_path):
    cases = (
        ('no_tables', 'mapping has no tables'),
        ('duplicate_target', 'mapping targets must be unique table names'),
        ('missing_primary_key', 'location: mapping must include its primary key'),
        ('unmapped_reference_column', "cargo: reference 'origin_id' is not mapped"),
        ('invalid_reference', "origin_id: invalid reference 'location'"),
        ('unmapped_reference_target', "origin_id: reference target 'unknown' is not mapped"),
        ('multi_dot_reference', "origin_id: reference target 'location.foo' is not mapped"),
        ('mismatched_reference', 'cargo.origin_id: reference does not match the model'),
        ('missing_referenced_column', 'location.missing: no referenced target column'),
    )
    for case, message in cases:
        case_dir = tmp_path / case
        case_dir.mkdir()
        snapshot = case_dir / 'snapshot'
        _snapshot(snapshot)
        mapping = copy.deepcopy(MAPPING)
        tables = mapping['tables']
        if case == 'no_tables':
            mapping['tables'] = []
        elif case == 'duplicate_target':
            tables.append(copy.deepcopy(tables[0]))
        elif case == 'missing_primary_key':
            tables[0]['columns'].pop('id')
        elif case == 'unmapped_reference_column':
            tables[2]['columns'].pop('origin_id')
        elif case == 'invalid_reference':
            tables[2]['refs']['origin_id'] = 'location'
        elif case == 'unmapped_reference_target':
            tables[2]['refs']['origin_id'] = 'unknown.id'
        elif case == 'multi_dot_reference':
            tables[2]['refs']['origin_id'] = 'location.foo.bar'
        elif case == 'mismatched_reference':
            tables[2]['refs']['origin_id'] = 'voyage.id'
        elif case == 'missing_referenced_column':
            tables[2]['refs']['origin_id'] = 'location.missing'

        mapping_file = case_dir / 'mapping.yaml'
        mapping_file.write_text(yaml.safe_dump(mapping), encoding='utf-8')

        with pytest.raises(CommandError) as error:
            call_command('load_data_snapshot', snapshot=str(snapshot), mapping=str(mapping_file))
        assert str(error.value) == message


@pytest.mark.django_db(transaction=True)
def test_load_snapshot_rejects_unknown_mapping_transform(tmp_path):
    snapshot = tmp_path / 'snapshot'
    table_rows = {
        table: (header.copy(), [row.copy() for row in rows])
        for table, (header, rows) in TABLE_ROWS.items()
    }
    table_rows['CARGO'][1][0][10] = '2026-11-15'
    _snapshot(snapshot, table_rows)
    mapping = copy.deepcopy(MAPPING)
    mapping['tables'][2]['columns']['eta'] = {'from': 'ETA', 'as': 'unknown'}
    mapping_file = tmp_path / 'mapping.yaml'
    mapping_file.write_text(yaml.safe_dump(mapping), encoding='utf-8')

    with pytest.raises(CommandError) as error:
        call_command('load_data_snapshot', snapshot=str(snapshot), mapping=str(mapping_file))
    assert str(error.value) == "unknown transform 'unknown'"


@pytest.mark.django_db(transaction=True)
def test_load_snapshot_rejects_transform_mapping_without_map_key(tmp_path):
    mapping = copy.deepcopy(MAPPING)
    mapping['tables'][2]['columns']['transport_status'] = {
        'from': 'TRANSPORT_STATUS',
        'as': {'values': {'0': 'NOT_RECEIVED'}},
    }
    mapping_path = tmp_path / 'mapping.yaml'
    mapping_path.write_text(yaml.safe_dump(mapping), encoding='utf-8')

    with pytest.raises(CommandError) as error:
        call_command(
            'load_data_snapshot',
            snapshot=str(FIXTURE_SNAPSHOT),
            mapping=str(mapping_path),
        )

    assert str(error.value) == "unknown transform {'values': {'0': 'NOT_RECEIVED'}}"


@pytest.mark.django_db(transaction=True)
def test_load_snapshot_rejects_invalid_column_definitions(tmp_path):
    for case, columns, expected in (
        ('not_a_mapping', ['id'], 'location: mapping has no columns'),
        ('empty_mapping', {}, 'location: mapping has no columns'),
        (
            'unknown_target_column',
            {'id': 'ID', 'missing': 'MISSING'},
            "location: no target column 'missing'",
        ),
        (
            'invalid_source',
            {'id': {'from': 7}},
            'id: mapping must name a source column',
        ),
    ):
        case_dir = tmp_path / case
        case_dir.mkdir()
        snapshot = case_dir / 'snapshot'
        _snapshot(snapshot)
        mapping = copy.deepcopy(MAPPING)
        mapping['tables'][0]['columns'] = columns
        mapping_path = case_dir / 'mapping.yaml'
        mapping_path.write_text(yaml.safe_dump(mapping), encoding='utf-8')

        with pytest.raises(CommandError) as error:
            call_command('load_data_snapshot', snapshot=str(snapshot), mapping=str(mapping_path))

        assert str(error.value) == expected


@pytest.mark.django_db(transaction=True)
def test_load_snapshot_preserves_date_and_timestamp_mapping_values(tmp_path):
    table_rows = {
        table: (header.copy(), [row.copy() for row in rows])
        for table, (header, rows) in TABLE_ROWS.items()
    }
    cargo = table_rows['CARGO'][1][0]
    cargo[1] = '2026-11-07T00:30:00+02:00'
    cargo[5] = '2026-11-07'
    cargo[10] = '2026-11-07T00:30:00+02:00'
    cargo[16] = '2026-11-07'
    snapshot = tmp_path / 'snapshot'
    _snapshot(snapshot, table_rows)

    mapping = copy.deepcopy(MAPPING)
    mapping['defaults']['timestamp_tz'] = 'Asia/Tokyo'
    mapping['tables'][2]['columns']['tracking_id'] = {
        'from': 'TRACKING_ID',
        'as': 'date',
    }
    mapping_path = tmp_path / 'mapping.yaml'
    mapping_path.write_text(yaml.safe_dump(mapping), encoding='utf-8')

    call_command('load_data_snapshot', snapshot=str(snapshot), mapping=str(mapping_path))

    cargo_record = CargoRecord.objects.get(pk=15)
    assert cargo_record.tracking_id == '2026-11-06'
    assert cargo_record.spec_arrival_deadline == date(2026, 11, 7)
    assert cargo_record.eta == date(2026, 11, 6)
    assert cargo_record.calculated_at == datetime(2026, 11, 6, 15, tzinfo=UTC)


@pytest.mark.django_db(transaction=True)
def test_load_snapshot_rejects_invalid_timestamp_value(tmp_path):
    table_rows = {
        table: (header.copy(), [row.copy() for row in rows])
        for table, (header, rows) in TABLE_ROWS.items()
    }
    table_rows['CARGO'][1][0][16] = 'not-a-time'
    snapshot = tmp_path / 'snapshot'
    _snapshot(snapshot, table_rows)
    mapping_path = tmp_path / 'mapping.yaml'
    mapping_path.write_text(yaml.safe_dump(MAPPING), encoding='utf-8')

    with pytest.raises(CommandError) as error:
        call_command('load_data_snapshot', snapshot=str(snapshot), mapping=str(mapping_path))

    assert str(error.value) == "not a timestamp: 'not-a-time'"


@pytest.mark.django_db(transaction=True)
def test_load_snapshot_parses_legacy_timestamp_value(tmp_path):
    cases = (
        ('fractional_offset', '2026-1-2 3:4:5.1+0000', datetime(2026, 1, 2, 3, 4, 5, 100000, tzinfo=UTC)),
        ('offset', '2026-1-2 3:4:5+0000', datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)),
        ('minute', '2026-1-2 3:4', datetime(2026, 1, 1, 18, 4, tzinfo=UTC)),
    )
    for case, timestamp, expected in cases:
        case_dir = tmp_path / case
        case_dir.mkdir()
        table_rows = {
            table: (header.copy(), [row.copy() for row in rows])
            for table, (header, rows) in TABLE_ROWS.items()
        }
        table_rows['CARGO'][1][0][16] = timestamp
        snapshot = case_dir / 'snapshot'
        _snapshot(snapshot, table_rows)
        mapping = copy.deepcopy(MAPPING)
        mapping['defaults']['timestamp_tz'] = 'Asia/Tokyo'
        mapping_path = case_dir / 'mapping.yaml'
        mapping_path.write_text(yaml.safe_dump(mapping), encoding='utf-8')

        call_command('load_data_snapshot', snapshot=str(snapshot), mapping=str(mapping_path))

        assert CargoRecord.objects.get(pk=15).calculated_at == expected


@pytest.mark.django_db(transaction=True)
def test_load_snapshot_uses_configured_and_default_null_markers(tmp_path):
    for case, marker in (('default', None), ('custom', 'NULL')):
        case_dir = tmp_path / case
        case_dir.mkdir()
        table_rows = {
            table: (header.copy(), [row.copy() for row in rows])
            for table, (header, rows) in TABLE_ROWS.items()
        }
        table_rows['CARGO'][1][0][11] = None
        table_rows['VOYAGE'][1][0][1] = ''
        snapshot = case_dir / 'snapshot'
        _snapshot(snapshot, table_rows)
        manifest_path = snapshot / 'manifest.json'
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        if marker is None:
            manifest.pop('null')
        else:
            manifest['null'] = marker
            for csv_path in snapshot.glob('*.csv'):
                csv_path.write_text(
                    csv_path.read_text(encoding='utf-8').replace(r'\N', marker),
                    encoding='utf-8',
                )
        manifest_path.write_text(json.dumps(manifest), encoding='utf-8')
        for source in table_rows:
            _refresh_manifest(snapshot, source, len(table_rows[source][1]))
        mapping_path = case_dir / 'mapping.yaml'
        mapping_path.write_text(yaml.safe_dump(MAPPING), encoding='utf-8')

        call_command('load_data_snapshot', snapshot=str(snapshot), mapping=str(mapping_path))

        assert CargoRecord.objects.get(pk=15).next_expected_handling_event_type is None
        assert VoyageRecord.objects.get(pk=9).voyage_number == ''


@pytest.mark.django_db(transaction=True)
def test_load_snapshot_reports_csv_read_errors(tmp_path, monkeypatch):
    snapshot = tmp_path / 'snapshot'
    _snapshot(snapshot)
    mapping_path = tmp_path / 'mapping.yaml'
    mapping_path.write_text(yaml.safe_dump(MAPPING), encoding='utf-8')
    original_open = Path.open

    def deny_location_csv(path, *args, **kwargs):
        if path.name == 'LOCATION.csv' and kwargs.get('mode', 'r') == 'r':
            raise PermissionError('permission denied')
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr(Path, 'open', deny_location_csv)

    with pytest.raises(CommandError) as error:
        call_command('load_data_snapshot', snapshot=str(snapshot), mapping=str(mapping_path))

    assert str(error.value) == f'{snapshot}/LOCATION.csv: permission denied'


@pytest.mark.django_db(transaction=True)
def test_load_snapshot_rejects_unregistered_target_model(tmp_path):
    mapping = copy.deepcopy(MAPPING)
    mapping['tables'][0]['target'] = 'missing_model'
    mapping_path = tmp_path / 'mapping.yaml'
    mapping_path.write_text(yaml.safe_dump(mapping), encoding='utf-8')

    with pytest.raises(CommandError) as error:
        call_command(
            'load_data_snapshot',
            snapshot=str(FIXTURE_SNAPSHOT),
            mapping=str(mapping_path),
        )

    assert str(error.value) == 'missing_model: no registered Django model for target table'


@pytest.mark.django_db(transaction=True)
def test_load_snapshot_rejects_non_nullable_forward_reference(tmp_path):
    snapshot = tmp_path / 'snapshot'
    _snapshot(snapshot)
    mapping = copy.deepcopy(MAPPING)
    tables = {table['target']: table for table in mapping['tables']}
    mapping['tables'] = [
        tables[target]
        for target in ('location', 'voyage', 'HandlingEvent', 'cargo', 'leg', 'carrier_movement')
    ]
    mapping_path = tmp_path / 'mapping.yaml'
    mapping_path.write_text(yaml.safe_dump(mapping), encoding='utf-8')

    with pytest.raises(CommandError) as error:
        call_command('load_data_snapshot', snapshot=str(snapshot), mapping=str(mapping_path))

    assert str(error.value) == 'HandlingEvent.cargo_id: a forward reference must be nullable'


@pytest.mark.django_db(transaction=True)
def test_load_snapshot_requires_postgresql(monkeypatch):
    monkeypatch.setattr(loader.connection, 'vendor', 'sqlite')

    with pytest.raises(CommandError) as error:
        call_command(
            'load_data_snapshot',
            snapshot='unused',
            mapping='unused',
        )

    assert str(error.value) == 'load_data_snapshot requires PostgreSQL'


@pytest.mark.django_db(transaction=True)
def test_load_snapshot_rejects_missing_or_non_object_mapping_files(tmp_path):
    cases = (
        (
            'missing',
            None,
            f"{tmp_path}/missing.yaml: unable to read mapping: [Errno 2] No such file or directory: '{tmp_path}/missing.yaml'",
        ),
        ('non_object', '[invalid]', f'{tmp_path}/non_object.yaml: mapping must be an object'),
    )
    for name, content, expected in cases:
        mapping_path = tmp_path / f'{name}.yaml'
        if content is not None:
            mapping_path.write_text(content, encoding='utf-8')

        with pytest.raises(CommandError) as error:
            call_command(
                'load_data_snapshot',
                snapshot=str(FIXTURE_SNAPSHOT),
                mapping=str(mapping_path),
            )

        assert str(error.value) == expected


@pytest.mark.django_db(transaction=True)
def test_load_data_snapshot_command_help_arguments_and_success_output(tmp_path, capsys):
    help_output = StringIO()
    with pytest.raises(SystemExit) as help_exit:
        call_command('load_data_snapshot', '--help', stdout=help_output)
    assert help_exit.value.code == 0
    help_text = capsys.readouterr().out
    description = next(line for line in help_text.splitlines() if 'mapping.' in line)
    assert description == 'Load a validated relational snapshot using its mapping.'

    for options, missing in (
        ({'mapping': str(FIXTURE_SNAPSHOT)}, '--snapshot'),
        ({'snapshot': str(FIXTURE_SNAPSHOT)}, '--mapping'),
    ):
        with pytest.raises(CommandError) as error:
            call_command('load_data_snapshot', **options)
        assert missing in str(error.value)

    mapping_path = tmp_path / 'mapping.yaml'
    mapping_path.write_text(yaml.safe_dump(MAPPING), encoding='utf-8')
    output = StringIO()
    call_command(
        'load_data_snapshot',
        snapshot=str(FIXTURE_SNAPSHOT),
        mapping=str(mapping_path),
        stdout=output,
    )
    assert output.getvalue().strip() == 'Loaded 7 rows across 6 mapped tables.'
