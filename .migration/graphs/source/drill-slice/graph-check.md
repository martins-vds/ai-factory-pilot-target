> source: eclipse-ee4j/cargotracker@f3beacf78de4f6d34edc4971ac87e38a5c6fe59d source_sha: f3beacf78de4f6d34edc4971ac87e38a5c6fe59d 

# Graph check: cargotracker-domain

- Commit: `f3beacf78de4f6d34edc4971ac87e38a5c6fe59d` · analyzed 2026-11-08T03:42:56.925113Z
- Languages: java, json, txt · frameworks: Jakarta EE
- 199 nodes, 313 edges, 5 layers

## Required node types

| Type | Count | Needed for |
|---|---|---|
| `endpoint` | **0** | entry points for slices (HTTP) |
| `screen` | **0** | UI screens (ledger kind: ui) |
| `page` | **0** | UI pages (alternative to screen) |
| `table` | 4 | data capabilities and data-migration slices |
| `service` | **0** | service boundaries |
| `domain` | 3 | bounded contexts |
| `flow` | 3 | business flows → slice anchors |
| `step` | 13 | flow steps → capabilities |

## Required edge types

| Type | Count | Needed for |
|---|---|---|
| `calls` | 85 | dependency resolution |
| `reads_from` | **0** | data access (read) |
| `writes_to` | **0** | data access (write) |
| `routes` | **0** | UI/HTTP routing |
| `tested_by` | **0** | legacy test inventory |
| `contains_flow` | 3 | domain → flow |
| `flow_step` | 13 | flow → step |

## All node types

`method` 126, `function` 18, `class` 16, `file` 15, `step` 13, `table` 4, `domain` 3, `flow` 3, `document` 1

## All edge types

`contains` 159, `calls` 85, `imports` 17, `exports` 15, `flow_step` 13, `implements` 5, `depends_on` 4, `inherits` 4, `defines_schema` 4, `cross_domain` 3, `contains_flow` 3, `documents` 1
