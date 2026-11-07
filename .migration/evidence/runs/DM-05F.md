# Run journal: DM-05F

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-07T18:23:25+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T18:24:55+00:00 | snapshot-preflight | 0 | 0.07 | `python .migration/harness/tools/data_reconcile.py snapshot .migration/data/snapshot` | `bee2f0acd5234102` |  | gate=data-snapshot tables=7 problems=0 |
| 2026-11-07T18:25:01+00:00 | data-load | 1 | 1.47 | `python manage.py load_data_snapshot --snapshot .migration/data/snapshot --mapping .migration/data/mapping.yaml` | `a06a9a1326808ba6` | Traceback (most recent call last): |  |
| 2026-11-07T18:25:08+00:00 | schema-migrate | 0 | 0.64 | `python manage.py migrate --noinput` | `56d728c244009843` |  |  |
| 2026-11-07T18:25:09+00:00 | data-load | 0 | 0.56 | `python manage.py load_data_snapshot --snapshot .migration/data/snapshot --mapping .migration/data/mapping.yaml` | `102e06696c233e34` |  |  |
| 2026-11-07T18:27:56+00:00 | invariants-red | 1 | 3.43 | `pytest -q tests/data_migration/test_invariants.py` | `09e0ee6d31763de3` | E           ValueError: 'AAA01' is not a valid UN/LOCODE |  |
| 2026-11-07T18:28:08+00:00 | invariants-green | 1 | 2.65 | `pytest -q tests/data_migration/test_invariants.py` | `6b1991a96cb39e50` | assert len(cargos) == CargoRecord.objects.count() == 2 |  |
| 2026-11-07T18:28:25+00:00 | invariants-green-2 | 0 | 2.58 | `pytest -q tests/data_migration/test_invariants.py` | `df589a78f8a8b32b` |  |  |
| 2026-11-07T18:28:44+00:00 | build-compile | 0 | 0.06 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T18:28:45+00:00 | build-check | 0 | 0.42 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T18:28:45+00:00 | idiom-ruff | 1 | 0.03 | `ruff check` | `2eb5cc1c405d57dd` | 318 \|         assert len(movements) == 2 |  |
| 2026-11-07T18:28:55+00:00 | idiom-ruff-rerun | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T18:28:55+00:00 | idiom-format | 0 | 0.02 | `ruff format --check` | `1e2a3e2494e870c6` |  |  |
| 2026-11-07T18:28:57+00:00 | invariants-final | 0 | 2.61 | `pytest -q tests/data_migration/test_invariants.py` | `28456d16762f935e` |  |  |
