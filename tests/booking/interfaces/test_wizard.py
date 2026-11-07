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
