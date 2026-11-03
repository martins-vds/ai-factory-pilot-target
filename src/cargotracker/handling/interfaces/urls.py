from django.urls import path

from cargotracker.handling.interfaces.rest import submit_handling_report

urlpatterns = [path('reports', submit_handling_report, name='handling-report')]
