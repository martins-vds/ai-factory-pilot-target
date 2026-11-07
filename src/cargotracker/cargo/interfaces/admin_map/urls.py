from django.urls import path

from cargotracker.cargo.composition import compose_admin_map_views

live_map, live_map_markers = compose_admin_map_views()

urlpatterns = [
    path('', live_map, name='admin_live_map'),
    path('markers/', live_map_markers, name='admin_live_map_markers'),
]
