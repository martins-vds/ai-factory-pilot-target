> source: eclipse-ee4j/cargotracker@f3beacf78de4f6d34edc4971ac87e38a5c6fe59d source_sha: f3beacf78de4f6d34edc4971ac87e38a5c6fe59d 

# Graph check: Eclipse Cargo Tracker

- Commit: `f3beacf78de4f6d34edc4971ac87e38a5c6fe59d` · analyzed 2026-11-02T18:09:51.319Z
- Languages: markdown, xml, java, html, properties, xhtml, css, csv, txt · frameworks: Jakarta EE, JSF, JAX-RS, Maven
- 369 nodes, 538 edges, 8 layers

## Required node types

| Type | Count | Needed for |
|---|---|---|
| `endpoint` | **0** | entry points for slices (HTTP) |
| `screen` | **0** | UI screens (ledger kind: ui) |
| `page` | **0** | UI pages (alternative to screen) |
| `table` | 1 | data capabilities and data-migration slices |
| `service` | **0** | service boundaries |
| `domain` | 4 | bounded contexts |
| `flow` | 8 | business flows → slice anchors |
| `step` | 30 | flow steps → capabilities |

## Required edge types

| Type | Count | Needed for |
|---|---|---|
| `calls` | 10 | dependency resolution |
| `reads_from` | **0** | data access (read) |
| `writes_to` | **0** | data access (write) |
| `routes` | **0** | UI/HTTP routing |
| `tested_by` | 8 | legacy test inventory |
| `contains_flow` | 8 | domain → flow |
| `flow_step` | 30 | flow → step |

## All node types

`file` 160, `class` 113, `function` 43, `step` 30, `config` 10, `flow` 8, `domain` 4, `table` 1

## All edge types

`imports` 177, `contains` 156, `exports` 61, `depends_on` 57, `flow_step` 30, `documents` 13, `calls` 10, `tested_by` 8, `contains_flow` 8, `related` 6, `implements` 4, `cross_domain` 4, `inherits` 3, `configures` 1
