# CRAP risk map

- Methods: 411 · coverage input: none (CRAP = complexity ranking)
- Above 30: **8** (1.9%)

## Top 10

| CRAP | CCN | Cov | Method | File:lines |
|---:|---:|---:|---|---|
| 182 | 13 | 0% | `Itinerary::isExpected( HandlingEvent event)` | source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Itinerary.java:56-105 |
| 156 | 12 | 0% | `Delivery::calculateNextExpectedActivity( RouteSpecification routeSpecification ,` | source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java:264-309 |
| 56 | 7 | 0% | `Delivery::calculateTransportStatus()` | source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java:213-230 |
| 42 | 6 | 0% | `CargoStatusDtoAssembler::getCargoStatusText( Cargo cargo)` | source/src/main/java/org/eclipse/cargotracker/interfaces/booking/facade/internal/assembler/CargoStatusDtoAssembler.java:33-50 |
| 42 | 6 | 0% | `TrackingEventsDtoAssembler::descriptionFrom( HandlingEvent . Type type , String ` | source/src/main/java/org/eclipse/cargotracker/interfaces/booking/facade/internal/assembler/TrackingEventsDtoAssembler.java:26-41 |
| 42 | 6 | 0% | `EventLogger::init()` | source/src/main/java/org/eclipse/cargotracker/interfaces/handling/mobile/EventLogger.java:115-144 |
| 42 | 6 | 0% | `CargoTrackingViewAdapter::getStatusText()` | source/src/main/java/org/eclipse/cargotracker/interfaces/tracking/web/CargoTrackingViewAdapter.java:81-98 |
| 42 | 6 | 0% | `CargoTrackingViewAdapter::HandlingEventViewAdapter::getDescription()` | source/src/main/java/org/eclipse/cargotracker/interfaces/tracking/web/CargoTrackingViewAdapter.java:164-181 |
| 30 | 5 | 0% | `CargoStatusDtoAssembler::getNextExpectedActivity( Cargo cargo)` | source/src/main/java/org/eclipse/cargotracker/interfaces/booking/facade/internal/assembler/CargoStatusDtoAssembler.java:62-81 |
| 30 | 5 | 0% | `EventLogger::validate( final String step)` | source/src/main/java/org/eclipse/cargotracker/interfaces/handling/mobile/EventLogger.java:158-169 |

## Hot files (methods above threshold)

| Methods | File |
|---:|---|
| 2 | source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java |
| 2 | source/src/main/java/org/eclipse/cargotracker/interfaces/tracking/web/CargoTrackingViewAdapter.java |
| 1 | source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Itinerary.java |
| 1 | source/src/main/java/org/eclipse/cargotracker/interfaces/booking/facade/internal/assembler/CargoStatusDtoAssembler.java |
| 1 | source/src/main/java/org/eclipse/cargotracker/interfaces/booking/facade/internal/assembler/TrackingEventsDtoAssembler.java |
| 1 | source/src/main/java/org/eclipse/cargotracker/interfaces/handling/mobile/EventLogger.java |
