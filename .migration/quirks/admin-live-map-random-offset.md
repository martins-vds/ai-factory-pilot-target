# Admin all-cargo map randomly shifts markers west and south

## Question
The source independently offsets each marker latitude and longitude by a random integer from -3 through -1 degrees on every map load; should the admin map preserve this behavior, use exact coordinates as in Track Cargo ruling #14, or do something else?

## Evidence
- Source: `.source/src/main/webapp/admin/tracking/mapFrame.xhtml:186-191` at `eclipse-ee4j/cargotracker@f3beacf78de4f6d34edc4971ac87e38a5c6fe59d`.
- Observation: both offsets are `Math.floor((Math.random() * 3) - 3)`. This source inspection establishes the formula; no new live-map runtime observation was made in this analyst task.
- Ruling: #14 fixes exact coordinates for Track Cargo only; parent task #99 leaves its applicability to this separate all-cargo map unresolved.
- Why it looks wrong: the offset is always negative and varies on reload, so marker positions do not remain at the configured city coordinates.

## Impact
- Ledger capabilities: `admin-live-map.marker-coordinates`.
- Blocks: implementation of the admin all-cargo marker coordinates until a human decides.

## Options
1. Preserve exactly (the target reproduces the random negative offsets and pins them with tests).
2. Fix (the target uses exact configured coordinates; record the approved divergence).
3. Other (specify an admin-map-specific placement rule).
