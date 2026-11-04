from datetime import UTC, date, datetime

import pytest
from django.core.management import call_command
from django.db import connection
from django.db.migrations.executor import MigrationExecutor

from cargotracker.cargo.infrastructure.models import CargoRecord
from cargotracker.location.infrastructure.models import LocationRecord


@pytest.mark.django_db(transaction=True)
def test_handling_event_timestamp_migration_preserves_legacy_dates_at_utc_midnight():
    assert connection.vendor == 'postgresql'
    latest_migrations = MigrationExecutor(connection).loader.graph.leaf_nodes()
    previous_migration = [('handling', '0002_registration_attempt')]
    target_migration = [('handling', '0003_preserve_handling_event_instants')]

    try:
        call_command('seed_sample_data')
        cargo = CargoRecord.objects.get(tracking_id='ABC123')
        location = LocationRecord.objects.get(unlocode='USNYC')

        MigrationExecutor(connection).migrate(previous_migration)
        old_apps = MigrationExecutor(connection).loader.project_state(previous_migration).apps
        old_event_record = old_apps.get_model('handling', 'HandlingEventRecord').objects.create(
            cargo_id=cargo.pk,
            location_id=location.pk,
            event_type='RECEIVE',
            completion_time=date(2026, 11, 3),
            registration_time=date(2026, 11, 4),
        )

        with connection.cursor() as cursor:
            cursor.execute("SET TIME ZONE 'America/Los_Angeles'")
            cursor.execute('SHOW TIME ZONE')
            assert cursor.fetchone()[0] == 'America/Los_Angeles'

        MigrationExecutor(connection).migrate(target_migration)
        with connection.cursor() as cursor:
            cursor.execute("SET TIME ZONE 'UTC'")
        new_apps = MigrationExecutor(connection).loader.project_state(target_migration).apps
        migrated_record = new_apps.get_model('handling', 'HandlingEventRecord').objects.get(
            pk=old_event_record.pk
        )

        assert migrated_record.completion_time == datetime(2026, 11, 3, tzinfo=UTC)
        assert migrated_record.registration_time == datetime(2026, 11, 4, tzinfo=UTC)
    finally:
        MigrationExecutor(connection).migrate(latest_migrations)
        with connection.cursor() as cursor:
            cursor.execute("SET TIME ZONE 'UTC'")
