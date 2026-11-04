# HR-04F-DURABLE — pinned acceptance harness rollout

- Issue: [martins-vds/ai-factory-pilot-target#185](https://github.com/martins-vds/ai-factory-pilot-target/issues/185)
- Acceptance issue: [martins-vds/ai-factory-pilot-target#132](https://github.com/martins-vds/ai-factory-pilot-target/issues/132)
- Setup PR: [#186](https://github.com/martins-vds/ai-factory-pilot-target/pull/186)
- Requested pilot main: `5cace249987e3ddd4ce3345a845168ca545bab55`
- Requested harness pin: `344241e92256a6048183f99063ca297fb96780de`
- Outcome: **blocked** — no clean checkout of the requested harness pin or its normal bootstrap/stack pack is available in this worker.

## Evidence

The committed journal at `../runs/HR-04F-DURABLE.md` contains each command, exit code and log fingerprint.

| Check | Result |
|---|---|
| Named pilot inputs | Pass — source lock, existing profile, and capability checklist all exist. |
| Pinned harness checkout prerequisite | **Blocked** — `afs-run` returned 1; neither expected workspace location contained both `tools/bootstrap.py` and `stacks/java-to-django.json`. See run `pinned-harness-checkout`. |
| Existing installation integrity | Pass — existing pin `9b805e17624c50d1e74cb008b3f1b0454c1be177`, 77 entries / 387 files, zero problems. This does not verify the requested pin. |
| Migration-state validation | Pass — 84 files checked, zero errors. |
| Protected input and prior-output preservation | Pass — `git diff --exit-code` against requested main found no changes to application/test/characterization files, profile, source lock, capabilities, slices, graphs, ledger, prior returns, costs, or prior HR-04F-HARNESS evidence/journals. |
| Source graph flow | Pass — 0 failures; 27 entry points, 18 reaching data. |
| Target graph flow | Pass — 0 failures; 7 entry points, 3 reaching data. |
| Both graph freshness | Pass — source and target graphs fresh. No graph was edited or rebuilt. |
| Requested acceptance installation | **Not installed** — current manifest pin is `9b805e17624c50d1e74cb008b3f1b0454c1be177`; requested pin check, executable `afs-acceptance` check, and `afs-acceptance.yml` existence check all fail. |

Bootstrap was not run: the required clean pinned checkout is absent. Consequently, the generated workflow's profile-derived Python, manual-only/read-only behavior, timeout, and failure/cancellation artifact upload cannot be verified. No installed files were hand-edited, and no fallback checkout or private-source skip was used.

The initial CI run [41916185215](https://github.com/martins-vds/ai-factory-pilot-target/actions/runs/41916185215) failed only because the plan-only commit did not yet contain the required return file. Its logs show migration-state, graph and changed-code gates passed. This return is added in the blocked handoff.

## Scope and acceptance boundary

No application, tests, templates, thresholds, source lock, capability decisions, slices, graphs, ledger, other-role returns, prior journals, or cost records were changed. No acceptance workflow was dispatched, no full mutation run was started, and no slice acceptance or human flow signoff is claimed.

## Next step

Provide a clean local harness checkout pinned exactly to `344241e92256a6048183f99063ca297fb96780de`. Resume on this branch, rerun setup checks, and use that checkout with the existing profile, capabilities and Java-to-Django stack pack through normal `tools/bootstrap.py`. Do not merge without separate named approval.
