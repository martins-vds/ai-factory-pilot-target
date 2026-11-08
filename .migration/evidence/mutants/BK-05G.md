# Surviving mutants: BK-05G

Written by `afs-mutation` on its last run (base `origin/main`): score 0.691, threshold 0.8, killed 38, survived 17. Each line is a mutant no test killed: add a test that fails on it, or simplify the code if it is equivalent. The diff under each line is the change mutmut made.

- `src/cargotracker/booking/interfaces/dialogs/views.py:18 Mutant #3`

  ```diff
  @@ -15,7 +15,7 @@
   def _find_cargo(cargo_dashboard: CargoDashboard, tracking_id: str) -> Cargo:
       cargo = cargo_dashboard.get_cargo_details(TrackingId(tracking_id))
       if cargo is None:
  -        raise Http404(f'Cargo with tracking ID {tracking_id} not found.')
  +        raise Http404(f'XXCargo with tracking ID {tracking_id} not found.XX')
       return cargo
  ```

- `src/cargotracker/booking/interfaces/dialogs/views.py:27 Mutant #12`

  ```diff
  @@ -24,7 +24,7 @@
           response = HttpResponse(status=204)
           response['HX-Redirect'] = '/admin/dashboard/'
           return response
  -    return redirect('/admin/dashboard/')
  +    return redirect('XX/admin/dashboard/XX')
   def create_dialog_views(
  ```

- `src/cargotracker/booking/interfaces/dialogs/views.py:47 Mutant #18`

  ```diff
  @@ -44,7 +44,7 @@
               if location not in (route_specification.origin, route_specification.destination)
           ]
           destination_value = (
  -            request.POST.get('destination', '')
  +            request.POST.get('destination', 'XXXX')
               if request.method == 'POST'
               else (destinations[0].unlocode.value if destinations else '')
           )
  ```

- `src/cargotracker/booking/interfaces/dialogs/views.py:48 Mutant #19`

  ```diff
  @@ -45,7 +45,7 @@
           ]
           destination_value = (
               request.POST.get('destination', '')
  -            if request.method == 'POST'
  +            if request.method != 'POST'
               else (destinations[0].unlocode.value if destinations else '')
           )
           destination_error = ''
  ```

- `src/cargotracker/booking/interfaces/dialogs/views.py:48 Mutant #20`

  ```diff
  @@ -45,7 +45,7 @@
           ]
           destination_value = (
               request.POST.get('destination', '')
  -            if request.method == 'POST'
  +            if request.method == 'XXPOSTXX'
               else (destinations[0].unlocode.value if destinations else '')
           )
           destination_error = ''
  ```

- `src/cargotracker/booking/interfaces/dialogs/views.py:49 Mutant #21`

  ```diff
  @@ -46,7 +46,7 @@
           destination_value = (
               request.POST.get('destination', '')
               if request.method == 'POST'
  -            else (destinations[0].unlocode.value if destinations else '')
  +            else (destinations[1].unlocode.value if destinations else '')
           )
           destination_error = ''
  ```

- `src/cargotracker/booking/interfaces/dialogs/views.py:49 Mutant #22`

  ```diff
  @@ -46,7 +46,7 @@
           destination_value = (
               request.POST.get('destination', '')
               if request.method == 'POST'
  -            else (destinations[0].unlocode.value if destinations else '')
  +            else (destinations[0].unlocode.value if destinations else 'XXXX')
           )
           destination_error = ''
  ```

- `src/cargotracker/booking/interfaces/dialogs/views.py:51 Mutant #24`

  ```diff
  @@ -48,7 +48,7 @@
               if request.method == 'POST'
               else (destinations[0].unlocode.value if destinations else '')
           )
  -        destination_error = ''
  +        destination_error = 'XXXX'
           if request.method == 'POST':
               destination_by_code = {location.unlocode.value: location for location in destinations}
  ```

