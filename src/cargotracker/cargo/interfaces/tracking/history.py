from cargotracker.cargo.domain.cargo import Cargo
from cargotracker.handling.domain.handling_event import HandlingEvent, HandlingEventType
from cargotracker.handling.domain.handling_history import HandlingHistory

_EVENT_DESCRIPTIONS = {
    HandlingEventType.RECEIVE: 'Received in {location}',
    HandlingEventType.LOAD: 'Loaded onto voyage {voyage} in {location}',
    HandlingEventType.UNLOAD: 'Unloaded off voyage {voyage} in {location}',
    HandlingEventType.CLAIM: 'Claimed in {location}',
    HandlingEventType.CUSTOMS: 'Cleared customs in {location}',
}


def get_event_description(event: HandlingEvent) -> str:
    return _EVENT_DESCRIPTIONS[event.event_type].format(
        location=event.location.name,
        voyage=event.voyage.voyage_number.value if event.voyage is not None else '',
    )


def get_history_rows(cargo: Cargo, history: HandlingHistory) -> list[dict[str, str | bool]]:
    return [
        {
            'description': get_event_description(event),
            'time': event.completion_time.strftime('%m/%d/%Y %I:%M %p UTC'),
            'expected': cargo.itinerary.is_expected(event),
        }
        for event in history.events
    ]
