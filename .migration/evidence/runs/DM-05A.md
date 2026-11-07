# Run journal: DM-05A

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-07T02:22:36+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T02:22:56+00:00 | snapshot-check | 0 | 0.04 | `python .migration/harness/tools/data_reconcile.py snapshot .migration/data/snapshot` | `bee2f0acd5234102` |  | gate=data-snapshot tables=7 problems=0 |
| 2026-11-07T02:25:01+00:00 | carrier-movement-schema-red | 4 | 3.15 | `pytest -q tests/voyage/test_repository.py::test_carrier_movement_schema_preserves_source_columns_and_references` | `fb63fb0b3413e4b2` | ERROR: found no collectors for /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/tests/voyage/test_repos |  |
