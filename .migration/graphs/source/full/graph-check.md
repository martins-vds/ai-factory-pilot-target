> source: eclipse-ee4j/cargotracker@f3beacf78de4f6d34edc4971ac87e38a5c6fe59d source_sha: f3beacf78de4f6d34edc4971ac87e38a5c6fe59d 

# Graph gate: source

- 465 nodes, 885 edges
- Edges added by harness enrichers: 162

## Required types (profile graph.require)

- node `table`: 7
- node `page`: 23
- node `endpoint`: 4
- edge `reads_from`: 17
- edge `writes_to`: 4
- edge `routes`: 25
- edge `calls`: 47

## Data paths (slice specs data_paths)

- `track-cargo` **src/main/webapp/public/track.xhtml**: `src/main/webapp/public/track.xhtml` →routes `Track` →calls `CargoRepository` ←implements `JpaCargoRepository` →reads_from `Cargo`
- `track-cargo` **src/main/webapp/admin/tracking/track.xhtml**: `src/main/webapp/admin/tracking/track.xhtml` →routes `Track` →calls `BookingServiceFacade` ←implements `DefaultBookingServiceFacade` →calls `LocationRepository` ←implements `JpaLocationRepository` →reads_from `Location`

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

AFS-RESULT gate=graph side=source verdict=pass failures=0 entry_points=27 reaching_data=18 enriched_edges=162

# Graph check: cargo-tracker

- Commit: `f3beacf78de4f6d34edc4971ac87e38a5c6fe59d` · analyzed 2026-11-03T04:43:46.237Z
- Languages: css, html, java, markdown, properties, xhtml, xml · frameworks: Jakarta EE, JUnit, Maven
- 465 nodes, 885 edges, 8 layers

## Required node types

| Type | Count | Needed for |
|---|---|---|
| `endpoint` | 4 | entry points for slices (HTTP) |
| `screen` | **0** | UI screens (ledger kind: ui) |
| `page` | 23 | UI pages (alternative to screen) |
| `table` | 7 | data capabilities and data-migration slices |
| `service` | **0** | service boundaries |
| `domain` | 4 | bounded contexts |
| `flow` | 9 | business flows → slice anchors |
| `step` | 31 | flow steps → capabilities |

## Required edge types

| Type | Count | Needed for |
|---|---|---|
| `calls` | 47 | dependency resolution |
| `reads_from` | 17 | data access (read) |
| `writes_to` | 4 | data access (write) |
| `routes` | 25 | UI/HTTP routing |
| `tested_by` | 8 | legacy test inventory |
| `contains_flow` | 9 | domain → flow |
| `flow_step` | 31 | flow → step |

## All node types

`file` 167, `class` 113, `function` 83, `step` 31, `page` 23, `config` 13, `flow` 9, `resource` 8, `table` 7, `endpoint` 4, `domain` 4, `document` 3

## All edge types

`imports` 364, `contains` 234, `exports` 78, `calls` 47, `flow_step` 31, `routes` 25, `reads_from` 17, `implements` 15, `depends_on` 10, `contains_flow` 9, `tested_by` 8, `related` 8, `inherits` 8, `triggers` 7, `configures` 6, `defines_schema` 6, `publishes` 5, `writes_to` 4, `cross_domain` 3
