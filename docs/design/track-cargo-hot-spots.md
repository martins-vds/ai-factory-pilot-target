# Track Cargo hot-spot design

**Ticket:** TC-07 · design only  
**Implementation checklist for:** TC-08, TC-10, TC-13  
**Behavior sources:** the committed source graph, Track Cargo ledger entries, tier-B characterization, and eight tier-A goldens  
**Architecture:** ADR-0001 through ADR-0003 and decision map #3

This design records the behavior to preserve or intentionally diverge from, and proposes small,
testable methods for the five risk-map hot spots. It adds no target implementation or tests. Domain
rules remain framework-free in `cargo.domain`; presentation formatting remains in tracking
interface adapters. Domain tests need no database. Adapter tests exercise their interface without
moving domain decisions into templates.

## Decisions

| Hot spot | Decision to carry into implementation | Evidence and ruling |
|---|---|---|
| `Itinerary.isExpected` | An empty itinerary accepts every declared handling-event type. Otherwise, `RECEIVE` is expected at the first leg's load location; `LOAD` and `UNLOAD` must match the applicable leg's location and voyage; `CLAIM` is expected at the final destination; `CUSTOMS` is expected. An event that does not match the route is unexpected. | Tier B `emptyItineraryAcceptsEveryHandlingType`; `abc123.json`, `jkl567.json`, and `mno456.json`; ledger `track-cargo.domain-event-expectation`. `jkl567.json` contains the unexpected final load. |
| `Delivery.calculateNextExpectedActivity` | With a routed, on-track delivery: no latest event means `RECEIVE` at the origin; `RECEIVE` → first-leg `LOAD`; `LOAD` → that leg's `UNLOAD`; intermediate `UNLOAD` → next-leg `LOAD`; final `UNLOAD` → `CLAIM` at destination; `CLAIM` → no activity. Unrouted or misdirected deliveries have no next activity. | Tier B `nextActivityForNoEventAndReceive`, `nextActivityAfterLoadAndUnload`, and `offTrackAndUnroutedCargoHaveNoNextActivity`; golden `abc123.json`, `def789.json`, `jkl567.json`, and `mno456.json`; ledger `track-cargo.domain-route-state` and `track-cargo.next-activity`. |
| `Delivery.calculateTransportStatus` | No latest event → `NOT_RECEIVED`; `LOAD` → `ONBOARD_CARRIER`; `UNLOAD`, `RECEIVE`, and `CUSTOMS` → `IN_PORT`; `CLAIM` → `CLAIMED`. Misdirection does not replace the status derived from the latest event. Preserve `UNKNOWN` as the fallback, but do not invent an event type to exercise it: the source default is unreachable for declared event types. | Tier B `transportStatusUsesTheLastEventType`; golden `abc123.json`, `def789.json`, `jkl567.json`, and `mno456.json`; ledger `track-cargo.domain-transport-status`. |
| `CargoTrackingViewAdapter.getStatusText` | Keep status-to-text formatting in the interface adapter. `IN_PORT` must say `In port {last-known location}` in the target, while destination and map-destination data remain unchanged. Other observed results are `Onboard voyage {number}`, `Not received`, and `Claimed`. | Goldens `abc123.json`, `jkl567.json`, `def789.json`, and `mno456.json`; ledger `track-cargo.status-text`. **Approved divergence #13:** source `abc123.json` says “In port Helsinki”; target must say “In port New York.” |
| `HandlingEventViewAdapter.getDescription` | Keep event wording in the interface adapter and derive the expected/unexpected marker from the domain result; do not duplicate itinerary rules in presentation code. Format all five event types with their observed location/voyage wording and preserve UTC source-format timestamps. | Goldens `abc123.json`, `jkl567.json`, and `mno456.json`; ledger `track-cargo.handling-history`. `jkl567.json` pins an unexpected event; `mno456.json` adds `CUSTOMS` and `CLAIM`. |

### Cross-cutting quirk rulings

