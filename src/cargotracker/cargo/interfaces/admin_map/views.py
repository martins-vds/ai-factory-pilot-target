from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from cargotracker.cargo.application.admin_map import build_admin_map_data
from cargotracker.cargo.infrastructure.repository import DjangoCargoRepository
from cargotracker.cargo.interfaces.tracking.map.coordinates import LOCATION_COORDINATES


def live_map(request: HttpRequest) -> HttpResponse:
    return render(request, 'admin/live_map.html', _map_context())


def live_map_markers(request: HttpRequest) -> HttpResponse:
    return render(request, 'admin/_live_map_markers.html', _map_context())


def _map_context() -> dict[str, object]:
    return {
        'map_data': build_admin_map_data(DjangoCargoRepository(), LOCATION_COORDINATES),
    }
