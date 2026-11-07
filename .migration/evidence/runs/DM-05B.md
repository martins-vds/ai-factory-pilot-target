# Run journal: DM-05B

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-07T03:49:34+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T03:50:47+00:00 | snapshot-check | 0 | 0.06 | `python .migration/harness/tools/data_reconcile.py snapshot .migration/data/snapshot` | `bee2f0acd5234102` |  | gate=data-snapshot tables=7 problems=0 |
| 2026-11-07T03:51:33+00:00 | migration-state | 0 | 1.2 | `python .migration/harness/tools/validate.py .migration` | `b0b54d83fe440639` |  |  |
| 2026-11-07T03:51:33+00:00 | snapshot-check-final | 0 | 0.06 | `python .migration/harness/tools/data_reconcile.py snapshot .migration/data/snapshot` | `bee2f0acd5234102` |  | gate=data-snapshot tables=7 problems=0 |
| 2026-11-07T03:52:34+00:00 | migration-state-final | 0 | 1.2 | `python .migration/harness/tools/validate.py .migration` | `6b717156df9fe00c` |  |  |
| 2026-11-07T04:15:03+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T04:18:14+00:00 | snapshot-check | 0 | 0.06 | `python .migration/harness/tools/data_reconcile.py snapshot .migration/data/snapshot` | `bee2f0acd5234102` |  | gate=data-snapshot tables=7 problems=0 |
| 2026-11-07T04:18:29+00:00 | build-compileall | 0 | 0.08 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T04:18:34+00:00 | build-django-check | 0 | 1.3 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T04:19:31+00:00 | behavior-tests | 0 | 54.02 | `pytest -q` | `c3ab17f3eac20a2e` |  |  |
| 2026-11-07T04:19:34+00:00 | idiom-ruff-check | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T04:19:37+00:00 | idiom-ruff-format | 0 | 0.02 | `ruff format --check` | `184b6bfbf75ff0af` |  |  |
| 2026-11-07T04:20:25+00:00 | crap-coverage | 0 | 44.51 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `3cb293849ec033d3` |  |  |
| 2026-11-07T04:20:28+00:00 | crap-lizard | 0 | 0.14 | `lizard --csv src` | `9bbde6d92b167ffe` |  |  |
| 2026-11-07T04:20:32+00:00 | crap-score | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `90405ac9114fd401` |  | gate=crap max=14.0 threshold=30 over=0 methods=4 |
| 2026-11-07T04:20:36+00:00 | mutation-changed | 0 | 0.08 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `36603172da4a0d74` |  | gate=mutation score=n/a reason=no-mutable-code-changed base=origin/main |
| 2026-11-07T04:21:22+00:00 | regression-tests | 0 | 43.01 | `pytest -q` | `582cdbe93e55b0ff` |  |  |
