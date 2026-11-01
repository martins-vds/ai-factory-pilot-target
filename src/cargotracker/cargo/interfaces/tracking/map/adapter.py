from __future__ import annotations

from urllib.parse import urlencode

from django.urls import reverse

from cargotracker.cargo.application.map_status import map_status_code
from cargotracker.cargo.domain.cargo import Cargo


def map_frame_url(cargo: Cargo) -> str:
    last_known_location = cargo.delivery.last_known_location
    query = {'statusCode': map_status_code(cargo)}
    if last_known_location is None:
        query['lastKnownLocationCode'] = 'XXXXX'
        query['lastKnownLocationName'] = 'Unknown'
    locations = {
        'origin': cargo.route_specification.origin,
        'destination': cargo.route_specification.destination,
    }
    if last_known_location is not None:
        locations['lastKnownLocation'] = last_known_location
    for role, location in locations.items():
        query[f'{role}Code'] = location.unlocode.value if location is not None else ''
        query[f'{role}Name'] = location.name if location is not None else ''
    return f'{reverse("cargo_map_frame")}?{urlencode(query)}'
