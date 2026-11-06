# Admin live map — source inventory (AM-02)

- Source: `eclipse-ee4j/cargotracker@f3beacf78de4f6d34edc4971ac87e38a5c6fe59d` (read-only).
- Ticket: `martins-vds/ai-factory-pilot-target#203` · Slice: `admin-live-map` · Owning proposal: [#204](https://github.com/martins-vds/ai-factory-pilot-target/pull/204).
- Graphs: `.migration/graphs/source/full/knowledge-graph.json` and `domain-graph.json`, merged from source SHA above; no graph was rebuilt.
- Target decision citations: [#90](https://github.com/martins-vds/ai-factory-pilot-target/issues/90) and ADR-0005 ([#100](https://github.com/martins-vds/ai-factory-pilot-target/issues/100)); exact-coordinate ruling [#14](https://github.com/martins-vds/ai-factory-pilot-target/issues/14) remains scoped to Track Cargo unless a human extends it.

## Graph findings and gaps

The full source knowledge graph reports 1,080 nodes and 2,137 edges; the domain graph has 9 flows. It identifies the two admin map pages, the REST `GET /cargo` and WebSocket `/tracking` endpoints, `CargoMonitoringService`, `JpaCargoRepository.findAll`, and the `Cargo` table. The domain graph includes `inspect-handled-cargo`, but no `admin-live-map` flow.

Graph discrepancies and uncovered scope:

1. `graph-check.md` says `src/main/webapp/admin/tracking/map.xhtml` has no path to data. The graph links `mapFrame.xhtml` to `GET /cargo`, then `getAllCargo` to `CargoRepository.findAll` and `JpaCargoRepository.findAll` to `Cargo`; the parent page's iframe edge is missing from the page graph. The pinned XHTML confirms the iframe at `map.xhtml:3-9`.
2. The knowledge-graph summary for `mapFrame.xhtml` says it renders cargo locations and voyage paths. The pinned page renders cargo markers and OSM tiles; it has no voyage-path rendering.
3. There is no domain-graph flow for the admin map's page/frame, all-cargo marker rendering, status/color precedence, tooltip, or click-through. The source settles these behaviors, so inventory continued. The normal graph workflow should add the missing flow; this session did not rebuild the graph.

The admin page embeds the frame at `src/main/webapp/admin/tracking/map.xhtml:3-9`. The frame calls `/cargo-tracker/rest/cargo` from `mapFrame.xhtml:164-169`. The source data chain is:

`admin/tracking/map.xhtml` → iframe `admin/tracking/mapFrame.xhtml` → `GET /cargo-tracker/rest/cargo` → `RestConfiguration @ApplicationPath("rest")` and `CargoMonitoringService @Path("/cargo")` → `getAllCargo()` → `CargoRepository.findAll()` → `JpaCargoRepository.findAll()` → `Cargo.findAll` → JPA `Cargo` entity rows.

`CargoMonitoringService.cargoToJson()` emits `trackingId`, `routingStatus`, `misdirected`, `transportStatus`, `atDestination`, `origin`, and `lastKnownLocation`. `Cargo` embeds `Delivery`; its origin and `Delivery.lastKnownLocation` reference `Location` entities. Delivery status derivation and handling-registration processing are shared dependencies, not new admin-map work: see existing accepted ledger entries `track-cargo.data-cargo`, `track-cargo.data-location`, `track-cargo.domain-route-state`, and `handling.registration-flow`. None of those entries was changed or duplicated.

The update chain is separately represented by the domain flow `inspect-handled-cargo`: handling registration emits the cargo-handled message; its consumer invokes inspection; inspection fires `CargoInspected`; `RealtimeCargoTrackingService` broadcasts to open `/tracking` sessions. The map client ignores the JSON fields and reloads the full frame on a message. The accepted handling-registration slice #113 supplies this dependency; its processing behavior is not inventoried again here.

## Observable source behavior

### Page, frame, and external map resources

- The JSF admin page uses the common admin template, title `Live Map`, and embeds `mapFrame.xhtml` through `request.contextPath`; the iframe is full-width and 960px tall.
- The frame uses local `dd.css`, Bootstrap 2.3.2 CSS, Leaflet 1.7.1 CSS/JS (integrity attributes), remote Leaflet marker images and shadow assets, and OpenStreetMap tiles with attribution. Leaflet creates the map at zoom 2 and adds a scale control.
- The REST fetch path is hard-coded as `/cargo-tracker/rest/cargo`; the WebSocket path instead derives the first path segment from `window.location.pathname`.

### Marker locations and coordinate behavior

For `NOT_RECEIVED`, the marker uses cargo origin; otherwise it uses last-known location. The frame defines these LOCODE-to-(latitude, longitude) values:

| LOCODE | Name | Latitude | Longitude |
|---|---|---:|---:|
| CNHKG | Hong Kong | 22 | 114 |
| AUMEL | Melbourne | -38 | 145 |
| SESTO | Stockholm | 59 | 18 |
| FIHEL | Helsinki | 60 | 25 |
| USCHI | Chicago | 42 | -88 |
| JNTKO | Tokyo | 36 | 140 |
| DEHAM | Hamburg | 54 | 10 |
| CNSHA | Shanghai | 31 | 121 |
| NLRTM | Rotterdam | 52 | 5 |
| SEGOT | Gothenburg | 58 | 12 |
| CNHGH | Hangzhou | 30 | 120 |
| USNYC | New York | 41 | -74 |
| USDAL | Dallas | 33 | -97 |

Each axis adds an independent `Math.floor((Math.random() * 3) - 3)`, which yields only -3, -2, or -1 degrees. It is not centered around zero and changes on each load. The source has a `TODO` to find a latitude/longitude service. This is the source behavior; whether Track Cargo ruling #14 applies to this separate map remains unresolved under #99. Draft: `.migration/quirks/admin-live-map-random-offset.md`.

The REST endpoint maps the `XXXXX` location sentinel to the string `Unknown`, but the frame's names and coordinate dictionaries have no `Unknown` entry. The lookup is therefore undefined before the offset is added; no live browser result was produced here. Draft: `.migration/quirks/admin-live-map-unknown-location.md`.

### Status precedence and marker colors

The frame chooses a status code in this order:

1. Initialize to `NOT_RECEIVED`.
2. If routing status is `NOT_ROUTED` or `MISROUTED`, use that routing status (it takes precedence over all following states).
3. Otherwise, if `misdirected` is true, use `MISDIRECTED`.
4. Otherwise, if `atDestination` is true, use `AT_DESTINATION`.
5. Otherwise use `transportStatus`.

| Status code | Marker |
|---|---|
| `NOT_ROUTED` | grey |
| `MISROUTED` | red |
| `MISDIRECTED` | red |
| `NOT_RECEIVED` | gold |
| `IN_PORT` | green |
| `ONBOARD_CARRIER` | green |
| `AT_DESTINATION` | black |
| `CLAIMED` | black |
| `UNKNOWN` | red |

Routing labels are `Not routed`, `Routed`, and `Misrouted`. Transport labels are `Not received`, ` In port` (including a leading space), `Onboard carrier`, `Claimed`, and `Unknown`. Delivery's routing, misdirection, arrival, and transport values are derived in the shared model and carried by the all-cargo response.

### Tooltips and navigation

Each marker binds a tooltip with tracking ID, routing status, misdirected Yes/No, transport status, at-destination Yes/No, origin name, and last-known-location name. Destination is in the REST JSON but is not shown in this tooltip. City names are resolved through the fixed location-name dictionary; an absent key renders as an undefined lookup.

Clicking a marker opens `/admin/show.xhtml?trackingId=<id>` in a new window named `winMap`, with the current frame dimensions. The URL is assembled with `http://`, the current host, and the first path segment as the application path.

### Empty, missing-data, and error behavior

- A valid empty cargo array still initializes the map, tiles, and scale control; it creates no markers and displays no explicit empty-state message.
- The fetch chain calls `response.json()` without checking `response.ok`. Fetch, JSON, or later promise-chain errors are caught and logged as `cannot fetch cargos`; no user-facing error is rendered.
- The endpoint substitutes `Unknown` for a `XXXXX` last-known code. No coordinate/name entry exists for `Unknown`; missing/unexpected status values likewise have no icon-map entry. The map's exact rendering for these cases was not run and remains for characterization.
- There is no explicit missing/partial field validation or retry loop in the frame.

### Original notification and connection-label behavior versus the approved target

On frame load, the client opens `ws://<host>/<applicationPath>/tracking`. Open sets the connection text to `online`; close sets it to `offline`; a message sets the misspelled text `mesage` and calls `location.reload(true)`. The status box is clickable and also forces a reload. The incoming message's JSON fields are not used by the client. On the server, `CargoInspected` is broadcast to open sessions; per-session `IOException` is logged as a warning.

These are source observations, not the target contract. #90 / ADR-0005 (#100) approves a server-rendered markers partial polled by htmx every `CARGO_MAP_POLL_SECONDS` (default 10), with every cargo-state change visible on the next poll. The inspection-triggered full reload is replaced; `/tracking` and its online/offline label are intentional drops and must remain explicitly accounted for. No target code was written here.

## Legacy tests and shared coverage

No map/frame, `CargoMonitoringService`, or WebSocket-specific test was found under the pinned source's `src/test/java`. Existing shared cargo-domain tests are:

- `legacy-test: .source/src/test/java/org/eclipse/cargotracker/domain/model/cargo/CargoTest.java::testRoutingStatus`
- `legacy-test: .source/src/test/java/org/eclipse/cargotracker/domain/model/cargo/CargoTest.java::testIsUnloadedAtFinalDestination`
- `legacy-test: .source/src/test/java/org/eclipse/cargotracker/domain/model/cargo/CargoTest.java::testIsMisdirected`

These test domain behavior, not all-cargo REST serialization, map rendering, marker colors, navigation, empty/error handling, or WebSocket reload. No legacy tests were modified or run in this analyst task.

## Risk evidence

Best-effort source risk artifacts are under `.migration/risk-map/admin-live-map/`. `afs-run` journal: `.migration/evidence/runs/AM-02.md`.

- Java Lizard CSV: 37 detected methods; CRAP complexity ranking reports 2 above 30. The two highest are shared `Delivery.calculateNextExpectedActivity` (CRAP 156, CCN 12) and `Delivery.calculateTransportStatus` (CRAP 56, CCN 7).
- Embedded JavaScript Lizard CSV: 3 detected methods; one above 30, `init()` (CRAP 110, CCN 10).
- Combined measured methods: 40; above 30: 3. This count is the sum of those two reports, not a count of the complete source slice.
- No LCOV or JaCoCo coverage was supplied. The CRAP tool therefore uses zero coverage as a complexity ranking; it is not measured source test coverage.
- Lizard emitted no method rows for `CargoMonitoringService.java` or `RealtimeCargoTrackingService.java`, including in a separate run on those files. Their method complexity is therefore not represented in these counts.
- This is a risk map, not a passing CRAP gate. Source tests and coverage were not run; existing shared `Delivery` risk is referenced, not re-owned.

## Durable outputs

- New pending ledger entries: `.migration/ledger/admin-live-map.*.yaml` (11 entries).
- Human decision drafts: `.migration/quirks/admin-live-map-random-offset.md`, `.migration/quirks/admin-live-map-unknown-location.md`, and `.migration/quirks/admin-live-map-in-port-label.md`.
- Return and graph-gap handoff: `.migration/returns/AM-02.afs-analyst.yaml` and `.migration/handoffs/AM-02.md`.
- Risk reports and raw tool CSVs: `.migration/risk-map/admin-live-map/`.
- No source, target application code, existing ledger, accepted return, graph, or historical evidence was modified.
