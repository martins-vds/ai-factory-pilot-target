from collections.abc import Callable

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from cargotracker.booking.application.registration import CargoRegistration
from cargotracker.location.domain.location import Location
from cargotracker.location.domain.repository import LocationRepository


def _preferred_location(
    locations: list[Location], preferred_code: str, excluded: Location | None = None
) -> Location | None:
    return next(
        (
            location
            for location in locations
            if location != excluded and location.unlocode.value == preferred_code
        ),
        next((location for location in locations if location != excluded), None),
    )


def create_booking_wizard_view(
    registration: CargoRegistration,
    locations: LocationRepository,
) -> Callable[[HttpRequest], HttpResponse]:
    def wizard(request: HttpRequest) -> HttpResponse:
        available_locations = locations.find_all()
        location_by_code = {location.unlocode.value: location for location in available_locations}
        data = request.POST
        origin = location_by_code.get(data.get('origin', ''))
        if origin is None:
            origin = _preferred_location(available_locations, 'USCHI')
        destination = location_by_code.get(data.get('destination', ''))
        if destination is None or destination == origin:
            destination = _preferred_location(available_locations, 'USDAL', origin)

        if request.method == 'POST' and data.get('action') == 'cancel':
            return redirect('/admin/dashboard/')
        if (
            request.method == 'POST'
            and data.get('step') == 'origin'
            and data.get('action') == 'next'
        ):
            return render(
                request,
                'booking/wizard/destination.html',
                {
                    'origin': origin,
                    'destination': destination,
                    'locations': [location for location in available_locations if location != origin],
                },
            )
        if (
            request.method == 'POST'
            and data.get('step') == 'destination'
            and data.get('action') == 'back'
        ):
            return render(
                request,
                'booking/wizard/origin.html',
                {'locations': available_locations, 'origin': origin},
            )
        return render(
            request,
            'booking/wizard/origin.html',
            {'locations': available_locations, 'origin': origin},
        )

    return wizard
