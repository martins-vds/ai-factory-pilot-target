# Run journal: AM-04E

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-08T14:02:32+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-08T14:04:09+00:00 | focused-test | 1 | 2.85 | `pytest -q tests/cargo/interfaces/test_admin_live_map_processing.py` | `ac9ea976eb87c238` | assert initial_cargo.delivery.transport_status.value == 'NOT_RECEIVED' |  |
| 2026-11-08T14:05:43+00:00 | focused-test | 0 | 2.48 | `pytest -q tests/cargo/interfaces/test_admin_live_map_processing.py` | `9beed22cc6e2e126` |  |  |
| 2026-11-08T14:06:06+00:00 | build-compileall | 0 | 0.05 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-08T14:06:11+00:00 | build-check | 0 | 0.36 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-08T14:06:15+00:00 | idiom-check | 0 | 0.03 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-08T14:06:18+00:00 | idiom-format | 1 | 0.03 | `ruff format --check` | `dab386381056ebc9` | 98 \|     assert 'data-coordinates="22,114"' in def789_marker |  |
| 2026-11-08T14:06:26+00:00 | format | 0 | 0.01 | `ruff format tests/cargo/interfaces/test_admin_live_map_processing.py` | `413a709001976657` |  |  |
| 2026-11-08T14:06:29+00:00 | idiom-format | 0 | 0.01 | `ruff format --check` | `2f72b17f517480b5` |  |  |
| 2026-11-08T14:06:34+00:00 | focused-test | 0 | 2.49 | `pytest -q tests/cargo/interfaces/test_admin_live_map_processing.py` | `9beed22cc6e2e126` |  |  |
| 2026-11-08T14:07:49+00:00 | tests | 0 | 70.55 | `pytest -q` | `ffab3bf8dbd743da` |  |  |
| 2026-11-08T14:09:22+00:00 | crap-coverage | 0 | 70.23 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `8a80c5c42f267d2d` |  |  |
| 2026-11-08T14:09:27+00:00 | crap-lizard | 0 | 0.17 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-08T14:09:30+00:00 | crap-score | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `46edc5c319c80c3b` |  | gate=crap max=26.0 threshold=30 over=0 methods=213 |
| 2026-11-08T14:09:34+00:00 | mutation-changed | 0 | 0.08 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `36603172da4a0d74` |  | gate=mutation score=n/a reason=no-mutable-code-changed base=origin/main |
| 2026-11-08T14:12:45+00:00 | tests-final | 0 | 69.31 | `pytest -q` | `c220b0bf30a4ac7d` |  |  |
