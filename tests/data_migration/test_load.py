import copy
import csv
import hashlib
import json
import shutil
from datetime import UTC, date, datetime
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
        ('missing_manifest', 'no manifest.json'),
        ('invalid_manifest', 'invalid manifest:'),
        ('invalid_table_list', 'tables must be an object'),
        ('missing_table_entry', 'CARGO: table is not listed'),
        ('missing_csv', 'LEG.csv: missing'),
        ('hash_mismatch', 'LOCATION: sha256 differs'),
        ('empty_file', r'empty file \(a header row is required\)'),
        ('duplicate_header', 'duplicate columns in header'),
        ('wrong_field_count', 'fields, header has'),
        ('row_count_mismatch', 'CARGO: 1 rows, manifest says 2'),
        ('missing_mapped_column', r'LOCATION: no column\(s\) MISSING in its CSV header'),
    )
    for case, message in cases:
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

        mapping_path = case_dir / 'mapping.yaml'
        mapping_path.write_text(yaml.safe_dump(mapping), encoding='utf-8')
        with pytest.raises(CommandError, match=message):
            call_command(
                'load_data_snapshot',
                snapshot=str(snapshot),
                mapping=str(mapping_path),
            )


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
def test_load_snapshot_rejects_unknown_timestamp_timezone(tmp_path):
    mapping = copy.deepcopy(MAPPING)
    mapping['defaults']['timestamp_tz'] = 'Not/A_Timezone'
    mapping_path = tmp_path / 'mapping.yaml'
    mapping_path.write_text(yaml.safe_dump(mapping), encoding='utf-8')

    with pytest.raises(CommandError, match="unknown timestamp timezone 'Not/A_Timezone'"):
        call_command(
            'load_data_snapshot',
            snapshot=str(FIXTURE_SNAPSHOT),
            mapping=str(mapping_path),
        )


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

    with pytest.raises(CommandError, match='not a boolean'):
        call_command('load_data_snapshot', snapshot=str(snapshot), mapping=str(mapping))


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

    with pytest.raises(CommandError, match='no mapping for value'):
        call_command('load_data_snapshot', snapshot=str(snapshot), mapping=str(mapping))

    assert not LocationRecord.objects.exists()


@pytest.mark.django_db(transaction=True)
def test_load_snapshot_rejects_invalid_mapping_references(tmp_path):
    cases = (
        ('no_tables', 'mapping has no tables'),
        ('duplicate_target', 'mapping targets must be unique table names'),
        ('missing_primary_key', 'mapping must include its primary key'),
        ('unmapped_reference_column', "reference 'origin_id' is not mapped"),
        ('invalid_reference', "invalid reference 'location'"),
        ('unmapped_reference_target', "reference target 'unknown' is not mapped"),
        ('mismatched_reference', 'reference does not match the model'),
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
        elif case == 'mismatched_reference':
            tables[2]['refs']['origin_id'] = 'voyage.id'
        elif case == 'missing_referenced_column':
            tables[2]['refs']['origin_id'] = 'location.missing'

        mapping_file = case_dir / 'mapping.yaml'
        mapping_file.write_text(yaml.safe_dump(mapping), encoding='utf-8')

        with pytest.raises(CommandError, match=message):
            call_command('load_data_snapshot', snapshot=str(snapshot), mapping=str(mapping_file))


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

    with pytest.raises(CommandError, match="unknown transform 'unknown'"):
        call_command('load_data_snapshot', snapshot=str(snapshot), mapping=str(mapping_file))
