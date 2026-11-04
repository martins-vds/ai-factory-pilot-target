> target_commit: f3f55da28fb45d597591b3ecdee7bae401591fef tree.src: 0e93c3b168c70406fb26e6574dda238a90341454 tree.templates: 6897757dbfdb8f98f8776e20891397d241892c0b 

# Graph gate: target

- 374 nodes, 929 edges
- Edges added by harness enrichers: 510

## Required types (profile graph.require)

- node `table`: 6
- node `endpoint`: 3
- edge `reads_from`: 20
- edge `writes_to`: 8
- edge `routes`: 7
- edge `calls`: 338

## Data paths (slice specs data_paths)

- `handling-registration` **endpoint=POST /rest/handling/reports**: `POST /rest/handling/reports` →routes `compose_handling_report_view` →calls `DjangoAttemptSubmissionRepository` →contains `DjangoAttemptSubmissionRepository.submit` →writes_to `handling_registration_attempt`
- `handling-registration` **command=process_handling_attempts**: `process_handling_attempts` →routes `Command` →calls `DjangoCargoRepository` →contains `DjangoCargoRepository.upsert` →reads_from `cargo`
- `track-cargo` **endpoint=/**: `/` →routes `compose_tracking_view` →calls `DjangoCargoRepository` →contains `DjangoCargoRepository.upsert` →reads_from `cargo`

## Entry points owned by a slice (ADR-0026)

- 5 owned, 0 not owned

## Entry points reaching data (for review)

- 3 of 7 pages/endpoints
  - no path: page `src/cargotracker/cargo/templates/cargo/interfaces/tracking/map/frame.html`
  - no path: endpoint `/tracking/map/`
  - no path: page `templates/base.html`
  - no path: page `templates/tracking/result.html`

## Gate

- PASS

AFS-RESULT gate=graph side=target verdict=pass failures=0 entry_points=7 reaching_data=3 enriched_edges=510

# Graph check: cargotracker

- Commit: `f3f55da28fb45d597591b3ecdee7bae401591fef` · analyzed 2026-11-04T19:09:10.920262Z
- Languages: python, html, markdown · frameworks: Django
- 374 nodes, 929 edges, 7 layers

## Required node types

| Type | Count | Needed for |
|---|---|---|
| `endpoint` | 3 | entry points for slices (HTTP) |
| `screen` | **0** | UI screens (ledger kind: ui) |
| `page` | 4 | UI pages (alternative to screen) |
| `table` | 6 | data capabilities and data-migration slices |
| `service` | **0** | service boundaries |
| `domain` | 5 | bounded contexts |
| `flow` | 7 | business flows → slice anchors |
| `step` | 27 | flow steps → capabilities |

## Required edge types

| Type | Count | Needed for |
|---|---|---|
| `calls` | 338 | dependency resolution |
| `reads_from` | 20 | data access (read) |
| `writes_to` | 8 | data access (write) |
| `routes` | 7 | UI/HTTP routing |
| `tested_by` | **0** | legacy test inventory |
| `contains_flow` | 7 | domain → flow |
| `flow_step` | 27 | flow → step |

## All node types

`method` 125, `file` 102, `class` 57, `function` 35, `step` 27, `flow` 7, `table` 6, `domain` 5, `page` 4, `endpoint` 3, `command` 2, `document` 1

## All edge types

`calls` 338, `contains` 209, `imports` 188, `exports` 75, `flow_step` 27, `implements` 22, `reads_from` 20, `depends_on` 11, `cross_domain` 9, `writes_to` 8, `routes` 7, `contains_flow` 7, `defines_schema` 6, `documents` 2
