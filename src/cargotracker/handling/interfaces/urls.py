from django.urls import path

from cargotracker.handling.composition import compose_handling_report_view

urlpatterns = [path('reports', compose_handling_report_view(), name='handling-report')]
