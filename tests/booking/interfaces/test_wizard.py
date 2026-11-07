import re
from datetime import date

import pytest
from django.core.management import call_command
from django.test import RequestFactory

from cargotracker.booking.application.registration import CargoRegistration
from cargotracker.booking.interfaces.wizard.views import create_booking_wizard_view
from cargotracker.cargo.domain.delivery import RoutingStatus, TransportStatus
from cargotracker.cargo.infrastructure.models import CargoRecord
from cargotracker.cargo.infrastructure.repository import DjangoCargoRepository
from cargotracker.location.infrastructure.repository import DjangoLocationRepository


@pytest.mark.django_db
def test_origin_step_is_open_and_defaults_to_chicago():
    call_command('seed_sample_data')
    wizard = create_booking_wizard_view(
        CargoRegistration(DjangoCargoRepository()),
        DjangoLocationRepository(),
    )

    response = wizard(RequestFactory().get('/booking/'))
    content = response.content.decode()

    assert response.status_code == 200
    assert 'Choose the origin of the new cargo' in content
    assert re.search(r'<option value="USCHI" selected', content)
    assert content.count('<option') == 13
    assert 'Cancel' in content
    assert 'Next' in content


@pytest.mark.django_db
def test_origin_next_opens_destination_with_dallas_and_excludes_origin():
    call_command('seed_sample_data')
    wizard = create_booking_wizard_view(
        CargoRegistration(DjangoCargoRepository()),
        DjangoLocationRepository(),
    )

    response = wizard(
        RequestFactory().post(
            '/booking/',
            {'step': 'origin', 'action': 'next', 'origin': 'USCHI'},
        )
    )
    content = response.content.decode()
    destination_options = re.search(
        r'<select\b[^>]*name="destination"[^>]*>(.*?)</select>', content, re.DOTALL
    )

    assert response.status_code == 200
    assert 'Set the destination for this new cargo coming from Chicago' in content
    assert destination_options is not None
    assert 'value="USDAL" selected' in destination_options.group(1)
    assert 'value="USCHI"' not in destination_options.group(1)
    assert destination_options.group(1).count('<option') == 12
    assert 'Back' in content
    assert 'Cancel' in content
    assert 'Next' in content


@pytest.mark.django_db
def test_invalid_origin_does_not_silently_select_the_default():
    call_command('seed_sample_data')
    wizard = create_booking_wizard_view(
        CargoRegistration(DjangoCargoRepository()),
        DjangoLocationRepository(),
    )

    response = wizard(
        RequestFactory().post(
            '/booking/',
            {'step': 'origin', 'action': 'next', 'origin': 'UNKNOWN'},
        )
    )
    content = response.content.decode()

    assert 'Choose the origin of the new cargo' in content
    assert 'Select a valid origin.' in content
    assert 'Set the destination for this new cargo' not in content


@pytest.mark.django_db
def test_invalid_destination_is_reported_on_destination_step():
    call_command('seed_sample_data')
    wizard = create_booking_wizard_view(
        CargoRegistration(DjangoCargoRepository()),
        DjangoLocationRepository(),
    )

    response = wizard(
        RequestFactory().post(
            '/booking/',
            {
                'step': 'destination',
                'action': 'next',
                'origin': 'USCHI',
                'destination': 'UNKNOWN',
            },
        )
    )
    content = response.content.decode()

    assert 'Set the destination for this new cargo coming from Chicago' in content
    assert 'Select a valid destination.' in content


@pytest.mark.django_db
def test_destination_next_opens_deadline_with_today_as_calendar_minimum(monkeypatch):
    call_command('seed_sample_data')
    today = date(2026, 11, 7)
    monkeypatch.setattr(
        'django.utils.timezone.localdate',
        lambda: today,
    )
    wizard = create_booking_wizard_view(
        CargoRegistration(DjangoCargoRepository()),
        DjangoLocationRepository(),
    )

    response = wizard(
        RequestFactory().post(
            '/booking/',
            {
                'step': 'destination',
                'action': 'next',
                'origin': 'USCHI',
                'destination': 'USDAL',
            },
        )
    )
    content = response.content.decode()

    assert response.status_code == 200
    assert 'Set the arrival deadline for this new Chicago-Dallas cargo' in content
    assert 'type="date"' in content
    assert 'min="2026-11-07"' in content
    assert 'Back' in content
    assert 'Cancel' in content
    assert re.search(r'<button\b[^>]*id="book-cargo"[^>]*disabled', content)


