> target_commit: 70374f81e3e034a015e9b29cef10c6cf3c627f58 tree.src: 6efc436302abfc7837dade1e0cb712203be4c516 

> Enriched in place by the harness (ADR-0020, enrich_graph.py) on top of the Understand Anything build recorded in SNAPSHOT.txt.

# Graph gate: target

- 201 nodes, 410 edges
- Edges added by harness enrichers: 90

## Required types (profile graph.require)

- node `table`: 5
- node `endpoint`: 3
- edge `reads_from`: 8
- edge `writes_to`: 5
- edge `routes`: 3
- edge `calls`: 80

## Data paths (slice specs data_paths)

- `track-cargo` **endpoint=/**: `/` →routes `compose_tracking_view` →calls `DjangoCargoRepository` →reads_from `cargo`

## Entry points reaching data (for review)

- 1 of 4 pages/endpoints
  - no path: page `src/cargotracker/cargo/templates/cargo/interfaces/tracking/map/frame.html`
  - no path: endpoint `/admin/`
  - no path: endpoint `/tracking/map/`

## Gate

- PASS

AFS-RESULT gate=graph side=target verdict=pass failures=0 entry_points=4 reaching_data=1 enriched_edges=90

# Graph check: cargotracker

- Commit: `70374f81e3e034a015e9b29cef10c6cf3c627f58` · analyzed 2026-11-02T18:08:29.107337Z
- Languages: html, python · frameworks: Django
- 201 nodes, 410 edges, 5 layers

## Required node types

| Type | Count | Needed for |
|---|---|---|
| `endpoint` | 3 | entry points for slices (HTTP) |
| `screen` | **0** | UI screens (ledger kind: ui) |
| `page` | 1 | UI pages (alternative to screen) |
| `table` | 5 | data capabilities and data-migration slices |
| `service` | **0** | service boundaries |
| `domain` | 4 | bounded contexts |
| `flow` | 7 | business flows → slice anchors |
| `step` | 30 | flow steps → capabilities |

## Required edge types

| Type | Count | Needed for |
|---|---|---|
| `calls` | 80 | dependency resolution |
| `reads_from` | 8 | data access (read) |
| `writes_to` | 5 | data access (write) |
| `routes` | 3 | UI/HTTP routing |
| `tested_by` | **0** | legacy test inventory |
| `contains_flow` | 7 | domain → flow |
| `flow_step` | 30 | flow → step |

## All node types

`file` 87, `class` 46, `step` 30, `function` 18, `flow` 7, `table` 5, `domain` 4, `endpoint` 3, `page` 1

## All edge types

`imports` 136, `calls` 80, `contains` 62, `exports` 56, `flow_step` 30, `reads_from` 8, `depends_on` 7, `contains_flow` 7, `cross_domain` 6, `defines_schema` 5, `writes_to` 5, `implements` 4, `routes` 3, `inherits` 1
