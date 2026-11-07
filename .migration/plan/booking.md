# Cargo booking and routing slice plan

**Status:** Draft for human approval; no tickets are published  
**Slice epic:** `martins-vds/ai-factory-pilot-target#224`  
**Parent task:** `martins-vds/ai-factory-pilot-target#222`  
**Decision map:** `martins-vds/ai-factory-pilot-target#3`  
**Anchor:** register cargo → list and route cargo → assign itinerary; change destination or deadline and re-evaluate route state

## Planning basis

- The 25 `booking.*.yaml` capabilities are characterized at tier A. Fifteen cite `legacy-test` contracts and ten are observation-based. The capability outcomes record 24 prediction matches and one difference (`route-assignment`); see `.migration/characterization/booking/observations.json` and `source-tests.json`.
- Source JUnit execution covered 16 tests across `CargoTest`, `ItineraryTest`, and `RouteSpecificationTest`. `ItineraryTest.testNextExpectedEvent` is an empty TODO. `BookingServiceTest`'s Arquillian tests were not run; their listed contracts are transcribed targets, not claims of executed source evidence. `ExternalRoutingServiceTest.testCalculatePossibleRoutes` and `CargoLifecycleScenarioTest.testCargoFromHongkongToStockholm` lack `@Test`; do not count them as executed legacy tests.
- ADR-0001 requires inward-only DDD layers per context. ADR-0002 selects Django templates with Tailwind, daisyUI, and htmx. ADR-0003 requires JPA-compatible table and column mappings. Decision #92 keeps booking/admin pages unauthenticated.
- Decision #89 keeps route finding in-process behind `RoutingService`, retains `GET /rest/graph-traversal/shortest-path`, and preserves randomized candidate generation (including a random voyage per leg). Its comment says the pathfinder ignores `deadline`; the still-open #238 disputes whether that behavior should be preserved. Hold the candidate request/filter policy until the operator resolves that conflict.
- The main booking risk-map hot spots, `Itinerary::isExpected` (CRAP 182) and `Delivery::calculateNextExpectedActivity` (156), already have target implementations from Track Cargo: `Itinerary.is_expected` and `Delivery._calculate_next_expected_activity`, decomposed into focused match/transition helpers. Track Cargo also implements the `Delivery::calculateTransportStatus` behavior (source CRAP 56). Reuse these `cargo.domain` calculations; do not create duplicate logic or another design ticket. Booking tests should exercise their existing public contracts where relevant.
- Open quirks #232–#239 and #250–#252 remain human decisions. Tickets that implement affected behavior must wait for the applicable ruling; no plan text here chooses to preserve or fix a quirk. In particular, #236 is the one observed/predicted mismatch: route assignment reached `show.xhtml` although the prediction expected `show.html`.
- This slice is not the separate production-data migration workstream (#223). It creates booking records through the application flow and reuses Track Cargo's existing cargo, location, voyage, and itinerary foundations.
- The committed source graph has a table-reaching path from each declared anchor. The Pathfinder implementation itself is in-memory and has no table edge; `admin/route.xhtml` is the end-to-end data-path anchor for both Route Cargo and its candidate-generation subflow. No direct source Pathfinder anchor is declared as a table path.
- Tickets below are planning labels, not published tracker IDs. Sizes fit the profile's `context.working_budget: 0.45`; dependencies are only genuine implementation blockers.

## Proposed tickets

### BK-01 — Implement cargo booking and route-specification updates

- **Size:** M
- **Worker:** `afs-migrator`
- **Blocked by:** none; uses the existing Track Cargo domain and persistence foundation.
- **Scope:** Add the booking application operations to create a cargo with a generated uppercase UUID-prefix tracking ID and empty itinerary, and to update destination or arrival deadline while preserving the other specification fields. Re-derive routing state using the existing cargo domain. Preserve source-visible date values and keep the open parse-error behavior (#234) out of scope until ruled.
- **Tests:** Test-first application/repository tests for the registration and specification-update contracts, including persisted fields and route-state reset. Transcribe `BookingServiceTest.testRegisterNew`, `testChangeDestination`, and `testChangeDeadline`; reuse, rather than duplicate, Track Cargo's route-specification and cargo-state tests.
- **Capabilities:** `booking.registration`, `booking.destination-change`, `booking.deadline-change`.

### BK-02 — Add the in-process randomized `RoutingService`

- **Size:** M
- **Worker:** `local`
- **Blocked by:** none within this slice; implementation of deadline request semantics waits for the human ruling on #238.
- **Scope:** Implement the pathfinder module and `RoutingService` boundary selected by #89, with randomized candidate paths and random per-leg voyages. Inject the random source so tests can seed it. Keep the public REST contract at `GET /rest/graph-traversal/shortest-path`; do not add an HTTP self-call. Implement endpoint validation and response shape from #89, but do not settle #238's deadline policy in this ticket.
- **Tests:** Deterministic seeded tests for the source contract (3–5 candidates, 1–5 shuffled intermediate ports, origin/destination endpoints, connected legs, increasing dates, and sample voyages), plus five-character origin/destination validation and JSON contract. Do not treat the unannotated source `testCalculatePossibleRoutes` as executed evidence.
- **Capabilities:** `booking.routing-pathfinder-api`.

### BK-03 — Implement route-candidate filtering and assignment

- **Size:** M
- **Worker:** `afs-migrator`
- **Blocked by:** BK-01, BK-02, and the human rulings needed for #232 and #238.
- **Scope:** Request candidates through `RoutingService`, convert transit paths to itineraries, apply the route-specification checks, and persist the selected itinerary. Keep source behavior for candidate generation separate from booking's acceptance/filter policy. Unknown-cargo behavior remains undecided until #232; do not infer a not-found response or preserve the null failure.
- **Tests:** Test-first coverage for candidate conversion/filtering and route assignment using `BookingServiceTest.testRouteCandidates` and `testAssignRoute`, plus the successful and missed-deadline `RouteSpecificationTest` contracts. Confirm the selected route updates routing state, ETA, and next activity through the existing Track Cargo domain.
- **Capabilities:** `booking.routing-candidates`, `booking.routing-assign`; contributes to `booking.cargo-not-found`.

### BK-04 — Build the cargo-registration wizard

- **Size:** M
- **Worker:** `afs-specialist-migrator`
- **Specialty:** `ui`
- **Blocked by:** BK-01.
- **Scope:** Deliver the three-step origin, destination, and deadline wizard using Django templates, Tailwind/daisyUI, and htmx. Preserve default selections, excluded origin choices, Back/Cancel/Next behavior, calendar bounds, duration message, and the disabled same-day booking state. Keep the front door open as decided in #92.
- **Tests:** UI tests for the three characterized wizard pages and submit path; assert a successful submission creates a cargo and returns to the dashboard. Cover `RouteSpecificationTest.testIsNotSatisfiedByWrongOrigin`, `testIsNotSatisfiedByWrongDestination`, and `testIsNotSatisfiedByMissedDeadline` at the applicable target boundaries, reusing Track Cargo domain coverage where it already proves the same contract. Cover the source `testRegisterNew` contract in the end-to-end target flow, without claiming the source Arquillian test ran.
- **Capabilities:** `booking.wizard-chain`, `booking.wizard-input-rules`, `booking.screen-origin`, `booking.screen-destination`, `booking.screen-deadline`.

### BK-05 — Build the cargo dashboard, tables, and details

- **Size:** M
- **Worker:** `afs-specialist-migrator`
- **Specialty:** `ui`
- **Blocked by:** BK-01, BK-03, and human rulings #232, #233, and #237.
- **Scope:** Render the dashboard's routed, not-routed, and claimed tables in source order, with their characterized fields and cargo links. Add the cargo-details view and preserve the observed claimed-cargo link behavior only as decided by the human. Unknown IDs and the orphan routed-table dialog also remain subject to their open rulings.
- **Tests:** Target view tests for all three table partitions, empty states, dashboard ordering, details fields, and a cargo moving from not-routed to routed after assignment. Pin any #232/#233/#237 outcome only after its ruling.
- **Capabilities:** `booking.dashboard-chain`, `booking.dashboard-filters`, `booking.screen-dashboard`, `booking.screen-routed-table`, `booking.screen-not-routed-table`, `booking.screen-claimed-table`, `booking.screen-cargo-details`; contributes to `booking.cargo-not-found`.

### BK-06 — Build route selection and itinerary screens

- **Size:** M
- **Worker:** `afs-specialist-migrator`
- **Specialty:** `ui`
- **Blocked by:** BK-03 and human rulings #236 and #252.
- **Scope:** Present cargo route details, candidate counts, numbered itinerary legs, the no-route guidance, and route assignment. Reproduce the observed `selectItinerary` states only after the human decides whether its blank-with-candidates behavior (#252) is preserved or changed. Apply the route-assignment redirect selected for #236.
- **Tests:** UI tests for populated and empty candidate lists, candidate assignment, and the resulting details page. Exercise the candidate properties from the unannotated source routing method as target assertions, not as executed legacy-test evidence.
- **Capabilities:** `booking.routing-chain`, `booking.screen-route`, `booking.screen-select-itinerary`, `booking.routing-assign`.

### BK-07 — Build destination and deadline edit dialogs

- **Size:** M
- **Worker:** `afs-specialist-migrator`
- **Specialty:** `ui`
- **Blocked by:** BK-01, BK-05, and human rulings #234, #235, and #251.
- **Scope:** Add the not-routed-table destination and deadline dialogs. Preserve the observed updates, closing behavior, and table refresh while implementing the operator's decisions on parse errors, mutation of destination options, and console warnings.
- **Tests:** Test-first dialog tests for initial values, filtered options, successful updates, retained route specification fields, and refreshed rows. Cover `BookingServiceTest.testChangeDestination` and `testChangeDeadline` contracts at the UI boundary.
- **Capabilities:** `booking.dialog-chain`, `booking.dialog-deadline`, `booking.dialog-destination`.

### BK-08 — Replay the booking characterization

- **Size:** M
- **Worker:** `afs-verifier`
- **Blocked by:** BK-01–BK-07 and the affected human quirk rulings.
- **Scope:** Independently replay the committed tier-A cases covering all 25 capabilities, with field-level comparisons. Distinguish approved divergences, unresolved quirks, and defects; do not blanket-ignore the route-assignment discrepancy or count unannotated source methods as executed evidence.
- **Acceptance:** All 25 ledger entries have an implementing ticket and target evidence; each `legacy-test` contract is tested in its implementing ticket. Report the 24 predicted capability matches and the route-assignment mismatch separately, then update the comparison only with a human ruling.

### BK-09 — Accept the cargo booking and routing slice

- **Size:** M
- **Worker:** `afs-auditor`
- **Blocked by:** BK-08.
- **Scope:** Independently verify all 25 booking ledger capabilities, the source/target graph paths, the approved quirk rulings, test-first evidence, and the profile gates through `afs-run`. Produce the slice acceptance evidence; do not treat progress labels as proof.
- **Acceptance:** No capability is unmapped, all required gates pass with committed evidence, and the operator's side-by-side sign-off remains outstanding until provided.

## Capability-to-ticket coverage

| Ledger capability | Ticket |
|---|---|
| `booking.cargo-not-found` | BK-03, BK-05 |
| `booking.dashboard-chain` | BK-05 |
| `booking.dashboard-filters` | BK-05 |
| `booking.deadline-change` | BK-01 |
| `booking.destination-change` | BK-01 |
| `booking.dialog-chain` | BK-07 |
| `booking.dialog-deadline` | BK-07 |
| `booking.dialog-destination` | BK-07 |
| `booking.registration` | BK-01 |
| `booking.routing-assign` | BK-03, BK-06 |
| `booking.routing-candidates` | BK-03 |
| `booking.routing-chain` | BK-06 |
| `booking.routing-pathfinder-api` | BK-02 |
| `booking.screen-cargo-details` | BK-05 |
| `booking.screen-claimed-table` | BK-05 |
| `booking.screen-dashboard` | BK-05 |
| `booking.screen-deadline` | BK-04 |
| `booking.screen-destination` | BK-04 |
| `booking.screen-not-routed-table` | BK-05 |
| `booking.screen-origin` | BK-04 |
| `booking.screen-route` | BK-06 |
| `booking.screen-routed-table` | BK-05 |
| `booking.screen-select-itinerary` | BK-06 |
| `booking.wizard-chain` | BK-04 |
| `booking.wizard-input-rules` | BK-04 |

## Dependencies and dispatch

1. BK-01 and BK-02 can proceed independently; BK-02 is the only ticket assigned to a local worker.
2. BK-03 follows both. BK-04 can follow BK-01 in parallel. BK-05 follows BK-01 and BK-03; BK-06 follows BK-03; BK-07 follows BK-01 and BK-05.
3. BK-08 waits for all implementation tickets and the relevant human rulings. BK-09 follows BK-08.
4. BK-04–BK-07 are all assigned to `afs-specialist-migrator` with `specialty: ui`, as required for the wizard, dashboard tables, route selection, and dialogs.

## Graph anchors and open questions

`.migration/slices/booking.yaml` anchors the five source flows at entry points that reach source tables. `Generate Candidate Paths` is represented by the end-to-end Route Cargo page because the Pathfinder is an in-memory service; the direct Pathfinder node has no source table path. The pathfinder's API behavior is tested as a service/endpoint capability, not presented as a persisted-data path.

Target anchors provisionally retain the source-visible page paths for the Django entry points and the exact REST path selected by #89. The operator must confirm those page URL mappings before tickets are dispatched; target graph paths are checked again at slice acceptance.

**Open questions for the Program Orchestrator:**

- Obtain human rulings for #232–#239 and #250–#252 before implementing their affected behaviors; #239 and #250 also require that unannotated methods not be reported as executed source tests.
- Reconcile the still-open #238 deadline question with #89's comment, which says the pathfinder accepts but ignores `deadline`; #238 blocks candidate generation/filter-policy implementation until confirmed.
- Confirm target URL mappings for the booking wizard, dashboard, cargo details, route selection, and edit dialogs; the slice spec currently uses source-visible paths provisionally.
