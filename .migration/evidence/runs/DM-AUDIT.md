# Run journal: DM-AUDIT

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-08T01:32:55+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-08T01:34:36+00:00 | snapshot-preflight | 0 | 0.06 | `python .migration/harness/tools/data_reconcile.py snapshot .migration/data/snapshot` | `bee2f0acd5234102` |  | gate=data-snapshot tables=7 problems=0 |
| 2026-11-08T01:34:37+00:00 | schema-migrate | 0 | 1.39 | `python manage.py migrate --noinput` | `56d728c244009843` |  |  |
| 2026-11-08T01:34:38+00:00 | data-load | 0 | 0.43 | `python manage.py load_data_snapshot --snapshot .migration/data/snapshot --mapping .migration/data/mapping.yaml` | `102e06696c233e34` |  |  |
| 2026-11-08T01:34:39+00:00 | data-export | 0 | 0.42 | `python manage.py export_data_snapshot --mapping .migration/data/mapping.yaml --out .migration/runs/DM-AUDIT-target-export` | `ba754ea10ff616fb` |  |  |
| 2026-11-08T01:34:39+00:00 | data-reconcile | 0 | 0.08 | `python .migration/harness/tools/data_reconcile.py reconcile --snapshot .migration/data/snapshot --target .migration/runs/DM-AUDIT-target-export --mapping .migration/data/mapping.yaml --report .migration/runs/DM-AUDIT-reconciliation.md` | `6a51c3b12234ee83` |  | gate=data-reconcile tables=6 rows=54 mismatched_tables=0 |
| 2026-11-08T01:34:42+00:00 | invariant-tests | 0 | 3.34 | `pytest -q tests/data_migration/test_invariants.py` | `b2dbdcf691b44ca3` |  |  |
