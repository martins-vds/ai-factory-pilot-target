from datetime import UTC, date, datetime, timedelta, timezone

import pytest
from django.db import connection, models

from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.cargo.infrastructure.models import CargoRecord
from cargotracker.cargo.infrastructure.repository import DjangoCargoRepository
from cargotracker.handling.domain.handling_event import HandlingEvent, HandlingEventType
from cargotracker.handling.infrastructure.models import HandlingEventRecord
from cargotracker.handling.infrastructure.repository import DjangoHandlingEventRepository
from cargotracker.location.domain.location import Location
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.location.infrastructure.models import LocationRecord
from cargotracker.voyage.domain.schedule import Schedule
from cargotracker.voyage.domain.voyage import Voyage
from cargotracker.voyage.domain.voyage_number import VoyageNumber
from cargotracker.voyage.infrastructure.models import VoyageRecord


def _cargo_record(tracking_id='ABC123'):
    origin = LocationRecord.objects.create(unlocode='USNYC', name='New York')
    destination = LocationRecord.objects.create(unlocode='FIHEL', name='Helsinki')
    cargo = CargoRecord.objects.create(
        tracking_id=tracking_id,
        origin=origin,
        spec_origin=origin,
        spec_destination=destination,
        spec_arrival_deadline=date(2026, 11, 12),
        transport_status='NOT_RECEIVED',
        misdirected=False,
        unloaded_at_dest=False,
        routing_status='NOT_ROUTED',
        calculated_at=datetime(2026, 11, 1, tzinfo=UTC),
    )
    return cargo, origin


@pytest.mark.django_db
def test_handling_event_schema_matches_source_jpa_mapping():
    with connection.cursor() as cursor:
        columns = [
            column.name
            for column in connection.introspection.get_table_description(cursor, 'HandlingEvent')
        ]

    assert set(columns) == {
        'id',
        'type',
        'voyage_id',
        'location_id',
        'completionTime',
        'registration',
        'cargo_id',
    }
    assert HandlingEventRecord._meta.db_table == 'HandlingEvent'
    assert HandlingEventRecord._meta.get_field('event_type').db_column == 'type'
    assert HandlingEventRecord._meta.get_field('event_type').max_length == 255
    assert HandlingEventRecord._meta.get_field('completion_time').db_column == 'completionTime'
    assert HandlingEventRecord._meta.get_field('completion_time').get_internal_type() == (
        'DateTimeField'
    )
    assert HandlingEventRecord._meta.get_field('registration_time').db_column == 'registration'
    assert (
        HandlingEventRecord._meta.get_field('registration_time').get_internal_type()
        == 'DateTimeField'
    )
    for field_name, db_column, related_model in (
        ('cargo', 'cargo_id', CargoRecord),
        ('location', 'location_id', LocationRecord),
        ('voyage', 'voyage_id', VoyageRecord),
    ):
        field = HandlingEventRecord._meta.get_field(field_name)
        assert field.db_column == db_column
        assert field.remote_field.model is related_model
        assert field.remote_field.on_delete is models.PROTECT
    assert HandlingEventRecord._meta.get_field('voyage').null


@pytest.mark.django_db
def test_repository_reads_and_orders_deduplicated_handling_history():
    cargo, origin = _cargo_record()
    voyage = VoyageRecord.objects.create(voyage_number='CM001')
    HandlingEventRecord.objects.create(
        cargo=cargo,
        location=origin,
        voyage=voyage,
        event_type=HandlingEventType.LOAD,
        completion_time=datetime(2026, 11, 3, tzinfo=UTC),
        registration_time=datetime(2026, 11, 3, tzinfo=UTC),
    )
    HandlingEventRecord.objects.create(
        cargo=cargo,
        location=origin,
        event_type=HandlingEventType.RECEIVE,
        completion_time=datetime(2026, 11, 1, tzinfo=UTC),
        registration_time=datetime(2026, 11, 1, tzinfo=UTC),
    )
    HandlingEventRecord.objects.create(
        cargo=cargo,
        location=origin,
        event_type=HandlingEventType.RECEIVE,
        completion_time=datetime(2026, 11, 1, tzinfo=UTC),
        registration_time=datetime(2026, 11, 2, tzinfo=UTC),
    )

    history = DjangoHandlingEventRepository().lookup_handling_history_of_cargo(TrackingId('ABC123'))

    assert [event.event_type for event in history.events] == [
        HandlingEventType.RECEIVE,
        HandlingEventType.LOAD,
    ]
    assert history.events[0].cargo.tracking_id == TrackingId('ABC123')
    assert history.events[0].location == Location(UnLocode('USNYC'), 'New York')
    assert history.events[0].completion_time == datetime(2026, 11, 1, tzinfo=UTC)
    assert history.events[0].registration_time == datetime(2026, 11, 2, tzinfo=UTC)
    assert history.events[1].voyage == Voyage(VoyageNumber('CM001'), Schedule.EMPTY)
    assert history.most_recent_event == history.events[1]


