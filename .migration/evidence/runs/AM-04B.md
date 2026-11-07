# Run journal: AM-04B

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-07T04:17:05+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T04:19:45+00:00 | red-all-cargo-data | 2 | 2.14 | `pytest -q tests/cargo/interfaces/test_admin_live_map_data.py` | `14ffb7e522c6d9a2` | _____ ERROR collecting tests/cargo/interfaces/test_admin_live_map_data.py ______ |  |
| 2026-11-07T04:20:02+00:00 | green-all-cargo-data | 0 | 1.41 | `pytest -q tests/cargo/interfaces/test_admin_live_map_data.py` | `38e13be45293b3a0` |  |  |
