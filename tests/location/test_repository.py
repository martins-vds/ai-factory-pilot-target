import pytest
from django.db import connection

from cargotracker.location.domain.location import Location
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.location.infrastructure.models import LocationRecord
from cargotracker.location.infrastructure.repository import DjangoLocationRepository


@pytest.mark.django_db
def test_repository_round_trips_source_location_fields():
    LocationRecord.objects.create(unlocode='USNYC', name='New York')
    repository = DjangoLocationRepository()

    assert repository.find(UnLocode('usnyc')) == Location(UnLocode('USNYC'), 'New York')
    assert repository.find_all() == [Location(UnLocode('USNYC'), 'New York')]


@pytest.mark.django_db
def test_location_schema_uses_source_table_and_columns():
    with connection.cursor() as cursor:
        columns = connection.introspection.get_table_description(cursor, 'location')

    assert [column.name for column in columns] == ['id', 'unlocode', 'name']


@pytest.mark.django_db
def test_repository_missing_location_raises_model_does_not_exist():
    with pytest.raises(LocationRecord.DoesNotExist):
        DjangoLocationRepository().find(UnLocode('USNYC'))
