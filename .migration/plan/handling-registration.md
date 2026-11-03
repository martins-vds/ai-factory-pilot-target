# Handling-registration slice plan

**Status:** Draft for human approval; no tickets are published
**Slice epic:** `martins-vds/ai-factory-pilot-target#113`
**Decision map:** `martins-vds/ai-factory-pilot-target#3`
**Anchor:** `POST /rest/handling/reports` → accepted attempt → registered event and re-derived cargo delivery

## Planning basis

- The 19 `handling.*.yaml` capabilities are characterized: 11 at tier A and 8 at tier B. The 28 committed golden records and the tier-B source tests are the differential and behavioral baselines.
- ADR-0001 sets the inward-only `interfaces → application → domain ← infrastructure` layers per bounded context. ADR-0003 requires source JPA table/column mappings to remain compatible.
- ADR-0004 and rulings #87, #94, and #95 keep asynchronous acceptance, replace JMS with PostgreSQL attempts and a worker, require at-least-once/idempotent processing without expiry, record permanent rejections, retry temporary failures, and retire notification queues in favor of log lines. Ruling #88 keeps the REST path and JSON contract, with `204` on acceptance, `400` field errors, and UTC `completionTime`.
- `DefaultCargoInspectionService::inspectCargo` is the handling hot spot (CRAP 20). Its design ticket precedes implementation; the target reuses Track Cargo's migrated `Delivery` calculations rather than reimplementing them.
- `graph_gate.py --side source` passes for the committed source graph: 27 entry points, zero failures. The run is recorded in `.migration/evidence/runs/HR-04.md`.

## Proposed tickets

The keys below are planning labels, not published tracker IDs. Sizes fit one fresh session within the profile budget. Files and packages listed under a ticket are exclusively owned by it; no two tickets edit the same path.

### HR-04A — Design cargo inspection re-derivation

- **Size:** S
- **Role:** `afs-specialist-migrator`, `specialty: messaging`
- **Blocked by:** none
- **Files:** `.migration/design/handling-registration-inspection.md`
- **Scope:** Write a decision table and test inventory for missing cargo, history loading/order, `Delivery` re-derivation and persistence, and misdirected/destination-unload outcomes. Specify reuse of the existing Track Cargo `Delivery` implementation and a decomposition that keeps changed methods at or below the profile CRAP limit of 30. No production code.
- **Acceptance:** Design is directly usable as the test-first checklist for HR-04D.
- **Capabilities:** design prerequisite for `handling.cargo-inspection`, `handling.misdirected-queue`, and `handling.delivered-queue`; these capabilities are implemented or retired in HR-04D.

### HR-04B — Add PostgreSQL registration attempts

