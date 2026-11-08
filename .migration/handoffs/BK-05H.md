## Handoff — afs-migrator · 2026-11-08T02:50:56Z
**State:** blocked · **Branch / PR:** `copilot/bk-05h-wire-booking-pathfinder-urls` / no PR found · **Last code commit:** `fbb76e13746e590e31d27d3532e5ab29a9a14a21`

### Done
- Registered the booking wizard, dashboard, cargo details, route-selection, itinerary, and dialog endpoints.
- Named the cargo-details route `booking:cargo-details` for AM-04D; included the existing pathfinder URLconf at root, preserving `/rest/graph-traversal/shortest-path`.
- `pytest -q tests/booking/test_urls.py` passed (4 tests) after strengthening endpoint coverage; see `.migration/evidence/runs/BK-05H.md`.
- Build checks passed (`compileall`, Django check); Ruff check and format passed.
- CRAP gate passed: max 26.0, threshold 30, 0 over-threshold methods.
- CodeQL reported no alerts.

### Remaining
- [ ] Resolve the nine surviving changed-code mutants and reach the profile threshold of 0.8.
- [ ] Run the full behavior and regression suites, CRAP, and final verification after resolving mutation survivors.
- [ ] Update and validate the return file with final gate results and the PR link once available.

### Decisions made
- The cargo-details route name is `booking:cargo-details`, with path `/admin/cargo/<tracking_id>/`.
- Other route patterns follow the existing booking template paths and remain provisional as stated in the approved plan.

### Blockers / questions
- The mutation gate failed twice; the migration contract stop rule requires stopping after two failed attempts on the same failure. The latest result is 0.763 (29 killed, 9 survived; threshold 0.8). Survivors are recorded in `.migration/evidence/mutants/BK-05H.md`.
- No PR was found for the working branch; `pr` is `null` until one exists.

### Failing commands
- `.migration/harness/tools/afs-run --ticket BK-05H --name mutation-changed -- python .migration/harness/tools/afs-mutation --changed-since origin/main` → exit 1, score 0.289; see `.migration/runs/BK-05H/20261108T024402086443Z-mutation-changed.log`.
- `.migration/harness/tools/afs-run --ticket BK-05H --name mutation-changed -- python .migration/harness/tools/afs-mutation --changed-since origin/main` → exit 1, score 0.763; see `.migration/runs/BK-05H/20261108T024709005157Z-mutation-changed.log`.

### Next step for the next session
Re-run setup, inspect the committed survivor diffs and mutation test selection, then make the smallest test or implementation adjustment that kills the remaining mutants. Rerun the exact profile mutation gate to at least 0.8, then run the remaining gates, update the return file, and validate `.migration`.

## Handoff — afs-migrator · 2026-11-08T04:05:48Z
**State:** blocked · **Branch / PR:** `copilot/bk-05h-fix-changed-code-mutation` (child of PR #419 head; no PR for this branch) · **Last commit:** `0e06252`

### Done
- Added callable-view assertions for booking, tracking, handling, map, admin-map and pathfinder URL resolution in `tests/booking/test_urls.py`; the targeted suite passes (4 tests), see `.migration/runs/BK-05H/20261108T035822617155Z-urls-targeted.log`.
- Build, behavior, idiom, CRAP and regression gates pass through `afs-run`; details are in `.migration/evidence/runs/BK-05H.md`. Behavior/regression each report 490 passed; CRAP max is 26.0 (threshold 30, zero over).
- Cargo details remains named `booking:cargo-details` at `/admin/cargo/<tracking_id>/`.

### Remaining
- [ ] Resolve the nine surviving changed-code mutants and reach 0.8; classify each survivor below as a missing-test gap (none appears equivalent).
- [ ] Validate the return and migration state after the mutation issue is resolved.

### Decisions made
- All nine diffs remove a required repository/view/URLconf registration and are classified as **missing tests**, not equivalent mutants. The new callable-view assertions did not change the official mutation score; the next session should investigate why the exact gate still reports these diffs as survivors before making another change.

### Blockers / questions
- The exact profile mutation gate returned 0.763 twice in this session after the focused test change. The same failure has repeated twice, so the migration-contract stop rule fires. Each survivor and its diff is listed here; the full generated report is `.migration/evidence/mutants/BK-05H.md`.
  - `src/cargotracker/booking/urls.py:21`, Mutant #5: `location_repository = DjangoLocationRepository()` → `location_repository = None`. **Missing test:** prove booking URL registration initializes dependencies and exposes resolvable wizard, routing and dialog views.
  - `src/cargotracker/booking/urls.py:27`, Mutant #7: `booking_wizard = create_booking_wizard_view(CargoRegistration(...), location_repository.find_all)` → `booking_wizard = None`. **Missing test:** resolve `/booking/` to a callable view and verify its supported method.
  - `src/cargotracker/booking/urls.py:28`, Mutant #8: `dashboard, cargo_details = create_booking_views(cargo_dashboard)` → `dashboard, cargo_details = None`. **Missing test:** resolve dashboard and cargo-details routes to callable views and verify dispatch/method behavior.
  - `src/cargotracker/booking/urls.py:38`, Mutant #9: `route_selection, select_itinerary = create_route_selection_views(...)` → `route_selection, select_itinerary = None`. **Missing test:** resolve route-selection and itinerary routes to callable views and verify supported methods.
  - `src/cargotracker/booking/urls.py:43`, Mutant #10: `destination_dialog, deadline_dialog = create_dialog_views(...)` → `destination_dialog, deadline_dialog = None`. **Missing test:** resolve destination/deadline routes to callable views and verify supported methods.
  - `src/cargotracker/urls.py:26`, Mutant #6: `include('cargotracker.booking.urls')` → `include('XXcargotracker.booking.urlsXX')`. **Missing test:** directly resolve and dispatch the booking endpoints through the project root URLconf.
  - `src/cargotracker/urls.py:27`, Mutant #8: `include('cargotracker.pathfinder.interfaces.urls')` → `include('XXcargotracker.pathfinder.interfaces.urlsXX')`. **Missing test:** resolve and dispatch the pathfinder endpoint through the project root URLconf.
  - `src/cargotracker/urls.py:28`, Mutant #10: `include('cargotracker.cargo.interfaces.tracking.map.urls')` → `include('XXcargotracker.cargo.interfaces.tracking.map.urlsXX')`. **Missing test:** resolve and dispatch the map endpoint through the project root URLconf.
  - `src/cargotracker/urls.py:29`, Mutant #12: `include('cargotracker.cargo.interfaces.admin_map.urls')` → `include('XXcargotracker.cargo.interfaces.admin_map.urlsXX')`. **Missing test:** resolve and dispatch the live-map endpoints through the project root URLconf.

### Failing commands
- `.migration/harness/tools/afs-run --ticket BK-05H --name mutation-changed -- python .migration/harness/tools/afs-mutation --changed-since origin/main` → exit 1, score 0.763, see `.migration/runs/BK-05H/20261108T035514881824Z-mutation-changed.log`.
- Same command after URL-test changes → exit 1, score 0.763, see `.migration/runs/BK-05H/20261108T035828842981Z-mutation-changed.log`.

### Next step for the next session
Re-run setup, inspect the exact mutation runner and its selected test node IDs against these nine diffs, then add a focused test that demonstrably kills at least one survivor in the profile gate. Continue one test/change at a time; stop and hand off again if the score remains below 0.8 after two honest attempts.
