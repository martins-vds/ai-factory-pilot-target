from collections.abc import Iterable
from dataclasses import dataclass
from typing import ClassVar

from cargotracker.handling.domain.handling_event import HandlingEvent


@dataclass(frozen=True, init=False)
class HandlingHistory:
    events: tuple[HandlingEvent, ...]

    EMPTY: ClassVar['HandlingHistory']

    def __init__(self, events: Iterable[HandlingEvent]):
        if events is None:
            raise TypeError('Handling events are required')
        handling_events = tuple(events)
        if any(not isinstance(event, HandlingEvent) for event in handling_events):
            raise TypeError('Handling history requires handling events')
        object.__setattr__(
            self,
            'events',
            tuple(sorted(set(handling_events), key=lambda event: event.completion_time)),
        )

    @property
    def most_recent_event(self) -> HandlingEvent | None:
        return self.events[-1] if self.events else None


HandlingHistory.EMPTY = HandlingHistory(())
