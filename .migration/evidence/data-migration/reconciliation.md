# Data reconciliation

- Snapshot: derby · taken 2026-11-07T00:40:49Z by martins-vds

| Target table | Source | Rows (snapshot / target) | Checksums match | Problems |
|---|---|---|---|---|
| `location` | `LOCATION` | 13 / 13 | yes | none |
| `voyage` | `VOYAGE` | 5 / 5 | yes | none |
| `cargo` | `CARGO` | 4 / 4 | yes | none |
| `HandlingEvent` | `HANDLINGEVENT` | 12 / 12 | yes | none |
| `leg` | `LEG` | 7 / 7 | yes | none |
| `carrier_movement` | `CARRIER_MOVEMENT` | 13 / 13 | yes | none |

## Rehearsal

The approved `data.load` and `data.export` commands were run against this snapshot before reconciliation. The run is repeatable with those profile commands and the mapping above.

Snapshot manifest counts: CARGO 4, CARRIER_MOVEMENT 13, HANDLINGEVENT 12, LEG 7, LOCATION 13, SEQUENCE 1, VOYAGE 5 (taken 2026-11-07T00:40:49Z).

`SEQUENCE` is excluded from row comparison per ruling #255: source IDs are loaded explicitly and the target's PostgreSQL-native sequences are realigned during loading. All six mapped tables (54 rows) matched on row count and checksum; no reference problems were reported.
