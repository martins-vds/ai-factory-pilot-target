# Graph check: cargo-tracker

- Commit: `a8cdf52effc852af7a9218b40bedb98b8451d4ae` · analyzed 2026-10-31T16:27:03.477604Z
- Languages: css, csv, html, java, json, markdown, properties, txt, xhtml, xml · frameworks: Jakarta EE, JPA, JSF, JAX-RS, JMS, Maven, Arquillian
- 437 nodes, 775 edges, 9 layers

## Required node types

| Type | Count | Needed for |
|---|---|---|
| `endpoint` | **0** | entry points for slices (HTTP) |
| `screen` | **0** | UI screens (ledger kind: ui) |
| `page` | **0** | UI pages (alternative to screen) |
| `table` | 1 | data capabilities and data-migration slices |
| `service` | **0** | service boundaries |
| `domain` | 4 | bounded contexts |
| `flow` | 11 | business flows → slice anchors |
| `step` | 38 | flow steps → capabilities |

## Required edge types

| Type | Count | Needed for |
|---|---|---|
| `calls` | 2 | dependency resolution |
| `reads_from` | **0** | data access (read) |
| `writes_to` | **0** | data access (write) |
| `routes` | **0** | UI/HTTP routing |
| `tested_by` | 13 | legacy test inventory |
| `contains_flow` | 11 | domain → flow |
| `flow_step` | 38 | flow → step |

## All node types

`file` 167, `class` 113, `function` 87, `step` 38, `config` 13, `flow` 11, `domain` 4, `document` 3, `table` 1

## All edge types

`imports` 364, `contains` 200, `exports` 96, `flow_step` 38, `related` 15, `tested_by` 13, `implements` 12, `contains_flow` 11, `configures` 8, `depends_on` 7, `inherits` 4, `cross_domain` 4, `calls` 2, `documents` 1
