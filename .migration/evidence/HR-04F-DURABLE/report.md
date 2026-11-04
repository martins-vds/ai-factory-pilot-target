# HR-04F-DURABLE — pinned acceptance harness installation

- Issue: [martins-vds/ai-factory-pilot-target#185](https://github.com/martins-vds/ai-factory-pilot-target/issues/185)
- Acceptance issue: [martins-vds/ai-factory-pilot-target#132](https://github.com/martins-vds/ai-factory-pilot-target/issues/132)
- Setup PR: [#186](https://github.com/martins-vds/ai-factory-pilot-target/pull/186)
- Pilot baseline: `5cace249987e3ddd4ce3345a845168ca545bab55`
- Installed harness pin: `344241e92256a6048183f99063ca297fb96780de`
- Outcome: **normal installation and independent verification pass; conditional human review remains.**

## Execution and independent verification

The committed journal at `../runs/HR-04F-DURABLE.md` preserves the initial worker failures, the coordinator's bootstrap and verification, and this session's independent checks. Raw logs are not committed.

| Check | Result |
|---|---|
| Coordinator normal bootstrap | Pass — coordinator's `coordinator-normal-bootstrap` row records exit 0 using a fresh checkout at the exact approved pin and the existing profile, capability checklist, and Java-to-Django stack pack. The coordinator executed this bootstrap; this verification session did not. |
| Independent public harness preflight | Pass — this session cloned the public repository to `/tmp/afs-HR-04F-DURABLE-review.mm0ATp/harness` and verified exact `HEAD=344241e92256a6048183f99063ca297fb96780de` and a clean worktree (`independent-clean-harness-pin`). |
| Generated delta source parity | Pass — changed evidence skills and `afs-acceptance` match files at the clean pin; existing workflow changes are pin-header-only; the new acceptance workflow exactly matches the pinned template rendered with the target profile's Python version. |
| Installed integrity | Pass — this session's `independent-installed-integrity`: pin `344241e`, 77 entries / 388 files, zero problems. The coordinator's `coordinator-installed-integrity` also passed. |
| Acceptance runner | Pass — executable `.migration/harness/tools/afs-acceptance` responds to `--help`; its SHA-256 matches the installed manifest and the file at the independent clean harness pin. No acceptance gates were run. |
| Generated workflow constraints | Pass (`acceptance-profile-contract`) — exact pinned-template rendering with profile-derived Python 3.13; manual `workflow_dispatch` only; `contents: read`; 360-minute job timeout; 330-minute gate timeout; artifact upload step uses `if: always()`. |
| Capability decisions | Pass — independent comparison against baseline confirms all capability/provider data is identical; only `checked_at` refreshed from `2026-11-04T18:58:45Z` to `2026-11-04T21:49:32Z`. |
| Protected input and history preservation | Pass — independent baseline comparison found source/app/test/template/profile/source-lock/slices/graphs/ledger unchanged, and all prior returns, other-role evidence, journals, handoffs, and costs unchanged. Only this ticket's own return/report/journal/handoff and this session's cost record are excluded. Prior rows of this ticket's journal are preserved byte-for-byte as a prefix. |
| Migration-state validation | Pass — this session checked 86 files, zero errors (`independent-migration-validation`, `final-schema-validation`, and `final-output-validation-current`). Coordinator output validation also passed. |
| Profile runtime | Pass — Python 3.13.17 matches the profile (`independent-runtime`). |
| Source/target graph freshness | Pass — both graphs remain fresh (`independent-graph-freshness`). |
| Source flow gate | Pass — 0 failures; 27 entry points, 18 reaching data (`independent-source-flow`). |
| Target flow gate | Pass — 0 failures; 7 entry points, 3 reaching data (`independent-target-flow`). |

No application changes or graph rebuilds occurred. No Auditor #184 evidence was edited.

## Preserved attempt history

Earlier worker runs `bootstrap` and `dependency-fetch-diagnostic` remain in the journal and document the restricted worker's credential prompt for a pinned skill dependency. The coordinator then completed normal bootstrap in its authorized environment without transferring credentials. Its first preservation check failed because it treated the normal `checked_at` refresh as a capability decision change; the corrected `coordinator-preserved-decisions` check passed. These failed rows remain as history and are not the current installation result.

The initial CI run [41916185215](https://github.com/martins-vds/ai-factory-pilot-target/actions/runs/41916185215) failed because the plan-only commit lacked a return file. CI on the coordinator-installed input head `43f538e3b73522ccbfef280643a2bd0a34d6f633` passed ([run 849](https://github.com/martins-vds/ai-factory-pilot-target/actions/runs/41920057694)). The evidence-finalization commit must also have green CI on its own final head before human merge review.

## Acceptance boundary and next step

This installs execution tooling only. No acceptance workflow was dispatched, no full mutation run was started in this worker, and no slice acceptance, full-mutation result, or human flow signoff is claimed. Research #173 remains excluded.

Next: independent final-head review and green final-head CI, followed by the coordinator's separately authorized human merge approval. Do not merge before those conditions.
