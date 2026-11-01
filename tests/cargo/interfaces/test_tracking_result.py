import re
from datetime import UTC, datetime, time, timedelta

import pytest
from django.core.management import call_command

from cargotracker.cargo.domain.handling_activity import HandlingActivity
from cargotracker.cargo.interfaces.tracking.next_activity import get_next_activity_text
from cargotracker.location.domain.location import Location
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.voyage.domain.schedule import Schedule
from cargotracker.voyage.domain.voyage import Voyage
from cargotracker.voyage.domain.voyage_number import VoyageNumber

NEW_YORK = Location(UnLocode('USNYC'), 'New York')
VOYAGE = Voyage(VoyageNumber('0100S'), Schedule.EMPTY)


@pytest.mark.django_db
def test_tracking_result_renders_ordered_history_with_utc_times_and_expectation_markers(client):
    call_command('seed_sample_data')

    response = client.post('/', {'tracking_id': 'ABC123'}, HTTP_HX_REQUEST='true')
    content = response.content.decode()

    assert response.status_code == 200
    assert 'id="handling-history"' in content
    descriptions = [
        'Received in Hong Kong',
        'Loaded onto voyage 0100S in Hong Kong',
        'Unloaded off voyage 0100S in New York',
    ]
    assert [content.index(description) for description in descriptions] == sorted(
        content.index(description) for description in descriptions
    )
    assert content.count('data-expectation="expected"') == 3
    today = datetime.now(UTC).date()
    expected_times = [
        datetime.combine(today + timedelta(days=offset), time.min, tzinfo=UTC).strftime(
            '%m/%d/%Y %I:%M %p UTC'
        )
        for offset in (-10, -7, -1)
    ]
    assert re.findall(r'<time>(.*?)</time>', content) == expected_times

    unexpected_response = client.post('/', {'tracking_id': 'JKL567'})
    assert 'data-expectation="unexpected"' in unexpected_response.content.decode()
    assert 'Loaded onto voyage 0100S in New York' in unexpected_response.content.decode()


@pytest.mark.django_db
def test_empty_history_and_absent_next_activity_are_rendered(client):
    call_command('seed_sample_data')

    response = client.post('/', {'tracking_id': 'DEF789'})
    content = response.content.decode()

    assert 'There are no events recorded for the tracking ID DEF789.' in content
    assert 'data-expectation=' not in content
    assert 'id="next-expected-activity"' not in content
    assert 'id="tracking-map"' in content


@pytest.mark.django_db
def test_tracking_result_renders_status_eta_map_and_next_activity(client):
    call_command('seed_sample_data')

    response = client.post('/', {'tracking_id': 'ABC123'})
    content = response.content.decode()

    assert 'In port New York' in content
    assert re.search(r'\d{2}/\d{2}/\d{4} 12:00 AM UTC', content)
    assert 'Next expected activity is to load cargo onto voyage 0200T in New York' in content
    assert 'id="tracking-map"' in content
    assert '/tracking/map/?statusCode=IN_PORT' in content


@pytest.mark.django_db
def test_misdirected_warning_and_absent_next_activity(client):
    call_command('seed_sample_data')

    jkl_response = client.post('/', {'tracking_id': 'JKL567'})
    jkl_content = jkl_response.content.decode()
    assert 'Cargo is misdirected' in jkl_content
    assert 'id="next-expected-activity"' not in jkl_content

    abc_response = client.post('/', {'tracking_id': 'ABC123'})
    assert 'Cargo is misdirected' not in abc_response.content.decode()

    mno_response = client.post('/', {'tracking_id': 'MNO456'})
    mno_content = mno_response.content.decode()
    assert 'Cleared customs in Dallas' in mno_content
    assert 'Claimed in Dallas' in mno_content
    assert mno_content.count('data-expectation="expected"') == 5
    assert 'id="next-expected-activity"' not in mno_content
    assert 'id="eta"' not in mno_content


@pytest.mark.parametrize(
    ('activity', 'expected'),
    [
        (
            HandlingActivity('RECEIVE', NEW_YORK),
            'Next expected activity is to receive cargo in New York',
        ),
        (
            HandlingActivity('LOAD', NEW_YORK, VOYAGE),
            'Next expected activity is to load cargo onto voyage 0100S in New York',
        ),
        (
            HandlingActivity('UNLOAD', NEW_YORK, VOYAGE),
            'Next expected activity is to unload cargo off of 0100S in New York',
        ),
        (
            HandlingActivity('CLAIM', NEW_YORK),
            'Next expected activity is to claim cargo in New York',
        ),
        (HandlingActivity.EMPTY, None),
    ],
)
def test_next_activity_text_matches_source_descriptions(activity, expected):
    assert get_next_activity_text(activity) == expected
