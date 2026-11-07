from collections.abc import Mapping

from cargotracker.cargo.domain.cargo import Cargo
from cargotracker.cargo.domain.delivery import TransportStatus
from cargotracker.cargo.domain.repository import CargoRepository
from cargotracker.location.domain.location import Location

UNKNOWN_LOCATION = {'code': 'XXXXX', 'name': 'Unknown'}


def build_admin_map_data(
    cargo_repository: CargoRepository,
    location_coordinates: Mapping[str, tuple[float, float]],
) -> list[dict[str, object]]:
    return [
        _cargo_map_data(cargo, location_coordinates) for cargo in cargo_repository.find_all()
    ]


def _cargo_map_data(
    cargo: Cargo, location_coordinates: Mapping[str, tuple[float, float]]
) -> dict[str, object]:
    origin = _location_data(cargo.origin)
    last_known_location = _location_data(cargo.delivery.last_known_location)
    location = (
        origin
        if cargo.delivery.transport_status is TransportStatus.NOT_RECEIVED
        else last_known_location
    )
    location = location or UNKNOWN_LOCATION
    code = location['code']
    coordinates = (
        list(location_coordinates[code])
        if code != UNKNOWN_LOCATION['code'] and code in location_coordinates
        else None
    )

    return {
        'tracking_id': cargo.tracking_id.value,
        'routing_status': cargo.delivery.routing_status.value,
        'misdirected': cargo.delivery.misdirected,
        'transport_status': cargo.delivery.transport_status.value,
        'at_destination': cargo.delivery.unloaded_at_destination,
        'origin': origin,
        'last_known_location': last_known_location or UNKNOWN_LOCATION,
        'location': location,
        'coordinates': coordinates,
    }


def _location_data(location: Location | None) -> dict[str, str] | None:
    if location is None:
        return None
    code = location.unlocode.value
    name = 'Unknown' if code == UNKNOWN_LOCATION['code'] else location.name
    return {'code': code, 'name': name}