| Ruling | Required outcome for this design |
|---|---|
| #12 — empty and unknown tracking IDs | Fix: show visible validation/not-found feedback and render no cargo result, history, or map when there is no cargo. Do not render an empty-history label by dereferencing a missing cargo. Golden `empty-id.json` and `unknown-id.json` record the source behavior; target lookup-message and no-cargo tests belong to TC-09, with the no-cargo view invariant also checked by TC-13. |
| #13 — `IN_PORT` names destination | Fix as above: use last-known location for the status sentence; preserve the route destination in its own field and in map data. TC-10 owns the behavior-changing assertion. |
| #14 — randomized map-marker offsets | Fix: configured coordinates are exact. This does not change any of these five methods; the map assertion belongs to TC-12. |
| #17 — claimed-cargo past ETA | Fix: a claimed cargo has no displayed ETA. The domain next activity remains absent after `CLAIM`; do not conflate this activity result with ETA policy. TC-11 owns the ETA assertion. |

The source `ItineraryTest.testNextExpectedEvent` is an empty TODO and is not evidence or coverage.
Use the tier-B cases and goldens cited here instead. The tier-B switch defaults for event expectation
and transport status are unreachable for the five declared event types; keep a safe fallback, but do
not fabricate a sixth event solely to exercise it.

## Proposed decomposition and CRAP targets

The plan's maximum is CRAP 30 per method, with complexity and coverage inputs enabled. Use
`CRAP = CC² × (1 − coverage)³ + CC`. The bounds below are cyclomatic-complexity (CC) design targets,
not claims of measured target scores. Keep each resulting method at CC ≤4 where practical (hard
ceiling 5); at CC ≤5 the formula is at most 30 even at zero coverage. Still measure actual coverage
and CRAP through the configured gate in implementation. Do not use exclusions, fake coverage,
suppressed complexity, or omit helpers from the input.

| Current hot spot | Proposed shape | Target CC per resulting method |
|---|---|---|
| `Itinerary.isExpected` — risk CC 13 / CRAP 182 | Keep the public decision as a small empty-itinerary guard and event-type dispatch. Put the route comparison for `RECEIVE`, `LOAD`, `UNLOAD`, and `CLAIM` in focused private predicates. Treat `CUSTOMS` and empty-itinerary acceptance as simple policy outcomes. Reuse the route's existing leg data; do not add a generic rules framework. | `is_expected` ≤2; `_receive_matches_first_leg` ≤2; `_load_matches_leg` ≤3; `_unload_matches_leg` ≤3; `_claim_matches_destination` ≤2. |
| `Delivery.calculateTransportStatus` — risk CC 7 / CRAP 56 | Replace the branching event switch with an explicit mapping from each declared event type to status, plus the no-event guard and `UNKNOWN` fallback. Keep it as domain logic. | `calculate_transport_status` ≤2; no helper is needed. |
| `Delivery.calculateNextExpectedActivity` — risk CC 12 / CRAP 156 | Keep routing/misdirection and no-event policy in a shallow public dispatcher. Extract the event transitions: after receive, after load, and after unload (next leg or final claim). A single focused leg lookup may be shared if it avoids repeating route-search conditions; avoid a second route state machine. Return no activity after claim. | `calculate_next_expected_activity` ≤4; `_after_receive` ≤2; `_after_load` ≤2; `_after_unload` ≤3; any shared leg lookup ≤3. |
| `CargoTrackingViewAdapter.getStatusText` — risk CC 6 / CRAP 42 | Keep formatting at the interface seam. Use a small lookup for constant texts and isolate only the dynamic `IN_PORT` and `ONBOARD_CARRIER` formatting if needed. Implement ruling #13 using last-known location, not destination. Keep the public adapter contract stable. | `get_status_text` ≤3; each dynamic formatter ≤1. |
| `HandlingEventViewAdapter.getDescription` — risk CC 6 / CRAP 42 | Use a fixed event-type-to-description format mapping (or equally small explicit dispatch) for `RECEIVE`, `LOAD`, `UNLOAD`, `CLAIM`, and `CUSTOMS`. Keep description generation separate from event-expectation policy; preserve event marker and UTC rendering in the containing history row. | `get_description` ≤2; any formatter helper ≤2. |

The separate `CargoTrackingViewAdapter.getNextExpectedActivity` is not one of these two CRAP-42
hot spots (ledger risk CC 5 / CRAP 30). TC-13 should characterize its output and absence behavior,
but should not expand or move domain decisions into that adapter.

