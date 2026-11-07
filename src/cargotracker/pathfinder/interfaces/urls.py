from django.urls import path

from cargotracker.pathfinder.interfaces.api import shortest_path

urlpatterns = [
    path('rest/graph-traversal/shortest-path', shortest_path, name='pathfinder-shortest-path'),
]
