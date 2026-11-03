> source: eclipse-ee4j/cargotracker@f3beacf78de4f6d34edc4971ac87e38a5c6fe59d source_sha: f3beacf78de4f6d34edc4971ac87e38a5c6fe59d 

# Graph gate: source

- 1080 nodes, 2137 edges
- Edges added by harness enrichers: 1352

## Required types (profile graph.require)

- node `table`: 7
- node `page`: 23
- node `endpoint`: 4
- edge `reads_from`: 23
- edge `writes_to`: 7
- edge `routes`: 25
- edge `calls`: 630

## Data paths (slice specs data_paths)

- `track-cargo` **src/main/webapp/public/track.xhtml**: `src/main/webapp/public/track.xhtml` →routes `Track` →contains `Track.onTrackById` →calls `CargoRepository.find` ←implements `JpaCargoRepository.find` →reads_from `Cargo`
- `track-cargo` **src/main/webapp/admin/tracking/track.xhtml**: `src/main/webapp/admin/tracking/track.xhtml` →routes `Track` →contains `Track.init` →calls `BookingServiceFacade.listAllTrackingIds` ←implements `DefaultBookingServiceFacade.listAllTrackingIds` →calls `CargoRepository.findAll` ←implements `JpaCargoRepository.findAll` →reads_from `Cargo`

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

AFS-RESULT gate=graph side=source verdict=pass failures=0 entry_points=27 reaching_data=18 enriched_edges=1352

# Graph check: cargo-tracker

- Commit: `f3beacf78de4f6d34edc4971ac87e38a5c6fe59d` · analyzed 2026-11-03T17:29:34.340Z
- Languages: css, csv, html, java, json, markdown, properties, txt, xhtml, xml · frameworks: Jakarta EE, JSF, PrimeFaces, Jersey, Arquillian, JUnit
- 1080 nodes, 2137 edges, 7 layers

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
| `step` | 33 | flow steps → capabilities |

## Required edge types

| Type | Count | Needed for |
|---|---|---|
| `calls` | 630 | dependency resolution |
| `reads_from` | 23 | data access (read) |
| `writes_to` | 7 | data access (write) |
| `routes` | 25 | UI/HTTP routing |
| `tested_by` | 13 | legacy test inventory |
| `contains_flow` | 9 | domain → flow |
| `flow_step` | 33 | flow → step |

## All node types

`method` 571, `file` 167, `class` 119, `function` 118, `step` 33, `page` 23, `config` 14, `flow` 9, `resource` 8, `table` 7, `endpoint` 4, `domain` 4, `document` 3

## All edge types

`contains` 834, `calls` 630, `imports` 364, `exports` 103, `implements` 47, `flow_step` 33, `routes` 25, `reads_from` 23, `tested_by` 13, `contains_flow` 9, `inherits` 7, `writes_to` 7, `triggers` 7, `related` 6, `defines_schema` 6, `depends_on` 5, `configures` 5, `publishes` 5, `documents` 4, `cross_domain` 4
