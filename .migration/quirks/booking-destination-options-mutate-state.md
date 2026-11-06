# Booking destination options mutate the backing location list

## Question
Should the target preserve or fix the destination-options getter mutating the bean's location list?

## Evidence
- Source: `src/main/java/org/eclipse/cargotracker/interfaces/booking/web/ChangeDestination.java:58-68` at `f3beacf78de4f6d34edc4971ac87e38a5c6fe59d`.
- Characterization: `getPotentialDestinations()` builds a removal list for origin and current destination, calls `locations.removeAll(...)` on the bean field, and returns that same mutated list.
- Why it looks wrong: a presentation getter changes stored bean state; subsequent calls observe a shortened list rather than the full location set loaded by `load()`.

## Impact
- Ledger capabilities: `booking.dialog.destination-options`
- Blocks: implementation of the destination-dialog capability in slice `booking` until a human decides.

## Options
1. Preserve exactly (the target reproduces the mutation; a test pins it).
2. Fix (the target returns filtered options without mutating its backing list; the divergence is recorded in the ledger with this ticket as approval).
3. Other
