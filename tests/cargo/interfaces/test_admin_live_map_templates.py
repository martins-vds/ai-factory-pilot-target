import pytest
from django.core.management import call_command
from django.test import override_settings
from django.urls import reverse


@pytest.mark.django_db
@override_settings(CARGO_MAP_POLL_SECONDS=17)
def test_admin_live_map_renders_leaflet_page_with_configured_htmx_polling(client):
    call_command('seed_sample_data')

    response = client.get(reverse('admin_live_map'))

    assert response.status_code == 200
    content = response.content.decode()
    assert 'id="live-map"' in content
    assert 'aria-label="Cargo location map"' in content
    assert 'leaflet@1.7.1/dist/leaflet.css' in content
    assert 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png' in content
    assert 'hx-get="/admin/live-map/markers/"' in content
    assert 'hx-trigger="every 17s"' in content
    assert 'hx-swap="innerHTML"' in content
    assert 'WebSocket' not in content
    assert 'Online' not in content
    assert 'Offline' not in content


@pytest.mark.django_db
def test_admin_live_map_exposes_a_marker_hook_that_clears_on_each_poll(client):
    call_command('seed_sample_data')

    response = client.get(reverse('admin_live_map'))

    assert response.status_code == 200
    content = response.content.decode()
    assert 'window.liveMapMarkers' in content
    assert 'clear()' in content
    assert 'add(marker)' in content
    assert 'hx-on::before-request="window.liveMapMarkers.clear()"' in content


@pytest.mark.django_db
def test_admin_live_map_marker_poll_returns_an_empty_marker_set(client):
    page_response = client.get(reverse('admin_live_map'))
    response = client.get(reverse('admin_live_map_markers'), HTTP_HX_REQUEST='true')

    page_content = page_response.content.decode()
    assert page_response.status_code == 200
    assert 'hx-target="#live-map-markers"' in page_content
    assert 'hx-swap="innerHTML"' in page_content
    assert response.status_code == 200
    assert not response.content.strip()
