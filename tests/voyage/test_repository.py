import pytest
from django.db import connection

from cargotracker.voyage.domain.schedule import Schedule
from cargotracker.voyage.domain.voyage import Voyage
from cargotracker.voyage.domain.voyage_number import VoyageNumber
from cargotracker.voyage.infrastructure.models import VoyageRecord
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
