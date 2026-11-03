from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import ClassVar

from cargotracker.handling.domain.handling_event import HandlingEvent


@dataclass(frozen=True, init=False)
class HandlingHistory:
    events: tuple[HandlingEvent, ...]
    _event_ids: tuple[int | None, ...] = field(compare=False, repr=False)

    EMPTY: ClassVar['HandlingHistory']

    def __init__(
        self,
        events: Iterable[HandlingEvent],
        event_ids: Iterable[int | None] | None = None,
    ):
        if events is None:
            raise TypeError('Handling events are required')
        handling_events = tuple(events)
        if any(not isinstance(event, HandlingEvent) for event in handling_events):
            raise TypeError('Handling history requires handling events')
        identifiers = tuple(event_ids) if event_ids is not None else (None,) * len(handling_events)
        if len(identifiers) != len(handling_events):
            raise ValueError('Handling event IDs must match the history events')
        if any(
            identifier is not None
            and (not isinstance(identifier, int) or isinstance(identifier, bool) or identifier < 1)
            for identifier in identifiers
        ):
            raise ValueError('Handling event IDs must be positive integers')
        distinct_events = {}
        for event, identifier in zip(handling_events, identifiers, strict=True):
            current = distinct_events.get(event)
            if current is None or (identifier or 0) > (current[1] or 0):
                distinct_events[event] = (event, identifier)
        ordered_events = sorted(
            distinct_events.values(),
            key=lambda item: (
                item[0].completion_time,
                item[0].registration_time,
                item[1] or 0,
            ),
        )
        object.__setattr__(self, 'events', tuple(event for event, _ in ordered_events))
        object.__setattr__(
            self, '_event_ids', tuple(identifier for _, identifier in ordered_events)
        )

    @property
    def most_recent_event(self) -> HandlingEvent | None:
        return self.events[-1] if self.events else None

    @property
    def most_recent_event_id(self) -> int | None:
        return self._event_ids[-1] if self._event_ids else None


HandlingHistory.EMPTY = HandlingHistory(())
