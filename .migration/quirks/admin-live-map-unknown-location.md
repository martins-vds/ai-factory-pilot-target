# Admin all-cargo map has no coordinate mapping for Unknown

## Question
When a cargo has the source's `Unknown` last-known-location sentinel, should the admin map preserve the resulting unmapped coordinate and location-label lookups or render that cargo another way?

## Evidence
- Source: `.source/src/main/java/org/eclipse/cargotracker/interfaces/booking/rest/CargoMonitoringService.java:48-51` and `.source/src/main/webapp/admin/tracking/mapFrame.xhtml:20-34,52-82,172-195,215-223` at `eclipse-ee4j/cargotracker@f3beacf78de4f6d34edc4971ac87e38a5c6fe59d`.
- Observation: the REST response converts the `XXXXX` location code to `"Unknown"`; the map's location-name, latitude, and longitude dictionaries have no `"Unknown"` key. The source formula therefore adds offsets to undefined coordinate lookups. The exact browser rendering consequence was not observed in this analyst task.
- Why it looks wrong: the endpoint explicitly supplies an unknown-location sentinel, but the map has no corresponding display/coordinate entry.

## Impact
- Ledger capabilities: `admin-live-map.marker-coordinates`, `admin-live-map.missing-data`.
- Blocks: implementation of unknown-location marker behavior until a human decides.

## Options
1. Preserve exactly (including the unmapped lookups) and characterize the observed browser result.
2. Fix (choose an explicit target behavior for unknown locations and record the divergence).
3. Other (specify a different marker and tooltip treatment).
