# Surviving mutants: BK-05E

Written by `afs-mutation` on its last run (base `origin/main`): score 0.929, threshold 0.8, killed 13, survived 1. Each line is a mutant no test killed: add a test that fails on it, or simplify the code if it is equivalent. The diff under each line is the change mutmut made.

- `src/cargotracker/booking/interfaces/dashboard/views.py:38 Mutant #12`

  ```diff
  @@ -35,7 +35,7 @@
       def cargo_details(request: HttpRequest, tracking_id: str) -> HttpResponse:
           cargo = cargo_repository.find(TrackingId(tracking_id))
           if cargo is None:
  -            raise Http404(f'Cargo with tracking ID {tracking_id} not found.')
  +            raise Http404(f'XXCargo with tracking ID {tracking_id} not found.XX')
           return render(request, 'booking/cargo_details.html', {'cargo': cargo})
       return dashboard, cargo_details
  ```

