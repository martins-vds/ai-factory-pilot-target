# Run journal: AM-04D

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-08T13:20:50+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-08T13:22:50+00:00 | hook-test-red | 1 | 4.41 | `pytest -q tests/cargo/interfaces/test_admin_live_map_templates.py::test_admin_live_map_exposes_a_marker_hook_that_clears_on_each_poll` | `eaa6b71a09427224` | assert response.status_code == 200 |  |
| 2026-11-08T13:22:59+00:00 | hook-test-green | 0 | 2.31 | `pytest -q tests/cargo/interfaces/test_admin_live_map_templates.py::test_admin_live_map_exposes_a_marker_hook_that_clears_on_each_poll` | `448843cb5dffaeac` |  |  |
| 2026-11-08T13:23:38+00:00 | markers-test-red | 1 | 1.59 | `pytest -q tests/cargo/interfaces/test_admin_live_map_markers.py` | `f4e115e3f3740ec6` | >       assert f'data-color="{expected_color}"' in content |  |
| 2026-11-08T13:23:52+00:00 | markers-test-green | 1 | 1.67 | `pytest -q tests/cargo/interfaces/test_admin_live_map_markers.py` | `c96856a97634eeea` | >       assert content.count('data-live-map-marker') == 1 |  |
| 2026-11-08T13:24:00+00:00 | markers-test-green | 0 | 1.67 | `pytest -q tests/cargo/interfaces/test_admin_live_map_markers.py` | `5379ac4e84754275` |  |  |
| 2026-11-08T13:24:07+00:00 | templates-check | 1 | 3.28 | `pytest -q tests/cargo/interfaces/test_admin_live_map_templates.py` | `fe5f61ffbab6bd42` | assert page_response.status_code == 200 |  |
| 2026-11-08T13:24:31+00:00 | markers-green-2 | 0 | 1.86 | `pytest -q tests/cargo/interfaces/test_admin_live_map_markers.py` | `f7031504289b6714` |  |  |
| 2026-11-08T13:24:32+00:00 | templates-green-2 | 1 | 3.45 | `pytest -q tests/cargo/interfaces/test_admin_live_map_templates.py` | `d045e8a2d2184a71` | If 'fail_on_restricted' is False, error won't be raised even if it's |  |
| 2026-11-08T13:24:42+00:00 | templates-green-3 | 0 | 2.81 | `pytest -q tests/cargo/interfaces/test_admin_live_map_templates.py` | `9394ef6123ea1f3c` |  |  |
| 2026-11-08T13:25:00+00:00 | live-map-targeted | 0 | 4.2 | `pytest -q tests/cargo/interfaces/test_admin_live_map_data.py tests/cargo/interfaces/test_admin_live_map_markers.py tests/cargo/interfaces/test_admin_live_map_templates.py` | `d556d0bff0d95c56` |  |  |
