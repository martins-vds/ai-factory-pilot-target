import csv
from datetime import UTC, date, datetime, timedelta, timezone
from io import StringIO
from pathlib import Path

import pytest
import yaml
from django.core.management import call_command
from django.core.management.base import CommandError

from cargotracker.cargo.infrastructure.models import CargoRecord
from cargotracker.location.infrastructure.models import LocationRecord

FIXTURE_SNAPSHOT = Path(__file__).parent / 'fixtures' / 'DM-05C'


@pytest.mark.django_db(transaction=True)
def test_export_round_trips_fixture_rows_in_primary_key_order(tmp_path):
    mapping = {
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
        ]
    }
    mapping_path = tmp_path / 'mapping.yaml'
    mapping_path.write_text(yaml.safe_dump(mapping, sort_keys=False), encoding='utf-8')

    call_command(
        'load_data_snapshot',
        snapshot=str(FIXTURE_SNAPSHOT),
        mapping=str(mapping_path),
    )
    output = tmp_path / 'nested' / 'export'
    stdout = StringIO()
    call_command(
        'export_data_snapshot',
        mapping=str(mapping_path),
        out=str(output),
        stdout=stdout,
    )
    assert stdout.getvalue() == 'Exported 3 rows across 2 mapped tables.\n'

    with (output / 'location.csv').open(newline='', encoding='utf-8') as stream:
        reader = csv.DictReader(stream)
        assert reader.fieldnames == ['id', 'unlocode', 'name']
        assert list(reader) == [
            {'id': '101', 'unlocode': 'USNYC', 'name': 'New York'},
            {'id': '102', 'unlocode': 'NLRTM', 'name': 'Rotterdam'},
        ]

    with (output / 'voyage.csv').open(newline='', encoding='utf-8') as stream:
        reader = csv.DictReader(stream)
        assert reader.fieldnames == ['id', 'voyage_number']
        assert list(reader) == [{'id': '900', 'voyage_number': ''}]

    call_command('export_data_snapshot', mapping=str(mapping_path), out=str(output))


@pytest.mark.django_db(transaction=True)
def test_export_preserves_null_and_empty_strings_and_uses_utc_primary_key_order(tmp_path):
    location = LocationRecord.objects.create(
        id=1,
        unlocode='USNYC',
        name='New York',
    )
    CargoRecord.objects.create(
        id=20,
        tracking_id='A-20',
        origin=location,
        spec_origin=location,
        spec_destination=location,
        spec_arrival_deadline=date(2026, 1, 1),
        transport_status='NOT_RECEIVED',
        next_expected_handling_event_type='',
        misdirected=True,
        unloaded_at_dest=False,
        routing_status='NOT_ROUTED',
        calculated_at=datetime(2026, 2, 1, 12, tzinfo=timezone(timedelta(hours=2))),
    )
    CargoRecord.objects.create(
        id=10,
        tracking_id='Z-10',
        origin=location,
        spec_origin=location,
        spec_destination=location,
        spec_arrival_deadline=date(2026, 1, 2),
        transport_status='NOT_RECEIVED',
        next_expected_handling_event_type=None,
        misdirected=False,
        unloaded_at_dest=False,
        routing_status='NOT_ROUTED',
        calculated_at=datetime(2026, 2, 1, 10, tzinfo=UTC),
    )
    mapping = {
        'defaults': {'timestamp_tz': 'America/New_York'},
        'tables': [
            {
                'target': 'cargo',
                'source': 'CARGO',
                'key': ['tracking_id', 'id'],
                'columns': {
                    'id': 'ID',
                    'tracking_id': 'TRACKING_ID',
                    'next_expected_handling_event_type': 'NEXT_EXPECTED_HANDLING_EVENT_TYPE',
                    'spec_arrival_deadline': 'SPEC_ARRIVAL_DEADLINE',
                    'misdirected': 'MISDIRECTED',
                    'calculated_at': {'from': 'CALCULATED_AT', 'as': 'timestamp'},
                },
            }
        ],
    }
    mapping_path = tmp_path / 'mapping.yaml'
    mapping_path.write_text(yaml.safe_dump(mapping, sort_keys=False), encoding='utf-8')
    output = tmp_path / 'export'

    call_command('export_data_snapshot', mapping=str(mapping_path), out=str(output))

    with (output / 'cargo.csv').open(newline='', encoding='utf-8') as stream:
        reader = csv.DictReader(stream)
        assert reader.fieldnames == [
            'id',
            'tracking_id',
            'next_expected_handling_event_type',
            'spec_arrival_deadline',
            'misdirected',
            'calculated_at',
        ]
        assert list(reader) == [
            {
                'id': '10',
                'tracking_id': 'Z-10',
                'next_expected_handling_event_type': r'\N',
                'spec_arrival_deadline': '2026-01-02',
                'misdirected': 'false',
                'calculated_at': '2026-02-01T10:00:00+00:00',
            },
            {
                'id': '20',
                'tracking_id': 'A-20',
                'next_expected_handling_event_type': '',
                'spec_arrival_deadline': '2026-01-01',
                'misdirected': 'true',
                'calculated_at': '2026-02-01T10:00:00+00:00',
            },
        ]


