from datetime import datetime, timedelta, timezone

import pytest

from cargotracker.location.domain.location import Location
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.voyage.domain.carrier_movement import CarrierMovement
from cargotracker.voyage.domain.schedule import Schedule
from cargotracker.voyage.domain.voyage import Voyage
from cargotracker.voyage.domain.voyage_builder import VoyageBuilder
from cargotracker.voyage.domain.voyage_number import VoyageNumber


def test_voyage_number_is_an_immutable_value_object():
    number = VoyageNumber('CM001')

    assert number == VoyageNumber('CM001')
    assert hash(number) == hash(VoyageNumber('CM001'))
    assert number.value == 'CM001'
    assert str(number) == 'CM001'

    with pytest.raises(AttributeError):
        number.value = 'CM002'


def test_voyage_number_rejects_non_string_values():
    with pytest.raises(TypeError, match='A voyage number must be a string'):
        VoyageNumber(None)


def test_voyage_builder_chains_movements_and_normalizes_times_to_utc():
    new_york = Location(UnLocode('USNYC'), 'New York')
    rotterdam = Location(UnLocode('NLRTM'), 'Rotterdam')
    helsinki = Location(UnLocode('FIHEL'), 'Helsinki')
    builder = VoyageBuilder(VoyageNumber('CM001'), new_york)

    result = builder.add_movement(
        rotterdam,
        datetime(2026, 11, 1, 12, tzinfo=timezone(timedelta(hours=2))),
        datetime(2026, 11, 2, 8, tzinfo=timezone.utc),
    )
    result.add_movement(
        helsinki,
        datetime(2026, 11, 2, 10, tzinfo=timezone.utc),
        datetime(2026, 11, 3, 10, tzinfo=timezone.utc),
    )
    voyage = builder.build()

    assert voyage.voyage_number == VoyageNumber('CM001')
    assert voyage.schedule.carrier_movements == (
        CarrierMovement(
            new_york,
            rotterdam,
            datetime(2026, 11, 1, 10, tzinfo=timezone.utc),
            datetime(2026, 11, 2, 8, tzinfo=timezone.utc),
        ),
        CarrierMovement(
            rotterdam,
            helsinki,
            datetime(2026, 11, 2, 10, tzinfo=timezone.utc),
            datetime(2026, 11, 3, 10, tzinfo=timezone.utc),
        ),
    )
    assert voyage == Voyage(VoyageNumber('CM001'), voyage.schedule)


def test_voyage_builder_requires_a_movement_to_build_a_schedule():
    location = Location(UnLocode('USNYC'), 'New York')

    with pytest.raises(ValueError, match='A voyage schedule must contain at least one movement'):
        VoyageBuilder(VoyageNumber('CM001'), location).build()


def test_voyage_without_schedule_has_an_empty_sentinel():
    assert Voyage.NONE.voyage_number == VoyageNumber('')
    assert Voyage.NONE.schedule == Schedule.EMPTY
