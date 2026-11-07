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
