# Booking detail lookup does not handle an unknown tracking ID

## Question
Should the source's unhandled unknown-tracking-ID failure be preserved or replaced with a deliberate not-found response?

## Evidence
- Source: `src/main/java/org/eclipse/cargotracker/infrastructure/persistence/jpa/JpaCargoRepository.java:32-44` returns `null` when no `Cargo.findByTrackingId` result exists; `src/main/java/org/eclipse/cargotracker/interfaces/booking/facade/internal/DefaultBookingServiceFacade.java:66-70` passes that null to `CargoRouteDtoAssembler.toDto`; `src/main/java/org/eclipse/cargotracker/interfaces/booking/facade/internal/assembler/CargoRouteDtoAssembler.java:12-22` dereferences it. The detail pages also dereference `cargoDetails.cargo`.
- Characterization: an unknown ID produces null at the repository boundary and has no explicit not-found branch in the facade/assembler/page flow.
- Why it looks wrong: an invalid or stale URL is handled as an unhandled null dereference rather than a user-visible not-found state.

## Impact
- Ledger capabilities: `booking.cargo-details`, `booking.routing.candidates`
- Blocks: implementing the not-found behavior of cargo detail and routing lookup until a human decides.

## Options
1. Preserve exactly (the target reproduces the unhandled failure; a test pins it).
2. Fix (the target returns an explicit not-found response; record the divergence in the ledger with this ticket as approval).
3. Other
