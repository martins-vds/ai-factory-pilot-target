import re
from dataclasses import dataclass

_VALID_UN_LOCODE = re.compile(r'[A-Za-z]{2}[A-Za-z2-9]{3}')


@dataclass(frozen=True)
class UnLocode:
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise TypeError('A UN/LOCODE must be a string')
        if not _VALID_UN_LOCODE.fullmatch(self.value):
            raise ValueError(f'{self.value!r} is not a valid UN/LOCODE')
        object.__setattr__(self, 'value', self.value.upper())

    def __str__(self):
        return self.value
