from cargotracker.cargo.domain.handling_activity import HandlingActivity

_ACTIVITY_DESCRIPTIONS = {
    'RECEIVE': 'receive cargo in {location}',
    'LOAD': 'load cargo onto voyage {voyage} in {location}',
    'UNLOAD': 'unload cargo off of {voyage} in {location}',
    'CLAIM': 'claim cargo in {location}',
}


def get_next_activity_text(activity: HandlingActivity) -> str | None:
    if activity.event_type is None:
        return None
    description = _ACTIVITY_DESCRIPTIONS[activity.event_type].format(
        location=activity.location.name,
        voyage=activity.voyage.voyage_number.value if activity.voyage is not None else '',
    )
    return f'Next expected activity is to {description}'
