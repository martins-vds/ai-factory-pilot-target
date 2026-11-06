# HARNESS-COORDINATOR-FIXES bootstrap report

## Status

Blocked before installation. The existing draft setup proposal is [PR #198](https://github.com/martins-vds/ai-factory-pilot-target/pull/198), based on target `main` at `a284b840e97e06452ca5370b941d22c4c6ae4f2d`. The installed manifest still identifies harness `ee54dfdda8d86b324fa2818aa82c6b5b6456dbd1`. This work does not establish Slice Coordinator or Program Orchestrator coverage.

## Setup and pinned-source verification

- `.source` is read-only and ignored; its commit matches `.migration/source.lock` at `f3beacf78de4f6d34edc4971ac87e38a5c6fe59d`.
- Initial migration validation exposed the shallow-history dependency for historical returns. After the ordinary `git fetch --unshallow origin`, `python .migration/harness/tools/validate.py .migration` passed: 92 files checked, 0 errors.
- `check_inputs.py` reported 0 named paths and 0 missing. `afs-services check` reported `db` healthy; `check_runtime.py` reported Python 3.13.17; RTK is 1.1.0.
- The `afs-run` setup probe exited 0. Its journal is `.migration/evidence/runs/HARNESS-COORDINATOR-FIXES.md`; raw log is `.migration/runs/HARNESS-COORDINATOR-FIXES/20261106T023439496060Z-setup-probe.log`.
- The exact source commit `e51998d716c229930e1e072cdcb05be0a872b4ef` was fetched into a clean detached worktree. Its tree is `728ee39572de27bd9ab01999a93d6bec28f0a555`, and the required bootstrap script and stack pack are present.
- Source postmerge Actions run [42150726578](https://github.com/martins-vds/ai-factory-swarm/actions/runs/42150726578) completed successfully on that exact source commit; both jobs passed. The source CI log reports 287 tests passing. These are source-repository results only.

## Baseline and preservation

The existing capability file contains 15 entries: 14 `met`, 0 `gap`, 0 `waived`, and 1 `not-applicable`. This count was independently read from the current file, not copied from a previous return. A pre-bootstrap hash inventory covered 187 protected migration-state files, including `source.lock`, profile, capabilities, ledgers, slices, graphs, returns, evidence, costs, and installed manifest. The failed bootstrap published no installation; those protected files remained unchanged. The target tracks 129 files under `src`, `tests`, and `templates`; none were modified.

## Normal bootstrap attempt

Exactly one normal bootstrap attempt used the pinned release's `tools/bootstrap.py`, the existing `.migration/profile.yaml` and `.migration/capabilities.yaml`, and the pinned `stacks/java-to-django.json`, with `--create-gap-issues`. Neither `--skip-private-sources` nor `--offline` was used.

The bootstrap exited 1 while fetching `https://github.com/martins-vds/code-migration-hackathon` at commit `4de661a9a830aaef70ff55e879c0cc540599cad8`. Its traceback reports that the child `git fetch -q --depth 1 ...` exited 128 with `CalledProcessError`. The bootstrap wrapper captured but did not print the child's stderr, so no more specific diagnostic is claimed. No second access attempt was made. No generated install, parity, installed-integrity, or post-install graph outcome is claimed.

## Next action

Parent to provide the already-authorized normal-bootstrap assistance for the exact pinned dependency without transferring credentials. The same original Bootstrapper must resume on PR #198, rerun setup checks, execute the pinned normal bootstrap, and independently verify the installation and protected-input preservation. Keep PR #198 available for independent exact-head and current-CI review; do not self-merge.

See `.migration/handoffs/HARNESS-COORDINATOR-FIXES.md` for the precise failure and continuation instructions.
