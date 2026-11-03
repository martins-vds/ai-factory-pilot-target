from typing import Protocol

from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.handling.domain.handling_event import HandlingEvent
from cargotracker.handling.domain.handling_history import HandlingHistory
from cargotracker.handling.domain.registration_attempt import RegistrationAttempt


class HandlingEventRepository(Protocol):
    def store(self, event: HandlingEvent) -> None: ...

    def upsert(self, event: HandlingEvent) -> int: ...

    def lookup_handling_history_of_cargo(self, tracking_id: TrackingId) -> HandlingHistory: ...


class RegistrationAttemptRepository(Protocol):
    def submit(self, attempt: RegistrationAttempt) -> RegistrationAttempt: ...

    def claim_next(self) -> RegistrationAttempt | None: ...

    def mark_registered(self, attempt_id: int) -> None: ...

    def mark_rejected(self, attempt_id: int, reason: str) -> None: ...
