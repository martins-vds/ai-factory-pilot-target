# Run journal: DM-AUDIT

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-07T23:20:27+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T23:21:14+00:00 | DM-05F-invariants | 0 | 4.72 | `pytest -q tests/data_migration/test_invariants.py` | `44cc03476d246aff` |  |  |
| 2026-11-07T23:21:28+00:00 | DM-05E-load | 1 | 0.45 | `python manage.py load_data_snapshot --snapshot .migration/data/snapshot --mapping .migration/data/mapping.yaml` | `a06a9a1326808ba6` | Traceback (most recent call last): |  |
| 2026-11-07T23:21:34+00:00 | DM-05E-schema-migrate | 0 | 0.49 | `python manage.py migrate --noinput` | `56d728c244009843` |  |  |
| 2026-11-07T23:21:42+00:00 | DM-05E-load | 0 | 0.43 | `python manage.py load_data_snapshot --snapshot .migration/data/snapshot --mapping .migration/data/mapping.yaml` | `102e06696c233e34` |  |  |
| 2026-11-07T23:21:45+00:00 | DM-05E-export | 0 | 0.44 | `python manage.py export_data_snapshot --mapping .migration/data/mapping.yaml --out .migration/runs/DM-AUDIT/target-export` | `ba754ea10ff616fb` |  |  |
| 2026-11-07T23:21:49+00:00 | DM-05E-reconcile | 0 | 0.08 | `python .migration/harness/tools/data_reconcile.py reconcile --snapshot .migration/data/snapshot --target .migration/runs/DM-AUDIT/target-export --mapping .migration/data/mapping.yaml --report .migration/runs/DM-AUDIT/reconciliation-current.md` | `6a51c3b12234ee83` |  | gate=data-reconcile tables=6 rows=54 mismatched_tables=0 |
| 2026-11-07T23:22:20+00:00 | DM-sequence-replacement | 0 | 2.02 | `pytest -q tests/data_migration/test_load.py::test_load_snapshot_realigns_each_sequence_to_max_plus_one` | `6c677bdc128b19c8` |  |  |
