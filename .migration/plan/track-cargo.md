# Track Cargo slice plan

**Status:** Approved by martins-vds on 2026-11-01, then published as sub-issues of #9
**Slice epic:** `martins-vds/ai-factory-pilot-target#9`
**Decision map:** `martins-vds/ai-factory-pilot-target#3`
**Anchor:** tracking form → cargo lookup → tracking result, history, and map

## Planning basis

- The 19 `track-cargo.*.yaml` ledger entries are characterized: 14 at tier A and 5 at tier B.
- The eight tier-A goldens cover `ABC123`, `JKL567`, `DEF789`, `MNO456`, padded and lowercase IDs,
  an empty ID, and an unknown ID. The seed must reproduce the four sample cargos and their related
  locations, voyages, legs, and handling events.
- ADR-0001 sets the `cargo`, `handling`, `voyage`, and `location` bounded contexts and their inward
  dependencies. ADR-0002 selects Django templates, Tailwind through `pytailwindcss`, htmx, Leaflet,
  and OpenStreetMap. ADR-0003 requires JPA-compatible table and column mappings.
- The CRAP map puts `Itinerary.isExpected` (182), `Delivery.calculateNextExpectedActivity` (156),
  `Delivery.calculateTransportStatus` (56), and two tracking view-adapter methods (42 each) above
  the threshold. Design and implementation are separate tickets; the implementation tests target a
  maximum CRAP score of 30 per method.
- No persisted `knowledge-graph.json` or `domain-graph.json` is present in the checkout. The ticket
  edges below are inferred from the ledger's graph-node/flow references, the risk map, and ADRs;
  the Orchestrator should resolve the graph question below before dispatch.

## Proposed tickets

All tickets are sized for one fresh session within the profile working budget. Dependencies are
blocking edges; unlisted relationships are not blockers.

### TC-01 — Establish the empty Django project and gates

- **Size:** M
- **Blocked by:** none
- **Scope:** Create the `cargotracker` Django project under `src/` with root `manage.py`, PostgreSQL
  17 configuration, and the agreed dependency/test/tool configuration. Install and wire
  `pytest-django`, `ruff`, coverage.py, lizard plus the CRAP checker, and mutmut. Configure
  `pytailwindcss` (standalone Tailwind CLI, no Node toolchain) and htmx. Keep this an empty-project
  foundation; do not begin slice behavior here.
- **Acceptance:** Run every profile gate through `afs-run` against the empty project and keep all
  gates enabled: `python -m compileall -q src`, `python manage.py check`, `ruff check`,
  `ruff format --check`, `pytest -q`, `lizard --csv src` followed by `crap.py` with the profile
  threshold, `mutmut run --paths-to-mutate {changed}`, and `mutmut run`. Both mutation commands
  must have a valid passing empty-project outcome rather than being disabled. Save run evidence.
- **Capabilities:** none; enabling foundation ticket.

### TC-02 — Implement the location bounded context

- **Size:** S
- **Blocked by:** TC-01
- **Scope:** Add the location domain types and repository protocol, then Django ORM mapping and
  repository for the source location table/columns. Preserve location names and UN/LOCODEs used by
  cargo, history, and map rendering.
- **Tests:** Domain tests without a database; pytest-django repository tests against PostgreSQL
  schema and round-trip mappings.
- **Capabilities:** `track-cargo.data-location`.

### TC-03 — Implement the voyage bounded context

- **Size:** S
- **Blocked by:** TC-01, TC-02
- **Scope:** Add voyage domain types and repository protocol, plus the JPA-compatible ORM mapping and
  repository for voyage identifiers.
- **Tests:** Voyage value-object and builder tests; PostgreSQL repository mapping tests.
- **Capabilities:** `track-cargo.data-voyage`.

### TC-04 — Implement cargo identity and persistence mappings

- **Size:** M
- **Blocked by:** TC-01, TC-02, TC-03
- **Scope:** Add the cargo context's tracking ID, cargo, route specification, leg, itinerary, and
  delivery model foundations and repository protocol. Map the source cargo and leg tables and
  embedded fields to the source JPA names per ADR-0003. Leave the risk-map hot-spot algorithms to
  TC-08, after TC-07's design.
- **Tests:** Domain value-object/model tests and PostgreSQL repository tests asserting the relevant
  table names, columns, relations, and read behavior.
- **Capabilities:** `track-cargo.data-cargo`, `track-cargo.data-leg`.

### TC-05 — Implement the handling bounded context

- **Size:** M
- **Blocked by:** TC-01, TC-02, TC-03, TC-04
- **Scope:** Add handling-event and handling-history domain types, repository protocol, and the
  JPA-compatible event mapping/repository. Preserve event completion times and cargo/location/voyage
  relations, deduplicate history, order it by completion time, and select the most recent event.
