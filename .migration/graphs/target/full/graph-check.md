> target_commit: d3453215147cdad68a9cfbd8cf187a3e9d4d6e34 tree.src: 0e93c3b168c70406fb26e6574dda238a90341454 tree.templates: 6897757dbfdb8f98f8776e20891397d241892c0b 

# Graph gate: target

- 366 nodes, 920 edges
- Edges added by harness enrichers: 506

## Required types (profile graph.require)

- node `table`: 6
- node `endpoint`: 3
- edge `reads_from`: 20
- edge `writes_to`: 8
- edge `routes`: 7
- edge `calls`: 337

## Data paths (slice specs data_paths)

- `handling-registration` **endpoint=POST /rest/handling/reports**: no matching node (match a node's name, or the end of its file path or id)
- `handling-registration` **command=process_handling_attempts**: `process_handling_attempts` →routes `Command` →calls `DjangoCargoRepository` →contains `DjangoCargoRepository.upsert` →reads_from `cargo`
- `track-cargo` **endpoint=/**: `/` →routes `compose_tracking_view` →calls `DjangoCargoRepository` →contains `DjangoCargoRepository.upsert` →reads_from `cargo`

## Entry points owned by a slice (ADR-0026)

- 4 owned, 1 not owned
  - endpoint=/rest/handling/reports (src/cargotracker/urls.py) is owned by no slice: reach it from a slice's data_paths.target or list it in its entry_points.target, or remove it

## Entry points reaching data (for review)

- 3 of 7 pages/endpoints
  - no path: page `src/cargotracker/cargo/templates/cargo/interfaces/tracking/map/frame.html`
  - no path: endpoint `/tracking/map/`
  - no path: page `templates/base.html`
  - no path: page `templates/tracking/result.html`

## Gate

- FAIL: slice handling-registration: data path from `endpoint=POST /rest/handling/reports`: no matching node (match a node's name, or the end of its file path or id)

AFS-RESULT gate=graph side=target verdict=fail failures=1 entry_points=7 reaching_data=3 enriched_edges=506

# Graph check: cargotracker

- Commit: `d3453215147cdad68a9cfbd8cf187a3e9d4d6e34` · analyzed 2026-11-04T18:00:20.731Z
- Languages: html, markdown, python · frameworks: Django
- 366 nodes, 920 edges, 7 layers

## Required node types

| Type | Count | Needed for |
|---|---|---|
| `endpoint` | 3 | entry points for slices (HTTP) |
| `screen` | **0** | UI screens (ledger kind: ui) |
| `page` | 4 | UI pages (alternative to screen) |
| `table` | 6 | data capabilities and data-migration slices |
| `service` | **0** | service boundaries |
| `domain` | 3 | bounded contexts |
| `flow` | 5 | business flows → slice anchors |
| `step` | 20 | flow steps → capabilities |

## Required edge types

| Type | Count | Needed for |
|---|---|---|
| `calls` | 337 | dependency resolution |
| `reads_from` | 20 | data access (read) |
| `writes_to` | 8 | data access (write) |
| `routes` | 7 | UI/HTTP routing |
| `tested_by` | **0** | legacy test inventory |
| `contains_flow` | 5 | domain → flow |
| `flow_step` | 20 | flow → step |

## All node types

`method` 125, `file` 102, `class` 64, `function` 31, `step` 20, `table` 6, `flow` 5, `page` 4, `endpoint` 3, `domain` 3, `command` 2, `document` 1

## All edge types

`calls` 337, `contains` 211, `imports` 188, `exports` 75, `implements` 22, `reads_from` 20, `flow_step` 20, `depends_on` 14, `writes_to` 8, `routes` 7, `defines_schema` 6, `contains_flow` 5, `cross_domain` 4, `configures` 2, `documents` 1
