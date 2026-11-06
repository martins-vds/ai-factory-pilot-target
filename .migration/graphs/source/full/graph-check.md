> source: eclipse-ee4j/cargotracker@f3beacf78de4f6d34edc4971ac87e38a5c6fe59d source_sha: f3beacf78de4f6d34edc4971ac87e38a5c6fe59d 

# Graph gate: source

- 1026 nodes, 2103 edges
- Edges added by harness enrichers: 1353

## Required types (profile graph.require)

- node `table`: 7
- node `page`: 23
- node `endpoint`: 4
- edge `reads_from`: 23
- edge `writes_to`: 7
- edge `routes`: 25
- edge `calls`: 631

## Data paths (slice specs data_paths)

- `handling-registration` **endpoint=POST /handling/reports**: `POST /handling/reports` →routes `HandlingReportService.submitReport` →calls `ApplicationEvents.receivedHandlingEventRegistrationAttempt` ←implements `JmsApplicationEvents.receivedHandlingEventRegistrationAttempt` →publishes `java:app/jms/HandlingEventRegistrationAttemptQueue` →triggers `HandlingEventRegistrationAttemptConsumer.onMessage` →calls `HandlingEventService.registerHandlingEvent` ←implements `DefaultHandlingEventService.registerHandlingEvent` →calls `HandlingEventRepository.store` ←implements `JpaHandlingEventRepository.store` →writes_to `HandlingEvent`
- `track-cargo` **src/main/webapp/public/track.xhtml**: `src/main/webapp/public/track.xhtml` →routes `Track` →contains `Track.onTrackById` →calls `CargoRepository.find` ←implements `JpaCargoRepository.find` →reads_from `Cargo`
- `track-cargo` **src/main/webapp/admin/tracking/track.xhtml**: `src/main/webapp/admin/tracking/track.xhtml` →routes `Track` →contains `Track.init` →calls `BookingServiceFacade.listAllTrackingIds` ←implements `DefaultBookingServiceFacade.listAllTrackingIds` →calls `CargoRepository.findAll` ←implements `JpaCargoRepository.findAll` →reads_from `Cargo`

## Entry points reaching data (for review)

- 19 of 27 pages/endpoints
  - no path: endpoint `GET /graph-traversal/shortest-path`
  - no path: endpoint `WS /tracking`
  - no path: page `src/main/webapp/WEB-INF/templates/common/admin.xhtml`
  - no path: page `src/main/webapp/WEB-INF/templates/common/public.xhtml`
  - no path: page `src/main/webapp/admin/about.xhtml`
  - no path: page `src/main/webapp/index.xhtml`
  - no path: page `src/main/webapp/public/about.xhtml`
  - no path: page `src/main/webapp/public/mapFrame.xhtml`

## Gate

- PASS

AFS-RESULT gate=graph side=source verdict=pass failures=0 entry_points=27 reaching_data=19 enriched_edges=1353

# Graph check: cargo-tracker

- Commit: `f3beacf78de4f6d34edc4971ac87e38a5c6fe59d` · analyzed 2026-11-06T15:23:08.771Z
- Languages: css, html, java, json, markdown, properties, xml · frameworks: Jakarta EE, Maven, JSF, Arquillian
- 1026 nodes, 2103 edges, 9 layers

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
| `step` | 36 | flow steps → capabilities |

## Required edge types

| Type | Count | Needed for |
|---|---|---|
| `calls` | 631 | dependency resolution |
| `reads_from` | 23 | data access (read) |
| `writes_to` | 7 | data access (write) |
| `routes` | 25 | UI/HTTP routing |
| `tested_by` | 25 | legacy test inventory |
| `contains_flow` | 9 | domain → flow |
| `flow_step` | 36 | flow → step |

## All node types

`method` 571, `file` 167, `class` 119, `function` 62, `step` 36, `page` 23, `config` 13, `flow` 9, `resource` 8, `table` 7, `endpoint` 4, `domain` 4, `document` 3

## All edge types

`contains` 785, `calls` 631, `imports` 364, `exports` 99, `implements` 47, `flow_step` 36, `tested_by` 25, `routes` 25, `reads_from` 23, `related` 13, `contains_flow` 9, `inherits` 7, `writes_to` 7, `triggers` 7, `defines_schema` 6, `depends_on` 5, `configures` 5, `publishes` 5, `cross_domain` 3, `documents` 1
