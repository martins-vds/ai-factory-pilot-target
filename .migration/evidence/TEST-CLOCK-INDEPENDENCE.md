# TEST-CLOCK-INDEPENDENCE — verifier evidence

- Issue: [martins-vds/ai-factory-pilot-target#199](https://github.com/martins-vds/ai-factory-pilot-target/issues/199)
- Target base: `a284b840e97e06452ca5370b941d22c4c6ae4f2d` (`origin/main`)
- Scope: test-only; no application, harness, profile, ledger, or acceptance changes.

## Reproduction and repair

The unchanged-main Actions run [42152788853](https://github.com/martins-vds/ai-factory-pilot-target/actions/runs/42152788853) failed this test and CRAP coverage: 320 passed, 1 failed at the latest-delivery assertion (`assert 810 == 821`). A controlled local reproduction fixed the seed clock at `2026-11-06T12:00Z` while retaining the original event timestamps (`2026-11-04T12:00Z` completion, `2026-11-03T12:00Z` registration); it failed because seeding created an ABC123 UNLOAD on November 5, later than the test events. The reproduction is recorded in the run journal and `.migration/runs/TEST-CLOCK-INDEPENDENCE/20261106T030432078910Z-controlled-baseline-2026-11-06.log`.

The test now fixes the seed clock to each controlled date and derives the equal event timestamps relative to it: November 5, 2026 (before the boundary), November 6, 2026 (the observed boundary), and January 15, 2027 (a later date). Both submitted events occur at noon on the seed's previous day, after the sample UNLOAD at midnight. Assertions that the higher persisted event ID determines latest delivery and history remain intact.

## Verification

All commands ran through `afs-run`; complete durable results are in [the TEST-CLOCK-INDEPENDENCE run journal](runs/TEST-CLOCK-INDEPENDENCE.md).

| Check | Result |
|---|---|
| Controlled pre-repair reproduction at November 6 | Expected failure; confirms seeded November 5 UNLOAD supersedes the hard-coded November 4 events |
| Three controlled date cases | Exit 0; 3 passed |
| Build | Exit 0; `compileall` and Django system check |
| Idiom | Exit 0; Ruff check and format check |
| Behavior and regression | Exit 0; 323 passed |
| CRAP | Exit 0; maximum 19.0, threshold 30 |
| Changed-code mutation | Exit 0; `n/a: no mutable code changed` (only tests changed; full mutation was not run) |

The verifier return is `.migration/returns/TEST-CLOCK-INDEPENDENCE.afs-verifier.yaml`. An owning proposal PR has not yet been created; see `.migration/handoffs/TEST-CLOCK-INDEPENDENCE.md`.
