# Next activity uses the first matching location on a repeated route

## Question
For a route that visits the same location more than once, should next-activity calculation preserve the source's first location-only leg match, follow the leg and voyage of the latest event, or do something else?

## Evidence
- Source: `.source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java:273-303` at pinned SHA `f3beacf78de4f6d34edc4971ac87e38a5c6fe59d`; `LOAD` and `UNLOAD` lookup uses location without matching the event's voyage.
- Characterization: tier-B and golden cases do not contain a repeated route location. Source-only case: itinerary A→B on V1, B→A on V2, A→C on V3; after the expected `LOAD` at A on V3, the source returns `UNLOAD` at B on V1.
- Why it looks wrong: the suggested next activity can refer to an earlier leg and voyage instead of the leg used by the latest event.

## Impact
- Ledger capabilities: `track-cargo.domain-route-state`, `track-cargo.next-activity`
- Blocks: no characterized TC-08 cases; any future fix needs a human ruling before changing the source-compatible result.

## Options
1. Preserve exactly and pin the repeated-location result with a test.
2. Fix the lookup to follow the event's matching leg/voyage and record the divergence with this ticket as approval.
3. Other
