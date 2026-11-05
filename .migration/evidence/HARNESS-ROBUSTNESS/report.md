# HARNESS-ROBUSTNESS — Bootstrapper report

## Attribution

- Role: `afs-bootstrapper`
- Issue: https://github.com/martins-vds/ai-factory-pilot-target/issues/192
- Proposal: https://github.com/martins-vds/ai-factory-pilot-target/pull/193
- Pilot base: `cbb55d9ff4faeb716fc0663ad4a9441b5321efd6`

## Pinned source and attempt

Acquired a clean detached worktree of `martins-vds/ai-factory-swarm` at
`ee54dfdda8d86b324fa2818aa82c6b5b6456dbd1`; its tree is
`28f0cd7d31fe82cf34347206d52cac157d539623`. The exact source's
`tools/bootstrap.py` was run against this pilot with the existing profile and
capabilities and `stacks/java-to-django.json`, without offline or private-source
skip options. The `pinned-normal-bootstrap` afs-run exited 1 while fetching
`martins-vds/code-migration-hackathon@4de661a9a830aaef70ff55e879c0cc540599cad8`.
The pinned dependency fetch diagnostic returned exit 128 with
`fatal: unable to get password from user`. No credentials were transferred.

The bootstrap did not publish generated files and left no bootstrap lock,
transaction marker, or staging tree. The profile, capabilities, source lock,
application files, graphs, ledger, existing returns, and prior acceptance
evidence were unchanged. The current capability file contains 15 entries:
14 `met`, 1 `not-applicable`, 0 `gap`, and 0 `waived`; there are no `ticket: new`
entries.

## Checks observed before installation

- Setup validation: 90 migration files checked, 0 errors.
- Final validation after adding this report, handoff, and return: 92 files
  checked, 0 errors.
- Ticket input check: 0 named paths, 0 missing.
- Installed harness integrity (still the old installation): 77 entries, 388
  files, 0 problems.
- Declared runtime: Python 3.13.17; test service `db` healthy.
- Existing source graph flow: PASS, 1,080 nodes, 2,137 edges, 18/27 entry
  points reaching data.
- Existing target graph flow: PASS, 374 nodes, 929 edges, 3/7 entry points
  reaching data; 5 slice-owned entry points, 0 unowned.
- The setup-probe afs-run exited 0.

These are observations of the pre-install pilot, not checks against the newly
approved harness source. No source/tool/template parity, new installed-integrity,
completion-workflow, corrected return-gate, or return-attribution verification
is claimed. No graph freshness check or acceptance/mutation run was performed.

## Outcome and next action

Normal bootstrap is blocked by access to the pinned private skill dependency.
This is an access blocker, not evidence of a newly discovered harness code gap.
No dependency was skipped and no harness files were patched. Request the existing
coordinator to run the same normal bootstrap from a credentialed environment
using a fresh checkout of the exact approved source and existing pilot inputs.
Once safely assisted, this original Bootstrapper session must independently
verify the resulting committed installation and finish this return.
