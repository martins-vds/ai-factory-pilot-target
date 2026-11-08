# Surviving mutants: BK-05G

Written by `afs-mutation` on its last run (base `origin/main`): score 0.907, threshold 0.8, killed 49, survived 5. Each line is a mutant no test killed: add a test that fails on it, or simplify the code if it is equivalent. The diff under each line is the change mutmut made.

- `src/cargotracker/booking/interfaces/dialogs/views.py:49 Mutant #21`

  ```diff
  @@ -46,7 +46,7 @@
           destination_value = (
               request.POST.get('destination')
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
  +        destination_error = None
           if request.method == 'POST':
               destination_by_code = {location.unlocode.value: location for location in destinations}
  ```

- `src/cargotracker/booking/interfaces/dialogs/views.py:57 Mutant #30`

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

- `src/cargotracker/booking/interfaces/dialogs/views.py:80 Mutant #44`

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

- `src/cargotracker/booking/interfaces/dialogs/views.py:86 Mutant #48`

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