def test_export_command_help_and_required_arguments(capsys):
    with pytest.raises(SystemExit) as exit:
        call_command('export_data_snapshot', '--help')
    assert exit.value.code == 0
    help_output = capsys.readouterr().out
    assert 'Export mapped target tables as a relational snapshot.' in help_output
    assert '--mapping MAPPING' in help_output
    assert '--out OUT' in help_output

    for options in ({'out': 'out'}, {'mapping': 'mapping.yaml'}):
        with pytest.raises(CommandError):
            call_command('export_data_snapshot', **options)


@pytest.mark.django_db(transaction=True)
def test_export_rejects_invalid_mappings_at_command_boundary(tmp_path):
    location = {
        'target': 'location',
        'source': 'LOCATION',
        'key': ['id'],
        'columns': {'id': 'ID', 'unlocode': 'UNLOCODE', 'name': 'NAME'},
    }
    cases = (
        ({}, 'mapping has no tables'),
        ({'tables': []}, 'mapping has no tables'),
        ({'tables': [location, location]}, 'mapping targets must be unique table names'),
        (
            {'tables': [{'target': 'unknown', 'key': ['id'], 'columns': {'id': 'ID'}}]},
            'unknown: no registered Django model for target table',
        ),
        (
            {'tables': [{'target': 'location', 'key': ['id'], 'columns': {}}]},
            'location: mapping has no columns',
        ),
        (
            {
                'tables': [
                    {'target': 'location', 'key': ['unknown'], 'columns': {'unknown': 'UNKNOWN'}}
                ]
            },
            "location: no target column 'unknown'",
        ),
        (
            {'tables': [{'target': 'location', 'key': [], 'columns': {'id': 'ID'}}]},
            'location: mapping key must name mapped target columns',
        ),
        (
            {'tables': [{'target': 'location', 'key': ['name'], 'columns': {'name': 'NAME'}}]},
            'location: mapping key must include the primary key',
        ),
        (
            {
                'defaults': {'timestamp_tz': 'Not/A_Timezone'},
                'tables': [location],
            },
            "unknown timestamp timezone 'Not/A_Timezone'",
        ),
    )
    for index, (mapping, expected) in enumerate(cases):
        mapping_path = tmp_path / f'mapping-{index}.yaml'
        mapping_path.write_text(yaml.safe_dump(mapping, sort_keys=False), encoding='utf-8')
        with pytest.raises(CommandError) as error:
            call_command(
                'export_data_snapshot',
                mapping=str(mapping_path),
                out=str(tmp_path / f'out-{index}'),
            )
        assert str(error.value) == expected

    non_object_mapping = tmp_path / 'non-object.yaml'
    non_object_mapping.write_text('[]', encoding='utf-8')
    with pytest.raises(CommandError) as error:
        call_command(
            'export_data_snapshot',
            mapping=str(non_object_mapping),
            out=str(tmp_path / 'non-object-out'),
        )
    assert str(error.value) == f'{non_object_mapping}: mapping must be an object'

    empty_mapping = tmp_path / 'empty.yaml'
    empty_mapping.write_text('', encoding='utf-8')
    with pytest.raises(CommandError) as error:
        call_command(
            'export_data_snapshot',
            mapping=str(empty_mapping),
            out=str(tmp_path / 'empty-out'),
        )
    assert str(error.value) == 'mapping has no tables'

    missing_mapping = tmp_path / 'missing.yaml'
    with pytest.raises(CommandError) as error:
        call_command(
            'export_data_snapshot',
            mapping=str(missing_mapping),
            out=str(tmp_path / 'missing-out'),
        )
    assert str(error.value).startswith(f'{missing_mapping}: unable to read mapping:')


@pytest.mark.django_db(transaction=True)
def test_export_reports_unwritable_output_paths(tmp_path):
    mapping = {
        'tables': [
            {
                'target': 'location',
                'source': 'LOCATION',
                'key': ['id'],
                'columns': {'id': 'ID', 'unlocode': 'UNLOCODE', 'name': 'NAME'},
            }
        ]
    }
    mapping_path = tmp_path / 'mapping.yaml'
    mapping_path.write_text(yaml.safe_dump(mapping, sort_keys=False), encoding='utf-8')

    output_file = tmp_path / 'output-file'
    output_file.write_text('not a directory', encoding='utf-8')
    with pytest.raises(CommandError) as error:
        call_command(
            'export_data_snapshot',
            mapping=str(mapping_path),
            out=str(output_file),
        )
    assert str(error.value).startswith(f'{output_file}:')

    output = tmp_path / 'output'
    output.mkdir()
    (output / 'location.csv').mkdir()
    with pytest.raises(CommandError) as error:
        call_command('export_data_snapshot', mapping=str(mapping_path), out=str(output))
    assert str(error.value).startswith(f'{output / "location.csv"}:')
