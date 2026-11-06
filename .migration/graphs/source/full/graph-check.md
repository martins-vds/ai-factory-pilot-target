> source: eclipse-ee4j/cargotracker@f3beacf78de4f6d34edc4971ac87e38a5c6fe59d source_sha: f3beacf78de4f6d34edc4971ac87e38a5c6fe59d 

# Graph gate: source

- 1009 nodes, 2093 edges
- Edges added by harness enrichers: 1350

## Required types (profile graph.require)

- node `table`: 7
- node `page`: 23
- node `endpoint`: 4
- edge `reads_from`: 23
- edge `writes_to`: 7
- edge `routes`: 25
- edge `calls`: 632

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

AFS-RESULT gate=graph side=source verdict=pass failures=0 entry_points=27 reaching_data=19 enriched_edges=1350

# Graph check: Eclipse Cargo Tracker

- Commit: `f3beacf78de4f6d34edc4971ac87e38a5c6fe59d` · analyzed 2026-11-06T18:56:27.735Z
- Languages: css, csv, html, java, markdown, properties, txt, xhtml, xml · frameworks: Jakarta EE, JUnit
- 1009 nodes, 2093 edges, 8 layers

## Required node types

| Type | Count | Needed for |
|---|---|---|
| `endpoint` | 4 | entry points for slices (HTTP) |
| `screen` | **0** | UI screens (ledger kind: ui) |
| `page` | 23 | UI pages (alternative to screen) |
| `table` | 7 | data capabilities and data-migration slices |
| `service` | **0** | service boundaries |
| `domain` | 1 | bounded contexts |
| `flow` | 1 | business flows → slice anchors |
| `step` | 4 | flow steps → capabilities |

## Required edge types

| Type | Count | Needed for |
|---|---|---|
| `calls` | 632 | dependency resolution |
| `reads_from` | 23 | data access (read) |
| `writes_to` | 7 | data access (write) |
| `routes` | 25 | UI/HTTP routing |
| `tested_by` | 9 | legacy test inventory |
| `contains_flow` | 1 | domain → flow |
| `flow_step` | 4 | flow → step |

## All node types

`method` 571, `file` 167, `class` 119, `function` 88, `page` 23, `config` 13, `resource` 8, `table` 7, `endpoint` 4, `step` 4, `document` 3, `domain` 1, `flow` 1

## All edge types

`contains` 811, `calls` 632, `imports` 364, `exports` 111, `implements` 48, `routes` 25, `reads_from` 23, `depends_on` 17, `tested_by` 9, `related` 8, `inherits` 7, `writes_to` 7, `triggers` 7, `configures` 6, `defines_schema` 6, `publishes` 5, `flow_step` 4, `documents` 2, `contains_flow` 1
