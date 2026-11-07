# Admin live-map characterization (AM-03)

- Source: `eclipse-ee4j/cargotracker@f3beacf78de4f6d34edc4971ac87e38a5c6fe59d` (read-only).
- Ticket: `martins-vds/ai-factory-pilot-target#245` · Slice: `admin-live-map` · Tier: A.
- Runtime: `JAVA_HOME=/usr/lib/jvm/temurin-8-jdk-amd64 characterization/legacy-runtime/run-payara.sh sleep 3600`.
- Page: `http://localhost:8080/cargo-tracker/admin/tracking/map.xhtml`; REST base: `/cargo-tracker/rest`.
- Evidence journal: `.migration/evidence/runs/AM-03.md`.
- Suite: `test_admin_live_map.py` (11 cases); captured HTTP outputs are the JSON goldens in this directory.

## Legacy test inventory

The pinned source has nine test classes. The AM-02 inventory found no map/frame, `CargoMonitoringService`, or WebSocket-specific test. The shared domain tests relevant to the data carried by the endpoint are:

- `legacy-test: .source/src/test/java/org/eclipse/cargotracker/domain/model/cargo/CargoTest.java::testRoutingStatus`
- `legacy-test: .source/src/test/java/org/eclipse/cargotracker/domain/model/cargo/CargoTest.java::testIsUnloadedAtFinalDestination`
- `legacy-test: .source/src/test/java/org/eclipse/cargotracker/domain/model/cargo/CargoTest.java::testIsMisdirected`

They do not cover the endpoint JSON, marker rendering, navigation, empty/error handling, or WebSocket reload.

## Observed endpoint and handling acceptance flow

The source page is titled `Live Map`, contains the `Live` admin navigation item, and embeds `mapFrame.xhtml` at 960px high. The frame creates a 600px map at zoom 2, adds a scale control, OpenStreetMap tiles, and Leaflet 1.7.1 resources. The observed `GET /cargo-tracker/rest/cargo` response was an array of four objects with exactly `trackingId`, `routingStatus`, `misdirected`, `transportStatus`, `atDestination`, `origin`, and `lastKnownLocation`.

The acceptance event was submitted through the real handling endpoint, not directly against the database:

```json
{"completionTime":"2026-11-07 01:02","trackingId":"DEF789","eventType":"RECEIVE","unLocode":"CNHKG","voyageNumber":null}
```

`POST /cargo-tracker/rest/handling/reports` returned 204. A subsequent real `GET /cargo-tracker/rest/cargo` showed `DEF789` changed from `NOT_RECEIVED` with location `Unknown` to `IN_PORT` at `CNHKG`; its routing status was `MISROUTED` and `misdirected` remained false. This is the acceptance golden in `cargo-after-handling.json`. The source derives transport status and last-known location from the latest handling event, while routing status is derived from itinerary and route specification.

## Marker rules, coordinates, colors, and tooltips

For `NOT_RECEIVED`, the marker uses origin; for every other transport status it uses last-known location. The source's configured latitude/longitude pairs are:

| LOCODE | Latitude | Longitude | LOCODE | Latitude | Longitude |
|---|---:|---:|---|---:|---:|
| CNHKG | 22 | 114 | AUMEL | -38 | 145 |
| SESTO | 59 | 18 | FIHEL | 60 | 25 |
| USCHI | 42 | -88 | JNTKO | 36 | 140 |
| DEHAM | 54 | 10 | CNSHA | 31 | 121 |
| NLRTM | 52 | 5 | SEGOT | 58 | 12 |
| CNHGH | 30 | 120 | USNYC | 41 | -74 |
| USDAL | 33 | -97 | | | |

Each axis adds `Math.floor((Math.random() * 3) - 3)`, so the offset is independently -3, -2, or -1 degrees. In the post-processing browser observation, the four points were `(40,-77)`, `(40,-75)`, `(20,113)`, and `(31,-100)`. Ruling #205 explicitly changes the target to the exact configured coordinates without these offsets.

Status precedence is routing `NOT_ROUTED` or `MISROUTED`, then `misdirected`, then `atDestination`, then `transportStatus`. Browser marker outputs confirmed gray for `NOT_ROUTED`, red for `MISROUTED` and `MISDIRECTED`, gold for `NOT_RECEIVED`, green for `IN_PORT` and `ONBOARD_CARRIER`, black for `AT_DESTINATION` and `CLAIMED`, and red for `UNKNOWN`. The complete observed precedence cases are in `edge-cases.json`.

