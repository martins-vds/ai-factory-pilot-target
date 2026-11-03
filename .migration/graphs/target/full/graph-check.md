> target_commit: 46261441655552d43b0564904ec4dd5cebee4676 tree.src: f6a76dfa27db13383bd1a6559885b360fe52e12e tree.templates: 6897757dbfdb8f98f8776e20891397d241892c0b 

# Graph gate: target

- 294 nodes, 664 edges
- Edges added by harness enrichers: 337

## Required types (profile graph.require)

- node `table`: 5
- node `endpoint`: 2
- edge `reads_from`: 18
- edge `writes_to`: 6
- edge `routes`: 5
- edge `calls`: 219

## Data paths (slice specs data_paths)

- `track-cargo` **endpoint=/**: `/` →routes `compose_tracking_view` →calls `DjangoCargoRepository` →contains `DjangoCargoRepository.upsert` →reads_from `cargo`

## Entry points owned by a slice (ADR-0026)

- 3 owned, 0 not owned

## Entry points reaching data (for review)

- 2 of 6 pages/endpoints
  - no path: page `src/cargotracker/cargo/templates/cargo/interfaces/tracking/map/frame.html`
  - no path: endpoint `/tracking/map/`
  - no path: page `templates/base.html`
  - no path: page `templates/tracking/result.html`

## Gate

- PASS

AFS-RESULT gate=graph side=target verdict=pass failures=0 entry_points=6 reaching_data=2 enriched_edges=337

# Graph check: cargotracker

- Commit: `46261441655552d43b0564904ec4dd5cebee4676` · analyzed 2026-11-03T17:28:35.571Z
- Languages: html, markdown, python · frameworks: Django
- 294 nodes, 664 edges, 7 layers

## Required node types

| Type | Count | Needed for |
|---|---|---|
| `endpoint` | 2 | entry points for slices (HTTP) |
| `screen` | **0** | UI screens (ledger kind: ui) |
| `page` | 4 | UI pages (alternative to screen) |
| `table` | 5 | data capabilities and data-migration slices |
| `service` | **0** | service boundaries |
| `domain` | 4 | bounded contexts |
| `flow` | 7 | business flows → slice anchors |
| `step` | 24 | flow steps → capabilities |

## Required edge types

| Type | Count | Needed for |
|---|---|---|
| `calls` | 219 | dependency resolution |
| `reads_from` | 18 | data access (read) |
| `writes_to` | 6 | data access (write) |
| `routes` | 5 | UI/HTTP routing |
| `tested_by` | **0** | legacy test inventory |
| `contains_flow` | 7 | domain → flow |
| `flow_step` | 24 | flow → step |

## All node types

`method` 91, `file` 90, `class` 46, `step` 24, `function` 19, `flow` 7, `table` 5, `page` 4, `domain` 4, `endpoint` 2, `document` 1, `command` 1

## All edge types

`calls` 219, `contains` 153, `imports` 136, `exports` 51, `flow_step` 24, `reads_from` 18, `implements` 16, `depends_on` 12, `contains_flow` 7, `writes_to` 6, `cross_domain` 6, `defines_schema` 5, `routes` 5, `related` 4, `documents` 2
