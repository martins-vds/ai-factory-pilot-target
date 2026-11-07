# Admin live-map slice plan

**Status:** Draft for human approval; no tickets are published
**Slice epic:** `martins-vds/ai-factory-pilot-target#202`
**Parent task:** `martins-vds/ai-factory-pilot-target#99`
**Decision map:** `martins-vds/ai-factory-pilot-target#3`
**Anchor:** Admin Live Cargo Map → server-rendered markers partial → `Cargo`

## Planning basis

- The 11 `admin-live-map.*.yaml` capabilities are characterized at tier A. The before/after-handling goldens record a real `RECEIVE` event processed through the handling flow; `DEF789` changes to `IN_PORT` at `CNHKG`.
- The source graph gate passes for `page=src/main/webapp/admin/tracking/map.xhtml` and `page=src/main/webapp/admin/tracking/mapFrame.xhtml`; both flow through `GET /cargo` to the `Cargo` table. The run is recorded in `.migration/evidence/runs/AM-04.md`.
- ADR-0002 selects Leaflet with OpenStreetMap. ADR-0005 / ruling #90 selects a server-rendered markers partial polled by htmx at `CARGO_MAP_POLL_SECONDS` (default 10), replacing the WebSocket and full-frame reload. The `/tracking` socket and online/offline label are dropped under #90.
- Rulings #205, #206, and #207 explicitly approve exact configured coordinates, an Unknown/unmapped list with a real tracking link and no invented point, and the normalized `In port` label, respectively. These are admin-map decisions, not inferred from Track Cargo's #14.
- Reuse the existing cargo repository, cargo/location mappings, and accepted handling-processing flow. No new persistence schema or production-data migration is planned.
- The source map-frame `init()` hotspot is CRAP 110 / CCN 10 in the best-effort risk map. A design ticket precedes its re-architected target presentation; target methods remain subject to the profile CRAP limit of 30.
- Quirk #253 remains open. Ruling #206 covers unknown/unmapped cargo generally, but does not unambiguously decide whether the source `NOT_RECEIVED` + `Unknown` sentinel is shown at its known origin or only in the unmapped list. Do not silently decide that case.
- Provisional target routes for slice anchors are `/admin/live-map/` and `/admin/live-map/markers/`; confirm them before approval. Marker click-through targets booking's admin cargo-details page (BK-05); its URL remains provisional until the revised booking plan names it.

## Proposed tickets

The labels below are planning keys, not published tracker IDs. Sizes fit one fresh session within the profile working budget. Dependencies are blocking edges; unlisted relationships are not blockers.

### AM-04A — Design the admin-map marker behavior