- **Size:** M
- **Role:** `afs-specialist-migrator`, `specialty: messaging`
- **Blocked by:** none
- **Files:** `src/cargotracker/handling/domain/registration_attempt.py`, `src/cargotracker/handling/domain/repository.py`, `src/cargotracker/handling/infrastructure/models.py`, `src/cargotracker/handling/infrastructure/attempt_submission_repository.py`, `src/cargotracker/handling/application/accept_registration.py`, `src/cargotracker/handling/models.py`, `src/cargotracker/handling/migrations/0002_registration_attempt.py`, `tests/handling/test_registration_attempt_repository.py`
- **Scope:** Add the durable attempts table and inward-facing submission API. Persist accepted attempts before the REST request returns; do not carry over the source TTL. The repository contract must support the worker's later claim and terminal-state processing without coupling the domain to Django.
- **Tests:** PostgreSQL repository/migration tests; tests exercise persisted accepted attempts, including the absence of an expiry.
- **Acceptance:** Schema and submission boundary are ready for the REST and worker tickets. No broker or worker loop in this ticket.
- **Capabilities:** `handling.registration-attempt-queue` → **replaced** (#87, #94).

### HR-04C — Implement the handling-report REST front door

- **Size:** M
- **Role:** `afs-migrator`
- **Blocked by:** HR-04B
- **Files:** `src/cargotracker/handling/interfaces/rest.py`, `src/cargotracker/handling/interfaces/urls.py`, `src/cargotracker/urls.py`, `tests/handling/interfaces/test_registration_reports.py`
- **Scope:** Implement `POST /rest/handling/reports` as a plain Django JSON view using the HR-04B submission API. Preserve the ruled JSON field names and validation bounds; return `204` for acceptance and `400` with field errors for malformed reports. Interpret `completionTime` in UTC. Reference checks remain in the worker; do not add a report-status API or rejection UI.
- **Tests:** View tests for accepted payloads, required/length/type field errors, UTC parsing, and insertion of an accepted attempt.
- **Capabilities:** `handling.rest-report-contract` → **migrated** (#88).

### HR-04D — Process attempts and inspect cargo

- **Size:** M
- **Role:** `afs-specialist-migrator`, `specialty: messaging`
- **Blocked by:** HR-04A, HR-04B
- **Files:** `src/cargotracker/handling/application/process_registration_attempt.py`, `src/cargotracker/handling/infrastructure/attempt_processing_repository.py`, `src/cargotracker/handling/management/commands/process_handling_attempts.py`, `compose.yaml`, `tests/handling/test_registration_processing.py`
- **Scope:** Implement the processing step and its `worker` Compose service. Claim rows safely for at-least-once processing; in one transaction, apply factory/reference rules, register and store the event, re-derive and store cargo delivery using the existing `Delivery` logic, and mark the attempt `registered`. Mark permanent failures `rejected` with a reason and message; retry temporary failures indefinitely with backoff and log after about 15 minutes. Keep inspection's misdirected and delivered outcomes as log lines. The Django management command runs the worker; tests invoke the processing step directly.
- **Tests:** Direct processing-step tests against PostgreSQL for idempotence, concurrent-safe claiming, registration/inspection atomicity, unknown-reference rejection, and temporary-failure retry.
- **Services:** Add `worker` to `compose.yaml`. CI's `services.test` remains `[db]`: processing tests call the step directly and need PostgreSQL, not a separately running worker or broker.
- **Capabilities:**
  - `handling.registration-flow` → **replaced** (#87, #94); `handling.registration-attempt-consumer` → **replaced** (#87, #95); `handling.cargo-handled-queue` → **replaced** (#87).
  - `handling.registration-service`, `handling.registration-factory-rules`, `handling.event-aggregate`, `handling.event-table`, `handling.history-ordering`, `handling.cargo-table`, `handling.leg-table`, `handling.location-table`, `handling.voyage-table`, `handling.carrier-movement-table`, and `handling.cargo-inspection` → **migrated**.
  - `handling.rejected-attempts-queue` → **dropped** (#95); `handling.misdirected-queue` and `handling.delivered-queue` → **dropped** (#87), with their outcome logs retained.

### HR-04E — Differentially replay the handling goldens

- **Size:** M
- **Role:** `afs-verifier`
- **Blocked by:** HR-04C, HR-04D
- **Files:** `tests/differential/test_handling_registration.py`
- **Scope:** Replay every committed golden case, preserving field-level comparison and date normalization. Assert `204` acceptance and the characterized persisted event/delivery results. Assert ruled contract changes explicitly: malformed fields return `400`; unknown references are accepted at the REST door then recorded as rejected; no one-second expiry; inspection updates share the registration transaction. Do not blanket-ignore differences.
- **Acceptance:** One differential test per golden record, including malformed reports, unknown references, multiple completion-time orderings, and seeded cargo inspection outcomes. Report every mismatch.
- **Capabilities:** Verification evidence for all 19 handling-registration capabilities; no separate capability ownership.

### HR-04F — Accept the handling-registration slice

- **Size:** M
- **Role:** `afs-auditor`
- **Blocked by:** HR-04E
- **Files:** `.migration/evidence/handling-registration/acceptance.md`, `.migration/returns/HR-04F.afs-auditor.yaml`
- **Scope:** Independently re-prove coverage of all 19 ledger entries, inspect the approved design and target graph paths, and run slice acceptance gates through `afs-run`. Verify roles, file ownership, database-backed tests, worker service configuration, and differential evidence.
- **Acceptance:** Gate 7 has no unowned capability; all required acceptance gates pass with committed evidence.
- **Capabilities:** Slice-level audit of all 19 capabilities.

## Dependencies and parallelism

Files remain disjoint across every pair of tickets. Dispatch these groups, with the stated blockers:

1. **Parallel:** HR-04A and HR-04B (design artifact vs. attempt persistence files).
2. After both complete, **parallel:** HR-04C and HR-04D (REST adapter vs. worker/processing files).
3. HR-04E follows both REST and processing; HR-04F follows the verifier.

This uses at most two of the profile's four parallel workers. Do not run HR-04C before the HR-04B submission API exists, or HR-04D before the design and attempt schema are accepted.

## Capability-to-ticket coverage

The following are planned end states, not claims that target implementation is already complete. Every replaced or dropped mechanism cites its ruling.

| Ledger capability | Ticket | Planned end state |
|---|---|---|
| `handling.cargo-handled-queue` | HR-04D | **replaced** — single worker transaction (#87) |
| `handling.cargo-inspection` | HR-04D | **migrated** — reuse `Delivery`; transactional re-derivation |
| `handling.cargo-table` | HR-04D | **migrated** — reuse existing cargo persistence |
| `handling.carrier-movement-table` | HR-04D | **migrated** — reuse existing voyage schedule mapping |
| `handling.delivered-queue` | HR-04D | **dropped** — outcome is a log line (#87) |
| `handling.event-aggregate` | HR-04D | **migrated** — preserve event invariants |
| `handling.event-table` | HR-04D | **migrated** — persist and query registered events |
| `handling.history-ordering` | HR-04D | **migrated** — completion-time ordering |
| `handling.leg-table` | HR-04D | **migrated** — reuse existing itinerary persistence |
| `handling.location-table` | HR-04D | **migrated** — reuse location lookup; worker checks references |
| `handling.misdirected-queue` | HR-04D | **dropped** — outcome is a log line (#87) |
| `handling.registration-attempt-consumer` | HR-04D | **replaced** — PostgreSQL worker (#87, #95) |
| `handling.registration-attempt-queue` | HR-04B | **replaced** — durable PostgreSQL attempts (#87, #94) |
| `handling.registration-factory-rules` | HR-04D | **migrated** — worker records permanent reference rejections (#95) |
| `handling.registration-flow` | HR-04D | **replaced** — PostgreSQL-backed async flow and atomic inspection (#87, #94) |
| `handling.registration-service` | HR-04D | **migrated** — register and persist the event |
| `handling.rejected-attempts-queue` | HR-04D | **dropped** — never-fed queue retired; rejection stored on the attempt (#95) |
| `handling.rest-report-contract` | HR-04C | **migrated** — ruled REST path, response, field errors, and UTC time (#88) |
| `handling.voyage-table` | HR-04D | **migrated** — reuse voyage lookup and worker-side reference checks |

## Slice spec and questions

The source anchor `endpoint=POST /handling/reports` must reach `HandlingEvent` through the source registration-attempt queue, consumer, registration service, and persistence. The target anchors are `endpoint=POST /rest/handling/reports` and the worker command `command=process_handling_attempts`; both must reach data. The worker command is also the `worker` service command. This slice adds no other target entry point.

**Open questions for the Program Orchestrator:**

- Confirm whether the slice specialist should choose the hand-rolled worker loop or Procrastinate; ADR-0004 permits either but does not choose.
- Confirm the exact permanent-rejection reason-code/message vocabulary for unknown references and invalid attempts; #95 requires a reason code but does not enumerate it.
- Confirm the retry backoff schedule and the operational meaning of the approximately-15-minute error log; ADR-0004 specifies indefinite retry but not the exact schedule.

## Planner return contract

```yaml
plan: .migration/plan/handling-registration.md
slices:
  - name: Handling registration
    anchor: POST /rest/handling/reports → accepted attempt → registered event and re-derived cargo delivery
    tickets: 6
    blocked_by: []
design_tickets:
  - HR-04A — Design cargo inspection re-derivation
data_slices:
  - HR-04B — PostgreSQL registration attempts
  - HR-04D — Handling-event and cargo inspection persistence
unmapped_capabilities: []
open_questions:
  - Confirm worker loop vs. Procrastinate.
  - Define permanent-rejection reason codes and messages.
  - Define the retry backoff schedule and approximately-15-minute error-log behavior.
```
