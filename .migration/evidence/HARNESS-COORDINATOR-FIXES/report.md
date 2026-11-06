# HARNESS-COORDINATOR-FIXES bootstrap report

## Current status

The pinned harness upgrade is installed on PR #198, not pilot `main`. The parent coordinator performed the normal bootstrap after the original Bootstrapper's access handoff; the same original Bootstrapper independently verified the installation and now integrated current `main`. The integration merge has parents `2e48049e66a8ee2ba9a2a4305122b82b5bc9c8c1` and `bce0c54cfa9b9c424e911b08f17c8f6bee75139f`, whose tree is `a470025b3ba7823c7fda80dfef06608310d4f5f4`. The installed release remains `martins-vds/ai-factory-swarm@e51998d716c229930e1e072cdcb05be0a872b4ef`, tree `728ee39572de27bd9ab01999a93d6bec28f0a555`.

All local installation, exact-source parity, migration-state and preservation checks passed against the new main baseline. Main's post-merge AFS harness run [42156736164](https://github.com/martins-vds/ai-factory-pilot-target/actions/runs/42156736164) passed all four jobs, including 323 tests. Exact integrated PR head `7535e01ea472d7ceb66406e552634e374c5b9243` passed AFS run [42157358781](https://github.com/martins-vds/ai-factory-pilot-target/actions/runs/42157358781), all four jobs. The earlier red test check was resolved by the separately authorized test-only repair merged in PR #200; this rollout did not implement or repeat that fix. No L1/L0 role coverage is claimed.

## Installer evidence

The unchanged parent installer record is `.migration/evidence/HARNESS-COORDINATOR-FIXES/parent-installation.md`. It records the parent's normal bootstrap, exact clean source pin/tree, existing profile/capabilities and stack pack, `--create-gap-issues`, and exit 0. Existing authorized access was used; no credentials were transferred, private source skipped, offline mode used, installed hotpatch applied, graph rebuilt, application edit made, or acceptance rerun. The parent is the installer; the original worker is the verifier.

## Original Bootstrapper setup and current-main integration verification

- The pinned read-only `.source` checkout matches `.migration/source.lock` at `f3beacf78de4f6d34edc4971ac87e38a5c6fe59d`; it is ignored and not writable. Complete target ancestry is present.
- Current setup passed: migration validation 96 files / 0 errors; ticket input check 0 missing paths; `afs-services check` reports `db` healthy; `check_runtime.py` reports Python 3.13.17; RTK is 1.1.0.
- The release was independently reacquired into a clean detached checkout at `e51998d716c229930e1e072cdcb05be0a872b4ef`, tree `728ee39572de27bd9ab01999a93d6bec28f0a555`.
- Through `afs-run`, the installed-manifest check reported 77 entries / 388 files / 0 problems, exact-source hashes matched 64/64 directly comparable installed files, and migration state validation passed (96 files / 0 errors).
- Against current `origin/main` at `bce0c54cfa9b9c424e911b08f17c8f6bee75139f`, all 41 pre-existing YAML returns are unchanged, including `TEST-CLOCK-INDEPENDENCE.afs-verifier`. All 216 baseline files under application code, tests, templates, graphs, slices, ledgers, costs, and acceptance evidence are unchanged. `.migration/profile.yaml` and `.migration/source.lock` are byte-identical; capability decisions/providers/statuses are unchanged (only ordinary `checked_at` refresh).
- The repaired ordering test, its verifier evidence, handoff, return, and cost record match current main byte-for-byte (6/6). The test-repair files and parent installation evidence remain preserved. The original Bootstrapper report is updated; the chronological handoff retains the prior access and verification history, and the per-ticket run journal has only appended rows.
- A `current-main-setup-probe` run passed. The first parity command in this continuation failed because the prior session's temporary source worktree was absent; after acquiring the exact immutable source commit, the parity check passed 64/64. This was an environment-path issue, not a parity mismatch.
- The original worker did not run the test-only repair or repeat bootstrap; this was a normal merge of current main and independent verification of the preserved install.

## Historical access and CI

The original Bootstrapper's one normal install attempt stopped fetching pinned dependency `martins-vds/code-migration-hackathon@4de661a9a830aaef70ff55e879c0cc540599cad8` with Git exit 128. That failure and its original access handoff remain historical. The parent subsequently completed normal bootstrap using existing authorized access.

Before PR #200 landed, PR #198 AFS runs `42152379401` and `42153195105` failed the same unchanged ordering test (320 passed, 1 failed). The baseline AFS run `42152788853` independently reproduced the failure on old main. The user-authorized test-only repair in PR #200 addressed that failure; this rollout did not change production behavior or test bytes itself. After that repair merged, main at `bce0c54` passed AFS run `42156736164` (all four jobs, 323 tests). This success is main evidence, not a substitute for the live AFS result on the final integrated PR head.

Intermediate integrated-head AFS run `42157072248` passed its base, migration and gate jobs, but its return-contract job failed because the workflow event still carried old base SHA `a284b840e97e06452ca5370b941d22c4c6ae4f2d` while `origin/main` was already `bce0c54cfa9b9c424e911b08f17c8f6bee75139f`. On final integrated head `7535e01`, the return-contract job passed in run `42157358781`; that run passed all four jobs.

## Next action

Parent to independently review the integrated exact PR head and its live current-head AFS check. Do not self-merge, alter the test repair, rerun acceptance/full mutation/human flow, rebuild graphs, or claim coordinator-role coverage. Historical acceptance and human attestation remain historical.

See `.migration/handoffs/HARNESS-COORDINATOR-FIXES.md` for the chronological original access handoff, independent verification, and current-main integration record.