- `src/cargotracker/booking/interfaces/dialogs/views.py:51 Mutant #25`

  ```diff
  @@ -48,7 +48,7 @@
               if request.method == 'POST'
               else (destinations[0].unlocode.value if destinations else '')
           )
  -        destination_error = ''
  +        destination_error = None
           if request.method == 'POST':
               destination_by_code = {location.unlocode.value: location for location in destinations}
  ```

- `src/cargotracker/booking/interfaces/dialogs/views.py:57 Mutant #31`

  ```diff
  @@ -54,7 +54,7 @@
               destination_by_code = {location.unlocode.value: location for location in destinations}
               destination = destination_by_code.get(destination_value)
               if destination is None:
  -                destination_error = 'Select a valid destination.'
  +                destination_error = 'XXSelect a valid destination.XX'
               else:
                   cargo_specification.change_destination(TrackingId(tracking_id), destination)
                   return _complete_dialog_update(request)
  ```

- `src/cargotracker/booking/interfaces/dialogs/views.py:57 Mutant #32`

  ```diff
  @@ -54,7 +54,7 @@
               destination_by_code = {location.unlocode.value: location for location in destinations}
               destination = destination_by_code.get(destination_value)
               if destination is None:
  -                destination_error = 'Select a valid destination.'
  +                destination_error = None
               else:
                   cargo_specification.change_destination(TrackingId(tracking_id), destination)
                   return _complete_dialog_update(request)
  ```

- `src/cargotracker/booking/interfaces/dialogs/views.py:68 Mutant #36`

  ```diff
  @@ -65,7 +65,7 @@
               {
                   'cargo': cargo,
                   'destinations': destinations,
  -                'destination_value': destination_value,
  +                'XXdestination_valueXX': destination_value,
                   'destination_error': destination_error,
               },
           )
  ```

- `src/cargotracker/booking/interfaces/dialogs/views.py:69 Mutant #37`

  ```diff
  @@ -66,7 +66,7 @@
                   'cargo': cargo,
                   'destinations': destinations,
                   'destination_value': destination_value,
  -                'destination_error': destination_error,
  +                'XXdestination_errorXX': destination_error,
               },
           )
  ```

- `src/cargotracker/booking/interfaces/dialogs/views.py:76 Mutant #40`

  ```diff
  @@ -73,7 +73,7 @@
       def deadline_dialog(request: HttpRequest, tracking_id: str) -> HttpResponse:
           cargo = _find_cargo(cargo_dashboard, tracking_id)
           deadline_value = (
  -            request.POST.get('deadline', '')
  +            request.POST.get('deadline', 'XXXX')
               if request.method == 'POST'
               else cargo.route_specification.arrival_deadline.date().isoformat()
           )
  ```

- `src/cargotracker/booking/interfaces/dialogs/views.py:80 Mutant #44`

  ```diff
  @@ -77,7 +77,7 @@
               if request.method == 'POST'
               else cargo.route_specification.arrival_deadline.date().isoformat()
           )
  -        deadline_error = ''
  +        deadline_error = 'XXXX'
           if request.method == 'POST':
               try:
  ```

- `src/cargotracker/booking/interfaces/dialogs/views.py:80 Mutant #45`

  ```diff
  @@ -77,7 +77,7 @@
               if request.method == 'POST'
               else cargo.route_specification.arrival_deadline.date().isoformat()
           )
  -        deadline_error = ''
  +        deadline_error = None
           if request.method == 'POST':
               try:
  ```

- `src/cargotracker/booking/interfaces/dialogs/views.py:86 Mutant #49`

  ```diff
  @@ -83,7 +83,7 @@
               try:
                   arrival_date = date.fromisoformat(deadline_value)
               except ValueError:
  -                deadline_error = 'Enter a valid arrival deadline.'
  +                deadline_error = 'XXEnter a valid arrival deadline.XX'
               else:
                   arrival_deadline = timezone.make_aware(datetime.combine(arrival_date, time.min))
                   cargo_specification.change_deadline(TrackingId(tracking_id), arrival_deadline)
  ```

