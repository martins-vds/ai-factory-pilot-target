> target_commit: 135c70a276d4b20d377d701e064c9c819de4151c tree.src: 2b8dbea633e8cb0e80c5ced292856425f4dc3358 tree.templates: 179209eaf66c393b325742efba8417e0ad1ff169 

# Graph gate: target

- 564 nodes, 1373 edges
- Edges added by harness enrichers: 782

## Required types (profile graph.require)

- node `table`: 7
- node `endpoint`: 13
- edge `reads_from`: 26
- edge `writes_to`: 14
- edge `routes`: 36
- edge `calls`: 535

## Data paths (slice specs data_paths)

- `admin-live-map` **endpoint=/admin/live-map/**: `/admin/live-map/` →routes `compose_admin_map_views` →calls `DjangoCargoRepository` →contains `DjangoCargoRepository.upsert` →reads_from `cargo` — reaches 2 data node(s): cargo, leg
- `admin-live-map` **endpoint=/admin/live-map/markers/**: `/admin/live-map/markers/` →routes `compose_admin_map_views` →calls `DjangoCargoRepository` →contains `DjangoCargoRepository.upsert` →reads_from `cargo` — reaches 2 data node(s): cargo, leg
- `booking` **endpoint=/booking/**: `/booking/` →routes `create_booking_wizard_view` →calls `CargoRegistration` →contains `CargoRegistration.register` →calls `CargoRepository.upsert` ←implements `DjangoCargoRepository.upsert` →reads_from `cargo` — reaches 2 data node(s): cargo, leg
- `booking` **endpoint=/admin/dashboard/**: `/admin/dashboard/` →routes `create_booking_views` →calls `CargoDashboard` →calls `CargoRepository` →contains `CargoRepository.upsert` ←implements `DjangoCargoRepository.upsert` →reads_from `cargo` — reaches 5 data node(s): HandlingEvent, cargo, leg, location, voyage
- `booking` **endpoint=/admin/cargo/<tracking_id>/**: `/admin/cargo/<str:tracking_id>/` →routes `create_booking_views` →calls `CargoDashboard` →calls `CargoRepository` →contains `CargoRepository.upsert` ←implements `DjangoCargoRepository.upsert` →reads_from `cargo` — reaches 5 data node(s): HandlingEvent, cargo, leg, location, voyage
- `booking` **endpoint=/admin/cargo/<tracking_id>/route/**: `/admin/cargo/<str:tracking_id>/route/` →routes `create_route_selection_views` →calls `CargoRouting` →contains `CargoRouting.assign_route` →calls `HandlingEventRepository.lookup_handling_history_of_cargo` ←implements `DjangoHandlingEventRepository.lookup_handling_history_of_cargo` →reads_from `HandlingEvent` — reaches 5 data node(s): HandlingEvent, cargo, leg, location, voyage
- `booking` **endpoint=/admin/cargo/<tracking_id>/itineraries/**: `/admin/cargo/<str:tracking_id>/itineraries/` →routes `create_route_selection_views` →calls `CargoRouting` →contains `CargoRouting.assign_route` →calls `HandlingEventRepository.lookup_handling_history_of_cargo` ←implements `DjangoHandlingEventRepository.lookup_handling_history_of_cargo` →reads_from `HandlingEvent` — reaches 5 data node(s): HandlingEvent, cargo, leg, location, voyage
- `booking` **endpoint=/admin/cargo/<tracking_id>/destination/**: `/admin/cargo/<str:tracking_id>/destination/` →routes `create_dialog_views` →calls `CargoDashboard` →calls `CargoRepository` →contains `CargoRepository.upsert` ←implements `DjangoCargoRepository.upsert` →reads_from `cargo` — reaches 5 data node(s): HandlingEvent, cargo, leg, location, voyage
- `booking` **endpoint=/admin/cargo/<tracking_id>/deadline/**: `/admin/cargo/<str:tracking_id>/deadline/` →routes `create_dialog_views` →calls `CargoDashboard` →calls `CargoRepository` →contains `CargoRepository.upsert` ←implements `DjangoCargoRepository.upsert` →reads_from `cargo` — reaches 5 data node(s): HandlingEvent, cargo, leg, location, voyage
- `data-migration` **command=load_data_snapshot**: `load_data_snapshot` →writes_to `location` — reaches 6 data node(s): HandlingEvent, cargo, carrier_movement, leg, location, voyage
- `handling-registration` **endpoint=POST /rest/handling/reports**: `POST /rest/handling/reports` →routes `compose_handling_report_view` →calls `DjangoAttemptSubmissionRepository` →contains `DjangoAttemptSubmissionRepository.submit` →writes_to `handling_registration_attempt`
- `handling-registration` **command=process_handling_attempts**: `process_handling_attempts` →routes `Command` →calls `DjangoCargoRepository` →contains `DjangoCargoRepository.upsert` →reads_from `cargo` — reaches 6 data node(s): HandlingEvent, cargo, handling_registration_attempt, leg, location, voyage
- `track-cargo` **endpoint=/**: `/` →routes `compose_tracking_view` →calls `DjangoCargoRepository` →contains `DjangoCargoRepository.upsert` →reads_from `cargo` — reaches 5 data node(s): HandlingEvent, cargo, leg, location, voyage

## Entry points owned by a slice (ADR-0026)

- 17 owned, 0 not owned

## Entry points reaching data (for review)

- 19 of 34 pages/endpoints
  - no path: page `templates/booking/cargo_details.html`
  - no path: page `templates/booking/route_selection/route.html`
  - no path: page `templates/booking/route_selection/select_itinerary.html`
  - no path: page `templates/booking/wizard/origin.html`
  - no path: page `templates/booking/wizard/destination.html`
  - no path: page `templates/admin/_live_map_markers.html`
  - no path: page `src/cargotracker/cargo/templates/cargo/interfaces/tracking/map/frame.html`
  - no path: endpoint `GET /rest/graph-traversal/shortest-path`
  - no path: endpoint `/tracking/map/`
  - no path: page `templates/base.html`
  - no path: page `templates/booking/dashboard/admin_base.html`
  - no path: page `templates/booking/dashboard/claimed_table.html`
  - no path: page `templates/booking/dashboard/routed_table.html`
  - no path: page `templates/booking/route_selection/_candidate_routes.html`
  - no path: page `templates/tracking/result.html`

## Gate

- PASS

AFS-RESULT gate=graph side=target verdict=pass failures=0 entry_points=34 reaching_data=19 enriched_edges=782

# Graph check: cargotracker

- Commit: `135c70a276d4b20d377d701e064c9c819de4151c` · analyzed 2026-11-08T22:09:44.830Z
- Languages: html, markdown, python · frameworks: Django, HTMX
- 564 nodes, 1373 edges, 7 layers

## Required node types

| Type | Count | Needed for |
|---|---|---|
| `endpoint` | 13 | entry points for slices (HTTP) |
| `screen` | **0** | UI screens (ledger kind: ui) |
| `page` | 21 | UI pages (alternative to screen) |
| `table` | 7 | data capabilities and data-migration slices |
| `service` | **0** | service boundaries |
| `domain` | 4 | bounded contexts |
| `flow` | 10 | business flows → slice anchors |
| `step` | 38 | flow steps → capabilities |

## Required edge types

| Type | Count | Needed for |
|---|---|---|
| `calls` | 535 | dependency resolution |
| `reads_from` | 26 | data access (read) |
| `writes_to` | 14 | data access (write) |
| `routes` | 36 | UI/HTTP routing |
| `tested_by` | **0** | legacy test inventory |
| `contains_flow` | 10 | domain → flow |
| `flow_step` | 38 | flow → step |

## All node types

`file` 149, `method` 147, `function` 93, `class` 77, `step` 38, `page` 21, `endpoint` 13, `flow` 10, `table` 7, `command` 4, `domain` 4, `document` 1

## All edge types

`calls` 535, `contains` 299, `imports` 269, `exports` 90, `flow_step` 38, `routes` 36, `reads_from` 26, `implements` 22, `depends_on` 16, `writes_to` 14, `contains_flow` 10, `defines_schema` 7, `related` 4, `cross_domain` 4, `documents` 2, `migrates` 1
