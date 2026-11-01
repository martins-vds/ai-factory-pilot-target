from dataclasses import dataclass
from typing import ClassVar

from cargotracker.voyage.domain.carrier_movement import CarrierMovement


@dataclass(frozen=True)
class Schedule:
    carrier_movements: tuple[CarrierMovement, ...]

    EMPTY: ClassVar['Schedule']

    def __post_init__(self):
        movements = tuple(self.carrier_movements)
        if any(not isinstance(movement, CarrierMovement) for movement in movements):
            raise TypeError('A schedule requires carrier movements')
        object.__setattr__(self, 'carrier_movements', movements)


Schedule.EMPTY = Schedule(())
