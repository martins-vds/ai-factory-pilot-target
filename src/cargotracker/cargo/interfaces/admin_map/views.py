from collections.abc import Callable

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from cargotracker.cargo.application.admin_map import build_admin_map_data
from cargotracker.cargo.domain.repository import CargoRepository
from cargotracker.cargo.interfaces.tracking.map.coordinates import LOCATION_COORDINATES


def create_admin_map_views(
    cargo_repository: CargoRepository,
) -> tuple[Callable[[HttpRequest], HttpResponse], Callable[[HttpRequest], HttpResponse]]:
    def live_map(request: HttpRequest) -> HttpResponse:
        return render(request, 'admin/live_map.html', _map_context(cargo_repository))

    def live_map_markers(request: HttpRequest) -> HttpResponse:
        return render(request, 'admin/_live_map_markers.html', _map_context(cargo_repository))

    return live_map, live_map_markers


def _map_context(cargo_repository: CargoRepository) -> dict[str, object]:
    return {
        'map_data': build_admin_map_data(cargo_repository, LOCATION_COORDINATES),
    }
