# Run journal: BK-05F

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-07T23:07:47+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T23:07:55+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T23:10:51+00:00 | route-ui-populated-red | 4 | 2.65 | `pytest -q tests/booking/interfaces/test_route_selection.py::test_route_selection_renders_populated_candidates_and_numbered_legs` | `b4cc25268b09cfd2` | ERROR: found no collectors for /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/tests/booking/interface |  |
| 2026-11-07T23:11:21+00:00 | route-ui-populated-green | 1 | 1.44 | `pytest -q tests/booking/interfaces/test_route_selection.py::test_route_selection_renders_populated_candidates_and_numbered_legs` | `30e0c6f92a86ec56` | assert response.status_code == 200 |  |
| 2026-11-07T23:11:30+00:00 | route-ui-populated-green | 0 | 1.44 | `pytest -q tests/booking/interfaces/test_route_selection.py::test_route_selection_renders_populated_candidates_and_numbered_legs` | `f51873a8b2568bb4` |  |  |
