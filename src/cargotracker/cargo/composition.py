from cargotracker.cargo.application.tracking import TrackingLookup
from cargotracker.cargo.infrastructure.repository import DjangoCargoRepository
from cargotracker.cargo.interfaces.tracking.views import create_tracking_view


def compose_tracking_view():
    return create_tracking_view(TrackingLookup(DjangoCargoRepository()))
