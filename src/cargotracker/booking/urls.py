from django.urls import path

from cargotracker.booking.application.dashboard import CargoDashboard
from cargotracker.booking.application.registration import CargoRegistration
from cargotracker.booking.application.routing import CargoRouting
from cargotracker.booking.application.specification import CargoSpecification
from cargotracker.booking.interfaces.dashboard.views import create_booking_views
from cargotracker.booking.interfaces.dialogs.views import create_dialog_views
from cargotracker.booking.interfaces.route_selection.views import create_route_selection_views
from cargotracker.booking.interfaces.wizard.views import create_booking_wizard_view
from cargotracker.cargo.infrastructure.repository import DjangoCargoRepository
from cargotracker.handling.infrastructure.repository import DjangoHandlingEventRepository
from cargotracker.location.infrastructure.repository import DjangoLocationRepository
from cargotracker.pathfinder.application.routing import RoutingService
from cargotracker.voyage.infrastructure.repository import DjangoVoyageRepository

app_name = 'booking'

cargo_repository = DjangoCargoRepository()
handling_event_repository = DjangoHandlingEventRepository()
location_repository = DjangoLocationRepository()
cargo_dashboard = CargoDashboard(cargo_repository)

booking_wizard = create_booking_wizard_view(
    CargoRegistration(cargo_repository),
    location_repository.find_all,
)
dashboard, cargo_details = create_booking_views(cargo_dashboard)
route_selection, select_itinerary = create_route_selection_views(
    CargoRouting(
        cargo_repository,
        location_repository,
        DjangoVoyageRepository(),
        handling_event_repository,
        RoutingService(),
    ),
    cargo_dashboard,
)
destination_dialog, deadline_dialog = create_dialog_views(
    cargo_dashboard,
    CargoSpecification(cargo_repository, handling_event_repository),
    location_repository.find_all,
)

urlpatterns = [
    path('booking/', booking_wizard, name='wizard'),
    path('admin/dashboard/', dashboard, name='dashboard'),
    path('admin/cargo/<str:tracking_id>/', cargo_details, name='cargo-details'),
    path('admin/cargo/<str:tracking_id>/route/', route_selection, name='route-selection'),
    path('admin/cargo/<str:tracking_id>/itineraries/', select_itinerary, name='select-itinerary'),
    path(
        'admin/cargo/<str:tracking_id>/destination/',
        destination_dialog,
        name='destination-dialog',
    ),
    path(
        'admin/cargo/<str:tracking_id>/deadline/',
        deadline_dialog,
        name='deadline-dialog',
    ),
]
