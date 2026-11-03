# CRAP risk map

- Source: `eclipse-ee4j/cargotracker@f3beacf78de4f6d34edc4971ac87e38a5c6fe59d`
- Scope: 30 handling-registration Java source files, including the REST DTO/endpoint, event producer and consumers, services, domain types, repositories, and persistence dependencies.
- Profile exclusions: none of the scoped files matched `*.min.js`, `*/webapp/resources/*`, or `*/soapui/*`.
- Lizard emitted no method for `HandlingReportService.java`; its `submitReport` method is absent from the method count. The REST ledger entry uses the measured DTO-validation complexity and calls out the missing endpoint measurement.

- Methods: 123 · coverage input: none (CRAP = complexity ranking)
- Above 30: **3** (2.4%)

## Top 5

| CRAP | CCN | Cov | Method | File:lines |
|---:|---:|---:|---|---|
| 182 | 13 | 0% | `Itinerary::isExpected( HandlingEvent event)` | src/main/java/org/eclipse/cargotracker/domain/model/cargo/Itinerary.java:56-105 |
| 156 | 12 | 0% | `Delivery::calculateNextExpectedActivity( RouteSpecification routeSpecification ,` | src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java:264-309 |
| 56 | 7 | 0% | `Delivery::calculateTransportStatus()` | src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java:213-230 |
| 20 | 4 | 0% | `DefaultCargoInspectionService::inspectCargo( TrackingId trackingId)` | src/main/java/org/eclipse/cargotracker/application/internal/DefaultCargoInspectionService.java:38-61 |
| 20 | 4 | 0% | `Delivery::calculateRoutingStatus( Itinerary itinerary , RouteSpecification route` | src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java:311-321 |

## Hot files (methods above threshold)

| Methods | File |
|---:|---|
| 2 | src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java |
| 1 | src/main/java/org/eclipse/cargotracker/domain/model/cargo/Itinerary.java |
