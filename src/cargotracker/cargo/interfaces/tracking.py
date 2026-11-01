from django.shortcuts import render

from cargotracker.cargo.interfaces.forms import TrackingForm


def track(request):
    return render(request, 'tracking/track.html', {'form': TrackingForm()})
