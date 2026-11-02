# Handoff: TC-15c

## Handoff — afs-migrator · 2026-11-02T14:06:42Z
**State:** resolved · **Branch / PR:** `copilot/tc-15c-raise-slice-mutation-score` / https://github.com/martins-vds/ai-factory-pilot-target/pull/73 · **Last commit:** `995cee5`
### Done
- Rechecked pinned source (`f3beacf78de4f6d34edc4971ac87e38a5c6fe59d`), read-only status, required inputs, and migration validation.
- `afs-services check` reported `services OK: db`; Compose reports PostgreSQL 17.
- Required full mutation gate ran through `afs-run`: `AFS-RESULT gate=mutation score=0.822 threshold=0.8 killed=426 survived=92 files=53 base=all`. Journal row and raw log: `.migration/evidence/runs/TC-15c.md`, `.migration/runs/TC-15c/20261102T134650750953Z-mutation-full.log`.
- Targeted tests passed (42), full suite passed (188), and build, Ruff and CRAP checks passed in the previous session; evidence is in `.migration/evidence/runs/TC-15c.md`.
- Completed `.migration/returns/TC-15c.afs-migrator.yaml`; `mutation_changed` contains the exact full-run score and `handoff: none`.
### Remaining
- [x] Run full mutation using the healthy Compose PostgreSQL 17 service.
- [x] Record exact full-run score, threshold and counts in the journal and return file.
- [x] Explain the prior score discrepancy and validate return/journal consistency.
### Decisions made
- Treat 0.822 as the current acceptance evidence. The issue's 0.797 and earlier local 0.810 runs have different mutant totals and environments; the exact cause cannot be isolated from available runs.
### Blockers / questions
- None.
### Failing commands
- None outstanding. The earlier missing `afs-services` command was supplied by the main merge.
### Next step for the next session
No further work required; TC-15c evidence and return artifacts are complete.
