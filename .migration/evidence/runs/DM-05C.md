# Run journal: DM-05C

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-07T05:14:19+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T05:15:05+00:00 | snapshot | 0 | 0.06 | `python .migration/harness/tools/data_reconcile.py snapshot .migration/data/snapshot` | `bee2f0acd5234102` |  | gate=data-snapshot tables=7 problems=0 |
| 2026-11-07T05:16:58+00:00 | loader-red | 1 | 3.13 | `pytest -q tests/data_migration/test_load.py` | `c29933f1f16abc82` | E               KeyError: 'load_data_snapshot' |  |
| 2026-11-07T05:18:03+00:00 | loader-green | 1 | 1.64 | `pytest -q tests/data_migration/test_load.py` | `24aadeb264b70940` | # Daft, but matches old exception sans the err msg. |  |
| 2026-11-07T05:18:23+00:00 | loader-green-2 | 0 | 1.56 | `pytest -q tests/data_migration/test_load.py` | `d44de49cc8aa128c` |  |  |
| 2026-11-07T05:18:31+00:00 | data-load | 1 | 0.39 | `python manage.py load_data_snapshot --snapshot .migration/data/snapshot --mapping .migration/data/mapping.yaml` | `3d0e4f7dc207cab6` | Traceback (most recent call last): |  |
| 2026-11-07T05:18:38+00:00 | migrate-db | 0 | 0.47 | `python manage.py migrate --noinput` | `56d728c244009843` |  |  |
| 2026-11-07T05:18:42+00:00 | data-load-2 | 0 | 0.39 | `python manage.py load_data_snapshot --snapshot .migration/data/snapshot --mapping .migration/data/mapping.yaml` | `102e06696c233e34` |  |  |
| 2026-11-07T05:19:43+00:00 | data-load-rerun | 0 | 0.42 | `python manage.py load_data_snapshot --snapshot .migration/data/snapshot --mapping .migration/data/mapping.yaml` | `102e06696c233e34` |  |  |
| 2026-11-07T05:19:47+00:00 | build-compile | 0 | 0.04 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T05:19:50+00:00 | build-check | 0 | 0.34 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T05:19:53+00:00 | idiom-ruff | 1 | 0.02 | `ruff check` | `996a433aeb71085f` |  |  |
| 2026-11-07T05:20:27+00:00 | idiom-ruff-2 | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T05:20:30+00:00 | idiom-format | 1 | 0.02 | `ruff format --check` | `307b7d568fbd28b7` | 158 \|     except OSError as error: |  |
| 2026-11-07T05:20:44+00:00 | idiom-format-2 | 0 | 0.01 | `ruff format --check` | `c98b86154f37b741` |  |  |
| 2026-11-07T05:20:54+00:00 | loader-regression | 0 | 1.57 | `pytest -q tests/data_migration/test_load.py` | `b29404b0332b987b` |  |  |
| 2026-11-07T05:21:39+00:00 | behavior | 1 | 41.18 | `pytest -q` | `5c979d86dc6e3f05` | assert settings.BASE_DIR == Path(__file__).resolve().parents[1] |  |
| 2026-11-07T05:51:33+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
