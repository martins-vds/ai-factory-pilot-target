# Run journal: DM-05A

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-07T02:22:36+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T02:22:56+00:00 | snapshot-check | 0 | 0.04 | `python .migration/harness/tools/data_reconcile.py snapshot .migration/data/snapshot` | `bee2f0acd5234102` |  | gate=data-snapshot tables=7 problems=0 |
| 2026-11-07T02:25:01+00:00 | carrier-movement-schema-red | 4 | 3.15 | `pytest -q tests/voyage/test_repository.py::test_carrier_movement_schema_preserves_source_columns_and_references` | `fb63fb0b3413e4b2` | ERROR: found no collectors for /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/tests/voyage/test_repos |  |
| 2026-11-07T02:25:33+00:00 | carrier-movement-schema-green | 0 | 1.24 | `pytest -q tests/voyage/test_repository.py::test_carrier_movement_schema_preserves_source_columns_and_references` | `f34bbeaad9b69d77` |  |  |
| 2026-11-07T02:26:10+00:00 | migration-state | 0 | 0.25 | `python manage.py makemigrations --check --dry-run` | `a2bfa7b376c38062` |  |  |
| 2026-11-07T02:26:16+00:00 | voyage-tests | 0 | 1.09 | `pytest -q tests/voyage` | `48e968ff39de4a93` |  |  |
| 2026-11-07T02:26:43+00:00 | build-compile | 0 | 0.03 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T02:26:43+00:00 | build-check | 0 | 0.23 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T02:26:43+00:00 | idiom-ruff-check | 1 | 0.02 | `ruff check` | `1799ceff487de515` |  |  |
| 2026-11-07T02:26:58+00:00 | idiom-ruff-check-rerun | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T02:26:58+00:00 | idiom-ruff-format | 1 | 0.02 | `ruff format --check` | `8deaa73bbea1d552` |  |  |
| 2026-11-07T02:27:02+00:00 | idiom-ruff-format | 0 | 0.01 | `ruff format --check` | `184b6bfbf75ff0af` |  |  |
| 2026-11-07T02:27:32+00:00 | behavior | 0 | 26.83 | `pytest -q` | `da3b7723990f6d4b` |  |  |
| 2026-11-07T02:27:59+00:00 | regression | 0 | 27.0 | `pytest -q` | `5c433f3b4a730f22` |  |  |
| 2026-11-07T02:28:32+00:00 | crap-pytest | 0 | 28.3 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `23f09ecafd4299f3` |  |  |
| 2026-11-07T02:28:32+00:00 | crap-lizard | 0 | 0.08 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T02:28:32+00:00 | crap-score | 0 | 0.03 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `34d1ce024bdfe792` |  | gate=crap max=19.0 threshold=30 over=0 methods=132 |
| 2026-11-07T02:28:56+00:00 | mutation-changed | 0 | 18.63 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `936ef0be3bf9d31e` |  | gate=mutation score=0.870 threshold=0.8 killed=20 survived=3 files=2 base=origin/main |
| 2026-11-07T02:29:40+00:00 | build-compile-final | 0 | 0.02 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T02:29:40+00:00 | build-check-final | 0 | 0.24 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T02:29:40+00:00 | idiom-ruff-check-final | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T02:29:41+00:00 | idiom-ruff-format-final | 0 | 0.01 | `ruff format --check` | `184b6bfbf75ff0af` |  |  |
| 2026-11-07T02:29:41+00:00 | migration-state-final | 0 | 0.27 | `python manage.py makemigrations --check --dry-run` | `a2bfa7b376c38062` |  |  |
| 2026-11-07T03:00:49+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
