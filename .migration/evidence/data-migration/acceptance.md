# Data-migration slice acceptance — DM-ACCEPT

- Epic: [Data migration #247](https://github.com/martins-vds/ai-factory-pilot-target/issues/247) · Ticket: [#413](https://github.com/martins-vds/ai-factory-pilot-target/issues/413)
- Acceptance run: [42427856017](https://github.com/martins-vds/ai-factory-pilot-target/actions/runs/42427856017), attempt 1 · Commit: `3d1fcec13586c2d89b7a079bfd14ca011e2522c0`
- Artifact: `afs-acceptance-3d1fcec13586c2d89b7a079bfd14ca011e2522c0-42427856017-1` · Independently verified with `afs-acceptance verify`
- Durable result: `.migration/evidence/acceptance-runs/42427856017-1.json` · Journal: `.migration/evidence/runs/DM-ACCEPT.md`
- Artifact retention expires 2026-12-08T01:15:37Z (30 days after upload).

## DM-05E reconciliation

The committed [reconciliation report](reconciliation.md) records the snapshot taken at `2026-11-07T00:40:49Z`, manifest counts, the approved `SEQUENCE` exclusion under ruling #255, and the six mapped tables. The mapping-driven load/export reconciliation matched 54 rows by count and checksum, with no dangling references:

| Target table | Source table | Snapshot / target rows | Checksum |
|---|---|---:|---|
| `location` | `LOCATION` | 13 / 13 | match |
| `voyage` | `VOYAGE` | 5 / 5 | match |
| `cargo` | `CARGO` | 4 / 4 | match |
| `HandlingEvent` | `HANDLINGEVENT` | 12 / 12 | match |
| `leg` | `LEG` | 7 / 7 | match |
| `carrier_movement` | `CARRIER_MOVEMENT` | 13 / 13 | match |

`SEQUENCE` has one manifest row and is excluded from row comparison: target-native PostgreSQL sequences are realigned during loading. No snapshot rows are committed.

## DM-05F invariants

`tests/data_migration/test_invariants.py` exercises four loaded-data invariants: cargo delivery re-derived from handling history, connected itinerary legs, existing voyage/location references for handling events, and ordered/connected carrier movements within each voyage schedule. The focused DM-05F journal records the invariant run and the deliberate broken-itinerary fixture check; the acceptance run's full `pytest -q` gate also passed.

## Acceptance gates and full mutation

Every planned gate in the verified artifact passed: runtime, harness integrity, services, graph freshness, source and target graph gates, build, idiom, tests, CRAP, and full mutation. The exact full-mutation result from the artifact journal is:

`gate=mutation score=0.914 threshold=0.8 killed=1895 survived=178 files=80 base=all`

The machine result and original workflow/artifact identity are preserved in the durable result archive above. Raw logs remain in the downloaded, gitignored artifact directory.

## Target graph

The target graph built and gated for commit `3d1fcec13586c2d89b7a079bfd14ca011e2522c0` records:

`command=load_data_snapshot`: reaches 6 data nodes — `HandlingEvent`, `cargo`, `carrier_movement`, `leg`, `location`, and `voyage`.

This is the six-table coverage required by the mapping. The independent gate-7 audit for the same commit is tracked separately in issue #414 / PR #416 and remains outstanding.

## Data ledger

| Ledger entry | Status | Evidence / disposition |
|---|---|---|
| `data.cargo` | `migrated` | Six-table reconciliation and cargo/handling-history invariant |
| `data.carrier-movement` | `migrated` | Reconciliation, schema test, and schedule-order invariant |
| `data.handling-event` | `migrated` | Reconciliation and handling-event reference invariant |
| `data.leg` | `migrated` | Reconciliation and connected-itinerary invariant |
| `data.location` | `migrated` | Six-table reconciliation |
| `data.sequence` | `replaced` | Approved ruling #255; target-native sequence realignment test |
| `data.voyage` | `migrated` | Six-table reconciliation and schedule invariant |

All seven entries use differential verification. The graph path is present for all six mapped tables; the independent Auditor has not yet closed issue #414.

## Ticket reconciliation status

The reconciliation file lists all 21 descendants returned by the epic's sub-issue tree. Fifteen work tickets have merged landing evidence. It also records the superseded coordinator, Auditor, and earlier Verifier attempts, plus open #379, #413, and #414. The file explicitly flags that closed-unmerged PR #388 has no coordinator return at its head, so the required ADR-0030 failed-return evidence for #387 is unavailable. The replacement Auditor #414 and current verification work also remain open; the epic is not ready to close.

## Human check — requested

Compare the legacy snapshot/export against the target's exported rows side by side for each mapped table (`LOCATION`, `VOYAGE`, `CARGO`, `HANDLINGEVENT`, `LEG`, and `CARRIER_MOVEMENT`): preserve source IDs, compare every mapped field including NULLs and timestamps, verify each foreign-key value, and confirm the row counts above. Separately compare the legacy `SEQUENCE` behavior with target-native sequence realignment by checking that the next generated ID after import is greater than the highest imported ID. Review the cargo delivery/history, itinerary continuity, handling-event references, and ordered carrier movements against the target invariants. No human comparison or sign-off is claimed here.

Automated acceptance evidence is green, but ticket reconciliation and independent gate-7 review are not complete. This report does not claim slice completion or human approval.
