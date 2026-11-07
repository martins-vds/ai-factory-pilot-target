# Run journal: DM-05D

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-07T18:23:05+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T18:25:57+00:00 | focused-tests-red | 1 | 3.71 | `pytest -q tests/data_migration/test_export.py` | `22ed5e1e4222ac2b` | E               KeyError: 'export_data_snapshot' |  |
| 2026-11-07T18:26:45+00:00 | focused-tests-green | 1 | 1.83 | `pytest -q tests/data_migration/test_export.py` | `4ff492f89c5a2b65` | >           assert reader.fieldnames == ['id', 'unlocode', 'name'] |  |
| 2026-11-07T18:26:59+00:00 | focused-tests-green | 0 | 1.82 | `pytest -q tests/data_migration/test_export.py` | `e72d445d99fd8599` |  |  |
| 2026-11-07T18:27:47+00:00 | idiom-ruff-check | 0 | 0.06 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T18:27:47+00:00 | idiom-ruff-format | 1 | 0.04 | `ruff format --check` | `9579572f2b14114c` |  |  |
| 2026-11-07T18:27:47+00:00 | build-compileall | 0 | 0.12 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T18:27:48+00:00 | build-django-check | 0 | 0.41 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T18:27:55+00:00 | idiom-ruff-format-rerun | 0 | 0.01 | `ruff format --check` | `c7a0bcb17dd5241a` |  |  |
| 2026-11-07T18:28:48+00:00 | behavior | 0 | 50.05 | `pytest -q` | `d0990b68bdbcbeb6` |  |  |
| 2026-11-07T18:29:41+00:00 | crap-coverage | 0 | 46.62 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `18f2ce24c0bac4a6` |  |  |
| 2026-11-07T18:29:44+00:00 | crap-lizard | 0 | 0.16 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T18:29:48+00:00 | crap-score | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `3b66fdac6c140535` |  | gate=crap max=26.0 threshold=30 over=0 methods=186 |
