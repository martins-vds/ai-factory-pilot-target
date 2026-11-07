## Handoff — afs-specialist-migrator · 2026-11-07T05:23:50Z
**State:** needs human  ·  **Branch / PR:** https://github.com/martins-vds/ai-factory-pilot-target/pull/322  ·  **Last commit:** d49ccaa1fcdfb3e6acf56df675d2424b0d94faff
### Done
- Implemented the registered `data_migration` app and transactional snapshot loader with deferred nullable references and PostgreSQL sequence realignment.
- Snapshot validation passed: 7 tables, 0 problems; `.migration/runs/DM-05C/20261107T051505728229Z-snapshot.log`.
- Focused loader test passed, including idempotency, cycle restoration, and new generated IDs in all six mapped tables; `.migration/runs/DM-05C/20261107T052053253774Z-loader-regression.log`.
- Actual snapshot loaded and reloaded successfully: 54 rows across 6 mapped tables; `.migration/runs/DM-05C/20261107T051842021718Z-data-load-2.log` and `.migration/runs/DM-05C/20261107T051943299455Z-data-load-rerun.log`.
- Build and idiom gates passed; CodeQL found no alerts.
### Remaining
- [ ] Resolve whether the out-of-scope settings test may be updated to include the required new app.
- [ ] After that decision, run the full suite and remaining CRAP and changed-code mutation gates, update the return, and validate `.migration/`.
### Decisions made
- Kept changes within the ticket's listed implementation and test paths; did not alter the separate project-settings test.
### Blockers / questions
- The full suite exposed a directly coupled stale assertion in `tests/test_project_settings.py`. Updating `INSTALLED_APPS` as required makes its exact old-list assertion fail; that path is excluded by the ticket's “Touch only the files listed” instruction.
- No workaround was used to mask the failing assertion.
### Failing commands
- `pytest -q` → exit 1; `.migration/runs/DM-05C/20261107T052058539589Z-behavior.log:22-48` (360 passed, one assertion failed).
### Next step for the next session
Ask the operator to authorize the one-line expectation update in `tests/test_project_settings.py`; if approved, add the app config to that expected list, then rerun behavior and all remaining gates through `afs-run`.

## Handoff — afs-specialist-migrator · 2026-11-07T06:02:16Z
**State:** blocked  ·  **Branch / PR:** https://github.com/martins-vds/ai-factory-pilot-target/pull/322  ·  **Last commit:** ee63ea1
### Done
- Updated only the `INSTALLED_APPS` expectation in `tests/test_project_settings.py` with the configured data migration app; full behavior and regression suites pass (363 tests), `.migration/runs/DM-05C/20261107T055935640995Z-behavior-rerun.log` and `.migration/runs/DM-05C/20261107T060125950277Z-regression.log`.
- Added public-command conversion and invalid-boolean tests in the ticket-listed `tests/data_migration/test_load.py`; focused run passed, `.migration/runs/DM-05C/20261107T055915510712Z-loader-transform-tests.log`.
- Build and idiom gates passed; latest rerun evidence is recorded in `.migration/evidence/runs/DM-05C.md`.
### Remaining
- [ ] Resolve the loader CRAP threshold failure; latest score is 38.7 with threshold 30.
- [ ] Rerun changed-code mutation on the updated tests and reach the 0.8 threshold.
- [ ] Rerun any affected gates and update the DM-05C return; remove the handoff pointer only when complete.
### Decisions made
- Kept tests at the public `load_data_snapshot` management-command seam and made no production-code change.
### Blockers / questions
- CRAP failed twice, triggering the repeated-failure stop rule. A fresh session should inspect the remaining loader coverage/complexity rather than continue this attempt.
- Mutation scored 0.590 against 0.8 before the additional conversion tests were added; it must be rerun against the updated test set.
### Failing commands
- `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` → exit 1, see `.migration/runs/DM-05C/20261107T060043680242Z-crap-score-rerun.log:38`.
- `python .migration/harness/tools/afs-mutation --changed-since origin/main` → exit 1, see `.migration/runs/DM-05C/20261107T055417218254Z-mutation-changed.log:3`.
### Next step for the next session
Resume DM-05C from issue #324: rerun changed-code mutation against the current tests, address the loader CRAP threshold, rerun the per-PR gates through `afs-run`, and update the return.

## Handoff — afs-specialist-migrator · 2026-11-07T13:05:12Z
**State:** blocked  ·  **Branch / PR:** https://github.com/martins-vds/ai-factory-pilot-target/pull/334  ·  **Last commit:** 71577865470b037437c269dacbcafde73d2fa991
### Done
- Split `load_snapshot` into mapping-driven clear, mapped insertion, deferred-reference restoration and sequence-realignment phases; preserved the transaction and two-phase reference cycle.
- Added public-command tests for carrier-movement field preservation (#254), imported IDs/sequence allocation and event-cycle restoration (#255/#258), source boolean/timestamp formats, unmapped enums with rollback, invalid mapping references and unknown transforms.
- Build and idiom gates passed; full behavior suite passed (366 tests), `.migration/runs/DM-05C/20261107T130055368414Z-behavior-final.log`.
- CRAP passed at max 29.8 / threshold 30, no methods over threshold; `.migration/runs/DM-05C/20261107T130223869398Z-crap-score-final.log`.
- CodeQL found no alerts.
### Remaining
- [ ] Review the 96 current survivors in `.migration/evidence/mutants/DM-05C.md`; add only source/mapping-justified public-command tests or simplify code proven equivalent.
- [ ] Reach the unchanged mutation threshold of 0.8, then rerun the full profile gates and validate `.migration/`.
- [ ] Update the return to `handoff: none` only after all gates pass.
### Decisions made
- Kept tests at the public `load_data_snapshot` management-command seam; left the mutation threshold unchanged.
- Replaced the parameterized mapping-error cases with one loop-based test because the mutation runner could not resolve parameterized test node IDs.
### Blockers / questions
- Changed-code mutation remains below threshold (0.682); the stop-and-handoff condition in issue #332 applies.
- The remaining survivors are concentrated in `_transform` (19), `_read_source_rows` (15) and `_prepare_tables` (12), with others listed in the committed survivor file.
### Failing commands
- `python .migration/harness/tools/afs-mutation --changed-since origin/main` → exit 1, score 0.682 vs 0.8; see `.migration/runs/DM-05C/20261107T125848264638Z-mutation-changed-rerun.log:2`.
### Next step for the next session
Resume DM-05C on PR #334 from this section. Analyze the current survivor list against mapping-defined behavior, add only justified tests or simplify demonstrably equivalent code, then rerun changed-code mutation and the profile gates; stop and hand off again if mutation remains below 0.8.
