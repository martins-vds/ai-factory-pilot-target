> target_commit: c304b7efac2a78e06530b79b36faeabc6689e5eb tree.src: f6a76dfa27db13383bd1a6559885b360fe52e12e tree.templates: 6897757dbfdb8f98f8776e20891397d241892c0b 

# Graph gate: target

- 216 nodes, 491 edges
- Edges added by harness enrichers: 166

## Required types (profile graph.require)

- node `table`: 5
- node `endpoint`: 2
- edge `reads_from`: 8
- edge `writes_to`: 5
- edge `routes`: 5
- edge `calls`: 149

## Data paths (slice specs data_paths)

- `track-cargo` **endpoint=/**: `/` →routes `compose_tracking_view` →calls `DjangoCargoRepository` →reads_from `cargo`

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

AFS-RESULT gate=graph side=target verdict=pass failures=0 entry_points=6 reaching_data=2 enriched_edges=166

# Graph check: cargotracker

- Commit: `c304b7efac2a78e06530b79b36faeabc6689e5eb` · analyzed 2026-11-03T16:52:35.885Z
- Languages: html, markdown, python · frameworks: Django
- 216 nodes, 491 edges, 7 layers

## Required node types

| Type | Count | Needed for |
|---|---|---|
| `endpoint` | 2 | entry points for slices (HTTP) |
| `screen` | **0** | UI screens (ledger kind: ui) |
| `page` | 4 | UI pages (alternative to screen) |
| `table` | 5 | data capabilities and data-migration slices |
| `service` | **0** | service boundaries |
| `domain` | 4 | bounded contexts |
| `flow` | 8 | business flows → slice anchors |
| `step` | 31 | flow steps → capabilities |

## Required edge types

| Type | Count | Needed for |
|---|---|---|
| `calls` | 149 | dependency resolution |
| `reads_from` | 8 | data access (read) |
| `writes_to` | 5 | data access (write) |
| `routes` | 5 | UI/HTTP routing |
| `tested_by` | **0** | legacy test inventory |
| `contains_flow` | 8 | domain → flow |
| `flow_step` | 31 | flow → step |

## All node types

`file` 90, `class` 48, `step` 31, `function` 22, `flow` 8, `table` 5, `page` 4, `domain` 4, `endpoint` 2, `document` 1, `command` 1

## All edge types

`calls` 149, `imports` 136, `contains` 65, `exports` 56, `flow_step` 31, `reads_from` 8, `contains_flow` 8, `depends_on` 7, `cross_domain` 6, `defines_schema` 5, `routes` 5, `writes_to` 5, `implements` 4, `configures` 3, `inherits` 2, `documents` 1
