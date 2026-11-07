from collections.abc import Callable
from datetime import datetime
from urllib.parse import quote

from django.core import signing
from django.core.signing import BadSignature
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from cargotracker.booking.application.dashboard import CargoDashboard
from cargotracker.booking.application.routing import CargoRouting
from cargotracker.cargo.domain.itinerary import Itinerary
from cargotracker.cargo.domain.leg import Leg
from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.location.domain.location import Location
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.voyage.domain.schedule import Schedule
from cargotracker.voyage.domain.voyage import Voyage
from cargotracker.voyage.domain.voyage_number import VoyageNumber

_CANDIDATE_SALT = 'booking.route_selection'


def create_route_selection_views(
    cargo_routing: CargoRouting,
    cargo_dashboard: CargoDashboard,
) -> tuple[Callable[[HttpRequest, str], HttpResponse], Callable[[HttpRequest, str], HttpResponse]]:
    @require_http_methods(['GET', 'POST'])
    def route_selection(request: HttpRequest, tracking_id: str) -> HttpResponse:
        if request.method == 'POST':
            cargo = cargo_dashboard.get_cargo_details(TrackingId(tracking_id))
            if cargo is None:
                raise Http404(f'Cargo with tracking ID {tracking_id} not found.')
            itinerary = _selected_itinerary(request, tracking_id)
            if not cargo.route_specification.is_satisfied_by(itinerary):
                raise Http404('The selected route no longer satisfies the route specification.')
            cargo_routing.assign_route(TrackingId(tracking_id), itinerary)
            return redirect(f'/admin/cargo/{quote(tracking_id, safe="")}/')
        context = _selection_context(
            cargo_routing,
            cargo_dashboard,
            tracking_id,
            'Try setting an arrival deadline further into the future.',
        )
        return render(request, 'booking/route_selection/route.html', context)

    @require_http_methods(['GET'])
    def select_itinerary(request: HttpRequest, tracking_id: str) -> HttpResponse:
        context = _selection_context(
            cargo_routing,
            cargo_dashboard,
            tracking_id,
            'Try setting the arrival deadline further into the future (a few weeks at least).',
        )
        return render(request, 'booking/route_selection/select_itinerary.html', context)

    return route_selection, select_itinerary


def _selection_context(
    cargo_routing: CargoRouting,
    cargo_dashboard: CargoDashboard,
    tracking_id_value: str,
    no_route_guidance: str,
) -> dict:
    tracking_id = TrackingId(tracking_id_value)
    cargo = cargo_dashboard.get_cargo_details(tracking_id)
    if cargo is None:
        raise Http404(f'Cargo with tracking ID {tracking_id} not found.')
    itineraries = cargo_routing.route_candidates(tracking_id)
    return {
        'cargo': cargo,
        'candidate_count': len(itineraries),
        'no_route_guidance': no_route_guidance,
        'routes': [
            {
                'itinerary': itinerary,
                'number': number,
                'token': signing.dumps(
                    {
                        'tracking_id': tracking_id.value,
                        'legs': _serialize_itinerary(itinerary),
                    },
                    salt=_CANDIDATE_SALT,
                ),
            }
            for number, itinerary in enumerate(itineraries, start=1)
        ],
    }


def _selected_itinerary(request: HttpRequest, tracking_id: str) -> Itinerary:
    try:
        candidate = signing.loads(request.POST.get('candidate', ''), salt=_CANDIDATE_SALT)
        if candidate['tracking_id'] != tracking_id:
            raise BadSignature('Candidate belongs to another cargo.')
        return _deserialize_itinerary(candidate['legs'])
    except (BadSignature, KeyError, TypeError, ValueError) as error:
        raise Http404('The selected route is invalid.') from error


def _serialize_itinerary(itinerary: Itinerary) -> list[dict]:
    return [
        {
            'voyage_number': leg.voyage.voyage_number.value,
            'load_location': {
                'unlocode': leg.load_location.unlocode.value,
                'name': leg.load_location.name,
            },
            'unload_location': {
                'unlocode': leg.unload_location.unlocode.value,
                'name': leg.unload_location.name,
            },
            'load_time': leg.load_time.isoformat(),
            'unload_time': leg.unload_time.isoformat(),
        }
        for leg in itinerary.legs
    ]


def _deserialize_itinerary(legs: list[dict]) -> Itinerary:
    return Itinerary(
        tuple(
            Leg(
                Voyage(VoyageNumber(leg['voyage_number']), Schedule.EMPTY),
                _deserialize_location(leg['load_location']),
                _deserialize_location(leg['unload_location']),
                datetime.fromisoformat(leg['load_time']),
                datetime.fromisoformat(leg['unload_time']),
            )
            for leg in legs
        )
    )


def _deserialize_location(value: dict) -> Location:
    return Location(UnLocode(value['unlocode']), value['name'])
