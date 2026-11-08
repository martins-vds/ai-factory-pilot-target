# Surviving mutants: BK-05H

Written by `afs-mutation` on its last run (base `origin/main`): score 0.763, threshold 0.8, killed 29, survived 9. Each line is a mutant no test killed: add a test that fails on it, or simplify the code if it is equivalent. The diff under each line is the change mutmut made.

- `src/cargotracker/booking/urls.py:21 Mutant #5`

  ```diff
  @@ -18,7 +18,7 @@
   cargo_repository = DjangoCargoRepository()
   handling_event_repository = DjangoHandlingEventRepository()
  -location_repository = DjangoLocationRepository()
  +location_repository = None
   cargo_dashboard = CargoDashboard(cargo_repository)
   booking_wizard = create_booking_wizard_view(
  ```

- `src/cargotracker/booking/urls.py:27 Mutant #7`

  ```diff
  @@ -21,10 +21,7 @@
   location_repository = DjangoLocationRepository()
   cargo_dashboard = CargoDashboard(cargo_repository)
  -booking_wizard = create_booking_wizard_view(
  -    CargoRegistration(cargo_repository),
  -    location_repository.find_all,
  -)
  +booking_wizard = None
   dashboard, cargo_details = create_booking_views(cargo_dashboard)
   route_selection, select_itinerary = create_route_selection_views(
       CargoRouting(
  ```

- `src/cargotracker/booking/urls.py:28 Mutant #8`

  ```diff
  @@ -25,7 +25,7 @@
       CargoRegistration(cargo_repository),
       location_repository.find_all,
   )
  -dashboard, cargo_details = create_booking_views(cargo_dashboard)
  +dashboard, cargo_details = None
   route_selection, select_itinerary = create_route_selection_views(
       CargoRouting(
           cargo_repository,
  ```

- `src/cargotracker/booking/urls.py:38 Mutant #9`

  ```diff
  @@ -26,16 +26,7 @@
       location_repository.find_all,
   )
   dashboard, cargo_details = create_booking_views(cargo_dashboard)
  -route_selection, select_itinerary = create_route_selection_views(
  -    CargoRouting(
  -        cargo_repository,
  -        location_repository,
  -        DjangoVoyageRepository(),
  -        handling_event_repository,
  -        RoutingService(),
  -    ),
  -    cargo_dashboard,
  -)
  +route_selection, select_itinerary = None
  ...
  ```

- `src/cargotracker/booking/urls.py:43 Mutant #10`

  ```diff
  @@ -36,11 +36,7 @@
       ),
       cargo_dashboard,
   )
  -destination_dialog, deadline_dialog = create_dialog_views(
  -    cargo_dashboard,
  -    CargoSpecification(cargo_repository, handling_event_repository),
  -    location_repository.find_all,
  -)
  +destination_dialog, deadline_dialog = None
   urlpatterns = [
       path('booking/', booking_wizard, name='wizard'),
  ```

- `src/cargotracker/urls.py:26 Mutant #6`

  ```diff
  @@ -23,7 +23,7 @@
   urlpatterns = [
       path('', compose_tracking_view(), name='track'),
       path('rest/handling/reports', compose_handling_report_view(), name='handling-report'),
  -    path('', include('cargotracker.booking.urls')),
  +    path('', include('XXcargotracker.booking.urlsXX')),
       path('', include('cargotracker.pathfinder.interfaces.urls')),
       path('tracking/map/', include('cargotracker.cargo.interfaces.tracking.map.urls')),
       path('admin/live-map/', include('cargotracker.cargo.interfaces.admin_map.urls')),
  ```

- `src/cargotracker/urls.py:27 Mutant #8`

  ```diff
  @@ -24,7 +24,7 @@
       path('', compose_tracking_view(), name='track'),
       path('rest/handling/reports', compose_handling_report_view(), name='handling-report'),
       path('', include('cargotracker.booking.urls')),
  -    path('', include('cargotracker.pathfinder.interfaces.urls')),
  +    path('', include('XXcargotracker.pathfinder.interfaces.urlsXX')),
       path('tracking/map/', include('cargotracker.cargo.interfaces.tracking.map.urls')),
       path('admin/live-map/', include('cargotracker.cargo.interfaces.admin_map.urls')),
   ]
  ```

- `src/cargotracker/urls.py:28 Mutant #10`

  ```diff
  @@ -25,7 +25,7 @@
       path('rest/handling/reports', compose_handling_report_view(), name='handling-report'),
       path('', include('cargotracker.booking.urls')),
       path('', include('cargotracker.pathfinder.interfaces.urls')),
  -    path('tracking/map/', include('cargotracker.cargo.interfaces.tracking.map.urls')),
  +    path('tracking/map/', include('XXcargotracker.cargo.interfaces.tracking.map.urlsXX')),
       path('admin/live-map/', include('cargotracker.cargo.interfaces.admin_map.urls')),
   ]
  ```

- `src/cargotracker/urls.py:29 Mutant #12`

  ```diff
  @@ -26,6 +26,6 @@
       path('', include('cargotracker.booking.urls')),
       path('', include('cargotracker.pathfinder.interfaces.urls')),
       path('tracking/map/', include('cargotracker.cargo.interfaces.tracking.map.urls')),
  -    path('admin/live-map/', include('cargotracker.cargo.interfaces.admin_map.urls')),
  +    path('admin/live-map/', include('XXcargotracker.cargo.interfaces.admin_map.urlsXX')),
   ]
  ```

