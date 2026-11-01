from typing import Protocol

from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.handling.domain.handling_event import HandlingEvent
from cargotracker.handling.domain.handling_history import HandlingHistory


class HandlingEventRepository(Protocol):
    def store(self, event: HandlingEvent) -> None: ...

    def lookup_handling_history_of_cargo(self, tracking_id: TrackingId) -> HandlingHistory: ...
