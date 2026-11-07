import csv
from datetime import UTC, date, datetime, timedelta, timezone
from pathlib import Path

import pytest
import yaml
from django.core.management import call_command

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
            }
        ]
    }
    mapping_path = tmp_path / 'mapping.yaml'
    mapping_path.write_text(yaml.safe_dump(mapping, sort_keys=False), encoding='utf-8')

    call_command(
        'load_data_snapshot',
        snapshot=str(FIXTURE_SNAPSHOT),
        mapping=str(mapping_path),
    )
    output = tmp_path / 'export'
    call_command('export_data_snapshot', mapping=str(mapping_path), out=str(output))

    with (output / 'location.csv').open(newline='', encoding='utf-8') as stream:
        reader = csv.DictReader(stream)
        assert reader.fieldnames == ['id', 'unlocode', 'name']
        assert list(reader) == [
            {'id': '101', 'unlocode': 'USNYC', 'name': 'New York'},
            {'id': '102', 'unlocode': 'NLRTM', 'name': 'Rotterdam'},
        ]


@pytest.mark.django_db(transaction=True)
def test_export_preserves_null_and_empty_strings_and_uses_utc_primary_key_order(tmp_path):
    location = LocationRecord.objects.create(
        id=1,
        unlocode='USNYC',
        name='New York',
    )
    CargoRecord.objects.create(
        id=20,
        tracking_id='EXPORT-20',
        origin=location,
        spec_origin=location,
        spec_destination=location,
        spec_arrival_deadline=date(2026, 1, 1),
        transport_status='NOT_RECEIVED',
        next_expected_handling_event_type='',
        misdirected=False,
        unloaded_at_dest=False,
        routing_status='NOT_ROUTED',
        calculated_at=datetime(2026, 2, 1, 12, tzinfo=timezone(timedelta(hours=2))),
    )
    CargoRecord.objects.create(
        id=10,
        tracking_id='EXPORT-10',
        origin=location,
        spec_origin=location,
        spec_destination=location,
        spec_arrival_deadline=date(2026, 1, 1),
        transport_status='NOT_RECEIVED',
        next_expected_handling_event_type=None,
        misdirected=False,
        unloaded_at_dest=False,
        routing_status='NOT_ROUTED',
        calculated_at=datetime(2026, 2, 1, 10, tzinfo=UTC),
    )
    mapping = {
        'tables': [
            {
                'target': 'cargo',
                'source': 'CARGO',
                'key': ['id'],
                'columns': {
                    'id': 'ID',
                    'next_expected_handling_event_type': 'NEXT_EXPECTED_HANDLING_EVENT_TYPE',
                    'calculated_at': {'from': 'CALCULATED_AT', 'as': 'timestamp'},
                },
            }
        ]
    }
    mapping_path = tmp_path / 'mapping.yaml'
    mapping_path.write_text(yaml.safe_dump(mapping, sort_keys=False), encoding='utf-8')
    output = tmp_path / 'export'

    call_command('export_data_snapshot', mapping=str(mapping_path), out=str(output))

    with (output / 'cargo.csv').open(newline='', encoding='utf-8') as stream:
        reader = csv.DictReader(stream)
        assert reader.fieldnames == ['id', 'next_expected_handling_event_type', 'calculated_at']
        assert list(reader) == [
            {
                'id': '10',
                'next_expected_handling_event_type': r'\N',
                'calculated_at': '2026-02-01T10:00:00+00:00',
            },
            {
                'id': '20',
                'next_expected_handling_event_type': '',
                'calculated_at': '2026-02-01T10:00:00+00:00',
            },
        ]
