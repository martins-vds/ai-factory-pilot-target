> source: eclipse-ee4j/cargotracker@f3beacf78de4f6d34edc4971ac87e38a5c6fe59d source_sha: f3beacf78de4f6d34edc4971ac87e38a5c6fe59d 

# Graph gate: source

- 448 nodes, 1034 edges
- Edges added by harness enrichers: 299

## Required types (profile graph.require)

- node `table`: 7
- node `page`: 23
- node `endpoint`: 4
- edge `reads_from`: 17
- edge `writes_to`: 4
- edge `routes`: 25
- edge `calls`: 203

## Data paths (slice specs data_paths)

- `track-cargo` **src/main/webapp/public/track.xhtml**: `src/main/webapp/public/track.xhtml` →routes `Track` →calls `CargoRepository` ←implements `JpaCargoRepository` →reads_from `Cargo`
- `track-cargo` **src/main/webapp/admin/tracking/track.xhtml**: `src/main/webapp/admin/tracking/track.xhtml` →routes `Track` →calls `BookingServiceFacade` ←implements `DefaultBookingServiceFacade` →calls `CargoRepository` ←implements `JpaCargoRepository` →reads_from `Cargo`

## Entry points reaching data (for review)

- 18 of 27 pages/endpoints
  - no path: endpoint `GET /graph-traversal/shortest-path`
  - no path: endpoint `WS /tracking`
  - no path: page `src/main/webapp/WEB-INF/templates/common/admin.xhtml`
  - no path: page `src/main/webapp/WEB-INF/templates/common/public.xhtml`
  - no path: page `src/main/webapp/admin/about.xhtml`
  - no path: page `src/main/webapp/admin/tracking/map.xhtml`
  - no path: page `src/main/webapp/index.xhtml`
  - no path: page `src/main/webapp/public/about.xhtml`
  - no path: page `src/main/webapp/public/mapFrame.xhtml`

## Gate

- PASS

AFS-RESULT gate=graph side=source verdict=pass failures=0 entry_points=27 reaching_data=18 enriched_edges=299

# Graph check: cargo-tracker

- Commit: `f3beacf78de4f6d34edc4971ac87e38a5c6fe59d` · analyzed 2026-11-03T14:42:56.902Z
- Languages: java, html, xml, css, markdown, json, properties · frameworks: Jakarta EE, JSF, JAX-RS, Maven
- 448 nodes, 1034 edges, 9 layers

## Required node types

| Type | Count | Needed for |
|---|---|---|
| `endpoint` | 4 | entry points for slices (HTTP) |
| `screen` | **0** | UI screens (ledger kind: ui) |
| `page` | 23 | UI pages (alternative to screen) |
| `table` | 7 | data capabilities and data-migration slices |
| `service` | **0** | service boundaries |
| `domain` | 4 | bounded contexts |
| `flow` | 10 | business flows → slice anchors |
| `step` | 32 | flow steps → capabilities |

## Required edge types

| Type | Count | Needed for |
|---|---|---|
| `calls` | 203 | dependency resolution |
| `reads_from` | 17 | data access (read) |
| `writes_to` | 4 | data access (write) |
| `routes` | 25 | UI/HTTP routing |
| `tested_by` | 11 | legacy test inventory |
| `contains_flow` | 10 | domain → flow |
| `flow_step` | 32 | flow → step |

## All node types

`file` 167, `class` 118, `function` 58, `step` 32, `page` 23, `config` 14, `flow` 10, `resource` 8, `table` 7, `endpoint` 4, `domain` 4, `document` 3

## All edge types

`imports` 364, `contains` 209, `calls` 203, `exports` 88, `flow_step` 32, `routes` 25, `related` 19, `reads_from` 17, `implements` 12, `tested_by` 11, `contains_flow` 10, `inherits` 7, `triggers` 7, `defines_schema` 6, `publishes` 5, `configures` 4, `depends_on` 4, `writes_to` 4, `cross_domain` 4, `documents` 3
