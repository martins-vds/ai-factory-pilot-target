# Handling-registration slice — acceptance evidence

- Ticket: HR-04F (#132) · Epic: #113 · Audited baseline: `5cace249987e3ddd4ce3345a845168ca545bab55`
- Date: 2026-11-04 UTC · Role: `afs-auditor`
- Scope: the 19 `handling.*` ledger entries only. This is an independent audit, not a whole-project acceptance.

## Graph refresh and paths

`check_graph_fresh.py --require source,target` passed. The source snapshot matches pinned
`eclipse-ee4j/cargotracker@f3beacf78de4f6d34edc4971ac87e38a5c6fe59d`. The target snapshot's source and
template tree identities match the audited checkout; its recorded target commit predates the merge
commit but the fresh tree check passed.

Both required flow gates were rerun through `afs-run`:

- Source: pass, 0 failures; 27 entry points, 18 reaching data. Current directed path:
  `endpoint=POST /handling/reports` → `HandlingReportService.submitReport` → `ApplicationEvents`
  → `JmsApplicationEvents` → registration-attempt queue → consumer → registration service
  → `JpaHandlingEventRepository.store` → `HandlingEvent`.
- Target: pass, 0 failures; 7 entry points, 3 reaching data; 5 owned and 0 unowned. The REST anchor
  reaches `DjangoAttemptSubmissionRepository.submit` → `handling_registration_attempt`; the worker
  command reaches `DjangoCargoRepository.upsert` → `cargo`. The processing/event/delivery continuation
  is independently exercised by PostgreSQL-backed tests below.

The checked-in source `graph-check.md` was generated before the handling slice was added and lists only
Track Cargo data paths. A fresh gate over the current slice specification and a direct resolution against
the current source graph both confirmed the handling path above; this is stale summary text, not a live
graph-path failure. No target graph alias or unowned entry point was found.

## Approved design, roles, and ownership

The plan's local header still says “Draft,” but issue #123 contains the human approval comment and
resolutions for all three planning questions. The approved plan assigns the design ticket to
`afs-specialist-migrator` (messaging), PostgreSQL attempts and worker processing to the messaging
specialist, REST to `afs-migrator`, differential replay to `afs-verifier`, and acceptance to
`afs-auditor`. Its ticket-owned paths are disjoint: HR-04A design; HR-04B attempt model/repository/
migration/tests; HR-04C REST/URLs/tests; HR-04D processing/worker/Compose/tests; HR-04E differential
test. The HR-04A–E returns corroborate these roles and the respective implementation/verifier evidence.
The existing HR-04E verifier return remains attributed to issue #176 / PR #177 and was not changed.

The worker is configured in `compose.yaml` as `python manage.py process_handling_attempts`, waits for
healthy PostgreSQL, and receives poll/backoff settings. The approved plan intentionally keeps CI's
`services.test: [db]`: tests call the processing step directly rather than running a second worker or
broker. `afs-services check` reported the configured `db` service healthy.

## Top-down and bottom-up findings

The REST view validates the ruled JSON fields, accepts valid reports with an empty `204` response and no
`Content-Type`, and returns `400` field errors for malformed reports. It persists an accepted attempt
before returning; it does not synchronously register an event or change cargo delivery. The worker claims
attempts with PostgreSQL locking, validates references, stores the event, reloads full history, derives
delivery through the existing `Delivery` domain logic, persists cargo, and marks the attempt registered
in one transaction. Permanent reference failures are recorded with reasons; temporary processing failures
retry indefinitely with backoff. Misdirected/delivered outcomes are logs, not queues.

The approved decisions are represented and exercised: #12 hides status/history for unknown cargo;
#13 uses last-known location for IN_PORT; #17 hides ETA after claim; #87 preserves asynchronous acceptance,
PostgreSQL-backed at-least-once processing and transactional inspection; #88 preserves the REST path and
field contract with approved 204/400 and UTC behavior; #94 removes the one-second expiry; #95 records
permanent rejections while retiring the never-fed rejection queue; #136 orders completion-time ties by
acceptance/registration time, then event ID; #171 preserves full UTC completion and registration instants
across reloads. Existing date-only rows are migrated to UTC midnight; missing sub-day precision is not
fabricated. `test_migration.py` and repository round-trip tests exercise these timestamp decisions.

The 28 source golden files remain unchanged. The full current test run passed all 321 tests, including all
28 `test_each_handling_registration_golden_matches_target` cases; the test asserts accepted responses have
no `Content-Type` and compares persisted event/delivery observations. The older
`.migration/evidence/handling-registration/differential/report.md` still records 13 pre-fix differences
(including `text/html` and noon-to-midnight). It is stale relative to the current tests and the later
`.migration/evidence/HR-04E-verification.md`; neither inherited report was edited. This audit relies on
the fresh run below, not the earlier pass claim.

## Capability coverage (gate 7)

Each current ledger status matches the approved plan. The dropped/replaced mechanisms are approved
divergences with their ruling citations; no ledger status was changed by this Auditor.

| Ledger entry | Status | Target counterpart | Focused evidence |
|---|---|---|---|
| `handling.cargo-handled-queue` | replaced (#87) | `process_registration_attempt` | `tests/handling/test_registration_processing.py::test_processing_registers_attempt_once_and_rederives_cargo_delivery` |
| `handling.cargo-inspection` | migrated | `Delivery.derived_from`, `DjangoCargoRepository.upsert` | `test_processing_registers_attempt_once_and_rederives_cargo_delivery`; `test_misdirected_and_delivered_outcomes_are_logged_independently` |
| `handling.cargo-table` | migrated | `CargoRecord`, `DjangoCargoRepository.upsert` | `test_processing_registers_attempt_once_and_rederives_cargo_delivery` |
| `handling.carrier-movement-table` | migrated | `VoyageRecord`, `LegRecord` | `tests/differential/test_handling_registration.py::test_each_handling_registration_golden_matches_target` |
| `handling.delivered-queue` | dropped (#87) | independent delivered log from derived delivery | `tests/handling/test_registration_processing.py::test_misdirected_and_delivered_outcomes_are_logged_independently` |
| `handling.event-aggregate` | migrated | `HandlingEvent` | `tests/handling/test_domain.py::test_handling_event_types_match_source_voyage_rules`; `test_unknown_references_reject_attempt_without_storing_event` |
| `handling.event-table` | migrated | `HandlingEventRecord`, `DjangoHandlingEventRepository` | `tests/handling/test_repository.py::test_repository_preserves_aware_completion_and_registration_instants`; `tests/handling/test_migration.py::test_handling_event_timestamp_migration_preserves_legacy_dates_at_utc_midnight` |
| `handling.history-ordering` | migrated | `HandlingHistory` | `tests/handling/test_domain.py::test_handling_history_breaks_completion_time_ties_by_registration_time_then_id`; repository ordering test |
| `handling.leg-table` | migrated | `LegRecord`, cargo repository | processing/delivery re-derivation test; golden replay |
| `handling.location-table` | migrated | `LocationRecord`, `DjangoLocationRepository.find` | `tests/handling/test_registration_processing.py::test_unknown_references_reject_attempt_without_storing_event` |
| `handling.misdirected-queue` | dropped (#87) | misdirected outcome log | `tests/handling/test_registration_processing.py::test_misdirected_outcome_is_logged` |
| `handling.registration-attempt-consumer` | replaced (#87, #95) | `process_handling_attempts` management command | REST-to-event/delivery integration test; worker command tests |
| `handling.registration-attempt-queue` | replaced (#87, #94) | `DjangoAttemptSubmissionRepository` / PostgreSQL attempts | `tests/handling/test_registration_attempt_repository.py::test_accept_registration_persists_attempt_without_expiry`; concurrent lock test |
| `handling.registration-factory-rules` | migrated (#95) | `_resolve_event`, `_resolve_location`, `_resolve_voyage` | unknown-reference rejection test; golden replay |
| `handling.registration-flow` | replaced (#87, #94) | `process_registration_attempt` | `test_registration_and_inspection_updates_roll_back_together`; concurrent processing test |
| `handling.registration-service` | migrated | event resolution and `DjangoHandlingEventRepository` | REST-to-event/delivery integration test; golden replay |
| `handling.rejected-attempts-queue` | dropped (#95) | rejection reason persisted on attempt; no queue | `tests/handling/test_registration_attempt_repository.py::test_repository_marks_rejected_attempt_with_its_reason`; unknown-reference rejection test |
| `handling.rest-report-contract` | migrated (#88) | REST view/form/URL composition | `tests/handling/interfaces/test_registration_reports.py`; 28-case differential replay |
| `handling.voyage-table` | migrated | `VoyageRecord`, `DjangoVoyageRepository.find` | unknown-reference rejection test; golden replay |

Five gap classes:

- **Missing:** none; every ledger entry has a target counterpart or an approved dropped/replaced fate.
- **Misplaced:** none found; REST, application/domain logic, and persistence follow the approved inward
  dependency direction.
- **Broken flow:** none; current graph paths and the real-database REST-to-attempt-to-event/delivery test
  connect the slice end to end.
- **Integration:** none; the source JMS queue mechanisms are replaced per approvals by the PostgreSQL
  attempt table and worker, with no broker required.
- **Untested:** none; current full suite and the targeted database-backed assertions pass.

## Historical gates and interrupted full mutation

The successful graph, build, idiom, behavior, CRAP, and changed-mutation results below were produced
in the preceding audit session on 2026-11-04. They are historical evidence, not fresh reruns in this
bounded recovery; their original timestamps, exits, results, and log hashes remain unchanged in
`.migration/evidence/runs/HR-04F.md`.

| Gate | Command(s) | Result |
|---|---|---|
| Graph freshness | `check_graph_fresh.py --require source,target` | pass |
| Graph source / target | `graph_gate.py --side source`; `graph_gate.py --side target --require-graph` | pass / pass |
| Build | `python -m compileall -q src`; `python manage.py check` | pass / pass |
| Idiom | `ruff check`; `ruff format --check` | pass / pass |
| Behavior/regression | `pytest -q` | 321 passed |
| CRAP | profile coverage, lizard, and `crap.py --max 30` commands | pass; max 19.0, threshold 30, 132 methods |
| Changed mutation | `afs-mutation --changed-since origin/main` | exit 0; `n/a: no mutable code changed` |
| Full mutation | `afs-mutation --all` | Interrupted externally; no completed result |

The coordinator confirmed that Actions run
[41896926094](https://github.com/martins-vds/ai-factory-pilot-target/actions/runs/41896926094)
ended `CANCELLED` after about 60 minutes. Its logs report `COPILOT_AGENT_TIMEOUT_MIN: 59` and
cleanup killing the `mutmut` and Python processes. The previous PR session has an authoritative
`copilot_work_finished` event at 2026-11-04 20:26:59Z on head
`ebe2d6c2400ea5d474ef072ca5264a8b8d8b63f2`; that event does not establish a mutation result.
No completed, attributable HR-04F full-mutation output survived: this checkout has no full-mutation
result in the journal and no HR-04F mutant report. The later setup-probe artifact is not mutation
evidence. No score, survivor count, or partial-shard result is inferred.

This is an infrastructure-interrupted gate, not evidence of an application or capability defect.
The existing test and capability evidence above remains as recorded, but full-profile mutation
acceptance remains unresolved.

## Human check and assessment

Issue #123 documents approval of the plan. The authorization to run this audit is not treated as an
acceptance sign-off. No separate human flow sign-off is evidenced here; no such check is claimed.

**Verdict: gaps-remain.** Full-profile mutation evidence is unresolved after the external worker
cancellation, and the required human flow sign-off is not evidenced. No capability-specific gap or
application defect is established by the interruption; the existing audit checked all 19
`handling.*` ledger entries and found no graph inconsistency or unowned entry point. Leave the PR
unmerged until the coordinator supplies a durable full-mutation result and the human flow sign-off is
recorded.

The schema-valid Auditor return is
[`.migration/returns/HR-04F.afs-auditor.yaml`](../../returns/HR-04F.afs-auditor.yaml);
the durable next-step handoff is [`.migration/handoffs/HR-04F.md`](../../handoffs/HR-04F.md).
