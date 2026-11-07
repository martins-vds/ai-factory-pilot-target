from collections.abc import Callable

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from cargotracker.cargo.domain.delivery import TransportStatus
from cargotracker.cargo.domain.repository import CargoRepository
from cargotracker.cargo.domain.tracking_id import TrackingId


def create_booking_views(
    cargo_repository: CargoRepository,
) -> tuple[Callable[[HttpRequest], HttpResponse], Callable[[HttpRequest, str], HttpResponse]]:
    def dashboard(request: HttpRequest) -> HttpResponse:
        cargos = cargo_repository.find_all()
        return render(
            request,
            'booking/dashboard/dashboard.html',
            {
                'routed_cargos': [
                    cargo
                    for cargo in cargos
                    if cargo.itinerary.legs
                    and cargo.delivery.transport_status is not TransportStatus.CLAIMED
                ],
                'not_routed_cargos': [cargo for cargo in cargos if not cargo.itinerary.legs],
                'claimed_cargos': [
                    cargo
                    for cargo in cargos
                    if cargo.delivery.transport_status is TransportStatus.CLAIMED
                ],
            },
        )

    def cargo_details(request: HttpRequest, tracking_id: str) -> HttpResponse:
        cargo = cargo_repository.find(TrackingId(tracking_id))
        if cargo is None:
            raise Http404(f'Cargo with tracking ID {tracking_id} not found.')
        return render(request, 'booking/cargo_details.html', {'cargo': cargo})

    return dashboard, cargo_details
