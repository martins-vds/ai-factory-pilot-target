# Run journal: DM-ACCEPT

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-07T21:43:08+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T21:44:54+00:00 | snapshot-validation | 0 | 0.06 | `python .migration/harness/tools/data_reconcile.py snapshot .migration/data/snapshot` | `bee2f0acd5234102` |  | gate=data-snapshot tables=7 problems=0 |
| 2026-11-07T21:45:08+00:00 | data-load | 1 | 1.1 | `python manage.py load_data_snapshot --snapshot .migration/data/snapshot --mapping .migration/data/mapping.yaml` | `a06a9a1326808ba6` | Traceback (most recent call last): |  |
| 2026-11-07T21:45:27+00:00 | migrate-db | 0 | 0.47 | `python manage.py migrate --noinput` | `56d728c244009843` |  |  |
| 2026-11-07T21:45:32+00:00 | data-load | 0 | 0.4 | `python manage.py load_data_snapshot --snapshot .migration/data/snapshot --mapping .migration/data/mapping.yaml` | `102e06696c233e34` |  |  |
| 2026-11-07T21:45:36+00:00 | data-export | 0 | 0.4 | `python manage.py export_data_snapshot --mapping .migration/data/mapping.yaml --out .migration/data/target-export` | `ba754ea10ff616fb` |  |  |
| 2026-11-07T21:45:40+00:00 | data-reconcile | 0 | 0.08 | `python .migration/harness/tools/data_reconcile.py reconcile --snapshot .migration/data/snapshot --target .migration/data/target-export --mapping .migration/data/mapping.yaml --report .migration/evidence/data-migration/acceptance.md` | `6a51c3b12234ee83` |  | gate=data-reconcile tables=6 rows=54 mismatched_tables=0 |
| 2026-11-07T21:45:47+00:00 | data-invariants | 0 | 2.81 | `pytest -q tests/data_migration/test_invariants.py` | `4f05905e932ff95f` |  |  |
| 2026-11-07T21:45:54+00:00 | build-compile | 0 | 0.05 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T21:45:57+00:00 | build-check | 0 | 0.35 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T21:46:00+00:00 | idiom-ruff-check | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T21:46:03+00:00 | idiom-format-check | 0 | 0.02 | `ruff format --check` | `27b0eb549ee60b2d` |  |  |
