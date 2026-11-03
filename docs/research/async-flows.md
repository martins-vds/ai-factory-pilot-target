# Research: how Cargo Tracker's asynchronous flows behave end to end

Answers the wayfinder research ticket *How do Cargo Tracker's asynchronous flows behave end to end?*
(martins-vds/ai-factory-pilot-target#86). Source: `eclipse-ee4j/cargotracker` at the pinned SHA
`f3beacf78de4f6d34edc4971ac87e38a5c6fe59d`; every claim links the line it rests on. Cross-checked against the
enriched source graph (`.migration/graphs/source/full`, harness ADR-0020).

## Summary

Handling-event registration is **fire-and-forget in two asynchronous steps**:

1. **Three front doors send a registration attempt to a queue and return at once.** These are REST
   `POST /handling/reports`, the event-logger page and the upload-folder batch job. None of them can tell
   the caller whether the event was registered.
2. **A consumer registers the handling event** (persisted), then queues "cargo handled".
3. **A second consumer inspects the cargo**: it re-derives the delivery state from the history, stores
   it, queues "misdirected" or "delivered" (both consumers only log), and fires an in-process event
   that pushes a JSON update to every open WebSocket session on the admin dashboard.

Between step 2 and step 3, the new handling event is stored but the cargo's derived delivery (status,
last known location, next activity) is not yet updated.

## The five queues

