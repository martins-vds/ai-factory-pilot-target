> source: eclipse-ee4j/cargotracker@f3beacf78de4f6d34edc4971ac87e38a5c6fe59d source_sha: f3beacf78de4f6d34edc4971ac87e38a5c6fe59d 

> Enriched in place by the harness (ADR-0020, enrich_graph.py) on top of the Understand Anything build recorded in SNAPSHOT.txt.

# Graph gate: source

- 406 nodes, 680 edges
- Edges added by harness enrichers: 142

## Required types (profile graph.require)

- node `table`: 7
- node `page`: 23
- node `endpoint`: 3
- edge `reads_from`: 17
- edge `writes_to`: 4
- edge `routes`: 22
- edge `calls`: 52

## Data paths (slice specs data_paths)

- `track-cargo` **src/main/webapp/public/track.xhtml**: `src/main/webapp/public/track.xhtml` →routes `Track` →calls `CargoRepository` ←implements `JpaCargoRepository` →reads_from `Cargo`
- `track-cargo` **src/main/webapp/admin/tracking/track.xhtml**: `src/main/webapp/admin/tracking/track.xhtml` →routes `Track` →calls `BookingServiceFacade` ←implements `DefaultBookingServiceFacade` →calls `LocationRepository` ←implements `JpaLocationRepository` →reads_from `Location`

## Entry points reaching data (for review)

- 17 of 26 pages/endpoints
  - no path: endpoint `GET /graph-traversal/shortest-path`
  - no path: page `src/main/webapp/WEB-INF/templates/common/admin.xhtml`
  - no path: page `src/main/webapp/WEB-INF/templates/common/public.xhtml`
  - no path: page `src/main/webapp/admin/about.xhtml`
  - no path: page `src/main/webapp/admin/tracking/map.xhtml`
  - no path: page `src/main/webapp/admin/tracking/mapFrame.xhtml`
  - no path: page `src/main/webapp/index.xhtml`
  - no path: page `src/main/webapp/public/about.xhtml`
  - no path: page `src/main/webapp/public/mapFrame.xhtml`

## Gate

- PASS

AFS-RESULT gate=graph side=source verdict=pass failures=0 entry_points=26 reaching_data=17 enriched_edges=142

# Graph check: Eclipse Cargo Tracker

- Commit: `f3beacf78de4f6d34edc4971ac87e38a5c6fe59d` · analyzed 2026-11-02T18:09:51.319Z
- Languages: markdown, xml, java, html, properties, xhtml, css, csv, txt · frameworks: Jakarta EE, JSF, JAX-RS, Maven
- 406 nodes, 680 edges, 8 layers

## Required node types

| Type | Count | Needed for |
|---|---|---|
| `endpoint` | 3 | entry points for slices (HTTP) |
| `screen` | **0** | UI screens (ledger kind: ui) |
| `page` | 23 | UI pages (alternative to screen) |
| `table` | 7 | data capabilities and data-migration slices |
| `service` | **0** | service boundaries |
| `domain` | 4 | bounded contexts |
| `flow` | 8 | business flows → slice anchors |
| `step` | 30 | flow steps → capabilities |

## Required edge types

| Type | Count | Needed for |
|---|---|---|
| `calls` | 52 | dependency resolution |
| `reads_from` | 17 | data access (read) |
| `writes_to` | 4 | data access (write) |
| `routes` | 22 | UI/HTTP routing |
| `tested_by` | 8 | legacy test inventory |
| `contains_flow` | 8 | domain → flow |
| `flow_step` | 30 | flow → step |

## All node types

`file` 160, `class` 113, `function` 43, `step` 30, `page` 23, `config` 10, `flow` 8, `table` 7, `resource` 5, `domain` 4, `endpoint` 3

## All edge types

`contains` 187, `imports` 177, `exports` 61, `depends_on` 57, `calls` 52, `flow_step` 30, `routes` 22, `reads_from` 17, `documents` 13, `implements` 11, `tested_by` 8, `contains_flow` 8, `inherits` 7, `related` 6, `defines_schema` 6, `triggers` 5, `writes_to` 4, `publishes` 4, `cross_domain` 4, `configures` 1
