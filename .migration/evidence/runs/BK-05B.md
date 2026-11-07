# Run journal: BK-05B

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-07T04:09:16+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T04:13:45+00:00 | red-routing | 2 | 1.99 | `pytest -q tests/pathfinder/test_routing.py` | `3c1bad0393671bb2` | ______________ ERROR collecting tests/pathfinder/test_routing.py _______________ |  |
| 2026-11-07T04:14:06+00:00 | routing-service | 0 | 0.77 | `pytest -q tests/pathfinder/test_routing.py` | `689cba347b5af559` |  |  |
