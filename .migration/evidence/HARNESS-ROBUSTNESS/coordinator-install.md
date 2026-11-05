# Coordinator installation assistance

The original `afs-bootstrapper` finished at 2026-11-05T19:00:57Z with a blocked
return and explicit installation ownership handoff at
`0e2d048477706b0032c7903ea3bff57dce0d627a`. This is the existing coordinator's
installation record, not another Bootstrapper execution or its final verification.

## Normal pinned installation

- Harness source: `martins-vds/ai-factory-swarm@ee54dfdda8d86b324fa2818aa82c6b5b6456dbd1`.
- Clean source tree: `28f0cd7d31fe82cf34347206d52cac157d539623`.
- Installation commit: `f369d19de2747d3f9939e3a2f3dcdeec7a898b2f`.
- Ran the source's ordinary `tools/bootstrap.py` against this exact handoff
  checkout, using the existing `.migration/profile.yaml`,
  `.migration/capabilities.yaml`, and source `stacks/java-to-django.json`, with
  `--create-gap-issues`.
- The existing coordinator's GitHub access supplied ordinary Git credentials
  through a process-local credential helper. No credentials were transferred,
  stored in the proposal, or sent to the worker. No offline/private-source skip,
  installed-file hotpatch, manual manifest, or moving source ref was used.
- Actual bootstrap: exit 0, 86.75 seconds, 10 agents and 61 skills installed.
- Actual new installation integrity: source `ee54dfd`, 77 entries, 388 files,
  0 problems. These counts were observed anew, not copied from the old installation.
- Direct source parity compared 41 installed agent/tool/schema/patch files.
- All 394 pre-existing files outside normal bootstrap publication paths and this
  ticket's append-only journal retained their exact content and modes. This
  includes the application, tests, profile, source lock, graphs, ledger, costs,
  all existing returns, the worker's handoff, and accepted/sign-off evidence.
  Capability documents differ only in the normal `checked_at` refresh.
- No bootstrap lock or transaction/staging residue remains.

## Preserved diagnostic history

The first local migration validation ran before committing this initial
installation of `PR_ATTRIBUTION_RULE_V1`. It rejected the unchanged historical
HR-04A and HR-04C null-PR returns because no committed introduction of the new
rule yet existed in pilot history. After the ordinary installation commit
established that history, validation passed: 92 files, 0 errors. Neither return,
the validator, nor its history exemption was patched to obtain that result.

The coordinator's first source-parity probe also incorrectly treated generated
`legacy-returns.json` as a source-copy file. The local probe was corrected to
compare only copied agent/tool/schema/patch entries and then passed. This was
a coordinator probe error, not a harness defect. Both failed diagnostic rows
and their subsequent passing results remain in the ticket's
[append-only run journal](../runs/HARNESS-ROBUSTNESS.md).

## Ownership returned for independent verification

The parent used host Python 3.14 for the installation and metadata checks only.
This is not evidence that the pilot's declared Python 3.13 runtime, services,
graph freshness, or application gates passed after installation.

The same original Bootstrapper must now independently verify the committed
installation using its declared runtime and setup, exact-source parity and
integrity, migration validation, generated reconciliation/return workflow and
event-head/base attribution behavior, graph freshness/flow, and protected-input
preservation. Its existing blocked return/report/handoff remain unchanged by
this assistance and must be honestly finalized by that worker.

No acceptance or mutation rerun, graph rebuild, application slice, epic-close
event, human attestation, research merge, or proposal merge was performed.
Final independent exact-head review/current CI still gate the separately
approved bounded rollout.
