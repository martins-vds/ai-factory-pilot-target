## Handoff — afs-specialist-migrator · 2026-11-07T23:10:28Z
**State:** blocked · **Branch / PR:** `copilot/am-04d-render-marker-partial` / PR not yet available · **Last commit:** `d1f73b9`

### Done
- Loaded the migration contract and UI guidance; setup passed. The source is pinned at `f3beacf78de4f6d34edc4971ac87e38a5c6fe59d`, read-only and ignored; target ancestry is complete; migration validation, input checks, setup probe, DB health, RTK, and Python runtime checks passed.
- Recorded the setup probe in `.migration/evidence/runs/AM-04D.md`.
- Read the approved marker design and confirmed #253 is resolved: `NOT_RECEIVED` uses its origin and reports `Last known location: Unknown`.
- Confirmed the booking details implementation exists (BK-05E return, issue #292 / PR #385), but its URL is not registered in the application's URL configuration. `src/cargotracker/urls.py` registers no booking route; `/admin/cargo/<tracking_id>/` appears only in a test URLconf and has no route name.

### Remaining
- [ ] Resolve the production BK-05 cargo-details route and expose a stable named route usable by the marker template.
- [ ] Resume AM-04D: test first, implement only `templates/admin/_live_map_markers.html` and `tests/cargo/interfaces/test_admin_live_map_markers.py`, then run required gates via `afs-run`.
- [ ] Update the return file with the resulting evidence and PR.

### Decisions made
- Did not edit the partial or its tests because the approved design says not to implement against a guessed booking URL; the booking URL is not currently registered or named.
- Did not change application URL wiring because it is outside this ticket's two-file scope.

### Blockers / questions
- The issue describes the booking cargo-details ticket as unpublished, while this checkout contains a completed BK-05E return. However, the production route remains absent, so the marker click-through cannot yet be implemented against a resolved target route.
- The operator/booking owner must publish or register the cargo-details route and provide its stable route name, or explicitly authorize an in-scope URL-wiring change.

### Failing commands
- None. No implementation or gate tests were run.

### Next step for the next session
Resolve the BK-05 cargo-details route and make it available as a named route in the application URL configuration; then restart AM-04D from setup and implement the marker partial against that route.
