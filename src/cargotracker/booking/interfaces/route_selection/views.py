from collections.abc import Callable

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from cargotracker.booking.application.dashboard import CargoDashboard
from cargotracker.booking.application.routing import CargoRouting
from cargotracker.cargo.domain.tracking_id import TrackingId


def create_route_selection_views(
    cargo_routing: CargoRouting,
    cargo_dashboard: CargoDashboard,
) -> tuple[Callable[[HttpRequest, str], HttpResponse], Callable[[HttpRequest, str], HttpResponse]]:
    def route_selection(request: HttpRequest, tracking_id: str) -> HttpResponse:
        context = _selection_context(cargo_routing, cargo_dashboard, tracking_id)
        return render(request, 'booking/route_selection/route.html', context)

    def select_itinerary(request: HttpRequest, tracking_id: str) -> HttpResponse:
        context = _selection_context(cargo_routing, cargo_dashboard, tracking_id)
        return render(request, 'booking/route_selection/select_itinerary.html', context)

    return route_selection, select_itinerary


def _selection_context(
    cargo_routing: CargoRouting,
    cargo_dashboard: CargoDashboard,
    tracking_id_value: str,
) -> dict:
    tracking_id = TrackingId(tracking_id_value)
    cargo = cargo_dashboard.get_cargo_details(tracking_id)
    if cargo is None:
        raise Http404(f'Cargo with tracking ID {tracking_id} not found.')
    itineraries = cargo_routing.route_candidates(tracking_id)
    return {
        'cargo': cargo,
        'candidate_count': len(itineraries),
        'routes': [
            {'itinerary': itinerary, 'number': number}
            for number, itinerary in enumerate(itineraries, start=1)
        ],
    }
