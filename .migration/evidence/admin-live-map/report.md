# Admin live map — source inventory (AM-02)

- Source: `eclipse-ee4j/cargotracker@f3beacf78de4f6d34edc4971ac87e38a5c6fe59d` (read-only).
- Ticket: `martins-vds/ai-factory-pilot-target#203`, continued under [#228](https://github.com/martins-vds/ai-factory-pilot-target/issues/228) · Slice: `admin-live-map` · Initial proposal: [#204](https://github.com/martins-vds/ai-factory-pilot-target/pull/204) · Continuation PR: [#229](https://github.com/martins-vds/ai-factory-pilot-target/pull/229).
- Graphs: `.migration/graphs/source/full/knowledge-graph.json` and `domain-graph.json`, merged from source SHA above; the normal graph update is recorded in [#212](https://github.com/martins-vds/ai-factory-pilot-target/issues/212). No graph was rebuilt in this session.
- Target decisions: [#205](https://github.com/martins-vds/ai-factory-pilot-target/issues/205) approves exact configured city coordinates with no random offsets; [#206](https://github.com/martins-vds/ai-factory-pilot-target/issues/206) approves a separate Unknown/unmapped list with each cargo's tracking link; [#207](https://github.com/martins-vds/ai-factory-pilot-target/issues/207) approves the normalized `In port` label. These are explicit admin-map decisions; #205 is not inferred from Track Cargo ruling [#14](https://github.com/martins-vds/ai-factory-pilot-target/issues/14).
- Harness `1f9aade`: ADR-0031 counts human sign-off only when a configured approver submits an approving review on the current PR head. Failure-drill definitions are installed; this inventory did not dispatch drills and does not claim human sign-off.

## Graph findings and gaps

The source knowledge graph has 1,003 nodes and 2,088 edges; the domain graph has 6 nodes and 5 edges, including one `Admin Live Cargo Map` flow with four steps. Combined, the graphs have 1,009 nodes and 2,093 edges. The new flow anchors the page/frame, cargo-list fetch, marker rendering, and tracking-event reload.

The directed source path is `admin/tracking/map.xhtml` →contains `mapFrame.xhtml` →routes `GET /cargo` →routes `CargoMonitoringService.getAllCargo` →calls `CargoRepository.findAll` →implemented by `JpaCargoRepository.findAll` →reads `Cargo`.

The graph update resolves the former missing page-to-frame/data edge and missing admin-map flow. One graph discrepancy remains: the knowledge-graph summary says `mapFrame.xhtml` renders voyage paths, but the pinned source renders cargo markers and OpenStreetMap tiles only; it has no voyage-path rendering.

The admin page embeds the frame at `src/main/webapp/admin/tracking/map.xhtml:3-9`. The frame calls `/cargo-tracker/rest/cargo` from `mapFrame.xhtml:164-169`. The source data chain is:

`admin/tracking/map.xhtml` → iframe `admin/tracking/mapFrame.xhtml` → `GET /cargo-tracker/rest/cargo` → `RestConfiguration @ApplicationPath("rest")` and `CargoMonitoringService @Path("/cargo")` → `getAllCargo()` → `CargoRepository.findAll()` → `JpaCargoRepository.findAll()` → `Cargo.findAll` → JPA `Cargo` entity rows.

`CargoMonitoringService.cargoToJson()` emits `trackingId`, `routingStatus`, `misdirected`, `transportStatus`, `atDestination`, `origin`, and `lastKnownLocation`. `Cargo` embeds `Delivery`; its origin and `Delivery.lastKnownLocation` reference `Location` entities. Delivery status derivation and handling-registration processing are shared dependencies, not new admin-map work: see existing accepted ledger entries `track-cargo.data-cargo`, `track-cargo.data-location`, `track-cargo.domain-route-state`, and `handling.registration-flow`. None of those entries was changed or duplicated.

The map flow's reload step reflects the source WebSocket behavior: handling registration emits the cargo-handled message; its consumer invokes inspection; inspection fires `CargoInspected`; `RealtimeCargoTrackingService` broadcasts to open `/tracking` sessions. The map client ignores the JSON fields and reloads the full frame on a message. The accepted handling-registration slice #113 supplies this dependency; its processing behavior is not inventoried again here. The current domain graph represents this page/frame flow rather than a separate inspection flow.

## Observable source behavior

### Page, frame, and external map resources

- The JSF admin page uses the common admin template, title `Live Map`, and embeds `mapFrame.xhtml` through `request.contextPath`; the iframe is full-width and 960px tall.
- The frame uses local `dd.css`, Bootstrap 2.3.2 CSS, Leaflet 1.7.1 CSS/JS (integrity attributes), remote Leaflet marker images and shadow assets, and OpenStreetMap tiles with attribution. Leaflet creates the map at zoom 2 and adds a scale control.
- The REST fetch path is hard-coded as `/cargo-tracker/rest/cargo`; the WebSocket path instead derives the first path segment from `window.location.pathname`.

### Marker locations and coordinate behavior

For `NOT_RECEIVED`, the source marker uses cargo origin; otherwise it uses last-known location. The frame defines these LOCODE-to-(latitude, longitude) values:

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

The source adds an independent `Math.floor((Math.random() * 3) - 3)` offset to each axis, yielding only -3, -2, or -1 degrees and changing on each load; it is not centered around zero. The source has a `TODO` to find a latitude/longitude service. The approved target divergence in [#205](https://github.com/martins-vds/ai-factory-pilot-target/issues/205) is to use the exact configured city coordinates with no offsets. This admin-map ruling is explicit and is not inferred from Track Cargo ruling #14.

The REST endpoint maps the `XXXXX` location sentinel to the string `Unknown`, but the frame's names and coordinate dictionaries have no `Unknown` entry. The lookup is therefore undefined before the offset is added; no live browser result was produced here. The approved target behavior in [#206](https://github.com/martins-vds/ai-factory-pilot-target/issues/206) is to keep valid markers visible and list unknown or unmapped cargo separately as Unknown with its real tracking link, without inventing a point.

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

Routing labels are `Not routed`, `Routed`, and `Misrouted`. Source transport labels are `Not received`, ` In port` (including a leading space), `Onboard carrier`, `Claimed`, and `Unknown`. The approved target divergence in [#207](https://github.com/martins-vds/ai-factory-pilot-target/issues/207) normalizes the label to `In port`. Delivery's routing, misdirection, arrival, and transport values are derived in the shared model and carried by the all-cargo response.

### Tooltips and navigation

Each marker binds a tooltip with tracking ID, routing status, misdirected Yes/No, transport status, at-destination Yes/No, origin name, and last-known-location name. The REST JSON contains seven fields and does not include destination. City names are resolved through the fixed location-name dictionary; an absent key renders as an undefined lookup.

The composed source tooltip HTML contains two literal spaces after `Transport Status:` for `IN_PORT`: the label is `" In port"` and the prefix already ends with a space. This is source-string behavior only; HTML/browser whitespace may collapse, and no live-browser observation established a visibly doubled gap. Ruling [#207](https://github.com/martins-vds/ai-factory-pilot-target/issues/207) approves the normalized target label `In port`; source characterization still records the literal source string.

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
- Closed human rulings linked from affected ledger entries: [#205](https://github.com/martins-vds/ai-factory-pilot-target/issues/205) (exact coordinates), [#206](https://github.com/martins-vds/ai-factory-pilot-target/issues/206) (separate Unknown/unmapped list with tracking links), and [#207](https://github.com/martins-vds/ai-factory-pilot-target/issues/207) (normalize to `In port`).
- Return and graph-gap handoff: `.migration/returns/AM-02.afs-analyst.yaml` and `.migration/handoffs/AM-02.md`.
- Risk reports and raw tool CSVs: `.migration/risk-map/admin-live-map/`.
- No source, target application code, existing ledger, accepted return, graph, or historical evidence was modified.
