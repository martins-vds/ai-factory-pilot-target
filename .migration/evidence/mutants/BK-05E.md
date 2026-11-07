# Surviving mutants: BK-05E

Written by `afs-mutation` on its last run (base `origin/main`): score 0.889, threshold 0.8, killed 16, survived 2. Each line is a mutant no test killed: add a test that fails on it, or simplify the code if it is equivalent. The diff under each line is the change mutmut made.

- `src/cargotracker/booking/application/dashboard.py:9 Mutant #1`

  ```diff
  @@ -6,7 +6,7 @@
   from cargotracker.cargo.domain.tracking_id import TrackingId
  -@dataclass(frozen=True)
  +@dataclass(frozen=False)
   class DashboardCargos:
       routed_cargos: list[Cargo]
       not_routed_cargos: list[Cargo]
  ```

- `src/cargotracker/booking/interfaces/dashboard/views.py:28 Mutant #8`

  ```diff
  @@ -25,7 +25,7 @@
       def cargo_details(request: HttpRequest, tracking_id: str) -> HttpResponse:
           cargo = cargo_dashboard.get_cargo_details(TrackingId(tracking_id))
           if cargo is None:
  -            raise Http404(f'Cargo with tracking ID {tracking_id} not found.')
  +            raise Http404(f'XXCargo with tracking ID {tracking_id} not found.XX')
           return render(request, 'booking/cargo_details.html', {'cargo': cargo})
       return dashboard, cargo_details
  ```

