from collections.abc import Callable
from datetime import date, datetime, time, timedelta

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

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


def _deadline_state(value: str, today: date) -> tuple[date | None, int | None, str]:
    if not value:
        return None, None, ''
    try:
        deadline = date.fromisoformat(value)
    except ValueError:
        return None, None, 'Enter a valid arrival deadline.'
    if deadline < today:
        return None, None, 'Arrival deadline cannot be before today.'
    duration = timedelta(days=(deadline - today).days, hours=4).days
    return deadline, duration, ''


def _origin_step(
    request: HttpRequest,
    locations: list[Location],
    origin: Location | None,
    destination: Location | None = None,
    deadline_value: str = '',
    error: str = '',
) -> HttpResponse:
    context = {
        'locations': [location for location in locations if location != destination],
        'origin': origin,
        'destination': destination,
        'deadline_value': deadline_value,
        'origin_error': error,
    }
    return render(request, 'booking/wizard/origin.html', context)


def _destination_step(
    request: HttpRequest,
    locations: list[Location],
    origin: Location | None,
    destination: Location | None,
    deadline_value: str = '',
    error: str = '',
) -> HttpResponse:
    context = {
        'origin': origin,
        'destination': destination,
        'locations': [location for location in locations if location != origin],
        'deadline_value': deadline_value,
        'destination_error': error,
    }
    return render(request, 'booking/wizard/destination.html', context)


def _deadline_context(
    origin: Location | None, destination: Location | None, value: str, today: date
) -> dict[str, object]:
    deadline, duration, deadline_error = _deadline_state(value, today)
    return {
        'today': today,
        'origin': origin,
        'destination': destination,
        'deadline': deadline,
        'deadline_value': value,
        'duration': duration,
        'bookable': duration is not None and duration >= 1 and origin != destination,
        'deadline_error': deadline_error,
    }


def _deadline_step(
    request: HttpRequest,
    registration: CargoRegistration,
    origin: Location | None,
    destination: Location | None,
) -> HttpResponse:
    deadline_value = request.POST.get('deadline', '')
    context = _deadline_context(origin, destination, deadline_value, timezone.localdate())
    context['validation_error'] = ''

    if request.POST.get('action') == 'book':
        if origin is None or destination is None:
            context['validation_error'] = 'Choose an origin and destination.'
        elif origin == destination:
            context['validation_error'] = 'Origin and destination cannot be the same.'
        elif context['deadline'] is None:
            context['validation_error'] = context['deadline_error'] or 'Choose an arrival deadline.'
        elif context['bookable']:
            registration.register(
                origin,
                destination,
                timezone.make_aware(datetime.combine(context['deadline'], time.min)),
            )
            return redirect('/admin/dashboard/')

    template = (
        'booking/wizard/_deadline_form.html'
        if request.headers.get('HX-Request') == 'true'
        else 'booking/wizard/deadline.html'
    )
    return render(request, template, context)


def create_booking_wizard_view(
    registration: CargoRegistration,
    locations: LocationRepository,
) -> Callable[[HttpRequest], HttpResponse]:
    def wizard(request: HttpRequest) -> HttpResponse:
        available_locations = locations.find_all()
        location_by_code = {location.unlocode.value: location for location in available_locations}
        data = request.POST
        origin = location_by_code.get(data.get('origin', ''))
        destination = location_by_code.get(data.get('destination', ''))
        deadline_value = data.get('deadline', '')

        if request.method != 'POST':
            return _origin_step(
                request,
                available_locations,
                _preferred_location(available_locations, 'USCHI'),
            )
        if data.get('action') == 'cancel':
            return redirect('/admin/dashboard/')
        if data.get('step') == 'destination' and data.get('action') == 'back':
            return _origin_step(request, available_locations, origin, destination, deadline_value)
        if data.get('step') == 'deadline' and data.get('action') == 'back':
            return _destination_step(
                request, available_locations, origin, destination, deadline_value
            )
        if data.get('step') == 'origin' and data.get('action') == 'next':
            if origin is None:
                return _origin_step(
                    request,
                    available_locations,
                    None,
                    destination,
                    deadline_value,
                    'Select a valid origin.',
                )
            if destination is None or destination == origin:
                destination = _preferred_location(available_locations, 'USDAL', origin)
            return _destination_step(
                request, available_locations, origin, destination, deadline_value
            )
        if data.get('step') == 'destination' and data.get('action') == 'next':
            if origin is None:
                return _origin_step(
                    request,
                    available_locations,
                    None,
                    destination,
                    deadline_value,
                    'Select a valid origin.',
                )
            if destination is None:
                return _destination_step(
                    request,
                    available_locations,
                    origin,
                    None,
                    deadline_value,
                    'Select a valid destination.',
                )
            context = _deadline_context(origin, destination, deadline_value, timezone.localdate())
            return render(request, 'booking/wizard/deadline.html', context)
        if data.get('step') == 'deadline':
            return _deadline_step(request, registration, origin, destination)
        return _origin_step(request, available_locations, origin, destination, deadline_value)

    return wizard
