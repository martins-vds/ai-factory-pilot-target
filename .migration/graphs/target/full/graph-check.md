> target_commit: 17e26a22bb9af4219576c09b8b2f099775c118ed tree.src: 8b7d31ec737c6a932b3e38ad8cb7274958785fee tree.templates: 80743ec372b9038134423563cb88704da0326a24 

# Graph gate: target

- 528 nodes, 1237 edges
- Edges added by harness enrichers: 722

## Required types (profile graph.require)

- node `table`: 7
- node `endpoint`: 6
- edge `reads_from`: 26
- edge `writes_to`: 14
- edge `routes`: 20
- edge `calls`: 490

## Data paths (slice specs data_paths)

- `admin-live-map` **endpoint=/admin/live-map/**: `/admin/live-map/` →routes `compose_admin_map_views` →calls `DjangoCargoRepository` →contains `DjangoCargoRepository.upsert` →reads_from `cargo` _(not built yet: AM-04D, AM-04E open)_
- `admin-live-map` **endpoint=/admin/live-map/markers/**: `/admin/live-map/markers/` →routes `compose_admin_map_views` →calls `DjangoCargoRepository` →contains `DjangoCargoRepository.upsert` →reads_from `cargo` _(not built yet: AM-04D, AM-04E open)_
- `booking` **endpoint=/booking/**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: BK-05F, BK-05G, BK-05H open)_
- `booking` **endpoint=/admin/dashboard/**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: BK-05F, BK-05G, BK-05H open)_
- `booking` **endpoint=/admin/cargo/<tracking_id>/**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: BK-05F, BK-05G, BK-05H open)_
- `booking` **endpoint=/admin/cargo/<tracking_id>/route/**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: BK-05F, BK-05G, BK-05H open)_
- `booking` **endpoint=/admin/cargo/<tracking_id>/itineraries/**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: BK-05F, BK-05G, BK-05H open)_
- `booking` **endpoint=/admin/dashboard/not-routed/**: no matching node (match a node's name, or the end of its file path or id) _(not built yet: BK-05F, BK-05G, BK-05H open)_
- `data-migration` **command=load_data_snapshot**: `load_data_snapshot` →writes_to `location`
- `handling-registration` **endpoint=POST /rest/handling/reports**: `POST /rest/handling/reports` →routes `compose_handling_report_view` →calls `DjangoAttemptSubmissionRepository` →contains `DjangoAttemptSubmissionRepository.submit` →writes_to `handling_registration_attempt`
- `handling-registration` **command=process_handling_attempts**: `process_handling_attempts` →routes `Command` →calls `DjangoCargoRepository` →contains `DjangoCargoRepository.upsert` →reads_from `cargo`
- `track-cargo` **endpoint=/**: `/` →routes `compose_tracking_view` →calls `DjangoCargoRepository` →contains `DjangoCargoRepository.upsert` →reads_from `cargo`

## Entry points owned by a slice (ADR-0026)

- 10 owned, 0 not owned

## Entry points reaching data (for review)

- 6 of 22 pages/endpoints
  - no path: page `templates/booking/dashboard/dashboard.html`
  - no path: page `templates/booking/cargo_details.html`
  - no path: page `templates/booking/wizard/origin.html`
  - no path: page `templates/booking/wizard/destination.html`
  - no path: page `templates/booking/wizard/deadline.html`
  - no path: page `templates/admin/_live_map_markers.html`
  - no path: page `src/cargotracker/cargo/templates/cargo/interfaces/tracking/map/frame.html`
  - no path: endpoint `GET /rest/graph-traversal/shortest-path`
  - no path: endpoint `/tracking/map/`
  - no path: page `templates/base.html`
  - no path: page `templates/booking/dashboard/admin_base.html`
  - no path: page `templates/booking/dashboard/claimed_table.html`
  - no path: page `templates/booking/dashboard/routed_table.html`
  - no path: page `templates/booking/dashboard/not_routed_table.html`
  - no path: page `templates/booking/wizard/_deadline_form.html`
  - no path: page `templates/tracking/result.html`

## Gate

- PASS

AFS-RESULT gate=graph side=target verdict=pass failures=0 entry_points=22 reaching_data=6 enriched_edges=722

# Graph check: cargotracker

- Commit: `17e26a22bb9af4219576c09b8b2f099775c118ed` · analyzed 2026-11-07T23:10:36.556Z
- Languages: html, markdown, python · frameworks: Django
- 528 nodes, 1237 edges, 6 layers

## Required node types

| Type | Count | Needed for |
|---|---|---|
| `endpoint` | 6 | entry points for slices (HTTP) |
| `screen` | **0** | UI screens (ledger kind: ui) |
| `page` | 16 | UI pages (alternative to screen) |
| `table` | 7 | data capabilities and data-migration slices |
| `service` | **0** | service boundaries |
| `domain` | 4 | bounded contexts |
| `flow` | 9 | business flows → slice anchors |
| `step` | 38 | flow steps → capabilities |

## Required edge types

| Type | Count | Needed for |
|---|---|---|
| `calls` | 490 | dependency resolution |
| `reads_from` | 26 | data access (read) |
| `writes_to` | 14 | data access (write) |
| `routes` | 20 | UI/HTTP routing |
| `tested_by` | **0** | legacy test inventory |
| `contains_flow` | 9 | domain → flow |
| `flow_step` | 38 | flow → step |

## All node types

`method` 147, `file` 141, `class` 79, `function` 76, `step` 38, `page` 16, `flow` 9, `table` 7, `endpoint` 6, `command` 4, `domain` 4, `document` 1

## All edge types

`calls` 490, `contains` 287, `imports` 241, `exports` 70, `flow_step` 38, `reads_from` 26, `implements` 21, `routes` 20, `writes_to` 14, `depends_on` 10, `contains_flow` 9, `defines_schema` 7, `cross_domain` 4
