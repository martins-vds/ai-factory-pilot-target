> target_commit: d7f4fe8012108e9bb44da59ea8cb59dadbf21f65 tree.src: 0f19d5ca6095737423b31f7af9103b75228e79f7 tree.templates: 6897757dbfdb8f98f8776e20891397d241892c0b 

# Graph gate: target

- 205 nodes, 417 edges
- Edges added by harness enrichers: 86

## Required types (profile graph.require)

- node `table`: 5
- node `endpoint`: 3
- edge `reads_from`: 8
- edge `writes_to`: 5
- edge `routes`: 5
- edge `calls`: 83

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

AFS-RESULT gate=graph side=target verdict=pass failures=0 entry_points=7 reaching_data=2 enriched_edges=86

# Graph check: cargotracker

- Commit: `d7f4fe8012108e9bb44da59ea8cb59dadbf21f65` · analyzed 2026-11-03T04:41:26.728Z
- Languages: html, python · frameworks: Django
- 205 nodes, 417 edges, 8 layers

## Required node types

| Type | Count | Needed for |
|---|---|---|
| `endpoint` | 3 | entry points for slices (HTTP) |
| `screen` | **0** | UI screens (ledger kind: ui) |
| `page` | 4 | UI pages (alternative to screen) |
| `table` | 5 | data capabilities and data-migration slices |
| `service` | **0** | service boundaries |
| `domain` | 4 | bounded contexts |
| `flow` | 6 | business flows → slice anchors |
| `step` | 25 | flow steps → capabilities |

## Required edge types

| Type | Count | Needed for |
|---|---|---|
| `calls` | 83 | dependency resolution |
| `reads_from` | 8 | data access (read) |
| `writes_to` | 5 | data access (write) |
| `routes` | 5 | UI/HTTP routing |
| `tested_by` | **0** | legacy test inventory |
| `contains_flow` | 6 | domain → flow |
| `flow_step` | 25 | flow → step |

## All node types

`file` 90, `class` 48, `step` 25, `function` 18, `flow` 6, `table` 5, `page` 4, `domain` 4, `endpoint` 3, `document` 1, `command` 1

## All edge types

`imports` 136, `calls` 83, `contains` 66, `exports` 58, `flow_step` 25, `reads_from` 8, `depends_on` 7, `cross_domain` 6, `contains_flow` 6, `implements` 5, `defines_schema` 5, `routes` 5, `writes_to` 5, `documents` 1, `related` 1
