from collections.abc import Mapping

from cargotracker.cargo.application.admin_map_data import (
    UNKNOWN_LOCATION as _UNKNOWN_LOCATION,
)
from cargotracker.cargo.application.admin_map_data import (
    cargo_map_data,
)
from cargotracker.cargo.domain.repository import CargoRepository

UNKNOWN_LOCATION = _UNKNOWN_LOCATION


def build_admin_map_data(
    cargo_repository: CargoRepository,
    location_coordinates: Mapping[str, tuple[float, float]],
) -> list[dict[str, object]]:
    return [cargo_map_data(cargo, location_coordinates) for cargo in cargo_repository.find_all()]
