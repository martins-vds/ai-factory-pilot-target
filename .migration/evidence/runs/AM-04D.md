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
| 2026-11-08T13:25:27+00:00 | idiom-ruff-check | 0 | 0.05 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-08T13:25:27+00:00 | idiom-ruff-format | 0 | 0.05 | `ruff format --check` | `507ad0521c6e9ec2` |  |  |
| 2026-11-08T13:25:27+00:00 | build-compile | 0 | 0.09 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-08T13:25:27+00:00 | build-check | 0 | 0.41 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-08T13:26:36+00:00 | tests | 0 | 65.19 | `pytest -q` | `0fa5beee4959f625` |  |  |
| 2026-11-08T13:27:55+00:00 | crap-coverage | 0 | 74.92 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `a5fd5905ddd010ce` |  |  |
| 2026-11-08T13:28:00+00:00 | crap-lizard | 0 | 0.16 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-08T13:28:03+00:00 | crap | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `46edc5c319c80c3b` |  | gate=crap max=26.0 threshold=30 over=0 methods=213 |
| 2026-11-08T13:28:08+00:00 | mutation-changed | 0 | 0.08 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `36603172da4a0d74` |  | gate=mutation score=n/a reason=no-mutable-code-changed base=origin/main |
| 2026-11-08T13:28:52+00:00 | endpoint-test | 0 | 2.4 | `pytest -q tests/cargo/interfaces/test_admin_live_map_markers.py::test_admin_live_map_marker_poll_renders_current_cargo_with_booking_link` | `c3875cce419d1114` |  |  |
