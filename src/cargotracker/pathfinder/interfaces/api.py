from datetime import UTC, datetime

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_GET

from cargotracker.pathfinder.application.routing import RoutingService
from cargotracker.pathfinder.domain.transit_path import TransitPath

routing_service = RoutingService()


@require_GET
def shortest_path(request: HttpRequest) -> HttpResponse:
    origin = request.GET.get('origin')
    if origin is None or len(origin) != 5:
        return _bad_request(0, origin)
    destination = request.GET.get('destination')
    if destination is None or len(destination) != 5:
        return _bad_request(1, destination)

    paths = routing_service.find_shortest_paths(origin, destination)
    return JsonResponse([_path_payload(path) for path in paths], safe=False)


def _bad_request(parameter_index: int, value: str | None) -> HttpResponse:
    if value is None:
        message = 'may not be null'
        invalid_value = 'null'
    else:
        message = 'size must be between 5 and 5'
        invalid_value = value
    path = (
        '__EJB31_Generated__GraphTraversalService__Intf____Bean__.'
        f'findShortestPath.arg{parameter_index}'
    )
    return HttpResponse(
        f'{message} (path = {path}, invalidValue = {invalid_value})\n',
        status=400,
        content_type='text/plain',
    )


def _path_payload(path: TransitPath) -> dict:
    return {
        'transitEdges': [
            {
                'fromDate': _format_route_date(edge.from_date),
                'fromUnLocode': edge.from_port,
                'toDate': _format_route_date(edge.to_date),
                'toUnLocode': edge.to_port,
                'voyageNumber': edge.voyage_number,
            }
            for edge in path.transit_edges
        ]
    }


def _format_route_date(value: datetime) -> str:
    utc_value = value.replace(tzinfo=UTC) if value.utcoffset() is None else value.astimezone(UTC)
    return utc_value.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
