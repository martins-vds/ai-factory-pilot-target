# Run journal: BK-05B

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-07T04:09:16+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T04:13:45+00:00 | red-routing | 2 | 1.99 | `pytest -q tests/pathfinder/test_routing.py` | `3c1bad0393671bb2` | ______________ ERROR collecting tests/pathfinder/test_routing.py _______________ |  |
| 2026-11-07T04:14:06+00:00 | routing-service | 0 | 0.77 | `pytest -q tests/pathfinder/test_routing.py` | `689cba347b5af559` |  |  |
| 2026-11-07T04:14:50+00:00 | red-pathfinder-api | 2 | 0.59 | `pytest -q tests/pathfinder/test_api.py` | `e2c8c9cdf835cd06` | ________________ ERROR collecting tests/pathfinder/test_api.py _________________ |  |
| 2026-11-07T04:15:05+00:00 | pathfinder-tests | 0 | 0.87 | `pytest -q tests/pathfinder` | `a97fe8d679efa4e9` |  |  |
| 2026-11-07T04:15:48+00:00 | pathfinder-tests | 0 | 0.8 | `pytest -q tests/pathfinder` | `d5d6c7e3d74efa9f` |  |  |
| 2026-11-07T04:17:33+00:00 | idiom-ruff-check | 1 | 0.02 | `ruff check` | `35e1ef8de2e4d81f` | 44 \|                 assert parsed.utcoffset() == timedelta(0) |  |
| 2026-11-07T04:18:02+00:00 | idiom-ruff-check-diagnostic | 1 | 0.01 | `ruff check` | `35e1ef8de2e4d81f` | 44 \|                 assert parsed.utcoffset() == timedelta(0) |  |
| 2026-11-07T04:18:46+00:00 | idiom-ruff-check | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T04:18:55+00:00 | idiom-format-check | 1 | 0.03 | `ruff format --check` | `a3d3652e21b3aa24` | 26 \|         assert all( |  |
| 2026-11-07T04:19:03+00:00 | idiom-format-check | 0 | 0.01 | `ruff format --check` | `273e81e5999dffa5` |  |  |
| 2026-11-07T04:19:07+00:00 | pathfinder-tests | 0 | 0.8 | `pytest -q tests/pathfinder` | `f891ca4c15593a9c` |  |  |
