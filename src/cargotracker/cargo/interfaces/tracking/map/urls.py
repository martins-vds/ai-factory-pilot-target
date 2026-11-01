from django.urls import path

from cargotracker.cargo.interfaces.tracking.map.views import map_frame

urlpatterns = [
    path('', map_frame, name='cargo_map_frame'),
]
