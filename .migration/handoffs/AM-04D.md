## Handoff — afs-specialist-migrator · 2026-11-08T12:49:11Z
**State:** blocked · **Branch / PR:** `copilot/am-04d-restart-marker-partial-against-booking-carg` / PR not yet available · **Last commit:** `94e8554c0fe40a9c10dd239a7fbac1e29b74a0fd`

### Done
- Loaded the migration contract and ran setup. Source SHA `f3beacf78de4f6d34edc4971ac87e38a5c6fe59d` matches the lock, is read-only and ignored; target ancestry is complete; migration validation, named-input checks, `afs-run` setup probe, DB health, RTK, and Python runtime checks passed.
- Recorded the setup probe in `.migration/evidence/runs/AM-04D.md`.
- Confirmed the booking route is now registered as `booking:cargo-details` in `src/cargotracker/booking/urls.py`; the route blocker from PR #396 is resolved.
- Reviewed `.migration/design/admin-live-map.md`, the AM-04D ticket, and the current parent map template. `templates/admin/live_map.html` keeps the Leaflet map in a local `const map` and exposes no map reference or marker-refresh hook to `_live_map_markers.html`.

### Remaining
- [ ] Agree an integration seam that lets the markers partial draw and refresh Leaflet markers (for example, expose the map through a stable page-level hook).
- [ ] If that requires changing `templates/admin/live_map.html` or its tests, obtain approval to extend AM-04D's explicitly limited file scope or create a separate prerequisite ticket.
- [ ] Resume test-first work in `tests/cargo/interfaces/test_admin_live_map_markers.py`, use `reverse('booking:cargo-details', args=[tracking_id])`, then implement and run every gate through `afs-run`.

### Decisions made
- Did not edit the partial or create tests: markup and detail links alone cannot draw or refresh map markers, and the existing parent page provides no integration hook. Changing that page is outside AM-04D's approved files.
- Did not hard-code a URL; the named booking route is available for the eventual link.

### Blockers / questions
- AM-04D currently permits only `templates/admin/_live_map_markers.html` and `tests/cargo/interfaces/test_admin_live_map_markers.py`. The Leaflet map instance is private to the inline script in `templates/admin/live_map.html`, so a functioning marker partial has no way to access it or clear/recreate markers on polling.
- The operator should approve a page-level map hook/file-scope extension, or assign the hook to a separate ticket before AM-04D resumes.

### Failing commands
- None. No implementation or gate tests were run.

### Next step for the next session
Resolve the map-instance integration seam and authorize any required scope change; then restart AM-04D from setup and implement test-first against the named booking route.
