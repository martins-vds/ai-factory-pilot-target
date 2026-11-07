from datetime import UTC, datetime

from django import forms
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_GET

from cargotracker.pathfinder.routing import RoutingService, TransitPath


class _ShortestPathForm(forms.Form):
    origin = forms.CharField(min_length=5, max_length=5, strip=False)
    destination = forms.CharField(min_length=5, max_length=5, strip=False)


routing_service = RoutingService()


@require_GET
def shortest_path(request: HttpRequest) -> HttpResponse:
    form = _ShortestPathForm(request.GET)
    if not form.is_valid():
        errors = {
            field: [error['message'] for error in field_errors]
            for field, field_errors in form.errors.get_json_data().items()
        }
        return JsonResponse({'errors': errors}, status=400)

    paths = routing_service.find_shortest_paths(
        form.cleaned_data['origin'], form.cleaned_data['destination']
    )
    return JsonResponse([_path_payload(path) for path in paths], safe=False)


def _path_payload(path: TransitPath) -> dict:
    return {
        'transitEdges': [
            {
                'voyageNumber': edge.voyage_number,
                'fromUnLocode': edge.from_port,
                'toUnLocode': edge.to_port,
                'fromDate': _format_route_date(edge.from_date),
                'toDate': _format_route_date(edge.to_date),
            }
            for edge in path.transit_edges
        ]
    }


def _format_route_date(value: datetime) -> str:
    utc_value = value.replace(tzinfo=UTC) if value.utcoffset() is None else value.astimezone(UTC)
    return utc_value.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
