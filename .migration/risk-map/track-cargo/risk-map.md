# CRAP risk map

- Methods: 137 · coverage input: none (CRAP = complexity ranking)
- Above 30: **5** (3.6%)

## Top 30

| CRAP | CCN | Cov | Method | File:lines |
|---:|---:|---:|---|---|
| 182 | 13 | 0% | `Itinerary::isExpected( HandlingEvent event)` | source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Itinerary.java:56-105 |
| 156 | 12 | 0% | `Delivery::calculateNextExpectedActivity( RouteSpecification routeSpecification ,` | source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java:264-309 |
| 56 | 7 | 0% | `Delivery::calculateTransportStatus()` | source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java:213-230 |
| 42 | 6 | 0% | `CargoTrackingViewAdapter::getStatusText()` | source/src/main/java/org/eclipse/cargotracker/interfaces/tracking/web/CargoTrackingViewAdapter.java:81-98 |
| 42 | 6 | 0% | `CargoTrackingViewAdapter::HandlingEventViewAdapter::getDescription()` | source/src/main/java/org/eclipse/cargotracker/interfaces/tracking/web/CargoTrackingViewAdapter.java:164-181 |
| 30 | 5 | 0% | `CargoTrackingViewAdapter::getNextExpectedActivity()` | source/src/main/java/org/eclipse/cargotracker/interfaces/tracking/web/CargoTrackingViewAdapter.java:114-133 |
| 20 | 4 | 0% | `CargoTrackingViewAdapter::getStatusCode()` | source/src/main/java/org/eclipse/cargotracker/interfaces/tracking/web/CargoTrackingViewAdapter.java:62-76 |
| 20 | 4 | 0% | `Delivery::calculateRoutingStatus( Itinerary itinerary , RouteSpecification route` | source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java:311-321 |
| 20 | 4 | 0% | `Delivery::equals( Object o)` | source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java:343-354 |
| 20 | 4 | 0% | `HandlingActivity::equals( Object obj)` | source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/HandlingActivity.java:82-96 |
| 20 | 4 | 0% | `Itinerary::equals( Object o)` | source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Itinerary.java:152-163 |
| 20 | 4 | 0% | `Leg::equals( Object o)` | source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Leg.java:91-102 |
| 20 | 4 | 0% | `RouteSpecification::isSatisfiedBy( Itinerary itinerary)` | source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/RouteSpecification.java:71-75 |
| 20 | 4 | 0% | `RouteSpecification::equals( Object o)` | source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/RouteSpecification.java:84-95 |
| 20 | 4 | 0% | `TrackingId::equals( Object o)` | source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/TrackingId.java:35-46 |
| 20 | 4 | 0% | `HandlingHistory::equals( Object o)` | source/src/main/java/org/eclipse/cargotracker/domain/model/handling/HandlingHistory.java:58-68 |
| 20 | 4 | 0% | `UnLocode::equals( Object o)` | source/src/main/java/org/eclipse/cargotracker/domain/model/location/UnLocode.java:54-65 |
| 20 | 4 | 0% | `VoyageNumber::equals( Object o)` | source/src/main/java/org/eclipse/cargotracker/domain/model/voyage/VoyageNumber.java:31-45 |
| 12 | 3 | 0% | `Delivery::calculateCurrentVoyage()` | source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java:240-246 |
| 12 | 3 | 0% | `Delivery::calculateUnloadedAtDestination( RouteSpecification routeSpecification)` | source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java:323-326 |
| 12 | 3 | 0% | `HandlingActivity::isEmpty()` | source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/HandlingActivity.java:98-108 |
| 6 | 2 | 0% | `Track::setTrackingId( String trackingId)` | source/src/main/java/org/eclipse/cargotracker/interfaces/tracking/web/Track.java:49-55 |
| 6 | 2 | 0% | `Track::onTrackById()` | source/src/main/java/org/eclipse/cargotracker/interfaces/tracking/web/Track.java:65-79 |
| 6 | 2 | 0% | `CargoTrackingViewAdapter::CargoTrackingViewAdapter( Cargo cargo , List<HandlingE` | source/src/main/java/org/eclipse/cargotracker/interfaces/tracking/web/CargoTrackingViewAdapter.java:24-31 |
| 6 | 2 | 0% | `CargoTrackingViewAdapter::getLastKnownLocationName()` | source/src/main/java/org/eclipse/cargotracker/interfaces/tracking/web/CargoTrackingViewAdapter.java:53-56 |
| 6 | 2 | 0% | `CargoTrackingViewAdapter::getEta()` | source/src/main/java/org/eclipse/cargotracker/interfaces/tracking/web/CargoTrackingViewAdapter.java:104-112 |
| 6 | 2 | 0% | `Delivery::getEstimatedTimeOfArrival()` | source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java:171-177 |
| 6 | 2 | 0% | `Delivery::calculateLastKnownLocation()` | source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java:232-238 |
| 6 | 2 | 0% | `Delivery::calculateMisdirectionStatus( Itinerary itinerary)` | source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java:248-254 |
| 6 | 2 | 0% | `Delivery::calculateEta( Itinerary itinerary)` | source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java:256-262 |

## Hot files (methods above threshold)

| Methods | File |
|---:|---|
| 2 | source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java |
| 2 | source/src/main/java/org/eclipse/cargotracker/interfaces/tracking/web/CargoTrackingViewAdapter.java |
| 1 | source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Itinerary.java |
