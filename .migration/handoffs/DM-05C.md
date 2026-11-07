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