- **Tests:** Domain tests for history ordering/deduplication and PostgreSQL repository mapping tests.
- **Capabilities:** `track-cargo.data-handling-event`, `track-cargo.domain-history-order`.

### TC-06 — Seed the characterized sample data

- **Size:** M
- **Blocked by:** TC-02, TC-03, TC-04, TC-05
- **Scope:** Add an idempotent target seed that reproduces the relevant `SampleDataGenerator` data:
  the four golden cargos (`ABC123`, `JKL567`, `DEF789`, `MNO456`), their locations, voyages,
  itineraries, and handling histories. Preserve date relationships used by the golden files so
  characterization date normalization remains meaningful. Do not treat this sample seed as a
  decision to migrate an arbitrary production Derby database.
- **Tests:** Seed twice and prove idempotency; assert all four records and their linked rows support
  the golden lookups.
- **Capabilities:** none; data-enabling ticket.

### TC-07 — Design the tracking hot-spot logic

- **Size:** M
- **Blocked by:** TC-04, TC-05
- **Scope:** Before implementation, produce a concise decision table and test-case inventory for
  `Itinerary.isExpected`, `Delivery.calculateNextExpectedActivity`,
  `Delivery.calculateTransportStatus`, and the two view-adapter hot spots. Cover the tier-B cases,
  golden cargo states, event types, empty itinerary/history, off-route state, and quirk rulings.
  Identify decompositions that preserve the public tracking behavior and allow each resulting method
  to meet the CRAP threshold without suppressing complexity or coverage inputs.
- **Acceptance:** Design is reviewable and directly usable as the test-first implementation checklist
  for TC-08, TC-10, and TC-13. No production implementation in this ticket.
- **Capabilities:** none; required design ticket.

### TC-08 — Implement and test cargo tracking domain calculations

- **Size:** M
- **Blocked by:** TC-07
- **Scope:** Implement the designed itinerary event expectation, transport/routing state, delivery
  status, misdirection, ETA calculation, and next-activity calculations in the cargo domain. Preserve
  the characterization behavior except for the explicitly ruled quirk fixes assigned to later
  named tickets.
- **Tests:** Test-first unit coverage for all tier-B cases and relevant golden states; measure CRAP
  with coverage input and keep each method at or below 30.
- **Capabilities:** `track-cargo.domain-event-expectation`, `track-cargo.domain-route-state`,
  `track-cargo.domain-transport-status`.

### TC-09 — Build the htmx tracking lookup and fix quirk #12

- **Size:** M
- **Blocked by:** TC-04, TC-05, TC-06
- **Scope:** Implement the tracking form and application lookup path as a server-rendered Django
  screen with an htmx result-fragment update and a usable non-JavaScript form submission. Preserve
  whitespace trimming and case sensitivity. Apply ruling #12: show a visible validation message for
  an empty ID and a visible not-found message for an unknown ID; render no cargo result, history, or
  map when no cargo is found.
- **Target tests:** `test_empty_and_unknown_ids_show_messages_without_cargo_result_or_map`, plus
  padded-ID and lowercase-ID lookup tests. Assert the form remains usable and no cargo-dependent
  fragment appears when lookup fails.
- **Capabilities:** `track-cargo.tracking-id-entry`, `track-cargo.not-found`.

### TC-10 — Fix quirk #13 in the in-port status text

- **Size:** S
- **Blocked by:** TC-06, TC-08
- **Scope:** Make an `IN_PORT` result name the last known location, not the route destination, while
  leaving destination fields and map destination unchanged.
- **Target test:** `test_in_port_status_names_last_known_location` using `ABC123`: status says
  `In port New York`; destination remains Helsinki.
- **Capabilities:** `track-cargo.status-text`.

### TC-11 — Fix quirk #17 for claimed-cargo ETA

- **Size:** S
- **Blocked by:** TC-06, TC-08
- **Scope:** Do not display an ETA for a claimed cargo.
- **Target test:** `test_claimed_cargo_hides_eta` using `MNO456`; verify the ETA field/text is absent,
  not a past scheduled date or a fabricated placeholder.
- **Capabilities:** `track-cargo.eta`.

### TC-12 — Implement the map and fix quirk #14

- **Size:** M
- **Blocked by:** TC-02, TC-03, TC-06, TC-08
- **Scope:** Add the Leaflet/OpenStreetMap map frame and its tracking-page integration, using the
  configured location coordinates and status. Apply ruling #14: every marker sits at its exact
  configured coordinates with no random offset.
- **Target test:** `test_map_markers_use_exact_configured_coordinates`; check all rendered marker
  coordinates against seeded location coordinates, and verify the tracked frame carries the
  expected status, origin, destination, and last-known-location data. No API key.
- **Capabilities:** `track-cargo.map-frame`, `track-cargo.map-integration`,
  `track-cargo.map-status-code`.

