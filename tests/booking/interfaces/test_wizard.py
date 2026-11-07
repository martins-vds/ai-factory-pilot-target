import re

import pytest
from django.core.management import call_command
from django.test import RequestFactory

from cargotracker.booking.application.registration import CargoRegistration
from cargotracker.booking.interfaces.wizard.views import create_booking_wizard_view
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
