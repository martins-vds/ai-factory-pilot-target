# Run journal: BK-05F

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-07T23:07:47+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T23:07:55+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T23:10:51+00:00 | route-ui-populated-red | 4 | 2.65 | `pytest -q tests/booking/interfaces/test_route_selection.py::test_route_selection_renders_populated_candidates_and_numbered_legs` | `b4cc25268b09cfd2` | ERROR: found no collectors for /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/tests/booking/interface |  |
| 2026-11-07T23:11:21+00:00 | route-ui-populated-green | 1 | 1.44 | `pytest -q tests/booking/interfaces/test_route_selection.py::test_route_selection_renders_populated_candidates_and_numbered_legs` | `30e0c6f92a86ec56` | assert response.status_code == 200 |  |
| 2026-11-07T23:11:30+00:00 | route-ui-populated-green | 0 | 1.44 | `pytest -q tests/booking/interfaces/test_route_selection.py::test_route_selection_renders_populated_candidates_and_numbered_legs` | `f51873a8b2568bb4` |  |  |
| 2026-11-07T23:11:57+00:00 | route-ui-empty-state | 0 | 1.45 | `pytest -q tests/booking/interfaces/test_route_selection.py::test_route_screens_explain_when_no_candidates_satisfy_the_deadline` | `baa6efe8d11cd56d` |  |  |
| 2026-11-07T23:12:05+00:00 | select-itinerary-candidates | 0 | 1.47 | `pytest -q tests/booking/interfaces/test_route_selection.py::test_select_itinerary_renders_candidate_routes_when_available` | `7b23e52dabef120c` |  |  |
| 2026-11-07T23:12:16+00:00 | route-assignment-red | 1 | 1.5 | `pytest -q tests/booking/interfaces/test_route_selection.py::test_assigning_candidate_redirects_to_details_with_the_selected_itinerary` | `d87db90c076ef66a` | E       IndexError: list index out of range |  |
| 2026-11-07T23:12:40+00:00 | route-assignment-green | 0 | 1.45 | `pytest -q tests/booking/interfaces/test_route_selection.py::test_assigning_candidate_redirects_to_details_with_the_selected_itinerary` | `baa6efe8d11cd56d` |  |  |
| 2026-11-07T23:12:50+00:00 | route-ui-tests | 0 | 1.61 | `pytest -q tests/booking/interfaces/test_route_selection.py` | `7bbfa9adac667373` |  |  |
| 2026-11-07T23:13:36+00:00 | route-ui-focused-tests | 0 | 1.79 | `pytest -q tests/booking/interfaces/test_route_selection.py` | `8c4b2d4a4d13e6aa` |  |  |
