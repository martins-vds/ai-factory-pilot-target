# HR-04E independent verification

- Verification issue: [#176](https://github.com/martins-vds/ai-factory-pilot-target/issues/176)
- Verification PR: [#177](https://github.com/martins-vds/ai-factory-pilot-target/pull/177)
- Target base: `copilot/hr-04e-fix` at `a46338cdd1cff6b3535278174b8b201b73a67ba2`
- Implementation under review: [PR #175](https://github.com/martins-vds/ai-factory-pilot-target/pull/175), pinned head `a46338cdd1cff6b3535278174b8b201b73a67ba2`
- Builder return: `.migration/returns/HR-04E-FIX.afs-specialist-migrator.yaml` names issue #174 and PR #175. Its original evidence rows remain in `.migration/evidence/runs/HR-04E-FIX.md`; the bounded attribution repair added its own validator row without changing earlier scores.
- Verifier change scope: no production changes; one PostgreSQL migration test was strengthened to assert event primary-key and cargo/location relation preservation.

## Result

The approved #171 UTC-instant persistence behavior, #136 deterministic ordering, and empty accepted-204 response are independently reproduced. The verifier return at `.migration/returns/HR-04E.afs-verifier.yaml` is the latest verdict for this ticket and supersedes the earlier HR-04E changes-required review against the pre-PR-175 implementation. That earlier result correctly described its then-current code: timestamps were truncated after reload and accepted 204s had a `Content-Type`. The earlier journal rows and observations remain unchanged; this verdict does not retroactively relabel them as passes.

## Independent checks

- The real PostgreSQL migration test creates a row under migration `0002`, runs the forward migration while the session timezone is `America/Los_Angeles`, and checks UTC-midnight completion and registration values. It now also asserts the event ID, FK IDs, and resolved cargo/location IDs survive. `python manage.py makemigrations --check --dry-run` reports no model-state drift. ADR-0004 and the handling inspection design document the reverse migration's irreversible loss of sub-day precision.
- Store and upsert tests preserve non-midnight, microsecond, offset-aware completion and registration instants, then reload them through both the record and history repository. Same-day completion order, registration-time ties opposing event-ID order, and equal-time ID fallback are covered; history and persisted cargo inspection agree. Processing uses each attempt's accepted registration time rather than processing time.
- The full suite passes all 28 immutable handling-registration golden cases. The approved #12/#13/#17/#87/#88 adjustments remain field-level expected-value changes and assertions; the comparison still checks exact fields and values. Accepted 204 tests assert status, empty bytes, and absent `Content-Type`; JSON errors, accepted-now/processed-later processing, no-expiry persistence, atomic rollback, and concurrency tests also pass.
- The handling-registration and tracking ledgers/design attribute timestamp persistence to #171 and equal-time ordering to #136. Relevant tracking-history capabilities retain their #171 attribution. The source checkout and source goldens were not changed.
- Gate 3 review found no documented ADR violation or spec gap. The Standards review noted only possible duplicated timestamp mapping in `store` and `upsert`, a non-blocking judgement call.
- Changed-code mutation produced 14 surviving mutants but passed the unchanged 0.8 threshold. The full-slice mutation gate was not run; it remains a slice-acceptance gate.

## Fresh profile gates

All commands were run through `afs-run --ticket HR-04E`; exact rows and log hashes are in `.migration/evidence/runs/HR-04E.md`.

| Gate | Exit / score | Result |
|---|---:|---|
| Build | 0 | compileall and Django system check passed |
| Behavior | 0 | 321 passed |
| Idiom | 0 | Ruff check and format check passed |
| CRAP | 19.0 | Maximum 19.0; threshold 30 |
| Changed mutation | 0.902 | 129 killed, 14 survived; threshold 0.8 |
| Regression | 0 | 321 passed |

No claim about PR #175's acceptance CI is made here; this report records independent local evidence only.
