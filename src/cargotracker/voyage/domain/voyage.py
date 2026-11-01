from dataclasses import dataclass
from typing import ClassVar

from cargotracker.voyage.domain.schedule import Schedule
from cargotracker.voyage.domain.voyage_number import VoyageNumber


@dataclass(frozen=True, eq=False)
class Voyage:
    voyage_number: VoyageNumber
    schedule: Schedule

    NONE: ClassVar['Voyage']

    def __post_init__(self):
        if not isinstance(self.voyage_number, VoyageNumber):
            raise TypeError('A voyage requires a voyage number')
        if not isinstance(self.schedule, Schedule):
            raise TypeError('A voyage requires a schedule')

    def __eq__(self, other):
        return isinstance(other, Voyage) and self.voyage_number == other.voyage_number

    def __hash__(self):
        return hash(self.voyage_number)

    def __str__(self):
        return f'Voyage {self.voyage_number}'


Voyage.NONE = Voyage(VoyageNumber(''), Schedule.EMPTY)
