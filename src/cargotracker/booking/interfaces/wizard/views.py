from collections.abc import Callable

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from cargotracker.booking.application.registration import CargoRegistration
from cargotracker.location.domain.repository import LocationRepository


def create_booking_wizard_view(
    registration: CargoRegistration,
    locations: LocationRepository,
) -> Callable[[HttpRequest], HttpResponse]:
    def wizard(request: HttpRequest) -> HttpResponse:
        available_locations = locations.find_all()
        default_origin = next(
            (location for location in available_locations if location.unlocode.value == 'USCHI'),
            available_locations[0] if available_locations else None,
        )
        return render(
            request,
            'booking/wizard/origin.html',
            {'locations': available_locations, 'origin': default_origin},
        )

    return wizard