- **Size:** S
- **Role:** `afs-specialist-migrator`, `specialty: ui`
- **Blocked by:** none
- **Files:** `.migration/design/admin-live-map.md`
- **Scope:** Before implementation, produce a decision table and test inventory for cargo location selection, status precedence and colors, tooltips, empty/failure behavior, known versus unmapped locations, and marker navigation. Record the approved divergences (#205, #206, #207, and #90) with their citations. Keep the #253 sentinel case explicitly unresolved and identify its dependent implementation behavior; do not make a new ruling.
- **Acceptance:** The design is a test-first checklist for AM-04B–AM-04E, reuses shared cargo status behavior where applicable, and gives a decomposition that keeps changed target methods at or below CRAP 30.
- **Capabilities:** design prerequisite; no capability is owned only by this ticket.

### AM-04B — Add the server-side all-cargo map query

- **Size:** M
- **Role:** `afs-migrator`
- **Blocked by:** AM-04A
- **Files:** `src/cargotracker/cargo/application/admin_map.py`, `src/cargotracker/cargo/interfaces/admin_map/urls.py`, `src/cargotracker/cargo/interfaces/admin_map/views.py`, `src/cargotracker/urls.py`, `src/cargotracker/settings.py`, `tests/cargo/interfaces/test_admin_live_map_data.py`
- **Scope:** Build the map view data from the existing `CargoRepository.find_all()` path and current cargo state; do not add a parallel REST/JAX-RS endpoint or duplicate cargo/location persistence. Expose the proposed page and markers routes, and define `CARGO_MAP_POLL_SECONDS` with default 10. Only known configured city locations receive coordinates; do not reuse a synthetic `XXXXX` coordinate as a real point. Preserve all cargo and status fields needed by the map.
- **Tests:** Verify all-cargo results, status/location mapping, the configured polling default, and that unknown/unmapped values are not assigned fabricated coordinates.
- **Capabilities:** `admin-live-map.cargo-source` → **replaced** (#90 / ADR-0005: query the target repository for the rendered partial instead of the source JSON resource); `admin-live-map.rest-resource-config` → **replaced** (#90 / ADR-0005: no target JAX-RS resource configuration).

### AM-04C — Build the admin map page

- **Size:** S
- **Role:** `afs-specialist-migrator`, `specialty: ui`
- **Blocked by:** AM-04A, AM-04B
- **Files:** `templates/admin/live_map.html`, `tests/cargo/interfaces/test_admin_live_map_templates.py`
- **Scope:** Add the server-rendered admin page and Leaflet/OpenStreetMap map shell. Poll the markers endpoint with htmx using `hx-trigger="every <CARGO_MAP_POLL_SECONDS>s"` and swap the markers without a full-page reload. Do not add a WebSocket or online/offline label.
- **Tests:** Assert the page renders the map and its htmx trigger from the configured setting, including a non-default setting value.
- **Capabilities:** `admin-live-map.page-frame` → **migrated**; `admin-live-map.map-provider` → **migrated** per ADR-0002; `admin-live-map.connection-status` → **dropped** (#90 / ADR-0005).

### AM-04D — Render the marker partial and unmapped cargo

- **Size:** M
- **Role:** `afs-specialist-migrator`, `specialty: ui`
- **Blocked by:** AM-04A, AM-04B, AM-04C, BK-05, and an answer to quirk #253 for the `NOT_RECEIVED` + `Unknown` sentinel case
- **Files:** `templates/admin/_live_map_markers.html`, `tests/cargo/interfaces/test_admin_live_map_markers.py`
- **Scope:** Render the current cargo markers and their status/tooltips in the htmx partial. Preserve source status precedence and color rules. Use exact configured coordinates with no random offset (#205); list unknown/unmapped cargo separately with its real tracking link and no invented point (#206). Normalize the `IN_PORT` tooltip label to `In port` (#207). Keep the #253 sentinel-specific presentation blocked until the operator resolves whether #206 covers that exact case. Preserve the characterized empty-map behavior; log data failures without inventing map data.
- **Tests:** Cover status precedence/colors, exact known-location coordinates, tooltip fields and normalized text, empty data, and mixed known/unmapped cargo with its real tracking link and no marker at a fabricated point. Add the #253 case only after its ruling.
- **Capabilities:** `admin-live-map.marker-coordinates` → **replaced** (#205, #206); `admin-live-map.marker-status` → **migrated**; `admin-live-map.marker-tooltip` → **replaced** (#206, #207; #253 remains open); `admin-live-map.empty-and-failure` → **migrated**; `admin-live-map.cargo-navigation` → **migrated** to the booking admin cargo-details page, with its URL pending the revised booking plan; `admin-live-map.notification-reload` → **replaced** (#90 / ADR-0005: the next htmx poll reflects committed cargo changes).

### AM-04E — Prove the handling-to-map update

- **Size:** M
- **Role:** `afs-migrator`
- **Blocked by:** AM-04B, AM-04C, AM-04D
- **Files:** `tests/cargo/interfaces/test_admin_live_map_processing.py`
- **Scope:** Exercise the real handling processing step for a seeded cargo, then request the markers partial. Do not directly mutate cargo state or mock the processing step. Verify the resulting location and status, and verify that the page's actual `hx-trigger` interval equals `CARGO_MAP_POLL_SECONDS`.
- **Acceptance test:** Process the characterized `DEF789` `RECEIVE` at `CNHKG` event; assert the partial shows last-known location `CNHKG` and transport status `IN_PORT`, while the existing `MISROUTED` precedence remains reflected in the marker status/color. Assert the configured non-default polling interval in the page markup.
- **Capabilities:** End-to-end evidence for the handling-to-map flow and the complete capability set; no capability is left unowned.

### AM-04F — Accept the admin live-map slice

- **Size:** M
- **Role:** `afs-auditor`
- **Blocked by:** AM-04E
- **Files:** `.migration/evidence/admin-live-map/acceptance.md`, `.migration/returns/AM-04F.afs-auditor.yaml`
- **Scope:** Independently re-prove coverage of all 11 ledger entries, the approved rulings and #253 resolution, the source/target graph anchors, the real handling-processing acceptance test, and every applicable profile gate through `afs-run`. Verify the UI specialist ownership of the page and markers partial.
- **Acceptance:** All required gates pass with committed evidence, all capabilities have an approved fate, and the operator performs the side-by-side flow check before epic #202 is closed.

## Dependencies and parallelism

1. AM-04A is the hot-spot design prerequisite.
2. AM-04B follows AM-04A. AM-04C follows AM-04A and AM-04B.
3. AM-04D follows the page and query tickets, but its `NOT_RECEIVED` + `Unknown` sentinel behavior cannot proceed until #253 is answered. Other map work may continue.
4. AM-04E follows the implementation; AM-04F follows the independent acceptance test.

The existing accepted handling-registration flow (#113) and cargo/location persistence are prerequisites already present in the target baseline, not new blocking slices. There is no separate data-migration slice.

## Cross-slice

- **Shared files:** `src/cargotracker/urls.py` is AM-04B's shared route-registration point; coordinate it with the booking ticket that wires booking routes. The booking draft on PR #259 does not identify that ticket or list target files, so do not run AM-04B in parallel with that URL-wiring work until the revised booking plan names its owner. `src/cargotracker/settings.py` is changed by AM-04B for `CARGO_MAP_POLL_SECONDS`, but the booking draft specifies no settings change. The map templates are feature-specific, and booking reuses the existing cargo model; neither plan identifies shared template or cargo-model edits.
- **Blocking dependency:** BK-05 builds the booking admin cargo-details page; AM-04D needs it for marker click-through. BK-05 and AM-04D cannot run in parallel. The destination URL stays provisional until the revised booking plan names it. Other admin-map work can proceed independently of BK-05.

## Capability-to-ticket coverage

These are planned fates, not claims that target implementation is complete. Every deliberate replacement/drop cites its approval.

| Ledger capability | Ticket | Planned fate |
|---|---|---|
| `admin-live-map.cargo-navigation` | AM-04D | **migrated** — marker opens the booking admin cargo-details page from BK-05; its target URL remains provisional until the revised booking plan names it |
| `admin-live-map.cargo-source` | AM-04B | **replaced** — server-side all-cargo query for the htmx partial (#90 / ADR-0005) |
| `admin-live-map.connection-status` | AM-04C | **dropped** — WebSocket and online/offline label (#90 / ADR-0005) |
| `admin-live-map.empty-and-failure` | AM-04D | **migrated** — empty map remains empty; failures are logged and do not fabricate markers |
| `admin-live-map.map-provider` | AM-04C | **migrated** — Leaflet and OpenStreetMap (ADR-0002) |
| `admin-live-map.marker-coordinates` | AM-04D | **replaced** — exact configured coordinates (#205); unknown/unmapped cargo listed without a fabricated point (#206); #253 remains open for its sentinel case |
| `admin-live-map.marker-status` | AM-04D | **migrated** — preserve status precedence and marker colors |
| `admin-live-map.marker-tooltip` | AM-04D | **replaced** — unknown locations in a separate list (#206), normalize `In port` (#207); #253 remains open for the sentinel case |
| `admin-live-map.notification-reload` | AM-04C, AM-04D | **replaced** — htmx polling after committed state changes (#90 / ADR-0005) |
| `admin-live-map.page-frame` | AM-04C | **migrated** — server-rendered admin page |
| `admin-live-map.rest-resource-config` | AM-04B | **replaced** — direct Django query replaces the source JAX-RS resource (#90 / ADR-0005) |

## Slice spec and open questions

- Source anchors: `page=src/main/webapp/admin/tracking/map.xhtml` and `page=src/main/webapp/admin/tracking/mapFrame.xhtml`; both must reach the `Cargo` table through the directed source graph.
- Provisional target anchors: `endpoint=/admin/live-map/` and `endpoint=/admin/live-map/markers/`. The page polls the markers endpoint; both routes are proposed pending operator approval.
- The slice adds no target endpoint beyond those anchors until the marker-click destination is decided.

**Open questions for the Program Orchestrator:**

- Resolve quirk #253: for a `NOT_RECEIVED` cargo whose `lastKnownLocation` is `Unknown` but whose origin is known, does ruling #206 require the unmapped list, or should the origin marker remain?
- Keep the marker click-through URL provisional until the revised booking plan names the BK-05 cargo-details route.
- Confirm the provisional `/admin/live-map/` and `/admin/live-map/markers/` route names before approving the plan.
