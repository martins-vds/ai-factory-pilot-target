# HR-04A — Cargo inspection re-derivation design

## Boundary and decisions

HR-04D processes an accepted handling attempt and, in the same database transaction, stores the handling event, rebuilds delivery from the cargo's complete history, persists the cargo snapshot, and marks the attempt registered. A permanent reference failure is rejected before inspection; it is not the inspection service's missing-cargo no-op.

Reuse `cargotracker.cargo.domain.delivery.Delivery.derived_from(route_specification, itinerary, handling_history)` for all delivery calculations. Do not copy its status, location, voyage, misdirection, ETA, next-activity, or destination-unload rules into handling code. Persist through `DjangoCargoRepository.upsert`, which maps the Delivery fields to the existing Cargo record. Follow the sample seeder's `dataclasses.replace(..., last_event_id=...)` pattern, but associate the ID of the history's latest-completion event—not necessarily the event most recently submitted. The history repository may expose that event's record ID for this purpose.

## Decision table

| Case / input | Inspection decision | Delivery and persistence | Outcome |
|---|---|---|---|
| Cargo lookup returns no cargo | Log the missing cargo and return before loading history. | No delivery derivation or cargo write. | No misdirected/delivered log and no inspection event. In HR-04D, a missing cargo reference during attempt validation is instead a permanent rejection before inspection. |
| Cargo exists; history is empty | Load the empty history and derive through the existing `Delivery`. | Persist the re-derived snapshot; the latest event ID is null. The existing Delivery rules yield no last location, `NOT_RECEIVED`, not misdirected, and not unloaded at destination. | No outcome log. |
| Cargo exists; events have distinct completion times, including insertion/submission order different from completion order | Load all events for this cargo. `HandlingHistory` deduplicates and sorts by completion time; use its most-recent event, not database or processing order. | Derive the entire Delivery from route specification, itinerary, and the complete ordered history. Persist its fields and the ID of the event with the greatest completion time. | Evaluate outcomes from the re-derived Delivery. |
| Latest event is not expected by the itinerary | No special handling branch in the derivation. | `Delivery.misdirected` is true; persist it with the other derived fields. | Emit the misdirected outcome log once; do not enqueue a message. |
| Latest event is `UNLOAD` at the route-specification destination | No special handling branch in the derivation. | `Delivery.unloaded_at_destination` is true; persist it with the other derived fields. | Emit the delivered outcome log once; do not enqueue a message. |
| The two Delivery outcome flags are both true | Keep the predicates independent; do not make delivered and misdirected mutually exclusive with `elif`. | Persist the same derived snapshot once. | Emit both outcome logs. |
| Event completion times tie | The source sorts by completion time without specifying a tie-breaker; set iteration can determine which event is last. | Order ties by registration time, then handling-event id, in `HandlingHistory` (ruling [#136](https://github.com/martins-vds/ai-factory-pilot-target/issues/136), fix). | HR-04D adds the equal-completion-time test and covers the resulting delivery outcome. |
| Failure occurs during event persistence, re-derivation, cargo persistence, or terminal attempt update | Let the failure reach the transaction boundary. | Roll back the event, cargo snapshot, and attempt state together; do not leave a partially registered attempt. | Retry/reject according to the existing HR-04D failure classification, not an inspection-specific queue. |

The source calls the misdirected and arrival notifications independently. The target retires those queues per ruling #87 and retains each applicable result as a log line. The separate `CargoInspected` source event is not part of the target contract.

## Test-first checklist for HR-04D

Write these PostgreSQL-backed tests before implementation in `tests/handling/test_registration_processing.py`; use stable completion timestamps and seeded route/event fixtures. Assert persisted state by reloading through the repositories, not only against in-memory objects.

1. **Missing references and missing cargo**
   - Unknown cargo is rejected by attempt reference validation; no handling event, history lookup, cargo write, or outcome log occurs.
   - If the inspection seam receives no cargo, it returns without history lookup, cargo persistence, or outcome logs.
2. **History loading and ordering**
   - Processing loads the full history for the cargo after the new event is stored, so that event is included.
   - Insert two or more events in an order different from their distinct completion times. Assert chronological order, the greatest-completion event drives Delivery, and its handling-record ID is persisted as `last_event_id`.
   - Assert events for another cargo are excluded. Exercise a repeated upsert to verify the history remains distinct.
   - Assert the tie order ruled in [#136](https://github.com/martins-vds/ai-factory-pilot-target/issues/136): registration time, then event id.
3. **Delivery re-derivation and persistence**
   - Assert `Delivery.derived_from` receives the cargo's route specification, itinerary, and full `HandlingHistory`; cover empty history and a history containing RECEIVE, LOAD/UNLOAD, and a final CLAIM or CUSTOMS.
   - After the transaction, reload the cargo and assert the stored transport status, last known location, current voyage, misdirected flag, ETA, next expected activity, unloaded-at-destination flag, routing status, and latest event ID match the derived Delivery. Do not assert an exact `calculated_at` clock value.
   - Force a failure after event insertion and assert PostgreSQL rolls back the event, cargo snapshot, and registered attempt state together.
4. **Misdirected and delivered outcomes**
   - Use a latest event outside the itinerary to assert the misdirected flag and one misdirected log; use an expected event to assert no such log.
   - Assert destination `UNLOAD` logs delivered; a destination event of another type and an `UNLOAD` elsewhere do not.
   - Assert each outcome is independently evaluated and both logs occur when both derived flags are true. Assert no JMS/broker/notification queue is used.
5. **Complexity guard**
   - Keep processing orchestration, event registration/reference resolution, history re-derivation, outcome logging, and persistence/attempt-state transitions in small, single-purpose methods. Run the profile CRAP gate and keep every changed method at or below 30; do not modify or duplicate `Delivery` calculations.

The HR-04A design is complete with this checklist; the three inspection/outcome ledger capabilities remain `pending` until HR-04D implements or retires them.