## Test-first inventory

Every listed case is anchored to a golden file or tier-B characterization. Any single-field negative
variant is explicitly derived from the cited observed positive/negative route case and must test the
same public method; it is not represented as a separately observed source result.

### TC-08 — domain calculations

#### `Itinerary.isExpected`

| Case | Input/state | Expected | Trace |
|---|---|---|---|
| IE-1 | Empty itinerary; each declared type: `RECEIVE`, `LOAD`, `UNLOAD`, `CLAIM`, `CUSTOMS` | `true` for every type, even if an activity would not otherwise fit a route | Tier B `emptyItineraryAcceptsEveryHandlingType` |
| IE-2 | `RECEIVE` at first-leg origin | Expected | `abc123.json` (Hong Kong) and `mno456.json` (New York) |
| IE-3 | `LOAD` at a planned leg's load location with its voyage | Expected | `abc123.json` (Hong Kong / 0100S) and `mno456.json` (New York / 0200T) |
| IE-4 | `UNLOAD` at a planned leg's unload location with its voyage | Expected | `abc123.json` (New York / 0100S) and `mno456.json` (Dallas / 0200T) |
| IE-5 | `CLAIM` at final destination | Expected | `mno456.json` (Dallas) |
| IE-6 | `CUSTOMS` | Expected | `mno456.json` (customs in Dallas) |
| IE-7 | Event at a location/voyage not matching the itinerary | Unexpected; delivery is misdirected | `jkl567.json` (unexpected final load in New York) and tier B `offTrackAndUnroutedCargoHaveNoNextActivity` (off-route receive). A focused wrong-location or wrong-voyage variant may change one field of this fixture. |

#### `Delivery.calculateTransportStatus`

| Case | Latest event | Expected status | Trace |
|---|---|---|---|
| TS-1 | None | `NOT_RECEIVED` | Tier B `transportStatusUsesTheLastEventType`; `def789.json` |
| TS-2 | `LOAD` | `ONBOARD_CARRIER` | Tier B `transportStatusUsesTheLastEventType`; `jkl567.json` |
| TS-3 | `UNLOAD` | `IN_PORT` | Tier B `transportStatusUsesTheLastEventType`; `abc123.json` |
| TS-4 | `RECEIVE` | `IN_PORT` | Tier B `transportStatusUsesTheLastEventType` |
| TS-5 | `CUSTOMS` | `IN_PORT` | Tier B `transportStatusUsesTheLastEventType` |
| TS-6 | `CLAIM` | `CLAIMED` | Tier B `transportStatusUsesTheLastEventType`; `mno456.json` |
| TS-7 | `LOAD` whose location makes the cargo misdirected | Still `ONBOARD_CARRIER`; routing state is separate from transport status | `jkl567.json`; tier B `offTrackAndUnroutedCargoHaveNoNextActivity` |

#### `Delivery.calculateNextExpectedActivity`

| Case | Delivery state | Expected activity | Trace |
|---|---|---|---|
| NA-1 | Routed itinerary, no latest event | `RECEIVE` at origin, no voyage | Tier B `nextActivityForNoEventAndReceive` |
| NA-2 | Latest event `RECEIVE` at origin | `LOAD` on first leg | Tier B `nextActivityForNoEventAndReceive` |
| NA-3 | Latest event `LOAD` on a leg | `UNLOAD` at that leg's destination, same voyage | Tier B `nextActivityAfterLoadAndUnload` |
| NA-4 | `UNLOAD` at an intermediate location | `LOAD` on the next leg | Tier B `nextActivityAfterLoadAndUnload` |
| NA-5 | `UNLOAD` at final destination | `CLAIM` at destination, no voyage | Tier B `nextActivityAfterLoadAndUnload` |
| NA-6 | Latest event `CLAIM` | No activity | Tier B `nextActivityAfterLoadAndUnload`; `mno456.json` |
| NA-7 | Empty history and no itinerary / unrouted | No activity | Tier B `offTrackAndUnroutedCargoHaveNoNextActivity`; `def789.json` |
| NA-8 | Off-route latest event / misdirected delivery | No activity | Tier B `offTrackAndUnroutedCargoHaveNoNextActivity`; `jkl567.json` |
| NA-9 | `CUSTOMS` before final `CLAIM` | Do not add a separate transition assertion from these artifacts: tier B does not characterize the intermediate next-activity state. The seeded `mno456.json` covers the customs event and the subsequent claimed/no-activity state. | `mno456.json`; tier B `nextActivityAfterLoadAndUnload` |