### TC-13 — Render tracking history, next activity, and misdirection

- **Size:** M
- **Blocked by:** TC-05, TC-06, TC-08, TC-09, TC-10, TC-11, TC-12
- **Scope:** Complete the cargo result presentation and htmx fragment for ordered history,
  expected/unexpected event descriptions and times, empty history, next expected activity, and the
  misdirected warning. Keep the two high-risk view-adapter responsibilities small and testable.
- **Tests:** Targeted view tests for empty and populated histories, event expectation markers, next
  activity presence/absence, and misdirected indicator presence/absence.
- **Capabilities:** `track-cargo.handling-history`, `track-cargo.misdirected-indicator`,
  `track-cargo.next-activity`.

### TC-14 — Replay every golden case against Django

- **Size:** M
- **Blocked by:** TC-09, TC-10, TC-11, TC-12, TC-13
- **Scope:** Replay all eight characterization inputs against the Django app and compare the
  normalized observable result, history, and map-frame data with the corresponding golden records.
  Preserve date normalization and report field-level mismatches; do not broadly ignore snapshot
  differences.
- **Expected, explicitly asserted divergences:** ruling #12 makes empty/unknown messages visible and
  suppresses cargo-dependent content without a cargo; ruling #13 changes `ABC123`'s in-port text
  from the destination to the last known location; ruling #14 removes random marker offsets in favor
  of exact coordinates; ruling #17 hides `MNO456`'s past ETA. All other characterized behavior
  should match.
- **Acceptance:** One differential test per golden record (including empty, unknown, padded, and
  lowercase inputs); expected divergences are named assertions, not blanket exclusions.

### TC-15 — Accept the Track Cargo slice

- **Size:** M
- **Blocked by:** TC-14
- **Scope:** Run slice acceptance through the AFS harness. Re-run all profile gates, including the
  target browser/end-to-end check, verify the approved quirk tests and differential evidence, confirm
  every ledger capability is linked to its implementation ticket and evidence, and attach the
  acceptance report under `.migration/evidence/track-cargo/`.
- **Acceptance:** Build, idiom, tests, CRAP (maximum 30), mutation score (minimum 0.8), and UI
  end-to-end gates pass with fresh `afs-run` evidence; no capability is left unmapped.
- **Capabilities:** none; acceptance ticket covering the complete slice.

## Capability-to-ticket coverage

| Ledger capability | Ticket |
|---|---|
| `track-cargo.data-cargo` | TC-04 |
| `track-cargo.data-handling-event` | TC-05 |
| `track-cargo.data-leg` | TC-04 |
| `track-cargo.data-location` | TC-02 |
| `track-cargo.data-voyage` | TC-03 |
| `track-cargo.domain-event-expectation` | TC-08 |
| `track-cargo.domain-history-order` | TC-05 |
| `track-cargo.domain-route-state` | TC-08 |
| `track-cargo.domain-transport-status` | TC-08 |
| `track-cargo.eta` | TC-11 |
| `track-cargo.handling-history` | TC-13 |
| `track-cargo.map-frame` | TC-12 |
| `track-cargo.map-integration` | TC-12 |
| `track-cargo.map-status-code` | TC-12 |
| `track-cargo.misdirected-indicator` | TC-13 |
| `track-cargo.next-activity` | TC-13 |
| `track-cargo.not-found` | TC-09 |
| `track-cargo.status-text` | TC-10 |
| `track-cargo.tracking-id-entry` | TC-09 |

## Resolved questions (2026-11-01)

1. **Graphs:** both are committed on `main` at `.migration/graphs/source/full/knowledge-graph.json`
   and `domain-graph.json` (#7). Tickets should read them there.
2. **Dates (martins-vds):** display times in **UTC** in the source's format, matching the golden files.
3. **Data (martins-vds):** no production data exists. The target regenerates the sample data as
   fixtures (TC-06), and `data-migration` is not applicable for this pilot (#1 closed).

## Planner return contract

```yaml
plan: .migration/plan/track-cargo.md
slices:
  - name: Track Cargo
    anchor: Tracking form → cargo lookup → result/history/map → cargo, handling, voyage, and location data
    tickets: 15
    blocked_by: []
design_tickets:
  - TC-07 — Design the tracking hot-spot logic
data_slices:
  - TC-02 — Location mappings
  - TC-03 — Voyage mappings
  - TC-04 — Cargo and leg mappings
  - TC-05 — Handling-event mappings
  - TC-06 — Characterized sample-data seed
unmapped_capabilities: []
open_questions:
  - Provide or regenerate source code/domain graph artifacts before dispatch.
  - Decide the target locale/time-zone policy for date display.
  - Clarify whether production Derby-to-PostgreSQL import is a separate future slice.
```
