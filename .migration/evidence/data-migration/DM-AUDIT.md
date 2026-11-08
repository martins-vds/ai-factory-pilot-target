# DM-AUDIT — gate 7 capability coverage

## Scope and evidence

Audited the data-migration slice at `3d1fcec13586c2d89b7a079bfd14ca011e2522c0`.
The successful Actions run is
[42427856017, attempt 1](https://github.com/martins-vds/ai-factory-pilot-target/actions/runs/42427856017),
artifact `afs-acceptance-3d1fcec13586c2d89b7a079bfd14ca011e2522c0-42427856017-1`.
`afs-acceptance verify` passed for that commit, run, and attempt. Its target graph under
`.migration/runs/downloaded-artifact/graph/target/full` is stamped for the audited commit; this
report does not rely on the committed target graph.

`check_graph_fresh.py --require source` passed. `graph_gate.py --side source` passed with 1,054
nodes, 2,139 edges, and zero failures.

The verified target graph has 526 nodes and 1,270 edges. Its
`.migration/runs/downloaded-artifact/graph/target/full/graph-check.md` entry for
`command=load_data_snapshot` reads:

> `load_data_snapshot` →writes_to `location` — reaches 6 data node(s): HandlingEvent, cargo,
> carrier_movement, leg, location, voyage

## Data capability checks

| Ledger entry | Target component(s) | In `load_data_snapshot` reached list | Evidence |
|---|---|---|---|
| `data.cargo` | `CargoRecord`, `LegRecord` (`src/cargotracker/cargo/infrastructure/models.py`) | `cargo` | Reconciliation: 4 rows, matching checksums. DM-05F invariant tests passed. |
| `data.carrier-movement` | `CarrierMovementRecord` (`src/cargotracker/voyage/infrastructure/models.py`) | `carrier_movement` | Reconciliation: 13 rows, matching checksums. Schedule-order invariant passed. |
| `data.handling-event` | `HandlingEventRecord` (`src/cargotracker/handling/infrastructure/models.py`) | `HandlingEvent` | Reconciliation: 12 rows, matching checksums. Handling reference invariant passed. |
| `data.leg` | `LegRecord` (`src/cargotracker/cargo/infrastructure/models.py`) | `leg` | Reconciliation: 7 rows, matching checksums. Connected-itinerary invariant passed. |
| `data.location` | `LocationRecord` (`src/cargotracker/location/infrastructure/models.py`) | `location` | Reconciliation: 13 rows, matching checksums. DM-05F invariant tests passed. |
| `data.sequence` | No target table by design; target-native sequences are realigned after import | Not applicable: this provider metadata table is replaced, not loaded as a target data table | The divergence is approved by issue #255. `tests/data_migration/test_load.py::test_load_snapshot_realigns_each_sequence_to_max_plus_one` passed as part of DM-05F. |
| `data.voyage` | `VoyageRecord` (`src/cargotracker/voyage/infrastructure/models.py`) | `voyage` | Reconciliation: 5 rows, matching checksums. Handling and carrier-movement invariants passed. |

The six mapped target tables are all reached by the loader. The source `SEQUENCE` provider table
is the sole non-table counterpart: `.migration/ledger/data.sequence.yaml` records its approved
replacement, and `.migration/evidence/data-migration/reconciliation.md` documents exclusion of
its one source row because PostgreSQL-native sequences are realigned after importing explicit
IDs. No target-table reachability is expected for that approved replacement.

## Fresh evidence

All commands below ran through `afs-run`; the durable records are in
`.migration/evidence/runs/DM-AUDIT.md`.

- Snapshot preflight: passed, 7 snapshot tables and no problems.
- Schema migration and snapshot load: passed; 54 rows loaded across 6 mapped tables.
- Target export: passed; 54 rows exported across 6 mapped tables.
- Reconciliation: passed; 6 tables, 54 rows, zero mismatches, and no dangling references.
- DM-05F invariant suite: passed, 4 tests.

The generated fresh reconciliation is in the ignored run directory
`.migration/runs/DM-AUDIT-reconciliation.md`; the committed DM-AUDIT journal records the command
and result. Existing committed DM-05E/DM-05F journals and reconciliation report provide prior
context; this verdict is based on the fresh runs above.

## Gap classification and verdict

- Missing capability: none. The approved `SEQUENCE` replacement preserves sequence allocation.
- Misplaced responsibility: none found.
- Broken flow: none; all six mapped tables are reachable from the loader.
- Missing integration: none found.
- Untested path: none; reconciliation and invariant evidence passed in this audit.
- Graph inconsistencies: none. The source graph is fresh, and the audited target graph is verified
  for the audited commit.

**Verdict: complete.** All seven `data.*` entries were checked. Six mapped tables have target
components, graph reachability, and passing fresh evidence; the seventh is a documented,
human-approved transformation rather than a missing target table.
