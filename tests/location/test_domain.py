import pytest

from cargotracker.location.domain.location import Location
from cargotracker.location.domain.un_locode import UnLocode


@pytest.mark.parametrize(
    ('value', 'expected'),
    [('usnyc', 'USNYC'), ('CNHGH', 'CNHGH'), ('GBB2B', 'GBB2B')],
)
def test_un_locode_normalizes_valid_codes(value, expected):
    assert UnLocode(value).value == expected


@pytest.mark.parametrize('value', ['USNY', 'USNYC1', 'U1NYC', 'USN0C', 'USN1C', ''])
def test_un_locode_rejects_invalid_codes(value):
    with pytest.raises(ValueError):
        UnLocode(value)


def test_location_identity_uses_un_locode_and_preserves_name():
    first = Location(UnLocode('USNYC'), 'New York')
    renamed = Location(UnLocode('USNYC'), 'New York City')

    assert first == renamed
    assert hash(first) == hash(renamed)
    assert first.name == 'New York'
    assert str(first) == 'New York [USNYC]'


def test_unknown_location_matches_source_sentinel():
    assert Location.UNKNOWN == Location(UnLocode('XXXXX'), 'Unknown location')


def test_location_is_immutable():
    location = Location(UnLocode('USNYC'), 'New York')

    with pytest.raises(AttributeError):
        location.name = 'New York City'
