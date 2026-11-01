import pytest
from django.core.management import call_command


def test_tracking_page_has_a_progressive_tracking_form(client):
    response = client.get('/')

    assert response.status_code == 200
    assert b'<form' in response.content
    assert b'method="post"' in response.content
    assert b'hx-post=' in response.content
    assert b'hx-target="#tracking-result"' in response.content
    assert b'name="tracking_id"' in response.content


@pytest.mark.django_db
def test_empty_and_unknown_ids_show_messages_without_cargo_result_or_map(client):
    call_command('seed_sample_data')

    empty_response = client.post('/', {'tracking_id': ''})
    assert b'tracking ID is required' in empty_response.content
    assert b'id="tracking-form"' in empty_response.content

    unknown_response = client.post('/', {'tracking_id': 'UNKNOWN'})
    assert b'Cargo with tracking ID UNKNOWN not found.' in unknown_response.content
    assert b'id="tracking-form"' in unknown_response.content

    for response in (empty_response, unknown_response):
        assert b'id="cargo-result"' not in response.content
        assert b'id="handling-history"' not in response.content
        assert b'id="tracking-map"' not in response.content


@pytest.mark.django_db
def test_padded_tracking_id_is_trimmed_in_htmx_lookup(client):
    call_command('seed_sample_data')

    response = client.post('/', {'tracking_id': ' ABC123 '}, HTTP_HX_REQUEST='true')

    assert response.status_code == 200
    assert b'id="cargo-result"' in response.content
    assert b'Cargo ABC123' in response.content
    assert b'id="tracking-form"' not in response.content


@pytest.mark.django_db
def test_lowercase_tracking_id_remains_case_sensitive(client):
    call_command('seed_sample_data')

    response = client.post('/', {'tracking_id': 'abc123'})

    assert b'Cargo with tracking ID abc123 not found.' in response.content
    assert b'id="tracking-form"' in response.content
    assert b'id="cargo-result"' not in response.content
    assert b'id="handling-history"' not in response.content
    assert b'id="tracking-map"' not in response.content


@pytest.mark.django_db
def test_regular_form_submission_renders_found_cargo(client):
    call_command('seed_sample_data')

    response = client.post('/', {'tracking_id': 'DEF789'})

    assert response.status_code == 200
    assert b'id="tracking-form"' in response.content
    assert b'id="cargo-result"' in response.content
    assert b'Cargo DEF789' in response.content
