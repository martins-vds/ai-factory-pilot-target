import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[3]


@pytest.fixture(scope='session')
def booking_recording():
    return json.loads(
        (ROOT / '.migration' / 'characterization' / 'booking' / 'observations.json').read_text()
    )
