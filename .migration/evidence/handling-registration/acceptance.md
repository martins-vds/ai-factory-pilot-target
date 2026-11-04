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

## Verified durable execution evidence

The original cloud-worker run
[41896926094](https://github.com/martins-vds/ai-factory-pilot-target/actions/runs/41896926094)
remains historical: it was cancelled at the 59-minute worker limit and has no completed mutation
result. It is superseded for technical-gate evidence by the separately approved durable workflow run
below; it is not represented as a successful run.

- Workflow: `.github/workflows/afs-acceptance.yml` (ID `407468483`); event `workflow_dispatch`.
- Run: [41924854967, attempt 1](https://github.com/martins-vds/ai-factory-pilot-target/actions/runs/41924854967),
  repository `martins-vds/ai-factory-pilot-target`, source commit
  `7e3d6d5427064c67b951a29ac9f8cfabfa77e3db`; run and acceptance job completed `success` at
  `2026-11-04T23:26:07Z`.
- Artifact: ID `13371474656`,
  `afs-acceptance-7e3d6d5427064c67b951a29ac9f8cfabfa77e3db-41924854967-1`, 34,525 bytes,
  ZIP SHA-256 `1f023eab634c89321869c3aec907c59428222746466010356dfacde3501dd60b`, created
  `2026-11-04T23:26:04Z`, expires `2026-12-04T23:26:04Z`.
- Independent artifact verification: downloaded to gitignored `.migration/runs/`, ZIP digest matched
  the Actions artifact metadata, all 22 entries passed path-safety and CRC checks, and
  `python .migration/harness/tools/afs-acceptance verify .migration/runs/acceptance-41924854967-1/artifact
  --commit 7e3d6d5427064c67b951a29ac9f8cfabfa77e3db --run-id 41924854967 --attempt 1` exited 0 with
  `status=verified`. Run metadata, repository, source commit, attempt, workflow, and artifact were
  independently checked; the verifier matched the pinned profile, source lock, installed harness,
  input tree, gate plan, journals, and raw-log digests.
- All 15 planned steps passed. Graph freshness and both graph gates passed; build and idiom gates
  passed; `pytest -q` reported 321 passed; CRAP was max 19.0 / threshold 30 / over 0 / 132 methods.
- Full-profile mutation completed in the workflow: score `0.869`, threshold `0.8`, killed `1126`,
  survived `169`, skipped `0`, files `61`, workers `4`, base `all`. The genuine survivor report is
  preserved at [`.migration/evidence/mutants/HR-04F.md`](../mutants/HR-04F.md). Its listed locations
  include handling domain, REST, persistence, worker, and shared `Delivery` logic. The report gives
  mutant IDs and source locations, but not mutation operators or patches; a location alone does not
  establish an observable capability defect. Reassessment against the focused domain, repository,
  REST, processing, rollback, concurrency, and 28-case golden tests did not establish a specific
  uncovered capability or justify a new gap ticket.

These are verified workflow executions, not local reruns. The committed
[acceptance result](../acceptance-runs/41924854967-1.json), the
[HR-04F journal](../runs/HR-04F.md), and survivor report preserve the attributable evidence. Raw gate
logs remain under the gitignored `.migration/runs/acceptance-41924854967-1/`.

## Human check and assessment

Issue #123 documents approval of the plan. The human operator explicitly attested: **“I completed
the human flow check and sign off”** for handling-registration at reviewed revision
`7e3d6d5427064c67b951a29ac9f8cfabfa77e3db`. The durable audit-trail record is the
[coordinator comment](https://github.com/martins-vds/ai-factory-pilot-target/pull/184#issuecomment-6645381666),
created `2026-11-04T23:45:44Z`; that creation time is the attestation-record timestamp, not a claimed
execution time. The check was performed by the human operator, not this Auditor. No separate exact
execution time, screenshots, or individual manual-step results were supplied, and none are inferred.

**Verdict: complete.** The independently verified durable technical gates pass, including the
full-profile mutation threshold. All 19 `handling.*` ledger entries were reassessed against the
approved rulings, graph paths, focused tests, source goldens, and surviving-mutant locations; no
capability gap, graph inconsistency, or unowned entry point was established. Together with the human
operator's explicit sign-off above, no unresolved slice acceptance gap remains. This Auditor does
not merge or approve PR #184; the coordinator retains final-head, CI, and merge checks.

The schema-valid Auditor return is
[`.migration/returns/HR-04F.afs-auditor.yaml`](../../returns/HR-04F.afs-auditor.yaml);
the durable next-step handoff is [`.migration/handoffs/HR-04F.md`](../../handoffs/HR-04F.md).
