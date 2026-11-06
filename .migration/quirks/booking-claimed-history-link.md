# Claimed-cargo history link opens the routing-details page

## Question
Should the claimed-cargo link preserve or correct its route to the page labeled as history?

## Evidence
- Source: `src/main/webapp/admin/tables/listClaimed.xhtml:11-19` labels the tracking link tooltip "Click to see history" and routes to `show.xhtml`; `src/main/webapp/admin/show.xhtml:20-112` displays route specification and itinerary state, not handling-event history.
- Characterization: clicking a claimed cargo's tracking ID navigates to the same cargo details page used by routed cargo; that page renders itinerary/routing information.
- Why it looks wrong: the link promises history but its destination does not show handling-event history.

## Impact
- Ledger capabilities: `booking.screen-claimed-table`, `booking.screen-cargo-details`
- Blocks: implementing the claimed-cargo link destination/label in slice `booking` until a human decides.

## Options
1. Preserve exactly (keep the tooltip and routing-details destination).
2. Fix (show the promised history or change the label; record the divergence in the ledger with this ticket as approval).
3. Other
