# CRAP risk map

- Methods: 37 · coverage input: none (CRAP = complexity ranking)
- Above 30: **2** (5.4%)

## Top 20

| CRAP | CCN | Cov | Method | File:lines |
|---:|---:|---:|---|---|
| 156 | 12 | 0% | `Delivery::calculateNextExpectedActivity( RouteSpecification routeSpecification ,` | home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java:264-309 |
| 56 | 7 | 0% | `Delivery::calculateTransportStatus()` | home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java:213-230 |
| 20 | 4 | 0% | `Delivery::calculateRoutingStatus( Itinerary itinerary , RouteSpecification route` | home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java:311-321 |
| 20 | 4 | 0% | `Delivery::equals( Object o)` | home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java:343-354 |
| 12 | 3 | 0% | `Delivery::calculateCurrentVoyage()` | home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java:240-246 |
| 12 | 3 | 0% | `Delivery::calculateUnloadedAtDestination( RouteSpecification routeSpecification)` | home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java:323-326 |
| 6 | 2 | 0% | `JpaCargoRepository::find( TrackingId trackingId)` | home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.source/src/main/java/org/eclipse/cargotracker/infrastructure/persistence/jpa/JpaCargoRepository.java:32-44 |
| 6 | 2 | 0% | `JpaCargoRepository::store( Cargo cargo)` | home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.source/src/main/java/org/eclipse/cargotracker/infrastructure/persistence/jpa/JpaCargoRepository.java:47-54 |
| 6 | 2 | 0% | `Delivery::getEstimatedTimeOfArrival()` | home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java:171-177 |
| 6 | 2 | 0% | `Delivery::calculateLastKnownLocation()` | home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java:232-238 |
| 6 | 2 | 0% | `Delivery::calculateMisdirectionStatus( Itinerary itinerary)` | home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java:248-254 |
| 6 | 2 | 0% | `Delivery::calculateEta( Itinerary itinerary)` | home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java:256-262 |
| 6 | 2 | 0% | `Delivery::onTrack()` | home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java:328-330 |
| 6 | 2 | 0% | `Delivery::sameValueAs( Delivery other)` | home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java:332-340 |
| 2 | 1 | 0% | `RestConfiguration::RestConfiguration()` | home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.source/src/main/java/org/eclipse/cargotracker/application/util/RestConfiguration.java:18-28 |
| 2 | 1 | 0% | `JpaCargoRepository::nextTrackingId()` | home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.source/src/main/java/org/eclipse/cargotracker/infrastructure/persistence/jpa/JpaCargoRepository.java:57-61 |
| 2 | 1 | 0% | `JpaCargoRepository::findAll()` | home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.source/src/main/java/org/eclipse/cargotracker/infrastructure/persistence/jpa/JpaCargoRepository.java:64-66 |
| 2 | 1 | 0% | `Delivery::JoinColumn( name = 'last_known_location_id')` | home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java:53-81 |
| 2 | 1 | 0% | `Delivery::Delivery( HandlingEvent lastEvent , Itinerary itinerary , RouteSpecifi` | home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java:83-95 |
| 2 | 1 | 0% | `Delivery::updateOnRouting( RouteSpecification routeSpecification , Itinerary iti` | home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java:102-106 |

## Hot files (methods above threshold)

| Methods | File |
|---:|---|
| 2 | home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java |
