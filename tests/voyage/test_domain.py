from datetime import UTC, datetime, timedelta, timezone

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
    with pytest.raises(TypeError) as error:
        VoyageNumber(None)

    assert str(error.value) == 'A voyage number must be a string'


def test_voyage_builder_chains_movements_and_normalizes_times_to_utc():
    new_york = Location(UnLocode('USNYC'), 'New York')
    rotterdam = Location(UnLocode('NLRTM'), 'Rotterdam')
    helsinki = Location(UnLocode('FIHEL'), 'Helsinki')
    builder = VoyageBuilder(VoyageNumber('CM001'), new_york)

    result = builder.add_movement(
        rotterdam,
        datetime(2026, 11, 1, 12, tzinfo=timezone(timedelta(hours=2))),
        datetime(2026, 11, 2, 8, tzinfo=UTC),
    )
    result.add_movement(
        helsinki,
        datetime(2026, 11, 2, 10, tzinfo=UTC),
        datetime(2026, 11, 3, 10, tzinfo=UTC),
    )
    voyage = builder.build()
    assert voyage.voyage_number == VoyageNumber('CM001')
    first, second = voyage.schedule.carrier_movements
    assert (
        first.departure_location,
        first.arrival_location,
        first.departure_time,
        first.arrival_time,
    ) == (
        new_york,
        rotterdam,
        datetime(2026, 11, 1, 10, tzinfo=UTC),
        datetime(2026, 11, 2, 8, tzinfo=UTC),
    )
    assert (
        second.departure_location,
        second.arrival_location,
        second.departure_time,
        second.arrival_time,
    ) == (
        rotterdam,
        helsinki,
        datetime(2026, 11, 2, 10, tzinfo=UTC),
        datetime(2026, 11, 3, 10, tzinfo=UTC),
    )
    assert voyage == Voyage(VoyageNumber('CM001'), voyage.schedule)

    assert str(voyage) == 'Voyage CM001'
    assert voyage == Voyage(VoyageNumber('CM001'), Schedule.EMPTY)
    assert voyage != Voyage(VoyageNumber('CM002'), voyage.schedule)
    assert voyage != object()

    with pytest.raises(AttributeError):
        voyage.schedule = Schedule.EMPTY


def test_carrier_movement_validates_inputs_and_is_immutable():
    new_york = Location(UnLocode('USNYC'), 'New York')
    rotterdam = Location(UnLocode('NLRTM'), 'Rotterdam')
    departure = datetime(2026, 11, 1, 10, tzinfo=UTC)
    arrival = datetime(2026, 11, 2, 10, tzinfo=UTC)

    with pytest.raises(TypeError) as error:
        CarrierMovement(None, rotterdam, departure, arrival)

    assert str(error.value) == 'A carrier movement requires departure and arrival locations'

    with pytest.raises(TypeError) as error:
        CarrierMovement(new_york, rotterdam, None, arrival)

    assert str(error.value) == 'A carrier movement time must be a datetime'

    movement = CarrierMovement(new_york, rotterdam, departure, arrival)
    with pytest.raises(AttributeError):
        movement.departure_time = arrival


def test_carrier_movement_treats_naive_times_as_utc():
    location = Location(UnLocode('USNYC'), 'New York')
    departure = datetime(2026, 11, 1, 10)
    arrival = datetime(2026, 11, 2, 10)

    movement = CarrierMovement(location, location, departure, arrival)

    assert movement.departure_time == datetime(2026, 11, 1, 10, tzinfo=UTC)
    assert movement.arrival_time == datetime(2026, 11, 2, 10, tzinfo=UTC)


def test_schedule_copies_movements_into_an_immutable_tuple():
    new_york = Location(UnLocode('USNYC'), 'New York')
    rotterdam = Location(UnLocode('NLRTM'), 'Rotterdam')
    movement = CarrierMovement(
        new_york,
        rotterdam,
        datetime(2026, 11, 1, 10, tzinfo=UTC),
        datetime(2026, 11, 2, 10, tzinfo=UTC),
    )
    movements = [movement]
    schedule = Schedule(movements)

    movements.clear()
    assert schedule.carrier_movements == (movement,)

    with pytest.raises(TypeError) as error:
        Schedule([object()])

    assert str(error.value) == 'A schedule requires carrier movements'
    with pytest.raises(AttributeError):
        schedule.carrier_movements = ()


def test_voyage_validates_its_number_and_schedule():
    with pytest.raises(TypeError) as error:
        Voyage(None, Schedule.EMPTY)

    assert str(error.value) == 'A voyage requires a voyage number'

    with pytest.raises(TypeError) as error:
        Voyage(VoyageNumber('CM001'), None)

    assert str(error.value) == 'A voyage requires a schedule'


def test_voyage_builder_requires_a_movement_to_build_a_schedule():
    location = Location(UnLocode('USNYC'), 'New York')

    with pytest.raises(ValueError) as error:
        VoyageBuilder(VoyageNumber('CM001'), location).build()

    assert str(error.value) == 'A voyage schedule must contain at least one movement'


def test_voyage_builder_validates_its_initial_inputs():
    location = Location(UnLocode('USNYC'), 'New York')

    with pytest.raises(TypeError) as error:
        VoyageBuilder(None, location)

    assert str(error.value) == 'A voyage requires a voyage number'

    with pytest.raises(TypeError) as error:
        VoyageBuilder(VoyageNumber('CM001'), None)

    assert str(error.value) == 'A voyage requires a departure location'


def test_voyage_without_schedule_has_an_empty_sentinel():
    assert Voyage.NONE.voyage_number == VoyageNumber('')
    assert Voyage.NONE.schedule == Schedule.EMPTY
