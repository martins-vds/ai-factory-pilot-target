# Routing request omits the arrival deadline

## Question
Should the candidate-routing request preserve or change the source's omission of the arrival deadline?

## Evidence
- Source: `src/main/java/org/eclipse/cargotracker/infrastructure/routing/ExternalRoutingService.java:60-68` sends only origin and destination; `src/main/java/org/eclipse/pathfinder/api/GraphTraversalService.java:34-38` accepts `deadline`, and `:38-77` generates candidates without using it. `RouteSpecification.isSatisfiedBy` later filters candidates at `src/main/java/org/eclipse/cargotracker/infrastructure/routing/ExternalRoutingService.java:73-81`.
- Characterization: route requests are generated without deadline input, then candidates arriving after the specification deadline are discarded.
- Why it looks wrong: feasible candidates are not generated against the requested deadline, so random generation can produce an empty result even when a timely path might exist. Decision #89 covers random route preservation but does not state whether this deadline behavior is intentional.

## Impact
- Ledger capabilities: `booking.routing.candidates`
- Blocks: implementation of candidate generation/filtering in slice `booking` until a human decides.

## Options
1. Preserve exactly (omit the deadline from generation and filter returned candidates; pin the behavior).
2. Fix (use deadline while generating candidates; record the divergence in the ledger with this ticket as approval).
3. Other
