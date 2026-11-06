# Booking and routing source inventory — BK-02

- Issue: [martins-vds/ai-factory-pilot-target#225](https://github.com/martins-vds/ai-factory-pilot-target/issues/225)
- Source: `eclipse-ee4j/cargotracker@f3beacf78de4f6d34edc4971ac87e38a5c6fe59d`
- Profile: `.migration/profile.yaml`
- Decisions applied as constraints: #89 (in-process target routing; preserve random routes), #92 (no authentication), ADR-0003 (mirrored schema).
- Setup: OK at the pinned source SHA. The source remained read-only; target ancestry, migration validation, runtime, ticket inputs and setup probe were verified. Analyst does not run test-service health checks.
- Source file reading: through the file `view` gate, at the smallest relevant ranges after graph inspection. Source was not modified.

## Graph first

The prebuilt full source graph was used as-is; it was not rebuilt.

| Graph | Path | Inventory |
|---|---|---|
| Knowledge | `.migration/graphs/source/full/knowledge-graph.json` | 1009 nodes, 2093 edges; graph gate passes. It lists the scoped pages and their JSF bean routes. |
| Domain | `.migration/graphs/source/full/domain-graph.json` | 6 nodes, 5 edges, 1 flow: `Admin Live Cargo Map` (`src/main/webapp/admin/tracking/map.xhtml`). No booking or routing flow is present. |

Graph queries were made against the checked-in JSON. The `understand-anything` skill/commands were not available through this session's skill loader, so `/understand-chat` and `/understand-explain` could not be invoked. No graph was regenerated. The available graph evidence was enough to trace pages and bean routes; source code was then read where details or graph completeness needed verification.

### Graph discrepancies

1. The domain graph has no booking/routing flow or entry point, despite the scoped wizard, dashboard, cargo-detail and route-selection pages. Booking inventory is therefore anchored to the source page/bean/service chain, not a domain-flow step.
2. The knowledge graph represents service boundaries as class/method nodes, not nodes of type `service` (the graph check reports zero service nodes). Its route chain is incomplete at the graph-traversal endpoint; source code settles the actual path through `ExternalRoutingService` and `GraphTraversalService`.
3. Dashboard page containment in the graph shows the three table includes and shared admin template. Source confirms the common template provides a Live Map navigation link; it does not embed the map into the dashboard content.

## Capability inventory

All new entries are `.migration/ledger/booking.*.yaml`, `slice: booking`, `status: pending`, `verification: pending`.

### Screens and flows

| Source screen | Observable behavior |
|---|---|
| `booking/booking.xhtml` | Step 1: select origin by location name/UN/LOCODE; Cancel returns to dashboard; Next advances. |
| `booking/booking-destination.xhtml` | Step 2: displays origin, offers a destination menu excluding origin, and supports Back, Cancel and Next. |
| `booking/booking-date.xhtml` | Step 3: inline calendar, `yyyy-MM-dd`, minimum date today; duration states are zero (“can't start and end the same day”), one day, or N days; Book Cargo disabled until `bookable`. Date selection AJAX refreshes duration and button. |
| `admin/dashboard.xhtml` | Includes `listRouted`, `listNotRouted`, then `listClaimed` inside the common admin template. No custom empty-table message or pagination is defined in these pages. |
| `admin/tables/listRouted.xhtml` | Routed-unclaimed rows show tracking ID, origin, destination, last-known location, transport status and deadline. The last-known code is hidden when it contains `XXXX`; detail link tooltip says itinerary details. |
| `admin/tables/listNotRouted.xhtml` | Unrouted rows show tracking ID/route link, origin, destination and deadline. Destination/deadline links open dynamic dialogs; `dialogReturn` refreshes this table. |
| `admin/tables/listClaimed.xhtml` | Claimed rows show tracking ID, origin, destination and deadline; link tooltip promises history. |
| `admin/show.xhtml` | Shows origin, destination and deadline. Routed cargo displays itinerary legs; misrouted cargo gets a Reroute button. Unrouted cargo gets a route link. |
| `admin/route.xhtml` | Loads cargo and candidates, displays origin/destination/deadline and candidate count; either a no-route message or numbered routes with voyage, load/unload locations and dates; selecting an option assigns its index. |
| `admin/selectItinerary.xhtml` | Reads tracking ID and loads candidates; its only content branch is an empty-candidate message recommending a later deadline. The populated candidate table is in `route.xhtml`. |
| `admin/dialogs/changeDestination.xhtml` | Displays origin/current destination, new-destination selector, Cancel and Update; update requests a page refresh after dialog completion. |
| `admin/dialogs/changeArrivalDeadlineDate.xhtml` | Displays origin/destination, date picker, Cancel and Update; update requests a page refresh after dialog completion. |

### Backing beans and call chains

- `Booking` is `@Named @FlowScoped("booking")`. `@PostConstruct` sets today and loads shipping locations. The location getter removes origin while on the destination page, or selected destination on the other wizard page. Setters resolve display names. `deadlineUpdated` computes standard days from today through the selected date plus a four-hour grace period and updates the duration panel/book button. `register` calls the facade for distinct locations; equality produces an ERROR FacesMessage (“Origin and destination cannot be the same.”), otherwise it returns the dashboard outcome.
- `ListCargo` is request-scoped. It loads all CargoRoute DTOs once and partitions them in memory into routed, routed-unclaimed, claimed and not-routed lists. The scoped table uses routed-unclaimed, not all routed. `getRoutedCargos` exists but is not bound by these pages.
- `CargoDetails` is request-scoped and loads a CargoRoute DTO by tracking ID. `ItinerarySelection` is view-scoped; `load` loads both cargo and route candidates; `assignItinerary(index)` maps/assigns the selected candidate then returns a detail-page outcome.
- `ChangeDestination` and `ChangeArrivalDeadlineDate` are view-scoped. Each loads cargo through `BookingServiceFacade`; the destination bean also loads shipping locations and removes origin/current destination from the options. Destination update calls `changeDestination`; deadline update calls `changeDeadline`; each closes the dynamic dialog with `DONE`.
- `ChangeDestinationDialog` and `ChangeArrivalDeadlineDateDialog` are session-scoped. `showDialog` opens the corresponding PrimeFaces dynamic modal with `trackingId`, modal/draggable true, non-resizable, 410×280. `handleReturn` is empty; Cancel closes with an empty result.
- Structural chain: JSF page → bean → `BookingServiceFacade`/`DefaultBookingServiceFacade` → `BookingService`/`DefaultBookingService` → Cargo, Location and Voyage repositories. `CargoRouteDtoAssembler` and `ItineraryCandidateDtoAssembler` translate to/from UI DTOs.

### Service behavior, validation and branches

- Registration uses `JpaCargoRepository.nextTrackingId()` (uppercase UUID prefix up to the first hyphen), resolves origin/destination, builds `RouteSpecification` and `Cargo`, stores it and logs the tracking ID. New cargo has an empty itinerary and `NOT_ROUTED` delivery state.
- `RouteSpecification` requires non-null origin, destination and deadline and rejects equal locations. `isSatisfiedBy` requires matching itinerary endpoints and a final arrival date strictly before the deadline. `Itinerary` rejects null/empty leg lists and null legs; its empty singleton is used before routing.
- Candidate request returns an empty list when the cargo lookup in `DefaultBookingService` is null. Otherwise the `RoutingService` adapter sends an HTTP GET to the configured pathfinder URL with origin/destination, maps returned edges to persisted Voyage/Location objects and keeps only itineraries satisfying the specification. HTTP, conversion and missing-reference errors are not translated here.
- `GraphTraversalService` accepts origin/destination/deadline but its source implementation does not use deadline. It creates 3–5 candidates with randomized intermediate sample locations, dates and voyage numbers. `ExternalRoutingService` does not send the deadline; the stricter route-specification check filters candidates after generation. Decision #89 governs the target transformation to in-process routing and preservation of random routes; it does not resolve the deadline quirk.
- Assignment stores the itinerary through `CargoRepository`; `Cargo` recalculates delivery/routing state synchronously. Destination/deadline changes preserve the original Cargo origin and current itinerary while replacing the route specification; status can become `MISROUTED`, as the service tests assert. These changes do not automatically request or assign a new route.
- Unknown tracking ID differs by call path: `JpaCargoRepository.find` catches `NoResultException`, logs at FINE and returns null. Candidate request handles null as an empty list; detail loading passes null to `CargoRouteDtoAssembler.toDto`, which dereferences it. There is no explicit not-found UI branch.
- `JpaLocationRepository.find` and `JpaVoyageRepository.find` use `getSingleResult` without a no-result translation; unknown lookup exceptions propagate.
- Deadline dialog load parses the DTO value with `MM/dd/yyyy`; `ParseException` is printed and swallowed, leaving its date unset. Normal DTO values are formatted with an additional time/time-zone suffix; `SimpleDateFormat.parse(String)` accepts the valid date prefix.
- Decision #92: no authentication or authorization check is present in the scoped page/bean paths. “Admin” is a navigation/template area, not an access-control boundary in this source.

### Persistence and overlap

- `Cargo` is the JPA entity/table with embedded TrackingId, RouteSpecification (including `spec_origin_id`, `spec_destination_id`, `spec_arrival_deadline`), Itinerary and Delivery, plus the immutable origin association. Its named queries return all cargo or find by tracking ID; no explicit list ordering is defined.
- `Leg` is an entity/table joined from the embedded itinerary by `cargo_id`; it stores voyage, load/unload location and load/unload time. Itinerary ordering is by `loadTime`. `JpaCargoRepository.store` explicitly persists each leg, then Cargo.
- `Location` and `Voyage` are repository-backed entities used for location choices and candidate DTO reconstruction. `persistence.xml` configures `CargoTrackerUnit`, the CargoTracker data source and schema generation action `create`.
- These are not new data capabilities: refer to `track-cargo.data-cargo`, `track-cargo.data-leg`, `track-cargo.data-location`, `track-cargo.data-voyage`, and the accepted `handling.cargo-table`, `handling.leg-table`, `handling.location-table`, and `handling.voyage-table`; none of those entries was changed. ADR-0003's mirrored-schema decision remains applicable.
- No `.migration/ledger/admin-live-map.*` entry exists in this checkout. The common admin shell has a Live Map link, but the inspected dashboard itself includes only the three tables; no duplicate map entry was created.

## Legacy JUnit coverage mapping

These are source test inventory references, not claims that tests were run in this analyst session. `BookingServiceTest` is an Arquillian integration test. None of the named JUnit classes is a JSF/page/dialog test suite.

| Ledger capability | Named source JUnit coverage |
|---|---|
| `booking.wizard-chain` | `BookingServiceTest.testRegisterNew`; `CargoLifecycleScenarioTest.testCargoFromHongkongToStockholm` |
| `booking.dashboard-chain` | None directly for dashboard composition or list loading |
| `booking.routing-chain` | `BookingServiceTest.testRouteCandidates`, `testAssignRoute`; `RouteSpecificationTest.testIsSatisfiedBySuccess`, `testIsNotSatisfiedByMissedDeadline`; `CargoTest.testRoutingStatus` |
| `booking.dialog-chain` | `BookingServiceTest.testChangeDestination`, `testChangeDeadline` (service outcomes only) |
| `booking.screen-origin` | No direct screen test; underlying registration: `BookingServiceTest.testRegisterNew` |
| `booking.screen-destination` | No direct screen test; underlying registration: `BookingServiceTest.testRegisterNew` |
| `booking.screen-deadline` | No direct calendar/duration/button test |
| `booking.screen-dashboard` | No direct dashboard test |
| `booking.screen-routed-table` | No direct table test; `CargoTest.testRoutingStatus` only exercises domain state |
| `booking.screen-not-routed-table` | No direct table/refresh test; `BookingServiceTest.testRegisterNew` establishes an unrouted initial state |
| `booking.screen-claimed-table` | No direct table test; `CargoLifecycleScenarioTest.testCargoFromHongkongToStockholm` exercises claim as part of the full lifecycle, not this UI |
| `booking.screen-cargo-details` | No page test; `BookingServiceTest.testAssignRoute`, `CargoTest.testRoutingStatus` exercise the underlying route state |
| `booking.screen-route` | `BookingServiceTest.testRouteCandidates`, `testAssignRoute`; all four `RouteSpecificationTest` satisfaction cases |
| `booking.screen-select-itinerary` | No direct page test; `BookingServiceTest.testRouteCandidates` exercises the service result |
| `booking.dialog-destination` | `BookingServiceTest.testChangeDestination` (service only) |
| `booking.dialog-deadline` | `BookingServiceTest.testChangeDeadline` (service only) |
| `booking.wizard-input-rules` | `RouteSpecificationTest.testIsNotSatisfiedByWrongOrigin`, `testIsNotSatisfiedByWrongDestination`, `testIsNotSatisfiedByMissedDeadline`; no test for the bean's same-origin message or four-hour duration rule |
| `booking.registration` | `BookingServiceTest.testRegisterNew`; `CargoLifecycleScenarioTest.testCargoFromHongkongToStockholm` |
| `booking.dashboard-filters` | No direct list-partition test; `CargoTest.testRoutingStatus` tests routed state, not the dashboard predicates |
| `booking.routing-candidates` | `BookingServiceTest.testRouteCandidates`; `RouteSpecificationTest` success/wrong-origin/wrong-destination/missed-deadline cases |
| `booking.routing-assign` | `BookingServiceTest.testAssignRoute`; `CargoTest.testRoutingStatus`; `CargoLifecycleScenarioTest.testCargoFromHongkongToStockholm` |
| `booking.destination-change` | `BookingServiceTest.testChangeDestination`; `CargoTest.testRoutingStatus` |
| `booking.deadline-change` | `BookingServiceTest.testChangeDeadline` |
| `booking.cargo-not-found` | No named source test |
| `booking.routing-pathfinder-api` | `BookingServiceTest.testRouteCandidates`; lifecycle scenario exercises the service path. `ExternalRoutingServiceTest.testCalculatePossibleRoutes` has no `@Test` annotation and is not executable JUnit coverage. |

`ItineraryTest.testCargoOnTrack` covers expected handling against itinerary legs, and `testCreateItinerary` covers null/empty rejection. `ItineraryTest.testNextExpectedEvent` is an empty TODO test; no next-event claim is inferred from it.

## Quirk drafts — no decisions made

The issues below are drafts for the coordinator; no behavior was fixed or selected. Because the ledger schema's `quirks` field accepts issue references only, affected entries point to draft paths in `notes`; add issue links after the coordinator publishes them.

- `.migration/quirks/booking-destination-options-mutate-state.md`
- `.migration/quirks/booking-route-selection-redirect.md`
- `.migration/quirks/booking-routing-ignores-deadline.md`
- `.migration/quirks/booking-routing-test-not-discovered.md`
- `.migration/quirks/booking-cargo-not-found-unhandled.md`
- `.migration/quirks/booking-deadline-dialog-parse-error.md`
- `.migration/quirks/booking-claimed-history-link.md`
- `.migration/quirks/booking-routed-table-test-dialog.md`

## Risk analysis and records

- Final risk outputs: `.migration/risk-map/booking/risk-map.md`, `lizard.csv`, `crap.csv`.
- Final lizard and non-blocking CRAP commands ran through `afs-run`; the full run journal is `.migration/evidence/runs/BK-02.md`. It preserves setup probe, final risk runs, and earlier diagnostics, including a rejected `--max 30` attempt because gate mode requires test-produced coverage.
- Risk scope: 224 parsed Java method rows; no coverage input, so 0% coverage; 3 methods are above CRAP 30. Lizard did not emit method rows for `Booking.java` or `GraphTraversalService.java`; their method risk remains unmeasured.
- Raw run logs are under ignored `.migration/runs/BK-02/`; the journal is the durable reference.
- The ADR-0021 session-cost record is generated by the session hook, not edited by this analyst. No new current-session record was present while this report was prepared; preserve/commit the hook-produced record with this ticket when emitted.
