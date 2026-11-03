> target_commit: fabb9970ca4e6194b1c348800f16ba2f7842bda8 tree.src: 0f19d5ca6095737423b31f7af9103b75228e79f7 tree.templates: 6897757dbfdb8f98f8776e20891397d241892c0b 

# Graph gate: target

- 193 nodes, 460 edges
- Edges added by harness enrichers: 176

## Required types (profile graph.require)

- node `table`: 5
- node `endpoint`: 3
- edge `reads_from`: 8
- edge `writes_to`: 5
- edge `routes`: 5
- edge `calls`: 149

## Data paths (slice specs data_paths)

- `track-cargo` **endpoint=/**: `/` →routes `compose_tracking_view` →calls `DjangoCargoRepository` →reads_from `cargo`

## Entry points reaching data (for review)

- 2 of 7 pages/endpoints
  - no path: page `src/cargotracker/cargo/templates/cargo/interfaces/tracking/map/frame.html`
  - no path: endpoint `/admin/`
  - no path: endpoint `/tracking/map/`
  - no path: page `templates/base.html`
  - no path: page `templates/tracking/result.html`

## Gate

- PASS

AFS-RESULT gate=graph side=target verdict=pass failures=0 entry_points=7 reaching_data=2 enriched_edges=176

# Graph check: cargotracker

- Commit: `fabb9970ca4e6194b1c348800f16ba2f7842bda8` · analyzed 2026-11-03T14:40:44.739Z
- Languages: html, markdown, python · frameworks: Django
- 193 nodes, 460 edges, 7 layers

## Required node types

| Type | Count | Needed for |
|---|---|---|
| `endpoint` | 3 | entry points for slices (HTTP) |
| `screen` | **0** | UI screens (ledger kind: ui) |
| `page` | 4 | UI pages (alternative to screen) |
| `table` | 5 | data capabilities and data-migration slices |
| `service` | **0** | service boundaries |
| `domain` | 5 | bounded contexts |
| `flow` | 3 | business flows → slice anchors |
| `step` | 14 | flow steps → capabilities |

## Required edge types

| Type | Count | Needed for |
|---|---|---|
| `calls` | 149 | dependency resolution |
| `reads_from` | 8 | data access (read) |
| `writes_to` | 5 | data access (write) |
| `routes` | 5 | UI/HTTP routing |
| `tested_by` | **0** | legacy test inventory |
| `contains_flow` | 3 | domain → flow |
| `flow_step` | 14 | flow → step |

## All node types

`file` 90, `class` 48, `function` 19, `step` 14, `table` 5, `domain` 5, `page` 4, `endpoint` 3, `flow` 3, `document` 1, `command` 1

## All edge types

`calls` 149, `imports` 136, `contains` 62, `exports` 57, `flow_step` 14, `reads_from` 8, `cross_domain` 7, `defines_schema` 5, `routes` 5, `writes_to` 5, `implements` 4, `depends_on` 3, `contains_flow` 3, `documents` 1, `related` 1
