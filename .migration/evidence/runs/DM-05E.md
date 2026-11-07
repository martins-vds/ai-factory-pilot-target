# Run journal: DM-05E

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-07T20:44:45+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T20:45:37+00:00 | snapshot-check | 0 | 0.05 | `python .migration/harness/tools/data_reconcile.py snapshot .migration/data/snapshot` | `bee2f0acd5234102` |  | gate=data-snapshot tables=7 problems=0 |
| 2026-11-07T20:46:00+00:00 | data-load | 1 | 1.2 | `python manage.py load_data_snapshot --snapshot .migration/data/snapshot --mapping .migration/data/mapping.yaml` | `a06a9a1326808ba6` | Traceback (most recent call last): |  |
| 2026-11-07T20:46:15+00:00 | db-migrate | 0 | 0.38 | `python manage.py migrate --noinput` | `56d728c244009843` |  |  |
| 2026-11-07T20:46:18+00:00 | data-load | 0 | 0.32 | `python manage.py load_data_snapshot --snapshot .migration/data/snapshot --mapping .migration/data/mapping.yaml` | `102e06696c233e34` |  |  |
| 2026-11-07T20:46:25+00:00 | data-export | 0 | 0.33 | `python manage.py export_data_snapshot --mapping .migration/data/mapping.yaml --out .migration/data/target-export` | `ba754ea10ff616fb` |  |  |
| 2026-11-07T20:46:29+00:00 | data-reconcile | 0 | 0.06 | `python .migration/harness/tools/data_reconcile.py reconcile --snapshot .migration/data/snapshot --target .migration/data/target-export --mapping .migration/data/mapping.yaml --report .migration/evidence/data-migration/reconciliation.md` | `6a51c3b12234ee83` |  | gate=data-reconcile tables=6 rows=54 mismatched_tables=0 |
| 2026-11-07T20:49:17+00:00 | build-compileall | 0 | 0.05 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T20:49:22+00:00 | build-django-check | 0 | 0.28 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T20:49:25+00:00 | idiom-ruff-check | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T20:49:29+00:00 | idiom-ruff-format | 0 | 0.02 | `ruff format --check` | `05facc7430ea9711` |  |  |
| 2026-11-07T20:50:17+00:00 | behavior | 0 | 44.2 | `pytest -q` | `a88d9e16e649616c` |  |  |
| 2026-11-07T20:51:10+00:00 | crap-coverage | 0 | 47.61 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `234b7551e0037b11` |  |  |
| 2026-11-07T20:51:14+00:00 | crap-lizard | 0 | 0.14 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T20:51:17+00:00 | crap-score | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `5ae953a68cbe67c7` |  | gate=crap max=26.0 threshold=30 over=0 methods=194 |
| 2026-11-07T20:52:00+00:00 | regression | 0 | 40.7 | `pytest -q` | `5cc62609ae8f7159` |  |  |
| 2026-11-07T20:52:04+00:00 | mutation-changed | 0 | 0.06 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `36603172da4a0d74` |  | gate=mutation score=n/a reason=no-mutable-code-changed base=origin/main |
