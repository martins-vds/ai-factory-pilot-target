from datetime import UTC, datetime


def as_utc(value: datetime, field_name: str) -> datetime:
    if not isinstance(value, datetime):
        label = 'ETA' if field_name == 'ETA' else field_name.capitalize()
        raise TypeError(f'{label} must be a datetime')
    if value.utcoffset() is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)
