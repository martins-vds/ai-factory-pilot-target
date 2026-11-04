# HR-04F-HARNESS: reviewed method-aware graph pin

- Issue: martins-vds/ai-factory-pilot-target#181.
- Starting main: `d3453215147cdad68a9cfbd8cf187a3e9d4d6e34`.
- Previous pin: `47eb35f851b318a90cadbba218a01a2b54880869`.
- Installed pin: `9b805e17624c50d1e74cb008b3f1b0454c1be177`, approved and merged
  martins-vds/ai-factory-swarm#67.
- Method: normal bootstrap from that clean merged harness checkout, using the existing
  profile, capabilities and Java-to-Django stack pack. No installed-file hand edits.

## Scope and preservation

The only installed tool change is method-aware Django graph enrichment. Generated
workflow changes are pin provenance headers; capability decisions are unchanged apart
from their automatic check timestamp. Profile/source lock, application/templates/tests,
characterization, slice anchors, existing graphs, ledger decisions, previous role
returns/journals and session cost records are unchanged.

Bootstrap retained 10 agents / 61 skills. Installed integrity checks 77 entries /
387 files with zero problems. The original tier A designation is retained, not newly
measured. Capability decisions remain 14 met / 1 not applicable / 0 gaps / 0 waivers.

## Recorded verification

Commands, exit codes and raw-log fingerprints are recorded in
`../runs/HR-04F-HARNESS.md` through `afs-run`.

- Normal pinned bootstrap and installed integrity pass.
- Byte-level input/previous-evidence preservation passes.
- `check_rollout.py` verifies the exact pin and capability decisions, then uses the
  installed parser on actual source files to prove that the composition/factory/handler
  chain resolves to POST only.
- Schema/output validation passes.

## Remaining acceptance prerequisites

This rollout does not regenerate graphs or claim fresh application tests, mutation
coverage or slice acceptance. Graph proposal #180 is the historical failing baseline;
its original artifacts remain untouched.

After separate review and explicit merge approval of this rollout, run normal
`afs-understand` on main with `side=target`. Review the newly generated graph and its
flow/ownership/freshness gates, then obtain separately named graph merge approval.
Only after both graph sides are fresh and pass flow gates should independent Auditor
#132 run full-slice acceptance, including full mutation. Research #173 is excluded.
