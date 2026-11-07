# Cargo booking and routing slice plan

**Status:** Draft for human approval; no tickets are published  
**Slice epic:** `martins-vds/ai-factory-pilot-target#224`  
**Parent task:** `martins-vds/ai-factory-pilot-target#222`  
**Decision map:** `martins-vds/ai-factory-pilot-target#3`  
**Anchor:** register cargo → list and route cargo → assign itinerary; change destination or deadline and re-evaluate route state

## Planning basis

- The 25 `booking.*.yaml` capabilities are characterized at tier A. Fifteen cite `legacy-test` contracts and ten are observation-based. The comparison records 24 prediction matches and one route-assignment difference; see `.migration/characterization/booking/observations.json` and `source-tests.json`.
- Source JUnit execution covered 16 tests across `CargoTest`, `ItineraryTest`, and `RouteSpecificationTest`. `ItineraryTest.testNextExpectedEvent` is an empty TODO. `BookingServiceTest`'s Arquillian tests were not run. The unannotated `ExternalRoutingServiceTest.testCalculatePossibleRoutes` (#239) and `CargoLifecycleScenarioTest.testCargoFromHongkongToStockholm` (#250) remain in the source inventory but are not executed legacy-test evidence.
- ADR-0001 requires inward-only DDD layers per context. ADR-0002 selects Django templates with Tailwind, daisyUI, and htmx. ADR-0003 requires JPA-compatible table and column mappings. Decision #92 keeps booking/admin pages unauthenticated.
- Decision #89 selects an in-process pathfinder behind `RoutingService`, retains `GET /rest/graph-traversal/shortest-path`, and preserves randomized candidate generation and a random voyage per leg. Its item 5 also rules that the endpoint accepts but ignores `deadline` and that booking filters candidates by arrival deadline; #238 is a duplicate ruling, not an open question.
- The source hot spots `Itinerary::isExpected` (CRAP 182) and `Delivery::calculateNextExpectedActivity` (156) already have target implementations in Track Cargo: `Itinerary.is_expected` and `Delivery._calculate_next_expected_activity`, decomposed into focused match/transition helpers. Reuse those `cargo.domain` calculations; do not duplicate them or add a design ticket. Track Cargo also implements `Delivery::calculateTransportStatus` (source CRAP 56).
- Closed rulings are incorporated below: #232 fixes unknown/stale IDs with HTTP 404; #233 fixes only the claimed-cargo link label; #234 shows a deadline field error; #235 avoids mutating destination options; #236 redirects assignment to cargo details; #237 drops the unreachable debug dialog; #238 preserves #89 item 5; #251 drops the unavailable-widget warning while keeping successful updates; and #252 renders candidate routes when present. #239 and #250 preserve the source test inventory and are not counted as executed evidence.
- This slice is not the separate production-data migration workstream (#223). It creates booking records through the application flow and reuses Track Cargo's existing cargo, location, voyage, and itinerary foundations.
- The committed source graph has a table-reaching path from each declared anchor. Candidate generation is in-memory; its source endpoint is tested as an endpoint capability, while the Route Cargo page anchors the persisted flow.
- Implementation tickets use the fresh IDs BK-05A through BK-05J so they do not reuse BK-02, BK-03, or BK-04. Implementation tickets own distinct files; verifier and auditor evidence files are distinct and the auditor waits for the verifier. Central URL registration is isolated in BK-05H. The plan fits `context.working_budget: 0.45` and respects `concurrency.max_parallel_workers: 4`.

## Proposed tickets

### BK-05A — Implement cargo registration and specification updates

- **Size:** M
- **Role:** `afs-migrator`
- **Files:** `src/cargotracker/booking/application/registration.py`, `src/cargotracker/booking/application/specification.py`, `tests/booking/application/test_registration.py`, `tests/booking/application/test_specification.py`
- **Blocked by:** none; reuses the existing Track Cargo domain and persistence foundation.
- **Scope:** Create a cargo with a generated uppercase UUID-prefix tracking ID and empty itinerary; update destination or arrival deadline while preserving the other specification fields. Re-derive routing state using the existing cargo domain.
- **Tests:** Test-first application/repository coverage for registration and specification updates, including persisted fields and route-state reset. Transcribe `BookingServiceTest.testRegisterNew`, `testChangeDestination`, and `testChangeDeadline`; reuse Track Cargo's existing domain tests rather than duplicating them. The unannotated scenario in #250 is not executed legacy evidence.
- **Capabilities:** `booking.registration`, `booking.destination-change`, `booking.deadline-change`.

### BK-05B — Add the in-process randomized `RoutingService`

- **Size:** M
- **Role:** `afs-migrator`
- **Worker:** `local`
- **Files:** `src/cargotracker/pathfinder/`, `tests/pathfinder/`
- **Blocked by:** none within this slice.
- **Scope:** Implement the pathfinder module and `RoutingService` boundary selected by #89, with randomized candidate paths and random per-leg voyages. Inject the random source so tests can seed it. Keep the public REST contract at `GET /rest/graph-traversal/shortest-path`; do not add an HTTP self-call. As ruled by #89 item 5 and #238, accept and ignore `deadline`; booking applies the arrival-deadline filter in BK-05C.
- **Tests:** Deterministic seeded tests for 3–5 candidates, 1–5 shuffled intermediate ports, origin/destination endpoints, connected legs, increasing dates, sample voyages, five-character origin/destination validation, and JSON response shape. The unannotated `testCalculatePossibleRoutes` in #239 is not executed source evidence.
- **Capabilities:** `booking.routing-pathfinder-api`.

### BK-05C — Implement candidate filtering and route assignment

- **Size:** M
- **Role:** `afs-migrator`
- **Files:** `src/cargotracker/booking/application/routing.py`, `tests/booking/application/test_routing.py`
- **Blocked by:** BK-05A and BK-05B.
- **Scope:** Request candidates through `RoutingService`, convert transit paths to itineraries, apply route-specification checks, and persist the selected itinerary. Apply #89 item 5 / #238 by filtering candidates against the arrival deadline. Implement the #232 ruling for unknown or stale tracking IDs: return the target cargo-not-found response with HTTP 404, consistent with Track Cargo #12.
- **Tests:** Test-first coverage for candidate conversion/filtering and route assignment using `BookingServiceTest.testRouteCandidates` and `testAssignRoute`, plus successful and missed-deadline `RouteSpecificationTest` contracts. Verify route state, ETA, and next activity through Track Cargo's existing domain. Do not count the unannotated methods in #239 or #250 as executed source evidence.
- **Capabilities:** `booking.routing-candidates`, `booking.routing-assign`, `booking.cargo-not-found`.

### BK-05D — Build the cargo-registration wizard

- **Size:** M
- **Role:** `afs-specialist-migrator`
- **Specialty:** `ui`
- **Files:** `src/cargotracker/booking/interfaces/wizard/views.py`, `templates/booking/wizard/`, `tests/booking/interfaces/test_wizard.py`
- **Blocked by:** BK-05A.
- **Scope:** Deliver the three-step origin, destination, and deadline wizard using Django templates, Tailwind/daisyUI, and htmx. Preserve default selections, excluded origin choices, Back/Cancel/Next behavior, calendar bounds, duration message, and disabled same-day booking state. Keep the front door open as decided in #92.
- **Tests:** UI tests for all characterized wizard pages and submit path; assert successful submission creates cargo and returns to the dashboard. Cover the applicable route-specification contracts at target boundaries, reusing Track Cargo domain coverage. #250's unannotated scenario is not executed legacy evidence.
- **Capabilities:** `booking.wizard-chain`, `booking.wizard-input-rules`, `booking.screen-origin`, `booking.screen-destination`, `booking.screen-deadline`.

### BK-05E — Build the cargo dashboard, tables, and details

- **Size:** M
- **Role:** `afs-specialist-migrator`
- **Specialty:** `ui`
- **Files:** `src/cargotracker/booking/interfaces/dashboard/views.py`, `templates/booking/dashboard/`, `templates/booking/cargo_details.html`, `tests/booking/interfaces/test_dashboard.py`, `tests/booking/interfaces/test_cargo_details.py`
- **Blocked by:** BK-05A and BK-05C.
- **Scope:** Render routed, not-routed, and claimed tables in source order with characterized fields and cargo links. Add the admin cargo-details page at the provisional URL `/admin/cargo/<tracking_id>/`. Implement #232's HTTP 404 cargo-not-found state for unknown/stale IDs. Apply #233 by changing only the claimed-cargo tooltip to “Click to see details”; keep its destination on cargo details and add no history view. Drop the unreachable debug dialog under #237.
- **Tests:** Cover all table partitions, empty states, dashboard ordering, detail fields/404, claimed-link label and destination, and cargo moving from not-routed to routed after assignment. Assert that the #237 debug dialog is absent.
- **Capabilities:** `booking.dashboard-chain`, `booking.dashboard-filters`, `booking.screen-dashboard`, `booking.screen-routed-table`, `booking.screen-not-routed-table`, `booking.screen-claimed-table`, `booking.screen-cargo-details`; contributes to `booking.cargo-not-found`.

### BK-05F — Build route selection and itinerary screens

- **Size:** M
- **Role:** `afs-specialist-migrator`
- **Specialty:** `ui`
- **Files:** `src/cargotracker/booking/interfaces/route_selection/views.py`, `templates/booking/route_selection/`, `tests/booking/interfaces/test_route_selection.py`
- **Blocked by:** BK-05C and BK-05E.
- **Scope:** Present cargo route details, candidate counts, numbered itinerary legs, no-route guidance, and route assignment. Apply #236: after assignment redirect to the cargo-details page at `/admin/cargo/<tracking_id>/`. Apply #252 by rendering candidate routes when present (the Planner's choice under the ruling); retain the empty-candidate message otherwise.
- **Tests:** Cover populated and empty candidate lists, candidate assignment, redirect destination, and resulting details page. Exercise the unannotated candidate properties as target assertions, not as executed legacy-test evidence (#239).
- **Capabilities:** `booking.routing-chain`, `booking.screen-route`, `booking.screen-select-itinerary`, `booking.routing-assign`.

### BK-05G — Build destination and deadline edit dialogs

- **Size:** M
- **Role:** `afs-specialist-migrator`
- **Specialty:** `ui`
- **Files:** `src/cargotracker/booking/interfaces/dialogs/views.py`, `templates/booking/dialogs/`, `tests/booking/interfaces/test_dialogs.py`
- **Blocked by:** BK-05A and BK-05E.
- **Scope:** Add destination and deadline dialogs to the not-routed table. Apply #234 by showing a field error when the deadline cannot be parsed; apply #235 by filtering destination options without mutating the backing location list; apply #251 by omitting the unavailable-widget warning while preserving successful updates and dialog completion.
- **Tests:** Cover initial values, filtered options and stable subsequent renders, parse-error feedback, successful updates, retained route-specification fields, successful dialog completion without the warning, and refreshed rows. Cover the change-destination/deadline contracts at the UI boundary.
- **Capabilities:** `booking.dialog-chain`, `booking.dialog-deadline`, `booking.dialog-destination`.

### BK-05H — Wire booking and pathfinder URLs

- **Size:** S
- **Role:** `afs-migrator`
- **Files:** `src/cargotracker/urls.py`, `src/cargotracker/booking/urls.py`, `tests/booking/test_urls.py`
- **Blocked by:** BK-05B, BK-05D, BK-05E, BK-05F, and BK-05G.
- **Scope:** Register the booking wizard, dashboard, cargo details, route-selection, dialog, and pathfinder endpoints. Use `/admin/cargo/<tracking_id>/` for cargo details and retain `/rest/graph-traversal/shortest-path` for the pathfinder API. Other booking route patterns remain provisional until the Program Orchestrator confirms them.
- **Tests:** Verify route names, methods, parameter resolution, the cargo-details URL, and the pathfinder's exact public path without introducing duplicate routes.
- **Capabilities:** Owns URL reachability for the booking page and routing capabilities above; no new ledger capability.

### BK-05I — Replay the booking characterization

- **Size:** M
- **Role:** `afs-verifier`
- **Files:** `tests/characterization/booking/`, `.migration/evidence/booking/replay.md`
- **Blocked by:** BK-05A through BK-05H and completion of the applicable closed rulings.
- **Scope:** Independently replay the committed tier-A cases covering all 25 capabilities, with field-level comparisons. Distinguish approved divergences, preserved quirks, and defects. Record #232–#237, #251, and #252 outcomes; record #238 as #89 item 5. Preserve the #239 and #250 test inventory without counting either unannotated method as executed evidence.
- **Acceptance:** All 25 ledger entries have an implementing ticket and target evidence; every `legacy-test` contract is tested by its implementing ticket. Report the 24 prediction matches and the approved route-assignment divergence separately.

### BK-05J — Accept the cargo booking and routing slice

- **Size:** M
- **Role:** `afs-auditor`
- **Files:** `.migration/evidence/booking/report.md`, `.migration/returns/BK-05J.afs-auditor.yaml`
- **Blocked by:** BK-05I.
- **Scope:** Independently verify all 25 booking ledger capabilities, source/target graph paths, ruled outcomes, test-first evidence, and profile gates through `afs-run`. Produce slice-acceptance evidence; do not treat progress labels as proof.
- **Acceptance:** No capability is unmapped, all required gates pass with committed evidence, and operator side-by-side sign-off remains outstanding until provided.

## Dependencies and dispatch

1. BK-05A and BK-05B can proceed independently; BK-05B is the only ticket assigned to a local worker. BK-05D can follow BK-05A. BK-05C follows BK-05A and BK-05B.
2. BK-05E follows BK-05A and BK-05C. BK-05F follows BK-05C and BK-05E. BK-05G follows BK-05A and BK-05E. BK-05H waits for the page and API modules whose routes it registers.
3. BK-05I waits for all implementation and URL-wiring tickets; BK-05J follows BK-05I.
4. BK-05D–BK-05G are assigned to `afs-specialist-migrator` with `specialty: ui`. Their owned files are separate; URL registration is isolated in BK-05H.

## Cross-slice

- **Shared files:** `src/cargotracker/urls.py` is owned by BK-05H for booking/pathfinder route registration and is also edited by admin-map ticket AM-04B. Do not run BK-05H and AM-04B in parallel; coordinate their URL changes. The admin-map plan also edits `src/cargotracker/settings.py` for map polling, but booking does not change settings. Booking reuses the existing cargo model; it does not edit cargo-model files. Booking templates live under `templates/booking/`, separate from the admin-map templates.
- **Admin-map dependency:** AM-04D waits for BK-05E, which provides the admin cargo-details page at `/admin/cargo/<tracking_id>/`. BK-05H registers that route; end-to-end marker navigation is accepted only after the URL wiring is present.

## Capability-to-ticket coverage

These are planned fates, not claims that target implementation is complete. Every deliberate replacement/drop cites its approval.

| Ledger capability | Ticket | Planned fate and ruling/evidence |
|---|---|---|
| `booking.cargo-not-found` | BK-05C, BK-05E | **migrated** — explicit HTTP 404 for unknown/stale IDs (#232; Track Cargo #12) |
| `booking.dashboard-chain` | BK-05E | **migrated** |
| `booking.dashboard-filters` | BK-05E | **migrated** |
| `booking.deadline-change` | BK-05A, BK-05G | **migrated** — parse failures show a field error (#234) |
| `booking.destination-change` | BK-05A, BK-05G | **migrated** — destination options do not mutate backing state (#235) |
| `booking.dialog-chain` | BK-05G | **migrated** — successful updates remain; unavailable-widget warning is dropped (#251) |
| `booking.dialog-deadline` | BK-05G | **migrated** — field error on parse failure (#234); warning dropped (#251) |
| `booking.dialog-destination` | BK-05G | **migrated** — stable filtered options (#235); warning dropped (#251) |
| `booking.registration` | BK-05A, BK-05D | **migrated** — #250 preserves the source test inventory; its unannotated scenario is not executed evidence |
| `booking.routing-assign` | BK-05C, BK-05F | **migrated** — redirect to cargo details (#236); #250 is not executed evidence |
| `booking.routing-candidates` | BK-05B, BK-05C | **migrated** — accept/ignore deadline and filter by arrival deadline (#89 item 5, #238); #239 is not executed evidence |
| `booking.routing-chain` | BK-05F | **migrated** |
| `booking.routing-pathfinder-api` | BK-05B, BK-05H | **migrated** — preserve the #89 endpoint and randomized behavior; deadline rule is #89 item 5 / #238 |
| `booking.screen-cargo-details` | BK-05E | **migrated** — unknown/stale IDs return 404 (#232) |
| `booking.screen-claimed-table` | BK-05E | **migrated** — correct only the link label; keep cargo-details destination (#233) |
| `booking.screen-dashboard` | BK-05E | **migrated** |
| `booking.screen-deadline` | BK-05D | **migrated** |
| `booking.screen-destination` | BK-05D | **migrated** |
| `booking.screen-not-routed-table` | BK-05E, BK-05G | **migrated** |
| `booking.screen-origin` | BK-05D | **migrated** |
| `booking.screen-route` | BK-05F | **migrated** — assignment redirects to cargo details (#236) |
| `booking.screen-routed-table` | BK-05E | **migrated**; unreachable debug dialog is **dropped** (#237) |
| `booking.screen-select-itinerary` | BK-05F | **migrated** — render candidates when present (#252) |
| `booking.wizard-chain` | BK-05D | **migrated** — #250's unannotated scenario is not executed evidence |
| `booking.wizard-input-rules` | BK-05D | **migrated** |

## Graph anchors and open questions

`.migration/slices/booking.yaml` anchors the five source flows at entry points that reach source tables. Candidate generation is in-memory and has no table edge; the Route Cargo page is the persisted-flow anchor, and the pathfinder endpoint is a separately listed target entry point.

The admin cargo-details URL is provisionally `/admin/cargo/<tracking_id>/` so AM-04D can target it. The other target URL patterns in `.migration/slices/booking.yaml` are also provisional; target graph paths will be checked again at slice acceptance.

**Open questions for the Program Orchestrator:**

- Confirm the provisional target URL contracts for the wizard, dashboard, route-selection, and dialog flows before approving the plan. The admin cargo-details route is provisionally `/admin/cargo/<tracking_id>/` and is the AM-04D destination.