@pytest.mark.parametrize(
    ('deadline', 'message', 'bookable'),
    [
        ('2026-11-07', "A journey can't start and end the same day!", False),
        ('2026-11-08', 'Journey duration is one day.', True),
        ('2026-11-09', 'Journey duration is 2 days.', True),
    ],
)
@pytest.mark.django_db
def test_deadline_change_updates_duration_and_booking_state(
    monkeypatch, deadline, message, bookable
):
    call_command('seed_sample_data')
    today = date(2026, 11, 7)
    monkeypatch.setattr('django.utils.timezone.localdate', lambda: today)
    wizard = create_booking_wizard_view(
        CargoRegistration(DjangoCargoRepository()),
        DjangoLocationRepository(),
    )

    response = wizard(
        RequestFactory().post(
            '/booking/',
            {
                'step': 'deadline',
                'origin': 'USCHI',
                'destination': 'USDAL',
                'deadline': deadline,
            },
            HTTP_HX_REQUEST='true',
        )
    )
    content = response.content.decode()
    book_button = re.search(r'<button\b[^>]*id="book-cargo"[^>]*>', content)

    assert response.status_code == 200
    assert message in content
    assert book_button is not None
    has_disabled_attribute = re.search(r'\sdisabled(?:\s|>)', book_button.group(0))
    assert (has_disabled_attribute is None) is bookable


@pytest.mark.django_db
def test_back_returns_to_destination_and_cancel_returns_to_dashboard():
    call_command('seed_sample_data')
    wizard = create_booking_wizard_view(
        CargoRegistration(DjangoCargoRepository()),
        DjangoLocationRepository(),
    )

    back_response = wizard(
        RequestFactory().post(
            '/booking/',
            {
                'step': 'deadline',
                'action': 'back',
                'origin': 'USCHI',
                'destination': 'USDAL',
                'deadline': '2026-11-08',
            },
        )
    )
    cancel_response = wizard(
        RequestFactory().post(
            '/booking/',
            {
                'step': 'deadline',
                'action': 'cancel',
                'origin': 'USCHI',
                'destination': 'USDAL',
            },
        )
    )

    assert 'Set the destination for this new cargo coming from Chicago' in (
        back_response.content.decode()
    )
    assert 'value="USDAL" selected' in back_response.content.decode()
    assert cancel_response.status_code == 302
    assert cancel_response.url == '/admin/dashboard/'


@pytest.mark.django_db
def test_back_from_destination_preserves_the_selected_origin():
    call_command('seed_sample_data')
    wizard = create_booking_wizard_view(
        CargoRegistration(DjangoCargoRepository()),
        DjangoLocationRepository(),
    )

    response = wizard(
        RequestFactory().post(
            '/booking/',
            {
                'step': 'destination',
                'action': 'back',
                'origin': 'USCHI',
                'destination': 'USDAL',
            },
        )
    )
    content = response.content.decode()

    assert 'Choose the origin of the new cargo' in content
    assert re.search(r'<option value="USCHI" selected', content)


@pytest.mark.django_db
def test_back_and_next_preserve_destination_and_deadline(monkeypatch):
    call_command('seed_sample_data')
    today = date(2026, 11, 7)
    monkeypatch.setattr('django.utils.timezone.localdate', lambda: today)
    wizard = create_booking_wizard_view(
        CargoRegistration(DjangoCargoRepository()),
        DjangoLocationRepository(),
    )
    factory = RequestFactory()

    destination_response = wizard(
        factory.post(
            '/booking/',
            {
                'step': 'deadline',
                'action': 'back',
                'origin': 'USCHI',
                'destination': 'USDAL',
                'deadline': '2026-11-09',
            },
        )
    )
    origin_response = wizard(
        factory.post(
            '/booking/',
            {
                'step': 'destination',
                'action': 'back',
                'origin': 'USCHI',
                'destination': 'USDAL',
                'deadline': '2026-11-09',
            },
        )
    )

    assert 'name="deadline" value="2026-11-09"' in destination_response.content.decode()
    origin_content = origin_response.content.decode()
    origin_options = re.search(
        r'<select\b[^>]*name="origin"[^>]*>(.*?)</select>', origin_content, re.DOTALL
    )
    assert origin_options is not None
    assert 'value="USDAL"' not in origin_options.group(1)
    assert 'name="destination" value="USDAL"' in origin_content
    assert 'name="deadline" value="2026-11-09"' in origin_content

    destination_next = wizard(
        factory.post(
            '/booking/',
            {
                'step': 'origin',
                'action': 'next',
                'origin': 'USCHI',
                'destination': 'USDAL',
                'deadline': '2026-11-09',
            },
        )
    )
    deadline_next = wizard(
        factory.post(
            '/booking/',
            {
                'step': 'destination',
                'action': 'next',
                'origin': 'USCHI',
                'destination': 'USDAL',
                'deadline': '2026-11-09',
            },
        )
    )

    assert 'value="USDAL" selected' in destination_next.content.decode()
    assert 'value="2026-11-09"' in deadline_next.content.decode()
    assert 'Journey duration is 2 days.' in deadline_next.content.decode()