### TC-10 — status text

| Case | Domain status / cargo | Expected target result | Trace and ruling |
|---|---|---|---|
| ST-1 | `IN_PORT`, ABC123 last-known New York, destination Helsinki | `In port New York`; destination remains Helsinki and map destination stays Helsinki | `abc123.json`; approved quirk #13 |
| ST-2 | `ONBOARD_CARRIER`, JKL567 voyage 0100S | `Onboard voyage 0100S` | `jkl567.json` |
| ST-3 | `NOT_RECEIVED`, DEF789 | `Not received` | `def789.json` |
| ST-4 | `CLAIMED`, MNO456 | `Claimed` | `mno456.json` |
| ST-5 | No cargo after empty or unknown lookup | No status adapter/result, history, or map is rendered; visible lookup feedback is owned by TC-09 | `empty-id.json`, `unknown-id.json`; approved quirk #12 |

The ledger's `[Unknown status]` fallback has no golden or reachable tier-B event case. Preserve the
fallback if the target status type supports it, but do not invent a source event or count it as
characterized coverage.

### TC-13 — history row descriptions and presentation

| Case | Row/state | Expected result | Trace |
|---|---|---|---|
| HD-1 | `RECEIVE` | `Received in {location}` and expected marker | `abc123.json` (Hong Kong), `mno456.json` (New York) |
| HD-2 | `LOAD` | `Loaded onto voyage {number} in {location}` and expected marker | `abc123.json` and `mno456.json` |
| HD-3 | `UNLOAD` | `Unloaded off voyage {number} in {location}` and expected marker | `abc123.json` and `mno456.json` |
| HD-4 | `CUSTOMS` | `Cleared customs in {location}` and expected marker | `mno456.json` |
| HD-5 | `CLAIM` | `Claimed in {location}` and expected marker | `mno456.json` |
| HD-6 | Route-mismatching `LOAD` | Same event description, unexpected marker; presentation does not recompute expectation | `jkl567.json` |
| HD-7 | Cargo with empty history | Show its empty-history sentence and zero rows | `def789.json` |
| HD-8 | No cargo (empty/unknown lookup) | Suppress cargo-dependent history and empty-history sentence; do not dereference a missing tracking ID | `empty-id.json`, `unknown-id.json`; approved quirk #12 |
| HD-9 | Populated history dates | Keep completion-time order and source date format in UTC; compare normalized date values, not host-local rendering | `abc123.json`, `jkl567.json`, and `mno456.json`; decision map #3 UTC decision |

Exercise adapter descriptions with each event type through the adapter interface. Assert both the
rendered description and the supplied expected flag for HD-1 through HD-6. In particular, keep the
unexpected JKL567 marker, the empty `DEF789` history, and the no-cargo #12 behavior distinct.

## Implementation handoff checklist

- [ ] TC-08: add domain tests first for IE-1–IE-7, TS-1–TS-7, and NA-1–NA-9; then implement with
  pure domain methods and no Django imports.
- [ ] TC-08: retain the five declared event types and unreachable-default note; don't promote the
  empty `ItineraryTest.testNextExpectedEvent` TODO to evidence.
- [ ] TC-10: test ST-1 as an explicit approved divergence, including unchanged destination/map data;
  test the other three observed statuses.
- [ ] TC-13: test HD-1–HD-9, UTC/source formatting, ordered rows, event flags, and no-cargo
  suppression. Keep the next-activity adapter a formatter over the domain result.
- [ ] All tickets: run the existing configured complexity and coverage gates; each resulting method
  must be at or below CRAP 30 using real inputs, without suppressions.
- [ ] Keep ETA quirk #17 in TC-11 and map quirk #14 in TC-12; do not absorb either into these
  hot-spot implementations.
