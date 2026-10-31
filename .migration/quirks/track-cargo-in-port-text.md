# Should IN_PORT name the destination or current location?

## Question
The status adapter renders `In port {route destination}` for every IN_PORT cargo, rather than naming the last-known location; preserve, fix, or something else?

## Evidence
- Source: `src/main/java/org/eclipse/cargotracker/interfaces/tracking/web/CargoTrackingViewAdapter.java:81-88`.
- Characterization: Static source trace only. For an IN_PORT cargo whose last-known location differs from its route destination, `getStatusText()` still returns `In port {destination name}`.
- Why it looks wrong: The text can identify the destination as the current port even while the latest handling event places the cargo elsewhere.

## Impact
- Ledger capabilities: `track-cargo.status-text`
- Blocks: `martins-vds/ai-factory-pilot-target#10`

## Options
1. Preserve exactly (target reproduces the quirk; a test pins it)
2. Fix (target diverges; the divergence is recorded in the ledger with this ticket as approval)
3. Other
