import pytest
from django.db import connection
from django.utils import timezone

from cargotracker.location.infrastructure.models import LocationRecord
from cargotracker.voyage.domain.schedule import Schedule
from cargotracker.voyage.domain.voyage import Voyage
from cargotracker.voyage.domain.voyage_number import VoyageNumber
from cargotracker.voyage.infrastructure.models import CarrierMovementRecord, VoyageRecord
from cargotracker.voyage.infrastructure.repository import DjangoVoyageRepository


@pytest.mark.django_db
def test_repository_finds_voyage_by_number():
    VoyageRecord.objects.create(voyage_number='CM001')

    assert DjangoVoyageRepository().find(VoyageNumber('CM001')) == Voyage(
        VoyageNumber('CM001'), Schedule.EMPTY
    )


@pytest.mark.django_db
def test_repository_returns_all_voyages_ordered_by_number():
    VoyageRecord.objects.create(voyage_number='CM002')
    VoyageRecord.objects.create(voyage_number='CM001')

    assert DjangoVoyageRepository().find_all() == [
        Voyage(VoyageNumber('CM001'), Schedule.EMPTY),
        Voyage(VoyageNumber('CM002'), Schedule.EMPTY),
    ]


@pytest.mark.django_db
def test_repository_missing_voyage_raises_model_does_not_exist():
    with pytest.raises(VoyageRecord.DoesNotExist):
        DjangoVoyageRepository().find(VoyageNumber('CM001'))


@pytest.mark.django_db
def test_voyage_schema_uses_source_table_and_columns():
    with connection.cursor() as cursor:
        description = connection.introspection.get_table_description(cursor, 'voyage')

    columns = {column.name: column for column in description}
    assert VoyageRecord._meta.db_table == 'voyage'
    assert VoyageRecord._meta.get_field('voyage_number').max_length == 255
    assert list(columns) == ['id', 'voyage_number']
    assert columns['voyage_number'].display_size == 255


@pytest.mark.django_db
def test_carrier_movement_schema_preserves_source_columns_and_references():
    with connection.cursor() as cursor:
        description = connection.introspection.get_table_description(cursor, 'carrier_movement')
        constraints = connection.introspection.get_constraints(cursor, 'carrier_movement')

    assert CarrierMovementRecord._meta.db_table == 'carrier_movement'
    assert {column.name for column in description} == {
        'id',
        'arrival_time',
        'departure_time',
        'arrival_location_id',
        'departure_location_id',
        'voyage_id',
    }
    assert {
        tuple(constraint['columns'])
        for constraint in constraints.values()
        if constraint.get('primary_key')
    } == {('id',)}
    assert {
        tuple(constraint['columns']): constraint['foreign_key']
        for constraint in constraints.values()
        if constraint.get('foreign_key')
    } == {
        ('arrival_location_id',): ('location', 'id'),
        ('departure_location_id',): ('location', 'id'),
        ('voyage_id',): ('voyage', 'id'),
    }

    departure = LocationRecord.objects.create(unlocode='DEHAM', name='Hamburg')
    arrival = LocationRecord.objects.create(unlocode='NLRTM', name='Rotterdam')
    voyage = VoyageRecord.objects.create(voyage_number='CM001')
    movement = CarrierMovementRecord.objects.create(
        arrival_time=timezone.now(),
        departure_time=timezone.now(),
        arrival_location=arrival,
        departure_location=departure,
        voyage=voyage,
    )

    saved_movement = CarrierMovementRecord.objects.select_related(
        'arrival_location', 'departure_location', 'voyage'
    ).get(pk=movement.pk)
    assert saved_movement.arrival_location == arrival
    assert saved_movement.departure_location == departure
    assert saved_movement.voyage == voyage
