from collections.abc import Callable
from datetime import date, datetime, time

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from cargotracker.booking.application.dashboard import CargoDashboard
from cargotracker.booking.application.specification import CargoSpecification
from cargotracker.cargo.domain.cargo import Cargo
from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.location.domain.location import Location


def _find_cargo(cargo_dashboard: CargoDashboard, tracking_id: str) -> Cargo:
    cargo = cargo_dashboard.get_cargo_details(TrackingId(tracking_id))
    if cargo is None:
        raise Http404(f'Cargo with tracking ID {tracking_id} not found.')
    return cargo


def _complete_dialog_update(request: HttpRequest) -> HttpResponse:
    if request.headers.get('HX-Request') == 'true':
        response = HttpResponse(status=204)
        response['HX-Redirect'] = '/admin/dashboard/'
        return response
    return redirect('/admin/dashboard/')


def create_dialog_views(
    cargo_dashboard: CargoDashboard,
    cargo_specification: CargoSpecification,
    list_shipping_locations: Callable[[], list[Location]],
) -> tuple[
    Callable[[HttpRequest, str], HttpResponse],
    Callable[[HttpRequest, str], HttpResponse],
]:
    def destination_dialog(request: HttpRequest, tracking_id: str) -> HttpResponse:
        cargo = _find_cargo(cargo_dashboard, tracking_id)
        route_specification = cargo.route_specification
        destinations = [
            location
            for location in list_shipping_locations()
            if location not in (route_specification.origin, route_specification.destination)
        ]
        destination_value = (
            request.POST.get('destination')
            if request.method == 'POST'
            else (destinations[0].unlocode.value if destinations else '')
        )
        destination_error = ''

        if request.method == 'POST':
            destination_by_code = {location.unlocode.value: location for location in destinations}
            destination = destination_by_code.get(destination_value)
            if destination is None:
                destination_error = 'Select a valid destination.'
            else:
                cargo_specification.change_destination(TrackingId(tracking_id), destination)
                return _complete_dialog_update(request)

        return render(
            request,
            'booking/dialogs/destination.html',
            {
                'cargo': cargo,
                'destinations': destinations,
                'destination_value': destination_value,
                'destination_error': destination_error,
            },
        )

    def deadline_dialog(request: HttpRequest, tracking_id: str) -> HttpResponse:
        cargo = _find_cargo(cargo_dashboard, tracking_id)
        deadline_value = (
            request.POST.get('deadline', '')
            if request.method == 'POST'
            else cargo.route_specification.arrival_deadline.date().isoformat()
        )
        deadline_error = ''

        if request.method == 'POST':
            try:
                arrival_date = date.fromisoformat(deadline_value)
            except ValueError:
                deadline_error = 'Enter a valid arrival deadline.'
            else:
                arrival_deadline = timezone.make_aware(datetime.combine(arrival_date, time.min))
                cargo_specification.change_deadline(TrackingId(tracking_id), arrival_deadline)
                return _complete_dialog_update(request)

        return render(
            request,
            'booking/dialogs/deadline.html',
            {
                'cargo': cargo,
                'deadline_value': deadline_value,
                'deadline_error': deadline_error,
            },
        )

    return destination_dialog, deadline_dialog
