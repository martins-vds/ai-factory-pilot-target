from django.shortcuts import render

from cargotracker.cargo.application.tracking import TrackingLookup
from cargotracker.cargo.infrastructure.repository import DjangoCargoRepository
from cargotracker.cargo.interfaces.forms import TrackingForm


def track(request):
    form = TrackingForm(request.POST if request.method == 'POST' else None)
    cargo = None
    message = None

    if form.is_bound:
        if form.is_valid():
            tracking_id = form.cleaned_data['tracking_id']
            cargo = TrackingLookup(DjangoCargoRepository()).find_cargo(tracking_id)
            if cargo is None:
                message = f'Cargo with tracking ID {tracking_id} not found.'
        else:
            message = form.errors['tracking_id'][0]

    context = {'form': form, 'cargo': cargo, 'message': message}
    template = 'tracking/result.html' if request.htmx else 'tracking/track.html'
    return render(request, template, context)
