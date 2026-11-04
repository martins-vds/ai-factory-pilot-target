# HR-04E-HARNESS: reviewed pin rollout

- Issue: martins-vds/ai-factory-pilot-target#178.
- Starting branch/head: `copilot/hr-04e-correct-verified-divergences` /
  `e25ccc8ecb4c0fe979e85116940fe2b6e9ce36ed`.
- Previous pin: `7f8c13956114077164f8b6e1308ece1cf7a0d7ed`.
- Installed pin: `47eb35f851b318a90cadbba218a01a2b54880869`, merged
  martins-vds/ai-factory-swarm#65 with explicit operator approval.
- Method: normal `tools/bootstrap.py` from that clean merged checkout, using the
  existing profile, capabilities and `stacks/java-to-django.json`. Installed files
  were generated, not hotpatched.

## Scope and preservation

The pin installs superseded-return attribution, the previously reviewed stale-stack
ancestry prerequisite and cross-slice differential guidance. Other generated workflow
changes are provenance-header updates. The manifest records 77 entries / 387 files,
with zero installed-integrity problems.

`check_rollout.py` confirms the profile and source lock are byte-identical to the
starting head, capability decisions are unchanged apart from `checked_at`, and the
generated dependent jobs and schema dependency are wired. There remain 14 met
capabilities, one not applicable, no gaps and no waivers. Existing characterization
tier A is retained, not newly measured.

Application code, tests, characterization/source goldens, ledger decisions, prior
Migrator/Verifier returns, their journals and session records are unchanged. Only the
Bootstrapper's own return/journal and this rollout evidence are added.

## Recorded verification

Every listed check ran through `afs-run --ticket HR-04E-HARNESS`; exact commands,
exit codes and log fingerprints are in `../runs/HR-04E-HARNESS.md`.

- Normal pinned bootstrap, installed integrity and schema/output validation pass.
- Preserved-input and generated-workflow checks pass.
- The new ancestry guard passes against the existing #169 stack topology.
- Installed `check_return_contract.py` accepts #169's original attribution from
  `HR-04E.afs-verifier.yaml@1c8716c7afe972c60b750b36aca91ffa80597a79`, parent #131 /
  PR #169, without altering the later #176 / #177 return.
- The prospective root-PR replay accepts its own original attribution at
  `2352576112fd3eecf559112fa3fea43e9e3394d8`, #131 / PR #167.
- The unchanged application/previous-evidence diff check passes.

The two JSON files are reduced replay fixtures, not archived GitHub delivery events.
Parent links #168 -> #131 -> #113 were verified through GitHub's actual issue API;
the CLI checks used that API too. The #167 fixture represents the prospective
integrated tree and is not a claim that the current remote #167 check passed.

Historical attribution proves provenance only. Current return validity and current
behavior gates still apply. This metadata rollout does not claim a fresh local
application suite, mutation run, full-slice acceptance, or a new source experiment.
The new rollout PR needs its own fresh CI and named merge approval. After it lands,
the paused approved sequence still requires fresh #169 and then #167 checks.
