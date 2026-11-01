from dataclasses import dataclass


@dataclass(frozen=True)
class TrackingId:
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise TypeError('A tracking ID must be a string')

    def __str__(self):
        return self.value
