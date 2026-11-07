# Surviving mutants: BK-05F

Written by `afs-mutation` on its last run (base `origin/main`): score 0.803, threshold 0.8, killed 49, survived 12. Each line is a mutant no test killed: add a test that fails on it, or simplify the code if it is equivalent. The diff under each line is the change mutmut made.

- `src/cargotracker/booking/interfaces/route_selection/views.py:21 Mutant #1`

  ```diff
  @@ -18,7 +18,7 @@
   from cargotracker.voyage.domain.voyage import Voyage
   from cargotracker.voyage.domain.voyage_number import VoyageNumber
  -_CANDIDATE_SALT = 'booking.route_selection'
  +_CANDIDATE_SALT = 'XXbooking.route_selectionXX'
   def create_route_selection_views(
  ```

- `src/cargotracker/booking/interfaces/route_selection/views.py:21 Mutant #2`

  ```diff
  @@ -18,7 +18,7 @@
   from cargotracker.voyage.domain.voyage import Voyage
   from cargotracker.voyage.domain.voyage_number import VoyageNumber
  -_CANDIDATE_SALT = 'booking.route_selection'
  +_CANDIDATE_SALT = None
   def create_route_selection_views(
  ```

- `src/cargotracker/booking/interfaces/route_selection/views.py:28 Mutant #5`

  ```diff
  @@ -25,7 +25,7 @@
       cargo_routing: CargoRouting,
       cargo_dashboard: CargoDashboard,
   ) -> tuple[Callable[[HttpRequest, str], HttpResponse], Callable[[HttpRequest, str], HttpResponse]]:
  -    @require_http_methods(['GET', 'POST'])
  +
       def route_selection(request: HttpRequest, tracking_id: str) -> HttpResponse:
           if request.method == 'POST':
               cargo = cargo_dashboard.get_cargo_details(TrackingId(tracking_id))
  ```

- `src/cargotracker/booking/interfaces/route_selection/views.py:33 Mutant #10`

  ```diff
  @@ -30,7 +30,7 @@
           if request.method == 'POST':
               cargo = cargo_dashboard.get_cargo_details(TrackingId(tracking_id))
               if cargo is None:
  -                raise Http404(f'Cargo with tracking ID {tracking_id} not found.')
  +                raise Http404(f'XXCargo with tracking ID {tracking_id} not found.XX')
               itinerary = _selected_itinerary(request, tracking_id)
               if not cargo.route_specification.is_satisfied_by(itinerary):
                   raise Http404('The selected route no longer satisfies the route specification.')
  ```

- `src/cargotracker/booking/interfaces/route_selection/views.py:36 Mutant #13`

  ```diff
  @@ -33,7 +33,7 @@
                   raise Http404(f'Cargo with tracking ID {tracking_id} not found.')
               itinerary = _selected_itinerary(request, tracking_id)
               if not cargo.route_specification.is_satisfied_by(itinerary):
  -                raise Http404('The selected route no longer satisfies the route specification.')
  +                raise Http404('XXThe selected route no longer satisfies the route specification.XX')
               cargo_routing.assign_route(TrackingId(tracking_id), itinerary)
               return redirect(f'/admin/cargo/{tracking_id}/')
           context = _selection_context(
  ```

- `src/cargotracker/booking/interfaces/route_selection/views.py:43 Mutant #15`

  ```diff
  @@ -40,7 +40,7 @@
               cargo_routing,
               cargo_dashboard,
               tracking_id,
  -            'Try setting an arrival deadline further into the future.',
  +            'XXTry setting an arrival deadline further into the future.XX',
           )
           return render(request, 'booking/route_selection/route.html', context)
  ```

- `src/cargotracker/booking/interfaces/route_selection/views.py:47 Mutant #19`

  ```diff
  @@ -44,7 +44,6 @@
           )
           return render(request, 'booking/route_selection/route.html', context)
  -    @require_http_methods(['GET'])
       def select_itinerary(request: HttpRequest, tracking_id: str) -> HttpResponse:
           context = _selection_context(
               cargo_routing,
  ```

- `src/cargotracker/booking/interfaces/route_selection/views.py:53 Mutant #20`

  ```diff
  @@ -50,7 +50,7 @@
               cargo_routing,
               cargo_dashboard,
               tracking_id,
  -            'Try setting the arrival deadline further into the future (a few weeks at least).',
  +            'XXTry setting the arrival deadline further into the future (a few weeks at least).XX',
           )
           return render(request, 'booking/route_selection/select_itinerary.html', context)
  ```

- `src/cargotracker/booking/interfaces/route_selection/views.py:69 Mutant #26`

  ```diff
  @@ -66,7 +66,7 @@
       tracking_id = TrackingId(tracking_id_value)
       cargo = cargo_dashboard.get_cargo_details(tracking_id)
       if cargo is None:
  -        raise Http404(f'Cargo with tracking ID {tracking_id} not found.')
  +        raise Http404(f'XXCargo with tracking ID {tracking_id} not found.XX')
       itineraries = cargo_routing.route_candidates(tracking_id)
       return {
           'cargo': cargo,
  ```

- `src/cargotracker/booking/interfaces/route_selection/views.py:94 Mutant #39`

  ```diff
  @@ -91,7 +91,7 @@
   def _selected_itinerary(request: HttpRequest, tracking_id: str) -> Itinerary:
       try:
  -        candidate = signing.loads(request.POST.get('candidate', ''), salt=_CANDIDATE_SALT)
  +        candidate = signing.loads(request.POST.get('candidate', 'XXXX'), salt=_CANDIDATE_SALT)
           if candidate['tracking_id'] != tracking_id:
               raise BadSignature('Candidate belongs to another cargo.')
           return _deserialize_itinerary(candidate['legs'])
  ```

- `src/cargotracker/booking/interfaces/route_selection/views.py:96 Mutant #43`

  ```diff
  @@ -93,7 +93,7 @@
       try:
           candidate = signing.loads(request.POST.get('candidate', ''), salt=_CANDIDATE_SALT)
           if candidate['tracking_id'] != tracking_id:
  -            raise BadSignature('Candidate belongs to another cargo.')
  +            raise BadSignature('XXCandidate belongs to another cargo.XX')
           return _deserialize_itinerary(candidate['legs'])
       except (BadSignature, KeyError, TypeError, ValueError) as error:
           raise Http404('The selected route is invalid.') from error
  ```

- `src/cargotracker/booking/interfaces/route_selection/views.py:99 Mutant #45`

  ```diff
  @@ -96,7 +96,7 @@
               raise BadSignature('Candidate belongs to another cargo.')
           return _deserialize_itinerary(candidate['legs'])
       except (BadSignature, KeyError, TypeError, ValueError) as error:
  -        raise Http404('The selected route is invalid.') from error
  +        raise Http404('XXThe selected route is invalid.XX') from error
   def _serialize_itinerary(itinerary: Itinerary) -> list[dict]:
  ```

