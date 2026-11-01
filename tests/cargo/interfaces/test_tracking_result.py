import re

import pytest
from django.core.management import call_command


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
    assert re.search(r'\d{2}/\d{2}/\d{4} 12:00 AM UTC', content)

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
