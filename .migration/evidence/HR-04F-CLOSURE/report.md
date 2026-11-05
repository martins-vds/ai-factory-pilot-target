# HR-04F-CLOSURE — blocked pinned bootstrap proposal

- Issue: [martins-vds/ai-factory-pilot-target#187](https://github.com/martins-vds/ai-factory-pilot-target/issues/187)
- Rollout proposal PR: [#188](https://github.com/martins-vds/ai-factory-pilot-target/pull/188) (draft; not merged)
- Approved harness commit: `2c8e00ab87e99f3d77976e3cf78c2a89011627fb`
- Pilot baseline: `f589d826100b34722eb29628ec93deb7ad450bb8`
- Existing installed harness pin: `344241e92256a6048183f99063ca297fb96780de`
- Outcome: **blocked before normal bootstrap; prior installation and acceptance evidence unchanged.**

## Checks performed

| Check | Result |
|---|---|
| Pinned source checkout | Pass — `.source` HEAD matches `.migration/source.lock` at `f3beacf78de4f6d34edc4971ac87e38a5c6fe59d`; read-only and ignored. |
| Migration-state validation | Pass — 88 files checked, zero errors. |
| Runtime and test services | Pass — Python 3.13.17 matches the profile; configured `db` service is healthy. |
| Setup probe | Pass — `true`, recorded in `.migration/evidence/runs/HR-04F-CLOSURE.md`. |
| Pinned bootstrap inputs | **Blocked** — `bootstrap-inputs` exited 1; `.migration/harness/tools/bootstrap.py` and `stacks/java-to-django.json` are absent. No clean harness checkout exists in the available workspace. See `.migration/runs/HR-04F-CLOSURE/20261105T140903835721Z-bootstrap-inputs.log`. |

The installed manifest identifies the existing pin as `344241e92256a6048183f99063ca297fb96780de`, not the approved commit. No normal bootstrap was attempted without the exact approved source and its stack pack. The current installation, profile, source lock, capability decisions/providers, graphs, ledger, application, tests, pre-existing returns, prior journal rows, costs, and acceptance archive were not changed by this proposal. The existing Tier A characterization and capability checklist are retained; capability counts remain 14 met, 0 gap, 0 waived, and 1 not applicable.

## Not claimed

Installed-file parity/integrity at the approved pin, generated fog workflow checks, graph freshness/flow gates, and the read-only epic113 attribution guard were not run because the approved installation was not produced. No epic closure, `--reopen`, fog task creation, application change, graph rebuild, full-mutation run, or acceptance verdict occurred. Existing acceptance evidence remains tied to its original execution revision; it was not remeasured on the approved harness.

## Required next step

Have the already-authorized coordinator perform the **normal** bootstrap on this rollout proposal using a clean checkout at the exact approved harness commit, the existing pilot profile and capability checklist, and `stacks/java-to-django.json`. The authorized execution must resolve the pinned private skill dependency `martins-vds/code-migration-hackathon@4de661a9a830aaef70ff55e879c0cc540599cad8` normally; do not transfer credentials, skip it, or fabricate an installation. Then request a fresh Bootstrapper session to independently verify the generated delta and run the specified `afs-run` integrity, state, graph, workflow, and read-only epic113 checks. Keep execution and verification actors distinct in the evidence.
