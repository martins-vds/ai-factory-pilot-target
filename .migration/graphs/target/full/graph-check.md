> target_commit: 70374f81e3e034a015e9b29cef10c6cf3c627f58 tree.src: 6efc436302abfc7837dade1e0cb712203be4c516 

# Graph check: cargotracker

- Commit: `70374f81e3e034a015e9b29cef10c6cf3c627f58` · analyzed 2026-11-02T18:08:29.107337Z
- Languages: html, python · frameworks: Django
- 190 nodes, 320 edges, 5 layers

## Required node types

| Type | Count | Needed for |
|---|---|---|
| `endpoint` | **0** | entry points for slices (HTTP) |
| `screen` | **0** | UI screens (ledger kind: ui) |
| `page` | **0** | UI pages (alternative to screen) |
| `table` | **0** | data capabilities and data-migration slices |
| `service` | **0** | service boundaries |
| `domain` | 4 | bounded contexts |
| `flow` | 7 | business flows → slice anchors |
| `step` | 30 | flow steps → capabilities |

## Required edge types

| Type | Count | Needed for |
|---|---|---|
| `calls` | 12 | dependency resolution |
| `reads_from` | **0** | data access (read) |
| `writes_to` | **0** | data access (write) |
| `routes` | **0** | UI/HTTP routing |
| `tested_by` | **0** | legacy test inventory |
| `contains_flow` | 7 | domain → flow |
| `flow_step` | 30 | flow → step |

## All node types

`file` 87, `class` 46, `step` 30, `function` 16, `flow` 7, `domain` 4

## All edge types

`imports` 136, `contains` 62, `exports` 56, `flow_step` 30, `calls` 12, `depends_on` 7, `contains_flow` 7, `cross_domain` 6, `implements` 3, `inherits` 1
