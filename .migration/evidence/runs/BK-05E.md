# Run journal: BK-05E

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-07T18:23:06+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T18:27:09+00:00 | tests-red | 2 | 2.95 | `pytest -q tests/booking/interfaces/test_dashboard.py tests/booking/interfaces/test_cargo_details.py` | `5919781dca1433e6` | _________ ERROR collecting tests/booking/interfaces/test_dashboard.py __________ |  |
| 2026-11-07T18:28:12+00:00 | tests-targeted | 0 | 2.94 | `pytest -q tests/booking/interfaces/test_dashboard.py tests/booking/interfaces/test_cargo_details.py` | `d45996ff8b3a07ca` |  |  |
| 2026-11-07T18:28:43+00:00 | tests-targeted | 0 | 2.84 | `pytest -q tests/booking/interfaces/test_dashboard.py tests/booking/interfaces/test_cargo_details.py` | `bf97953a21a0c167` |  |  |
| 2026-11-07T18:29:05+00:00 | build-compileall | 0 | 0.05 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T18:29:05+00:00 | build-django-check | 0 | 0.31 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T18:29:08+00:00 | idiom-ruff-check | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T18:29:08+00:00 | idiom-ruff-format | 1 | 0.02 | `ruff format --check` | `f7623b4d5336db55` | 77 \|     assert response.status_code == 200 |  |
| 2026-11-07T18:29:13+00:00 | idiom-ruff-format | 0 | 0.01 | `ruff format --check` | `c7a0bcb17dd5241a` |  |  |
| 2026-11-07T18:30:01+00:00 | tests | 0 | 44.68 | `pytest -q` | `fde32fcce61583e5` |  |  |
| 2026-11-07T18:30:44+00:00 | crap-coverage | 0 | 37.61 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `ff6e6eba749aaa31` |  |  |
| 2026-11-07T18:30:44+00:00 | crap-lizard | 0 | 0.12 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T18:30:44+00:00 | crap-score | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `efcf0c40f9c44d17` |  | gate=crap max=26.0 threshold=30 over=0 methods=180 |
| 2026-11-07T18:31:15+00:00 | mutation-changed | 0 | 25.98 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `4e8520baafe17cc5` |  | gate=mutation score=0.929 threshold=0.8 killed=13 survived=1 files=1 base=origin/main |
| 2026-11-07T20:44:35+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T20:47:54+00:00 | verifier-detail-tests | 0 | 5.11 | `pytest -q tests/booking/interfaces/test_cargo_details.py` | `0a1e2d419eae0218` |  |  |
| 2026-11-07T20:48:20+00:00 | verifier-build-compileall | 0 | 0.06 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T20:48:20+00:00 | verifier-build-django-check | 0 | 0.36 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T20:48:21+00:00 | verifier-idiom-ruff-check | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T20:48:21+00:00 | verifier-idiom-ruff-format | 0 | 0.02 | `ruff format --check` | `df313bb2dd82ede5` |  |  |
| 2026-11-07T20:49:18+00:00 | verifier-behavior-tests | 0 | 53.4 | `pytest -q` | `d4ed7b94c4c2b1e2` |  |  |
| 2026-11-07T20:50:08+00:00 | verifier-crap-coverage | 0 | 50.38 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `25723541bf65ac80` |  |  |
| 2026-11-07T20:50:13+00:00 | verifier-crap-lizard | 0 | 0.13 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T20:50:13+00:00 | verifier-crap-score | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `d7e339dad131f4ec` |  | gate=crap max=26.0 threshold=30 over=0 methods=197 |
| 2026-11-07T20:51:05+00:00 | verifier-mutation-changed | 0 | 44.25 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `a4fbfa3725b2cc52` |  | gate=mutation score=0.929 threshold=0.8 killed=13 survived=1 files=1 base=origin/main |
| 2026-11-07T20:57:24+00:00 | verifier-final-build-compileall | 0 | 0.04 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T20:57:24+00:00 | verifier-final-build-check | 0 | 0.35 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T20:57:24+00:00 | verifier-final-ruff-check | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T20:57:24+00:00 | verifier-final-ruff-format | 0 | 0.01 | `ruff format --check` | `df313bb2dd82ede5` |  |  |
| 2026-11-07T20:58:17+00:00 | verifier-final-tests | 0 | 52.56 | `pytest -q` | `02533171d3bff4eb` |  |  |
| 2026-11-07T20:59:11+00:00 | verifier-final-crap-coverage | 0 | 54.21 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `8cdfed8b0e55cc51` |  |  |
| 2026-11-07T20:59:11+00:00 | verifier-final-crap-lizard | 0 | 0.13 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T20:59:11+00:00 | verifier-final-crap-score | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `d7e339dad131f4ec` |  | gate=crap max=26.0 threshold=30 over=0 methods=197 |
| 2026-11-07T20:59:56+00:00 | verifier-final-mutation-changed | 0 | 44.8 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `a4fbfa3725b2cc52` |  | gate=mutation score=0.929 threshold=0.8 killed=13 survived=1 files=1 base=origin/main |
| 2026-11-07T21:31:57+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T21:34:37+00:00 | dashboard-unit-red | 4 | 1.41 | `pytest -q tests/booking/application/test_dashboard.py::test_dashboard_partitions_cargos_in_source_order` | `1b9a23635dee64e8` | ERROR: found no collectors for /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/tests/booking/applicati |  |
| 2026-11-07T21:34:47+00:00 | dashboard-unit-green | 0 | 1.17 | `pytest -q tests/booking/application/test_dashboard.py::test_dashboard_partitions_cargos_in_source_order` | `fc1803812b63de5c` |  |  |
| 2026-11-07T21:34:57+00:00 | details-unit-red | 1 | 1.15 | `pytest -q tests/booking/application/test_dashboard.py::test_cargo_details_returns_the_requested_cargo` | `d6013be83c49e184` | >       assert dashboard.get_cargo_details(tracking_id) is cargo |  |
| 2026-11-07T21:35:05+00:00 | details-unit-green | 0 | 1.13 | `pytest -q tests/booking/application/test_dashboard.py::test_cargo_details_returns_the_requested_cargo` | `aa4ec373bf9e8ac7` |  |  |
| 2026-11-07T21:35:47+00:00 | dashboard-focused | 0 | 3.47 | `pytest -q tests/booking/application/test_dashboard.py tests/booking/interfaces/test_dashboard.py tests/booking/interfaces/test_cargo_details.py` | `bf2132de0842b464` |  |  |
| 2026-11-07T21:36:51+00:00 | build-compileall | 0 | 0.06 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T21:36:52+00:00 | build-django-check | 0 | 0.28 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T21:36:55+00:00 | idiom-ruff-check | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T21:36:55+00:00 | idiom-ruff-format | 1 | 0.02 | `ruff format --check` | `9579d0777594546c` |  |  |
| 2026-11-07T21:36:59+00:00 | idiom-ruff-format | 0 | 0.01 | `ruff format --check` | `5eb321ace635f2f7` |  |  |
| 2026-11-07T21:37:45+00:00 | behavior-tests | 0 | 43.54 | `pytest -q` | `d7490892b545f182` |  |  |
| 2026-11-07T21:38:32+00:00 | crap-coverage | 0 | 42.18 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `ea541836f7c1fa4a` |  |  |
| 2026-11-07T21:38:33+00:00 | crap-lizard | 0 | 0.12 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T21:38:33+00:00 | crap-score | 0 | 0.03 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `b9503a992dcb184b` |  | gate=crap max=26.0 threshold=30 over=0 methods=200 |
| 2026-11-07T21:39:22+00:00 | mutation-changed | 0 | 31.8 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `5999fe24b4e42e1e` |  | gate=mutation score=0.889 threshold=0.8 killed=16 survived=2 files=2 base=origin/main |
| 2026-11-07T21:40:12+00:00 | dashboard-regression-tests | 0 | 3.37 | `pytest -q tests/booking/application/test_dashboard.py tests/booking/interfaces/test_dashboard.py tests/booking/interfaces/test_cargo_details.py` | `2d0ea00fa33633a6` |  |  |
| 2026-11-07T21:40:20+00:00 | idiom-ruff-check | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T21:40:20+00:00 | idiom-ruff-format | 0 | 0.01 | `ruff format --check` | `5eb321ace635f2f7` |  |  |
| 2026-11-07T21:40:36+00:00 | build-compileall | 0 | 0.04 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T21:40:37+00:00 | build-django-check | 0 | 0.32 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T21:40:41+00:00 | idiom-ruff-check | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T21:40:41+00:00 | idiom-ruff-format | 0 | 0.01 | `ruff format --check` | `5eb321ace635f2f7` |  |  |
| 2026-11-07T21:41:27+00:00 | behavior-tests | 0 | 42.29 | `pytest -q` | `fddb6e4fb88365ba` |  |  |
| 2026-11-07T21:42:13+00:00 | crap-coverage | 0 | 42.07 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `bdee467ad53514ec` |  |  |
| 2026-11-07T21:42:13+00:00 | crap-lizard | 0 | 0.12 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T21:42:13+00:00 | crap-score | 0 | 0.03 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `b9503a992dcb184b` |  | gate=crap max=26.0 threshold=30 over=0 methods=200 |
| 2026-11-07T21:42:47+00:00 | mutation-changed | 0 | 30.99 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `bcb36e02130d930c` |  | gate=mutation score=1.000 threshold=0.8 killed=17 survived=0 files=2 base=origin/main |
| 2026-11-07T21:45:04+00:00 | final-build-compileall | 0 | 0.03 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T21:45:04+00:00 | final-build-check | 0 | 0.28 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T21:45:04+00:00 | final-ruff-check | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T21:45:04+00:00 | final-ruff-format | 0 | 0.01 | `ruff format --check` | `5eb321ace635f2f7` |  |  |
| 2026-11-07T21:45:48+00:00 | final-tests | 0 | 43.87 | `pytest -q` | `b29b2fa5eafadfbf` |  |  |
| 2026-11-07T21:46:38+00:00 | final-crap-coverage | 0 | 49.35 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `c8cb45c4e538473a` |  |  |
| 2026-11-07T21:46:38+00:00 | final-crap-lizard | 0 | 0.13 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T21:46:38+00:00 | final-crap-score | 0 | 0.03 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `b9503a992dcb184b` |  | gate=crap max=26.0 threshold=30 over=0 methods=200 |
| 2026-11-07T21:47:09+00:00 | final-mutation-changed | 0 | 30.91 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `bcb36e02130d930c` |  | gate=mutation score=1.000 threshold=0.8 killed=17 survived=0 files=2 base=origin/main |
| 2026-11-07T22:18:51+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T22:21:42+00:00 | verifier-characterization-dashboard | 0 | 5.01 | `pytest -q tests/characterization/test_booking.py tests/booking/interfaces/test_dashboard.py tests/booking/interfaces/test_cargo_details.py` | `974031136f6ce25c` |  |  |
| 2026-11-07T22:21:46+00:00 | verifier-build-compileall | 0 | 0.06 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T22:21:49+00:00 | verifier-build-django-check | 0 | 0.38 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T22:21:53+00:00 | verifier-idiom-ruff-check | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T22:21:56+00:00 | verifier-idiom-ruff-format | 0 | 0.02 | `ruff format --check` | `dd6674ff09df8dc3` |  |  |
| 2026-11-07T22:22:59+00:00 | verifier-behavior-tests | 0 | 58.87 | `pytest -q` | `e47ca725c3a37ee2` |  |  |
| 2026-11-07T22:24:00+00:00 | verifier-crap-coverage | 0 | 56.56 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `df89e59f45ba5fd6` |  |  |
| 2026-11-07T22:24:03+00:00 | verifier-crap-lizard | 0 | 0.15 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T22:24:08+00:00 | verifier-crap-score | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `b9503a992dcb184b` |  | gate=crap max=26.0 threshold=30 over=0 methods=200 |
| 2026-11-07T22:24:56+00:00 | verifier-mutation-changed | 0 | 42.03 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `bcb36e02130d930c` |  | gate=mutation score=1.000 threshold=0.8 killed=17 survived=0 files=2 base=origin/main |
| 2026-11-07T22:27:56+00:00 | verifier-details-enhanced | 0 | 2.08 | `pytest -q tests/booking/interfaces/test_cargo_details.py::test_cargo_details_render_route_fields_and_itinerary` | `4584379751fa8190` |  |  |
| 2026-11-07T22:28:02+00:00 | verifier-final-compileall | 0 | 0.04 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T22:28:07+00:00 | verifier-final-django-check | 0 | 0.35 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T22:28:10+00:00 | verifier-final-ruff-check | 1 | 0.01 | `ruff check` | `f6ee7cff6d9e45aa` | Found 1 error. |  |
| 2026-11-07T22:28:22+00:00 | verifier-final-ruff-check | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T22:28:25+00:00 | verifier-final-ruff-format | 0 | 0.01 | `ruff format --check` | `dd6674ff09df8dc3` |  |  |
| 2026-11-07T22:29:20+00:00 | verifier-final-tests | 0 | 50.99 | `pytest -q` | `fee723410dc1366b` |  |  |
| 2026-11-07T22:30:14+00:00 | verifier-final-crap-coverage | 0 | 51.02 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `b44057555254a4eb` |  |  |
| 2026-11-07T22:30:17+00:00 | verifier-final-crap-lizard | 0 | 0.14 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T22:30:21+00:00 | verifier-final-crap-score | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `b9503a992dcb184b` |  | gate=crap max=26.0 threshold=30 over=0 methods=200 |
| 2026-11-07T22:31:03+00:00 | verifier-final-mutation-changed | 0 | 38.89 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `bcb36e02130d930c` |  | gate=mutation score=1.000 threshold=0.8 killed=17 survived=0 files=2 base=origin/main |
