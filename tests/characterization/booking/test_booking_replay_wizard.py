import re
from datetime import date, datetime, time

import pytest
from django.core.management import call_command
from django.utils import timezone

from cargotracker.cargo.domain.itinerary import Itinerary
from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.cargo.infrastructure.models import CargoRecord
from cargotracker.cargo.infrastructure.repository import DjangoCargoRepository

TODAY = date(2026, 11, 7)


@pytest.mark.django_db
def test_origin_step_fields_match_tier_a_recording(client, booking_recording):
    call_command('seed_sample_data')
    expected = booking_recording['cases']['wizard-origin']['observed']
    origin_code = re.search(r'\((\w+)\) selected by default', expected).group(1)
    location_count = int(re.search(r'(\d+) locations offered', expected).group(1))

    response = client.get('/booking/')
    content = response.content.decode()
    options = re.findall(r'<option\b([^>]*)>(.*?)</option>', content, re.DOTALL)
    selected = [attrs for attrs, _ in options if re.search(r'\bselected(?:\s|$)', attrs)]

    assert response.status_code == 200
    assert len(selected) == 1
    assert f'value="{origin_code}"' in selected[0]
    assert len(options) == location_count
    assert 'UN/LOCODE' in expected
    assert 'Cancel' in content and 'Next' in content


@pytest.mark.django_db
def test_destination_step_fields_match_tier_a_recording(client, booking_recording):
    call_command('seed_sample_data')
    expected = booking_recording['cases']['wizard-destination']['observed']
    destination_code = re.search(r'defaults destination to \w+ \((\w+)\)', expected).group(1)
    location_count = int(re.search(r'offers (\d+) locations excluding', expected).group(1))
    origin_code = 'USCHI'

    response = client.post(
        '/booking/',
        {'step': 'origin', 'action': 'next', 'origin': origin_code},
    )
    content = response.content.decode()
    options_markup = re.search(
        r'<select\b[^>]*name="destination"[^>]*>(.*?)</select>', content, re.DOTALL
    ).group(1)

    assert response.status_code == 200
    assert f'value="{destination_code}" selected' in options_markup
    assert f'value="{origin_code}"' not in options_markup
    assert options_markup.count('<option') == location_count
    assert 'Chicago' in content
    assert all(action in content for action in ('Back', 'Cancel', 'Next'))


@pytest.mark.django_db
def test_deadline_step_fields_match_tier_a_recording(client, booking_recording, monkeypatch):
    call_command('seed_sample_data')
    monkeypatch.setattr('django.utils.timezone.localdate', lambda: TODAY)
    expected = booking_recording['cases']['wizard-deadline']['observed']

    response = client.post(
        '/booking/',
        {'step': 'destination', 'action': 'next', 'origin': 'USCHI', 'destination': 'USDAL'},
    )
    content = response.content.decode()
    assert response.status_code == 200
    assert 'min="2026-11-07"' in content
    assert 'Chicago-Dallas' in content

    same_day = client.post(
        '/booking/',
        {
            'step': 'deadline',
            'origin': 'USCHI',
            'destination': 'USDAL',
            'deadline': '2026-11-07',
        },
        HTTP_HX_REQUEST='true',
    )
    next_day = client.post(
        '/booking/',
        {
            'step': 'deadline',
            'origin': 'USCHI',
            'destination': 'USDAL',
            'deadline': '2026-11-08',
        },
        HTTP_HX_REQUEST='true',
    )
    same_day_content = same_day.content.decode()
    next_day_content = next_day.content.decode()

    assert "A journey can't start and end the same day!" in expected
    assert 'Journey duration is one day.' in expected
    assert "A journey can't start and end the same day!" in same_day_content
    assert 'Journey duration is one day.' in next_day_content
    assert re.search(r'<button\b[^>]*id="book-cargo"[^>]*disabled', same_day_content)
    assert not re.search(r'<button\b[^>]*id="book-cargo"[^>]*disabled', next_day_content)


@pytest.mark.django_db
def test_wizard_chain_preserves_recorded_selections_and_actions(client, booking_recording):
    call_command('seed_sample_data')
    expected = booking_recording['cases']['wizard-destination']['observed']

    destination = client.post(
        '/booking/',
        {'step': 'origin', 'action': 'next', 'origin': 'USCHI'},
    )
    deadline = client.post(
        '/booking/',
        {
            'step': 'destination',
            'action': 'next',
            'origin': 'USCHI',
            'destination': 'USDAL',
        },
    )
    back = client.post(
        '/booking/',
        {
            'step': 'destination',
            'action': 'back',
            'origin': 'USCHI',
            'destination': 'USDAL',
        },
    )
    cancelled = client.post(
        '/booking/',
        {
            'step': 'deadline',
            'action': 'cancel',
            'origin': 'USCHI',
            'destination': 'USDAL',
        },
    )

    assert 'USDAL' in expected
    assert 'value="USDAL" selected' in destination.content.decode()
    assert 'name="deadline"' in deadline.content.decode()
    assert 'value="USCHI" selected' in back.content.decode()
    assert cancelled.status_code == 302
    assert cancelled.url == '/admin/dashboard/'


@pytest.mark.django_db
def test_registration_fields_match_tier_a_recording(client, booking_recording, monkeypatch):
    call_command('seed_sample_data')
    monkeypatch.setattr('django.utils.timezone.localdate', lambda: TODAY)
    expected = booking_recording['cases']['registration']['observed']
    before = set(CargoRecord.objects.values_list('tracking_id', flat=True))

    response = client.post(
        '/booking/',
        {
            'step': 'deadline',
            'action': 'book',
            'origin': 'USCHI',
            'destination': 'USDAL',
            'deadline': '2026-11-08',
        },
    )

    new_tracking_id = (
        set(CargoRecord.objects.values_list('tracking_id', flat=True)) - before
    ).pop()
    cargo = DjangoCargoRepository().find(TrackingId(new_tracking_id))

    assert response.status_code == 302
    assert response.url == '/admin/dashboard/'
    assert re.fullmatch(r'[A-F0-9]{8}', new_tracking_id)
    assert 'D613CF52' in expected and 'B147E0B7' in expected
    assert cargo is not None
    assert cargo.route_specification.origin.unlocode.value == 'USCHI'
    assert cargo.route_specification.destination.unlocode.value == 'USDAL'
    assert cargo.route_specification.arrival_deadline == timezone.make_aware(
        datetime.combine(date(2026, 11, 8), time.min)
    )
    assert cargo.itinerary == Itinerary.EMPTY
    assert cargo.delivery.transport_status.value == 'NOT_RECEIVED'
    assert cargo.delivery.routing_status.value == 'NOT_ROUTED'
