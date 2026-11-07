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
| 2026-11-07T23:14:04+00:00 | build-compile | 0 | 0.06 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T23:14:08+00:00 | build-django-check | 0 | 0.29 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T23:14:11+00:00 | idiom-ruff-check | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T23:14:13+00:00 | idiom-ruff-format | 0 | 0.02 | `ruff format --check` | `c3ac60a207092b7f` |  |  |
| 2026-11-07T23:15:02+00:00 | behavior | 0 | 44.5 | `pytest -q` | `2cd8216bb3af3078` |  |  |
| 2026-11-07T23:15:51+00:00 | crap-coverage | 0 | 43.73 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `ee3d9f5a93695ee8` |  |  |
| 2026-11-07T23:15:54+00:00 | crap-lizard | 0 | 0.12 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T23:15:58+00:00 | crap-score | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `c1f7b4ca904f936a` |  | gate=crap max=26.0 threshold=30 over=0 methods=208 |
| 2026-11-07T23:16:58+00:00 | mutation-changed | 0 | 56.53 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `0a4bcffd98d4085f` |  | gate=mutation score=0.828 threshold=0.8 killed=48 survived=10 files=1 base=origin/main |
| 2026-11-07T23:19:39+00:00 | no-route-guidance-red | 1 | 1.61 | `pytest -q tests/booking/interfaces/test_route_selection.py::test_route_screens_explain_when_no_candidates_satisfy_the_deadline` | `45ce6ef361911e1f` | assert route_response.status_code == 200 |  |
| 2026-11-07T23:19:50+00:00 | no-route-guidance-green | 0 | 1.44 | `pytest -q tests/booking/interfaces/test_route_selection.py::test_route_screens_explain_when_no_candidates_satisfy_the_deadline` | `baa6efe8d11cd56d` |  |  |
| 2026-11-07T23:19:56+00:00 | build-compile-final | 0 | 0.04 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T23:20:00+00:00 | django-check-final | 0 | 0.31 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T23:20:04+00:00 | idiom-final | 0 | 0.02 | `bash -c 'ruff check && ruff format --check'` | `07a2e0ea53bd64f2` |  |  |
| 2026-11-07T23:20:10+00:00 | idiom-ruff-check-final | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T23:20:13+00:00 | idiom-ruff-format-final | 0 | 0.01 | `ruff format --check` | `c3ac60a207092b7f` |  |  |
| 2026-11-07T23:21:07+00:00 | behavior-final | 0 | 51.05 | `pytest -q` | `7c14b01758950b7e` |  |  |
| 2026-11-07T23:21:53+00:00 | crap-coverage-final | 0 | 42.29 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `1bce9f64c07d81f0` |  |  |
| 2026-11-07T23:21:57+00:00 | crap-lizard-final | 0 | 0.12 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T23:21:57+00:00 | crap-score-final | 0 | 0.03 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `c1f7b4ca904f936a` |  | gate=crap max=26.0 threshold=30 over=0 methods=208 |
| 2026-11-07T23:23:01+00:00 | mutation-changed-final | 0 | 59.77 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `94fd5d6e80493ea3` |  | gate=mutation score=0.803 threshold=0.8 killed=49 survived=12 files=1 base=origin/main |
| 2026-11-07T23:23:22+00:00 | http-method-test | 0 | 1.41 | `pytest -q tests/booking/interfaces/test_route_selection.py::test_route_screens_reject_unsupported_http_methods` | `a558b8376cd28466` |  |  |
| 2026-11-07T23:24:09+00:00 | behavior-after-http-test | 0 | 43.77 | `pytest -q` | `2031f4ad9510cea0` |  |  |
| 2026-11-07T23:25:14+00:00 | mutation-changed-final | 0 | 61.09 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `94fd5d6e80493ea3` |  | gate=mutation score=0.803 threshold=0.8 killed=49 survived=12 files=1 base=origin/main |
| 2026-11-07T23:25:33+00:00 | http-method-test-valid-cargo | 0 | 1.5 | `pytest -q tests/booking/interfaces/test_route_selection.py::test_route_screens_reject_unsupported_http_methods` | `f51873a8b2568bb4` |  |  |
| 2026-11-07T23:26:42+00:00 | mutation-changed-final | 0 | 64.58 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `94fd5d6e80493ea3` |  | gate=mutation score=0.803 threshold=0.8 killed=49 survived=12 files=1 base=origin/main |
| 2026-11-07T23:27:47+00:00 | behavior-final-467 | 0 | 45.11 | `pytest -q` | `c26d6d9b6bcf9177` |  |  |
| 2026-11-07T23:29:04+00:00 | crap-coverage-final-467 | 0 | 46.55 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `aeae45f0cde2980f` |  |  |
| 2026-11-07T23:29:08+00:00 | crap-lizard-final-467 | 0 | 0.12 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T23:29:08+00:00 | crap-score-final-467 | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `c1f7b4ca904f936a` |  | gate=crap max=26.0 threshold=30 over=0 methods=208 |
