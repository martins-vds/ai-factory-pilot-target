from collections.abc import Callable

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from cargotracker.cargo.application.tracking import TrackingLookup
from cargotracker.cargo.interfaces.forms import TrackingForm
from cargotracker.cargo.interfaces.tracking.eta import format_eta
from cargotracker.cargo.interfaces.tracking.history import get_history_rows
from cargotracker.cargo.interfaces.tracking.map.adapter import map_frame_url
from cargotracker.cargo.interfaces.tracking.next_activity import get_next_activity_text
from cargotracker.cargo.interfaces.tracking.status_text import get_status_text


def create_tracking_view(lookup: TrackingLookup) -> Callable[[HttpRequest], HttpResponse]:
    def track(request: HttpRequest) -> HttpResponse:
        form = TrackingForm(request.POST if request.method == 'POST' else None)
        context = {'form': form}

        if form.is_bound:
            if form.is_valid():
                tracking_id = form.cleaned_data['tracking_id']
                cargo = lookup.find_cargo(tracking_id)
                if cargo is None:
                    context['message'] = f'Cargo with tracking ID {tracking_id} not found.'
                else:
                    history = lookup.find_handling_history(cargo)
                    context.update(
                        cargo=cargo,
                        status_text=get_status_text(cargo),
                        eta=format_eta(cargo),
                        map_url=map_frame_url(cargo),
                        history_rows=get_history_rows(cargo, history),
                        next_activity_text=get_next_activity_text(
                            cargo.delivery.next_expected_activity
                        ),
                        misdirected=cargo.delivery.misdirected,
                    )
            else:
                context['message'] = form.errors['tracking_id'][0]

        template = 'tracking/result.html' if request.htmx else 'tracking/track.html'
        return render(request, template, context)

    return track
