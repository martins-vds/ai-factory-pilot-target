from urllib.parse import urlencode

from django.urls import reverse

from cargotracker.cargo.domain.cargo import Cargo


def map_status_code(cargo: Cargo) -> str:
    if not cargo.itinerary.legs:
        return 'NOT_ROUTED'
    if cargo.delivery.unloaded_at_destination:
        return 'AT_DESTINATION'
    if cargo.delivery.misdirected:
        return 'MISDIRECTED'
    return cargo.delivery.transport_status.value


def map_frame_url(cargo: Cargo) -> str:
    last_known_location = cargo.delivery.last_known_location
    locations = {
        'lastKnownLocation': last_known_location,
        'origin': cargo.route_specification.origin,
        'destination': cargo.route_specification.destination,
    }
    query = {'statusCode': map_status_code(cargo)}
    for role, location in locations.items():
        query[f'{role}Code'] = location.unlocode.value if location is not None else ''
        query[f'{role}Name'] = location.name if location is not None else ''
    return f'{reverse("cargo_map_frame")}?{urlencode(query)}'
