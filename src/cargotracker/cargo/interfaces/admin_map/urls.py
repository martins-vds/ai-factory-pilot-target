from django.urls import path

from cargotracker.cargo.interfaces.admin_map import views

urlpatterns = [
    path('', views.live_map, name='admin_live_map'),
    path('markers/', views.live_map_markers, name='admin_live_map_markers'),
]