@pytest.mark.django_db
def test_same_day_booking_is_rejected_even_when_submitted_directly(monkeypatch):
    call_command('seed_sample_data')
    today = date(2026, 11, 7)
    monkeypatch.setattr('django.utils.timezone.localdate', lambda: today)
    existing_tracking_ids = set(CargoRecord.objects.values_list('tracking_id', flat=True))
    wizard = create_booking_wizard_view(
        CargoRegistration(DjangoCargoRepository()),
        DjangoLocationRepository(),
    )

    response = wizard(
        RequestFactory().post(
            '/booking/',
            {
                'step': 'deadline',
                'action': 'book',
                'origin': 'USCHI',
                'destination': 'USDAL',
                'deadline': today.isoformat(),
            },
        )
    )
    content = response.content.decode()

    assert response.status_code == 200
    assert "A journey can't start and end the same day!" in content
    assert re.search(r'<button\b[^>]*id="book-cargo"[^>]*disabled', content)
    assert not CargoRecord.objects.exclude(tracking_id__in=existing_tracking_ids).exists()


@pytest.mark.django_db
def test_book_cargo_persists_registration_and_redirects_to_dashboard(monkeypatch):
    call_command('seed_sample_data')
    today = date(2026, 11, 7)
    monkeypatch.setattr('django.utils.timezone.localdate', lambda: today)
    existing_tracking_ids = set(CargoRecord.objects.values_list('tracking_id', flat=True))
    wizard = create_booking_wizard_view(
        CargoRegistration(DjangoCargoRepository()),
        DjangoLocationRepository(),
    )

    response = wizard(
        RequestFactory().post(
            '/booking/',
            {
                'step': 'deadline',
                'action': 'book',
                'origin': 'USCHI',
                'destination': 'USDAL',
                'deadline': '2026-11-08',
            },
        )
    )
    cargo = CargoRecord.objects.exclude(tracking_id__in=existing_tracking_ids).get()

    assert response.status_code == 302
    assert response.url == '/admin/dashboard/'
    assert cargo.origin.unlocode == 'USCHI'
    assert cargo.spec_origin.unlocode == 'USCHI'
    assert cargo.spec_destination.unlocode == 'USDAL'
    assert cargo.spec_arrival_deadline == date(2026, 11, 8)
    assert cargo.transport_status == TransportStatus.NOT_RECEIVED.value
    assert cargo.routing_status == RoutingStatus.NOT_ROUTED.value


@pytest.mark.django_db
def test_same_origin_and_destination_cannot_be_submitted(monkeypatch):
    call_command('seed_sample_data')
    today = date(2026, 11, 7)
    monkeypatch.setattr('django.utils.timezone.localdate', lambda: today)
    existing_tracking_ids = set(CargoRecord.objects.values_list('tracking_id', flat=True))
    wizard = create_booking_wizard_view(
        CargoRegistration(DjangoCargoRepository()),
        DjangoLocationRepository(),
    )

    response = wizard(
        RequestFactory().post(
            '/booking/',
            {
                'step': 'deadline',
                'action': 'book',
                'origin': 'USCHI',
                'destination': 'USCHI',
                'deadline': '2026-11-08',
            },
        )
    )

    assert response.status_code == 200
    assert 'Origin and destination cannot be the same.' in response.content.decode()
    assert not CargoRecord.objects.exclude(tracking_id__in=existing_tracking_ids).exists()
