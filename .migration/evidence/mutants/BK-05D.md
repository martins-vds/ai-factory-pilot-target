# Surviving mutants: BK-05D

Written by `afs-mutation` on its last run (base `origin/main`): score 0.876, threshold 0.8, killed 134, survived 19. Each line is a mutant no test killed: add a test that fails on it, or simplify the code if it is equivalent. The diff under each line is the change mutmut made.

- `src/cargotracker/booking/interfaces/wizard/views.py:31 Mutant #8`

  ```diff
  @@ -28,7 +28,7 @@
       try:
           deadline = date.fromisoformat(value)
       except ValueError:
  -        return None, None, 'Enter a valid arrival deadline.'
  +        return None, None, 'XXEnter a valid arrival deadline.XX'
       if deadline < today:
           return None, None, 'Arrival deadline cannot be before today.'
       duration = timedelta(days=(deadline - today).days, hours=4).days
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:33 Mutant #10`

  ```diff
  @@ -30,7 +30,7 @@
       except ValueError:
           return None, None, 'Enter a valid arrival deadline.'
       if deadline < today:
  -        return None, None, 'Arrival deadline cannot be before today.'
  +        return None, None, 'XXArrival deadline cannot be before today.XX'
       duration = timedelta(days=(deadline - today).days, hours=4).days
       return deadline, duration, ''
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:34 Mutant #12`

  ```diff
  @@ -31,7 +31,7 @@
           return None, None, 'Enter a valid arrival deadline.'
       if deadline < today:
           return None, None, 'Arrival deadline cannot be before today.'
  -    duration = timedelta(days=(deadline - today).days, hours=4).days
  +    duration = timedelta(days=(deadline - today).days, hours=5).days
       return deadline, duration, ''
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:61 Mutant #25`

  ```diff
  @@ -58,7 +58,7 @@
       locations: list[Location],
       origin: Location | None,
       destination: Location | None,
  -    deadline_value: str = '',
  +    deadline_value: str = 'XXXX',
       error: str = '',
   ) -> HttpResponse:
       context = {
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:98 Mutant #53`

  ```diff
  @@ -95,7 +95,7 @@
   ) -> HttpResponse:
       deadline_value = request.POST.get('deadline', '')
       context = _deadline_context(origin, destination, deadline_value, timezone.localdate())
  -    context['validation_error'] = ''
  +    context['XXvalidation_errorXX'] = ''
       if request.POST.get('action') == 'book':
           if origin is None or destination is None:
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:98 Mutant #55`

  ```diff
  @@ -95,7 +95,7 @@
   ) -> HttpResponse:
       deadline_value = request.POST.get('deadline', '')
       context = _deadline_context(origin, destination, deadline_value, timezone.localdate())
  -    context['validation_error'] = ''
  +    context['validation_error'] = None
       if request.POST.get('action') == 'book':
           if origin is None or destination is None:
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:102 Mutant #63`

  ```diff
  @@ -99,7 +99,7 @@
       if request.POST.get('action') == 'book':
           if origin is None or destination is None:
  -            context['validation_error'] = 'Choose an origin and destination.'
  +            context['validation_error'] = 'XXChoose an origin and destination.XX'
           elif origin == destination:
               context['validation_error'] = 'Origin and destination cannot be the same.'
           elif context['deadline'] is None:
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:104 Mutant #67`

  ```diff
  @@ -101,7 +101,7 @@
           if origin is None or destination is None:
               context['validation_error'] = 'Choose an origin and destination.'
           elif origin == destination:
  -            context['validation_error'] = 'Origin and destination cannot be the same.'
  +            context['validation_error'] = 'XXOrigin and destination cannot be the same.XX'
           elif context['deadline'] is None:
               context['validation_error'] = context['deadline_error'] or 'Choose an arrival deadline.'
           elif context['bookable']:
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:106 Mutant #73`

  ```diff
  @@ -103,7 +103,7 @@
           elif origin == destination:
               context['validation_error'] = 'Origin and destination cannot be the same.'
           elif context['deadline'] is None:
  -            context['validation_error'] = context['deadline_error'] or 'Choose an arrival deadline.'
  +            context['validation_error'] = context['deadline_error'] or 'XXChoose an arrival deadline.XX'
           elif context['bookable']:
               registration.register(
                   origin,
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:131 Mutant #89`

  ```diff
  @@ -128,7 +128,7 @@
           available_locations = list_shipping_locations()
           location_by_code = {location.unlocode.value: location for location in available_locations}
           data = request.POST
  -        origin = location_by_code.get(data.get('origin', ''))
  +        origin = location_by_code.get(data.get('origin', 'XXXX'))
           destination = location_by_code.get(data.get('destination', ''))
           deadline_value = data.get('deadline', '')
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:132 Mutant #92`

  ```diff
  @@ -129,7 +129,7 @@
           location_by_code = {location.unlocode.value: location for location in available_locations}
           data = request.POST
           origin = location_by_code.get(data.get('origin', ''))
  -        destination = location_by_code.get(data.get('destination', ''))
  +        destination = location_by_code.get(data.get('destination', 'XXXX'))
           deadline_value = data.get('deadline', '')
           if request.method != 'POST':
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:143 Mutant #104`

  ```diff
  @@ -140,7 +140,7 @@
               )
           if data.get('action') == 'cancel':
               return redirect('/admin/dashboard/')
  -        if data.get('step') == 'destination' and data.get('action') == 'back':
  +        if data.get('XXstepXX') == 'destination' and data.get('action') == 'back':
               return _origin_step(request, available_locations, origin, destination, deadline_value)
           if data.get('step') == 'deadline' and data.get('action') == 'back':
               return _destination_step(
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:143 Mutant #106`

  ```diff
  @@ -140,7 +140,7 @@
               )
           if data.get('action') == 'cancel':
               return redirect('/admin/dashboard/')
  -        if data.get('step') == 'destination' and data.get('action') == 'back':
  +        if data.get('step') == 'XXdestinationXX' and data.get('action') == 'back':
               return _origin_step(request, available_locations, origin, destination, deadline_value)
           if data.get('step') == 'deadline' and data.get('action') == 'back':
               return _destination_step(
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:143 Mutant #107`

  ```diff
  @@ -140,7 +140,7 @@
               )
           if data.get('action') == 'cancel':
               return redirect('/admin/dashboard/')
  -        if data.get('step') == 'destination' and data.get('action') == 'back':
  +        if data.get('step') == 'destination' and data.get('XXactionXX') == 'back':
               return _origin_step(request, available_locations, origin, destination, deadline_value)
           if data.get('step') == 'deadline' and data.get('action') == 'back':
               return _destination_step(
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:143 Mutant #109`

  ```diff
  @@ -140,7 +140,7 @@
               )
           if data.get('action') == 'cancel':
               return redirect('/admin/dashboard/')
  -        if data.get('step') == 'destination' and data.get('action') == 'back':
  +        if data.get('step') == 'destination' and data.get('action') == 'XXbackXX':
               return _origin_step(request, available_locations, origin, destination, deadline_value)
           if data.get('step') == 'deadline' and data.get('action') == 'back':
               return _destination_step(
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:150 Mutant #121`

  ```diff
  @@ -147,7 +147,7 @@
                   request, available_locations, origin, destination, deadline_value
               )
           if (
  -            data.get('step') in {'origin', 'destination'}
  +            data.get('step') in {'origin', 'XXdestinationXX'}
               and data.get('action') == 'next'
               and origin is None
           ):
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:160 Mutant #127`

  ```diff
  @@ -157,7 +157,7 @@
                   None,
                   destination,
                   deadline_value,
  -                'Select a valid origin.',
  +                'XXSelect a valid origin.XX',
               )
           if data.get('step') == 'origin' and data.get('action') == 'next':
               if destination is None or destination == origin:
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:168 Mutant #146`

  ```diff
  @@ -165,7 +165,7 @@
               return _destination_step(
                   request, available_locations, origin, destination, deadline_value
               )
  -        if data.get('step') == 'destination' and data.get('action') == 'next':
  +        if data.get('step') == 'destination' or data.get('action') == 'next':
               if destination is None:
                   return _destination_step(
                       request,
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:176 Mutant #148`

  ```diff
  @@ -173,7 +173,7 @@
                       origin,
                       None,
                       deadline_value,
  -                    'Select a valid destination.',
  +                    'XXSelect a valid destination.XX',
                   )
               context = _deadline_context(origin, destination, deadline_value, timezone.localdate())
               return render(request, 'booking/wizard/deadline.html', context)
  ```

