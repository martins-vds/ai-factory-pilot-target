# HARNESS-ROBUSTNESS — Bootstrapper report

## Attribution and actors

- Role: `afs-bootstrapper`
- Issue: https://github.com/martins-vds/ai-factory-pilot-target/issues/192
- Proposal: https://github.com/martins-vds/ai-factory-pilot-target/pull/193
- Pilot base: `cbb55d9ff4faeb716fc0663ad4a9441b5321efd6`
- Approved harness: `martins-vds/ai-factory-swarm@ee54dfdda8d86b324fa2818aa82c6b5b6456dbd1`, tree `28f0cd7d31fe82cf34347206d52cac157d539623`.
- Installation actor: the existing coordinator ran normal bootstrap and committed it as `f369d19de2747d3f9939e3a2f3dcdeec7a898b2f`. This Bootstrapper did not install it. The coordinator's installation record is `.migration/evidence/HARNESS-ROBUSTNESS/coordinator-install.md`.
- Verification actor: this original Bootstrapper independently checked the committed installation in the declared Python 3.13.17 environment.

## Independent installation verification

Fresh afs-run observations:

- Installed integrity: harness `0.2.0`, pin `ee54dfd`, 77 entries, 388 files, 0 problems.
- Direct source parity: 41 agent/tool/schema/patch files byte-match the clean exact-source checkout (10 agents, 25 tools, 5 schemas, 1 patch).
- Generated template parity: all 7 workflow templates, 2 hook templates, and both instruction blocks match the exact source's rendered/copied output. The stack pack is the source's `stacks/java-to-django.json` (SHA-256 `a3943db24166e7ee68f6dd7ccba67fa1d36d893211899f644393133de9a29bef`); all 15 of its skills appear in the installed manifest.
- Completion workflow: `afs-map-fog.yml` runs ticket reconciliation, then return validation, then fog re-walk; checkout uses full history and the job has `issues: write`, `pull-requests: read`, and `contents: read`.
- Return attribution: installed tools byte-match the exact source. The event check uses the PR event's `head.sha` and `base.sha`, requires both commits, checks configured base against event base, and scopes changed-return/superseded-history inspection to that event head/base.
- Focused exact-source regressions: 89 tests passed across `test_return_contract.py`, `test_ticket_guard.py`, and `test_check_slice_returns.py`, including event-head identity, inherited returns, superseded attribution, recursive ticket reconciliation, and historical pre-rule compatibility.
- Migration validation: 92 files, 0 errors. Runtime: Python 3.13.17. Test service `db`: healthy.
- Graph freshness: source and target both fresh. Source flow: PASS, 1,080 nodes, 2,137 edges, 18/27 entry points reach data. Target flow: PASS, 374 nodes, 929 edges, 3/7 reach data, 5 slice-owned entry points, 0 unowned.

## Preservation

- The profile and `.migration/source.lock` are byte-identical to pilot base.
- The 15 capability decisions/providers/statuses are unchanged apart from the normal `checked_at` refresh: 14 `met`, 1 `not-applicable`, 0 `gap`, 0 `waived`.
- All 39 pre-existing return files are byte-identical, including all 3 historical null-PR returns. Pre-existing costs, handoffs, prior evidence, application/tests/templates, slices, graphs, and ledger are unchanged. Existing rows in this ticket's run journal remain as a prefix; new runs append.
- Independent tree comparison from the worker handoff checkpoint to the install commit found all 353 pre-existing tracked files outside normal bootstrap publication paths and this ticket's append-only journal unchanged in content and mode. The audit was corrected to treat the coordinator's new session-cost record as an addition, not a changed pre-existing record.
- No acceptance or full mutation run, graph rebuild, slice dispatch, epic state change, or human-flow check was performed.

## Initial access blocker and resolution

The original worker's normal bootstrap attempt remains recorded in this journal: it exited 1 fetching pinned private skill dependency `martins-vds/code-migration-hackathon@4de661a9a830aaef70ff55e879c0cc540599cad8` (`fatal: unable to get password from user`). No dependency was skipped and no credential was transferred. The coordinator subsequently completed the requested ordinary bootstrap from the exact clean source and existing inputs; no installed-file patch or moving source ref was used.

## Outcome

Independent installation verification passed. This proposal is not merged. It awaits independent exact-final-head review and current CI; only the coordinator may apply the retained conditional merge approval after those checks.
