from collections.abc import Callable

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from cargotracker.cargo.application.tracking import TrackingLookup
from cargotracker.cargo.interfaces.forms import TrackingForm


def create_tracking_view(lookup: TrackingLookup) -> Callable[[HttpRequest], HttpResponse]:
    def track(request: HttpRequest) -> HttpResponse:
        form = TrackingForm(request.POST if request.method == 'POST' else None)
        cargo = None
        message = None

        if form.is_bound:
            if form.is_valid():
                tracking_id = form.cleaned_data['tracking_id']
                cargo = lookup.find_cargo(tracking_id)
                if cargo is None:
                    message = f'Cargo with tracking ID {tracking_id} not found.'
            else:
                message = form.errors['tracking_id'][0]

        context = {'form': form, 'cargo': cargo, 'message': message}
        template = 'tracking/result.html' if request.htmx else 'tracking/track.html'
        return render(request, template, context)

    return track
