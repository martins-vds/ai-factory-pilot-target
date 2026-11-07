from cargotracker.cargo.application.tracking import TrackingLookup
from cargotracker.cargo.infrastructure.repository import DjangoCargoRepository
from cargotracker.cargo.interfaces.admin_map.views import create_admin_map_views
from cargotracker.cargo.interfaces.tracking.views import create_tracking_view
from cargotracker.handling.infrastructure.repository import DjangoHandlingEventRepository


def compose_admin_map_views():
    return create_admin_map_views(DjangoCargoRepository())


def compose_tracking_view():
    return create_tracking_view(
        TrackingLookup(DjangoCargoRepository(), DjangoHandlingEventRepository())
    )
