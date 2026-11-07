# Run journal: BK-05C

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-07T16:40:08+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T16:42:53+00:00 | candidate-red | 2 | 2.59 | `pytest -q tests/booking/application/test_routing.py` | `3179e843e9d1b415` | __________ ERROR collecting tests/booking/application/test_routing.py __________ |  |
| 2026-11-07T16:43:24+00:00 | candidate-green | 0 | 1.42 | `pytest -q tests/booking/application/test_routing.py` | `f34bbeaad9b69d77` |  |  |
| 2026-11-07T16:44:03+00:00 | routing-targeted | 0 | 1.66 | `pytest -q tests/booking/application/test_routing.py` | `5fab16bbbfe95d6d` |  |  |
| 2026-11-07T16:44:21+00:00 | routing-targeted-final | 0 | 1.6 | `pytest -q tests/booking/application/test_routing.py` | `2b74d93201e1a766` |  |  |
| 2026-11-07T16:45:21+00:00 | build-compile | 0 | 0.05 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T16:45:22+00:00 | build-django-check | 0 | 0.32 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T16:45:26+00:00 | idiom-ruff-check | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T16:45:26+00:00 | idiom-ruff-format | 1 | 0.02 | `ruff format --check` | `c5799973cf5ac7a2` |  |  |
| 2026-11-07T16:45:32+00:00 | idiom-ruff-check | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T16:45:32+00:00 | idiom-ruff-format | 0 | 0.01 | `ruff format --check` | `b200c2b9a71ab204` |  |  |
| 2026-11-07T16:45:39+00:00 | behavior | 2 | 1.96 | `pytest -q` | `77116fc577637b30` | ______________ ERROR collecting tests/pathfinder/test_routing.py _______________ |  |
| 2026-11-07T17:21:41+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T17:23:27+00:00 | behavior | 0 | 25.41 | `pytest -q` | `b062d3162cd12ed3` |  |  |
| 2026-11-07T17:24:07+00:00 | regression | 0 | 25.08 | `pytest -q` | `28ab10fd14d00307` |  |  |
| 2026-11-07T17:24:38+00:00 | crap-coverage | 0 | 24.51 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `7deb901f9bf73a64` |  |  |
| 2026-11-07T17:24:41+00:00 | crap-lizard | 0 | 0.08 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T17:24:44+00:00 | crap-score | 0 | 0.03 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `33a2d7a0b3756fa4` |  | gate=crap max=19.0 threshold=30 over=0 methods=160 |
| 2026-11-07T17:24:57+00:00 | mutation-changed | 0 | 9.6 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `49769f89644d20b0` |  | gate=mutation score=0.929 threshold=0.8 killed=13 survived=1 files=1 base=origin/main |
