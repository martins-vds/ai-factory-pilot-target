from collections.abc import Callable

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from cargotracker.booking.application.dashboard import CargoDashboard
from cargotracker.cargo.domain.tracking_id import TrackingId


def create_booking_views(
    cargo_dashboard: CargoDashboard,
) -> tuple[Callable[[HttpRequest], HttpResponse], Callable[[HttpRequest, str], HttpResponse]]:
    def dashboard(request: HttpRequest) -> HttpResponse:
        cargos = cargo_dashboard.get_dashboard()
        return render(
            request,
            'booking/dashboard/dashboard.html',
            {
                'routed_cargos': cargos.routed_cargos,
                'not_routed_cargos': cargos.not_routed_cargos,
                'claimed_cargos': cargos.claimed_cargos,
            },
        )

    def cargo_details(request: HttpRequest, tracking_id: str) -> HttpResponse:
        cargo = cargo_dashboard.get_cargo_details(TrackingId(tracking_id))
        if cargo is None:
            raise Http404(f'Cargo with tracking ID {tracking_id} not found.')
        return render(request, 'booking/cargo_details.html', {'cargo': cargo})

    return dashboard, cargo_details
