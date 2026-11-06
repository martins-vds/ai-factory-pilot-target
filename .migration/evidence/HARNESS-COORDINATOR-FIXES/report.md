# HARNESS-COORDINATOR-FIXES bootstrap report

## Current status

The pinned harness upgrade is installed on the proposal branch and was independently verified by the original Bootstrapper. The installer was the parent coordinator; this worker did not run or repeat the installation. PR [#198](https://github.com/martins-vds/ai-factory-pilot-target/pull/198) is based on target `main` at `a284b840e97e06452ca5370b941d22c4c6ae4f2d`, with current verified head `cacfb625f9b9280173614276b51fa85e1797e2b2`. The installed release is `martins-vds/ai-factory-swarm@e51998d716c229930e1e072cdcb05be0a872b4ef`, tree `728ee39572de27bd9ab01999a93d6bec28f0a555`.

Installation and preservation checks pass. The current AFS harness check is blocked by an application test failure described below. This rollout does not establish Slice Coordinator or Program Orchestrator role coverage, and the harness is not installed on pilot `main`.

## Parent installation (installer evidence)

The parent installation record is `.migration/evidence/HARNESS-COORDINATOR-FIXES/parent-installation.md`. It records the parent's unchanged normal bootstrap command, exact clean source pin/tree, existing profile/capabilities and stack pack, `--create-gap-issues`, exit 0, and the parent as installer. The parent used existing authorized access; no credentials were transferred, private source skipped, offline mode used, installed hotpatch applied, graph rebuilt, application file changed, or acceptance rerun.

The parent's own recorded checks were: 77 manifest entries / 388 files / 0 integrity problems; migration validation 94 files / 0 errors; 64 direct source-file comparisons; and its own preservation baseline. Those are attributed to the parent and are not represented as this worker's commands.

## Original Bootstrapper setup and independent verification

- The pinned read-only `.source` checkout matches `.migration/source.lock` at `f3beacf78de4f6d34edc4971ac87e38a5c6fe59d`; it is ignored and not writable.
- This resumed checkout was shallow. After the ordinary `git fetch --unshallow origin`, `python .migration/harness/tools/validate.py .migration` passed: 94 files checked, 0 errors. Ticket input check reported 0 missing paths; `afs-services check` reported `db` healthy; `check_runtime.py` reported Python 3.13.17; RTK is 1.1.0.
- The source release was independently fetched into a clean detached checkout. `HEAD` is `e51998d716c229930e1e072cdcb05be0a872b4ef`, tree `728ee39572de27bd9ab01999a93d6bec28f0a555`.
- Independent `afs-run` verification passed: `.migration/harness/tools/check_installed.py` reported 77 entries / 388 files / 0 problems; an exact-source hash comparison matched 64 installed files to the pinned release with 0 mismatches; migration validation passed (94 files, 0 errors). Raw logs are under `.migration/runs/HARNESS-COORDINATOR-FIXES/`; the append-only committed journal is `.migration/evidence/runs/HARNESS-COORDINATOR-FIXES.md`.
- An independent byte-for-byte comparison checked 780 baseline tracked files outside the expected generated-install and own-journal paths: 0 unexpected changes and 0 missing files. All 40 pre-existing YAML returns are unchanged from `main` at `a284b840e97e06452ca5370b941d22c4c6ae4f2d`. `.migration/profile.yaml`, `.migration/source.lock`, graphs, slices, ledgers, costs, acceptance evidence, and application files are preserved. Capability semantics are unchanged; only the ordinary `checked_at` timestamp refreshed.
- Before updating these records, the original worker's report, handoff and return matched their committed state at `7002c5e`. The current run journal retains that commit's exact byte prefix; parent and original-worker runs are appended, not substituted.

## Original access blocker (historical)

The original Bootstrapper's one normal install attempt stopped fetching pinned dependency `martins-vds/code-migration-hackathon@4de661a9a830aaef70ff55e879c0cc540599cad8` with Git exit 128. This failure and handoff remain in the journal and prior handoff section as history. After that ownership handoff, the parent completed the same normal bootstrap with existing authorized access. This original worker neither repeated the inaccessible installation nor used a skip or bypass.

## Current proposal check

The `Copilot Setup Steps` PR run [42152379388](https://github.com/martins-vds/ai-factory-pilot-target/actions/runs/42152379388) passed at current head `cacfb625f9b9280173614276b51fa85e1797e2b2`.

The current AFS harness check [42152379401](https://github.com/martins-vds/ai-factory-pilot-target/actions/runs/42152379401), also at that exact head, failed its gates job. Its tests reported 320 passed and one failed: `tests/handling/test_registration_processing.py::test_equal_completion_and_registration_times_use_event_id_for_delivery` at line 386, asserting `cargo.delivery.last_event_id == unload_event.pk` (actual 810, expected 821). The CRAP test command also stopped on that same failed test. The identical test failed on earlier head `7002c5e` in run `42151830272`. Its cause is not established; it is not labeled flaky or attributed to the harness. Application and test bytes match `main`, and none were changed or rerun locally for this rollout.

## Next action

Keep PR #198 for the parent's independent exact-head review and resolution of the reported current check. Do not change application/tests, self-merge, or claim coordinator-role coverage. The historical null-PR returns, accepted evidence and human attestation remain historical; no acceptance or human-flow rerun was performed.

See `.migration/handoffs/HARNESS-COORDINATOR-FIXES.md` for the chronological ownership handoff and current continuation status.