Tooltips contain tracking ID, routing label, misdirected Yes/No, transport label, at-destination Yes/No, origin, and last-known location; destination is absent. The source `IN_PORT` label begins with a space, resulting in two literal spaces after `Transport Status:` in tooltip HTML; no claim is made about visible whitespace collapsing. Clicking a marker opened `http://localhost:8080/cargo-tracker/admin/show.xhtml?trackingId=DEF789` in target `winMap` with the current frame dimensions.

## Unknown sentinel, empty, and failure behavior

The real initial `DEF789` row has `transportStatus=NOT_RECEIVED`, `origin=CNHKG`, and `lastKnownLocation=Unknown`. A controlled fetch replay in the live browser frame using that exact REST row produced one gray marker at its origin, with no console error; its tooltip showed `Last known location: undefined` because `Unknown` is absent from the source location-name dictionary. This resolves the open browser-consequence question from AM-02. A draft quirk ticket records the unexpected tooltip/location behavior.

Two controlled browser inputs were used only to exercise otherwise unavailable client branches; these do not represent database rows:

- An empty JSON array initialized the map and scale with no markers and no empty-state message. A simulated HTTP 500 carrying the same valid JSON array was treated identically because the client does not inspect `response.ok`.
- A rejected fetch logged `cannot fetch cargos`; it left the map uninitialized and displayed no user-facing message.
- A controlled `IN_PORT` row with last-known location `Unknown` calculated NaN coordinates, created no marker, and logged `cannot fetch cargos` with `Invalid LatLng object: (NaN, NaN)`. The real seeded sentinel cargo does not take this branch because its `NOT_RECEIVED` status selects its origin instead.

The `Unknown`/unmapped target behavior is governed by ruling #206: list those cargos separately with their tracking links and do not invent a point. Ruling #207 normalizes the source ` In port` label to `In port` in the target.

## Notification and observed-versus-predicted

The frame's WebSocket connected and showed `online`. After the real handling event, the browser made a second `GET mapFrame.xhtml` and fetched cargo again, consistent with the source message handler's full-frame reload. The socket message's transient source label is the misspelling `mesage`; the connection indicator click also forces a reload. Ruling #90 / ADR-0005 intentionally replaces this source WebSocket/full-reload mechanism with htmx polling in the target.

| Case | Source-derived prediction | Browser/HTTP observation | Result |
|---|---|---|---|
| Cargo endpoint | Seven named fields; `XXXXX` location is `Unknown` | Four rows and seven fields; `DEF789` location was `Unknown` | Match |
| Handling processing | Latest `RECEIVE` yields `IN_PORT` and event location | `DEF789` became `IN_PORT` at `CNHKG`, routing `MISROUTED` | Match |
| Location and coordinate rule | `NOT_RECEIVED` uses origin; otherwise last-known plus -3..-1 offsets | Four observed markers used those locations and offset ranges | Match |
| Status and colors | Routing, misdirected, arrival, transport precedence and icon table | Controlled browser cases produced the expected icon colors | Match |
| Tooltip | Seven values; unknown name lookup is undefined; `IN_PORT` literal leading space | Rendered tooltip HTML matched those strings | Match |
| Navigation | Tracking link opens admin details in `winMap` | Captured matching URL, window name, and dimensions | Match |
| Empty/HTTP error | Empty array renders base map; `response.ok` ignored | Empty and HTTP-500 empty JSON produced zero markers and scale | Match |
| Fetch error | Promise rejection is caught and logged without UI state | `cannot fetch cargos`; no user-facing message | Match |
| Unknown sentinel | `NOT_RECEIVED` selects origin; tooltip dictionary has no `Unknown` key | Origin marker visible; tooltip ended in `undefined` | Match |
| Page and provider | Admin page embeds frame with map and external Leaflet/OSM resources | Page, frame, controls, Leaflet, and tiles loaded | Match |
| Notification | WebSocket opens online and message reloads frame | Connected online; handling event caused frame and cargo reload | Match |

Predicted/observed: 11 matches, 0 differences. Findings that look surprising are recorded as source behavior and in the quirk draft; target divergences are the already-approved rulings above.
