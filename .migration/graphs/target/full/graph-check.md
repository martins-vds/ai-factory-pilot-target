> target_commit: c239f78a8c26a114c4bda6dacb89a72e8318fbe9 tree.src: 72218370a027da890c3fb91baa6f10e77affaf5f tree.templates: 8a7ad8626077b41b83ff446d71596de65ec8d016 

# Graph gate: target

- 518 nodes, 1207 edges
- Edges added by harness enrichers: 670

## Required types (profile graph.require)

- node `table`: 7
- node `endpoint`: 6
- edge `reads_from`: 20
- edge `writes_to`: 8
- edge `routes`: 16
- edge `calls`: 480

## Data paths (slice specs data_paths)

- `admin-live-map` **endpoint=/admin/live-map/**: **NO PATH** from 1 matching node(s) to a table/schema over calls/contains/inherits/publishes/reads_from/routes/triggers/writes_to (implements backwards)
- `admin-live-map` **endpoint=/admin/live-map/markers/**: **NO PATH** from 1 matching node(s) to a table/schema over calls/contains/inherits/publishes/reads_from/routes/triggers/writes_to (implements backwards)
- `booking` **endpoint=/booking/**: no matching node (match a node's name, or the end of its file path or id)
- `booking` **endpoint=/admin/dashboard/**: no matching node (match a node's name, or the end of its file path or id)
- `booking` **endpoint=/admin/cargo/<tracking_id>/**: no matching node (match a node's name, or the end of its file path or id)
- `booking` **endpoint=/admin/cargo/<tracking_id>/route/**: no matching node (match a node's name, or the end of its file path or id)
- `booking` **endpoint=/admin/cargo/<tracking_id>/itineraries/**: no matching node (match a node's name, or the end of its file path or id)
- `booking` **endpoint=/admin/dashboard/not-routed/**: no matching node (match a node's name, or the end of its file path or id)
- `data-migration` **command=load_data_snapshot**: **NO PATH** from 1 matching node(s) to a table/schema over calls/contains/inherits/publishes/reads_from/routes/triggers/writes_to (implements backwards)
- `handling-registration` **endpoint=POST /rest/handling/reports**: `POST /rest/handling/reports` →routes `compose_handling_report_view` →calls `DjangoAttemptSubmissionRepository` →contains `DjangoAttemptSubmissionRepository.submit` →writes_to `handling_registration_attempt`
- `handling-registration` **command=process_handling_attempts**: `process_handling_attempts` →routes `Command` →calls `DjangoCargoRepository` →contains `DjangoCargoRepository.upsert` →reads_from `cargo`
- `track-cargo` **endpoint=/**: `/` →routes `compose_tracking_view` →calls `DjangoCargoRepository` →contains `DjangoCargoRepository.upsert` →reads_from `cargo`

## Entry points owned by a slice (ADR-0026)

- 10 owned, 0 not owned

## Entry points reaching data (for review)

- 3 of 16 pages/endpoints
  - no path: page `templates/booking/wizard/origin.html`
  - no path: page `templates/booking/wizard/destination.html`
  - no path: page `templates/booking/wizard/deadline.html`
  - no path: page `templates/admin/live_map.html`
  - no path: page `templates/admin/_live_map_markers.html`
  - no path: page `src/cargotracker/cargo/templates/cargo/interfaces/tracking/map/frame.html`
  - no path: endpoint `GET /rest/graph-traversal/shortest-path`
  - no path: endpoint `/tracking/map/`
  - no path: endpoint `/admin/live-map/`
  - no path: endpoint `/admin/live-map/markers/`
  - no path: page `templates/base.html`
  - no path: page `templates/booking/wizard/_deadline_form.html`
  - no path: page `templates/tracking/result.html`

## Gate

- FAIL: slice admin-live-map: data path from `endpoint=/admin/live-map/`: **NO PATH** from 1 matching node(s) to a table/schema over calls/contains/inherits/publishes/reads_from/routes/triggers/writes_to (implements backwards)
- FAIL: slice admin-live-map: data path from `endpoint=/admin/live-map/markers/`: **NO PATH** from 1 matching node(s) to a table/schema over calls/contains/inherits/publishes/reads_from/routes/triggers/writes_to (implements backwards)
- FAIL: slice booking: data path from `endpoint=/booking/`: no matching node (match a node's name, or the end of its file path or id)
- FAIL: slice booking: data path from `endpoint=/admin/dashboard/`: no matching node (match a node's name, or the end of its file path or id)
- FAIL: slice booking: data path from `endpoint=/admin/cargo/<tracking_id>/`: no matching node (match a node's name, or the end of its file path or id)
- FAIL: slice booking: data path from `endpoint=/admin/cargo/<tracking_id>/route/`: no matching node (match a node's name, or the end of its file path or id)
- FAIL: slice booking: data path from `endpoint=/admin/cargo/<tracking_id>/itineraries/`: no matching node (match a node's name, or the end of its file path or id)
- FAIL: slice booking: data path from `endpoint=/admin/dashboard/not-routed/`: no matching node (match a node's name, or the end of its file path or id)
- FAIL: slice data-migration: data path from `command=load_data_snapshot`: **NO PATH** from 1 matching node(s) to a table/schema over calls/contains/inherits/publishes/reads_from/routes/triggers/writes_to (implements backwards)

AFS-RESULT gate=graph side=target verdict=fail failures=9 entry_points=16 reaching_data=3 enriched_edges=670

# Graph check: cargotracker

- Commit: `c239f78a8c26a114c4bda6dacb89a72e8318fbe9` · analyzed 2026-11-07T21:45:53.221577Z
- Languages: html, json, markdown, python · frameworks: Django
- 518 nodes, 1207 edges, 9 layers

## Required node types

| Type | Count | Needed for |
|---|---|---|
| `endpoint` | 6 | entry points for slices (HTTP) |
| `screen` | **0** | UI screens (ledger kind: ui) |
| `page` | 10 | UI pages (alternative to screen) |
| `table` | 7 | data capabilities and data-migration slices |
| `service` | **0** | service boundaries |
| `domain` | 6 | bounded contexts |
| `flow` | 11 | business flows → slice anchors |
| `step` | 34 | flow steps → capabilities |

## Required edge types

| Type | Count | Needed for |
|---|---|---|
| `calls` | 480 | dependency resolution |
| `reads_from` | 20 | data access (read) |
| `writes_to` | 8 | data access (write) |
| `routes` | 16 | UI/HTTP routing |
| `tested_by` | **0** | legacy test inventory |
| `contains_flow` | 11 | domain → flow |
| `flow_step` | 34 | flow → step |

## All node types

`method` 144, `file` 133, `function` 85, `class` 77, `step` 34, `flow` 11, `page` 10, `table` 7, `endpoint` 6, `domain` 6, `command` 4, `document` 1

## All edge types

`calls` 480, `contains` 281, `imports` 235, `exports` 69, `flow_step` 34, `implements` 21, `reads_from` 20, `routes` 16, `depends_on` 12, `contains_flow` 11, `writes_to` 8, `defines_schema` 7, `cross_domain` 6, `inherits` 4, `configures` 2, `documents` 1