@pytest.mark.django_db
def test_repository_stores_event_relations_and_completion_dates():
    cargo_record, origin = _cargo_record()
    voyage_record = VoyageRecord.objects.create(voyage_number='CM001')
    cargo = DjangoCargoRepository().find(TrackingId('ABC123'))
    event = HandlingEvent(
        cargo,
        datetime(2026, 11, 4, tzinfo=UTC),
        datetime(2026, 11, 5, tzinfo=UTC),
        HandlingEventType.LOAD,
        Location(UnLocode('USNYC'), 'New York'),
        Voyage(VoyageNumber('CM001'), Schedule.EMPTY),
    )

    DjangoHandlingEventRepository().store(event)

    record = HandlingEventRecord.objects.get()
    assert record.cargo == cargo_record
    assert record.location == origin
    assert record.voyage == voyage_record
    assert record.completion_time == datetime(2026, 11, 4, tzinfo=UTC)
    assert record.registration_time == datetime(2026, 11, 5, tzinfo=UTC)


@pytest.mark.parametrize('operation', ['store', 'upsert'])
@pytest.mark.django_db
def test_repository_preserves_aware_completion_and_registration_instants(operation):
    _, origin = _cargo_record()
    cargo = DjangoCargoRepository().find(TrackingId('ABC123'))
    completion_time = datetime(
        2026, 11, 4, 13, 15, 16, 123456, tzinfo=timezone(timedelta(hours=2))
    )
    registration_time = datetime(
        2026, 11, 4, 14, 17, 18, 654321, tzinfo=timezone(timedelta(hours=2))
    )
    event = HandlingEvent(
        cargo,
        completion_time,
        registration_time,
        HandlingEventType.RECEIVE,
        Location(UnLocode('USNYC'), 'New York'),
        None,
    )

    getattr(DjangoHandlingEventRepository(), operation)(event)

    expected_completion = datetime(2026, 11, 4, 11, 15, 16, 123456, tzinfo=UTC)
    expected_registration = datetime(2026, 11, 4, 12, 17, 18, 654321, tzinfo=UTC)
    record = HandlingEventRecord.objects.get(cargo__tracking_id='ABC123')
    history = DjangoHandlingEventRepository().lookup_handling_history_of_cargo(
        TrackingId('ABC123')
    )

    assert record.location == origin
    assert record.completion_time == expected_completion
    assert record.registration_time == expected_registration
    assert history.events[0].completion_time == expected_completion
    assert history.events[0].registration_time == expected_registration


@pytest.mark.django_db
def test_repository_orders_same_day_events_by_instants_before_persisted_id():
    cargo, origin = _cargo_record()
    late_registration = datetime(2026, 11, 3, 12, 30, tzinfo=UTC)
    early_registration = datetime(2026, 11, 3, 12, 15, tzinfo=UTC)
    equal_completion = datetime(2026, 11, 3, 10, 0, tzinfo=UTC)
    later_completion = datetime(2026, 11, 3, 11, 0, tzinfo=UTC)
    later_registration_record = HandlingEventRecord.objects.create(
        cargo=cargo,
        location=origin,
        event_type=HandlingEventType.RECEIVE,
        completion_time=equal_completion,
        registration_time=late_registration,
    )
    earlier_registration_record = HandlingEventRecord.objects.create(
        cargo=cargo,
        location=origin,
        event_type=HandlingEventType.CUSTOMS,
        completion_time=equal_completion,
        registration_time=early_registration,
    )
    later_completion_record = HandlingEventRecord.objects.create(
        cargo=cargo,
        location=origin,
        event_type=HandlingEventType.CLAIM,
        completion_time=later_completion,
        registration_time=datetime(2026, 11, 3, 9, 0, tzinfo=UTC),
    )

    history = DjangoHandlingEventRepository().lookup_handling_history_of_cargo(
        TrackingId('ABC123')
    )

    assert later_registration_record.pk < earlier_registration_record.pk
    assert [event.id for event in history.events] == [
        earlier_registration_record.pk,
        later_registration_record.pk,
        later_completion_record.pk,
    ]