| Queue | Sent by | Consumed by | What the consumer does |
|---|---|---|---|
| `HandlingEventRegistrationAttemptQueue` | the three front doors, via [JmsApplicationEvents.java:62:62](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/infrastructure/messaging/jms/JmsApplicationEvents.java#L62) | `HandlingEventRegistrationAttemptConsumer` | registers the handling event ([HandlingEventRegistrationAttemptConsumer.java:32](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/infrastructure/messaging/jms/HandlingEventRegistrationAttemptConsumer.java#L32)) |
| `CargoHandledQueue` | `DefaultHandlingEventService` after storing the event ([DefaultHandlingEventService.java:53](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/application/internal/DefaultHandlingEventService.java#L53)) | `CargoHandledConsumer` | inspects the cargo ([CargoHandledConsumer.java:41](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/infrastructure/messaging/jms/CargoHandledConsumer.java#L41)) |
| `MisdirectedCargoQueue` | `DefaultCargoInspectionService` when the cargo is misdirected ([DefaultCargoInspectionService.java:51](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/application/internal/DefaultCargoInspectionService.java#L51)) | `MisdirectedCargoConsumer` | logs one INFO line only ([MisdirectedCargoConsumer.java:24](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/infrastructure/messaging/jms/MisdirectedCargoConsumer.java#L24)) |
| `DeliveredCargoQueue` | `DefaultCargoInspectionService` when unloaded at destination ([DefaultCargoInspectionService.java:55](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/application/internal/DefaultCargoInspectionService.java#L55)) | `DeliveredCargoConsumer` | logs one INFO line only ([DeliveredCargoConsumer.java:24](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/infrastructure/messaging/jms/DeliveredCargoConsumer.java#L24)) |
| `RejectedRegistrationAttemptsQueue` | **nothing**: defined in [web.xml:95](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/webapp/WEB-INF/web.xml#L95), but no code sends to it (also absent as a `publishes` edge in the graph) | `RejectedRegistrationAttemptsConsumer` | would log one INFO line ([RejectedRegistrationAttemptsConsumer.java:24](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/infrastructure/messaging/jms/RejectedRegistrationAttemptsConsumer.java#L24)) |

All messages are sent at low priority, without message IDs or timestamps. A registration attempt's
time-to-live is **1000 ms** ([JmsApplicationEvents.java:62:62](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/infrastructure/messaging/jms/JmsApplicationEvents.java#L62)):
an attempt not delivered within one second expires and is dropped.

## What each caller observes

- **REST `POST /handling/reports`** ([HandlingReportService.java:44](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/interfaces/handling/rest/HandlingReportService.java#L44)): bean
  validation on the JSON body; parses the completion time (`yyyy-MM-dd HH:mm`); sends the attempt
  ([HandlingReportService.java:62](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/interfaces/handling/rest/HandlingReportService.java#L62)); returns no body (`void`). An unparseable
  completion time is rethrown as a `RuntimeException` ([HandlingReportService.java:64](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/interfaces/handling/rest/HandlingReportService.java#L64)),
  so the client gets a server error rather than a validation error. Unknown cargo, voyage or location are
  not checked here, so the client is told nothing about them.
- **Event-logger page** (`src/main/webapp/event-logger/`, bean `EventLogger`): sends the attempt
  ([EventLogger.java:189](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/interfaces/handling/mobile/EventLogger.java#L189)) and always shows "Event submitted"
  ([EventLogger.java:191](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/interfaces/handling/mobile/EventLogger.java#L191)).
- **Upload folder (batch)**: a timer starts the batch job every **2 minutes**; its comment says
  "fifteen" ([UploadDirectoryScanner.java:18](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/interfaces/handling/file/UploadDirectoryScanner.java#L18)).
  - **Input:** the job reads every file in `/tmp/uploads`
    ([EventFilesProcessorJob.xml:5:5](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/resources/META-INF/batch-jobs/EventFilesProcessorJob.xml#L5))
    in chunks of 12 lines ([EventFilesProcessorJob.xml:16:16](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/resources/META-INF/batch-jobs/EventFilesProcessorJob.xml#L16)).
  - **Each good line:** sent as an attempt and appended to an archive CSV
    ([EventItemWriter.java:51](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/interfaces/handling/file/EventItemWriter.java#L51)).
  - **Each unparseable line:** appended to `/tmp/failed/failed_<job>_<instance>.csv`
    ([LineParseExceptionListener.java:45](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/interfaces/handling/file/LineParseExceptionListener.java#L45)).
  - **The file itself:** deleted once read ([EventItemReader.java:82](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/interfaces/handling/file/EventItemReader.java#L82)).
  - **No row-level verification:** a line that parses but names an unknown cargo is archived as if it
    succeeded.
- **Tracking page (already migrated) and the admin dashboard**: see "Consistency window" below.

## Registration, step by step

1. `HandlingEventRegistrationAttemptConsumer` calls `registerHandlingEvent`
   ([HandlingEventRegistrationAttemptConsumer.java:32](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/infrastructure/messaging/jms/HandlingEventRegistrationAttemptConsumer.java#L32)).
2. `DefaultHandlingEventService` (a stateless EJB, container-managed transaction,
   [DefaultHandlingEventService.java:20](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/application/internal/DefaultHandlingEventService.java#L20)) creates the event with the factory, stores
   it ([DefaultHandlingEventService.java:50](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/application/internal/DefaultHandlingEventService.java#L50)), then sends "cargo handled"
   ([DefaultHandlingEventService.java:53](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/application/internal/DefaultHandlingEventService.java#L53)). Its own comment notes that the cargo
   aggregate is updated "asynchronously!" ([DefaultHandlingEventService.java:48](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/application/internal/DefaultHandlingEventService.java#L48)).
3. **Rejection:** the factory throws for unknown cargo, voyage or location
   ([HandlingEventFactory.java:67](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/domain/model/handling/HandlingEventFactory.java#L67), [HandlingEventFactory.java:81](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/domain/model/handling/HandlingEventFactory.java#L81),
   [HandlingEventFactory.java:91](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/domain/model/handling/HandlingEventFactory.java#L91)). The consumer rethrows as a `RuntimeException`, so the
   message is redelivered and finally goes to the **server's** dead-letter queue, as its comment says
   ([HandlingEventRegistrationAttemptConsumer.java:35](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/infrastructure/messaging/jms/HandlingEventRegistrationAttemptConsumer.java#L35)). It does not go to
   `RejectedRegistrationAttemptsQueue`. Nothing user-visible happens.
4. `CargoHandledConsumer` calls `inspectCargo` ([CargoHandledConsumer.java:41](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/infrastructure/messaging/jms/CargoHandledConsumer.java#L41)).
   This:
   - re-derives delivery progress from the full history ([DefaultCargoInspectionService.java:48](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/application/internal/DefaultCargoInspectionService.java#L48));
   - queues "misdirected" or "delivered" ([DefaultCargoInspectionService.java:51](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/application/internal/DefaultCargoInspectionService.java#L51),
     [DefaultCargoInspectionService.java:55](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/application/internal/DefaultCargoInspectionService.java#L55));
   - stores the cargo ([DefaultCargoInspectionService.java:58](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/application/internal/DefaultCargoInspectionService.java#L58));
   - fires the in-process `@CargoInspected` event ([DefaultCargoInspectionService.java:60](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/application/internal/DefaultCargoInspectionService.java#L60)).
5. `RealtimeCargoTrackingService`, the WebSocket endpoint `/tracking`
   ([RealtimeCargoTrackingService.java:28](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/interfaces/booking/socket/RealtimeCargoTrackingService.java#L28)), observes that event
   ([RealtimeCargoTrackingService.java:48](https://github.com/eclipse-ee4j/cargotracker/blob/f3beacf78de4f6d34edc4971ac87e38a5c6fe59d/src/main/java/org/eclipse/cargotracker/interfaces/booking/socket/RealtimeCargoTrackingService.java#L48)). It sends every open session a JSON
   object with `trackingId`, `origin`, `destination`, `lastKnownLocation` and `transportStatus`.

## Consistency window

Between steps 2 and 4, a tracking lookup shows the new event in the handling history (read live), but the
cargo's stored delivery state (transport status, last known location, misdirection, ETA, next activity)
is from before it. The window lasts as long as the "cargo handled" message waits. The dashboard's live
update arrives only after inspection.

## Facts the decisions downstream depend on

- **What the async design is for:** what is observable is "accepted immediately; registered later, or
  silently not at all". No front door reports success or rejection. Rejections leave only server logs
  and the server's dead-letter queue.
- **Loss is possible by design:** the 1-second time-to-live means a registration attempt can expire
  unconsumed under load.
- **Only two consumers do work** (registration and inspection). The misdirected, delivered and rejected
  consumers only log, and the rejected queue is never fed.
- **The real-time push depends on inspection,** not on registration.
- **The graph sees the flow at class level only.** `JmsApplicationEvents` publishes to all four live
  queues, so the graph's path for a REST report shortcuts through the cargo-handled queue. The real
  route is registration queue → registration consumer → store → cargo-handled queue → inspection. A
  method-level enricher rule would make this exact; the code above is the authority.

## Quirk candidates opened for rulings

- The 1-second time-to-live can silently drop handling-event registrations.
- `RejectedRegistrationAttemptsQueue` is defined and consumed, but never fed.
- The upload-folder scan runs every 2 minutes, while its comment says every fifteen.
