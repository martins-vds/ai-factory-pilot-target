# Run journal: AM-04D

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-08T13:20:50+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-08T13:22:50+00:00 | hook-test-red | 1 | 4.41 | `pytest -q tests/cargo/interfaces/test_admin_live_map_templates.py::test_admin_live_map_exposes_a_marker_hook_that_clears_on_each_poll` | `eaa6b71a09427224` | assert response.status_code == 200 |  |
| 2026-11-08T13:22:59+00:00 | hook-test-green | 0 | 2.31 | `pytest -q tests/cargo/interfaces/test_admin_live_map_templates.py::test_admin_live_map_exposes_a_marker_hook_that_clears_on_each_poll` | `448843cb5dffaeac` |  |  |
