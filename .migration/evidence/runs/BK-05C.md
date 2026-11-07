# Run journal: BK-05C

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-07T16:40:08+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T16:42:53+00:00 | candidate-red | 2 | 2.59 | `pytest -q tests/booking/application/test_routing.py` | `3179e843e9d1b415` | __________ ERROR collecting tests/booking/application/test_routing.py __________ |  |
| 2026-11-07T16:43:24+00:00 | candidate-green | 0 | 1.42 | `pytest -q tests/booking/application/test_routing.py` | `f34bbeaad9b69d77` |  |  |
