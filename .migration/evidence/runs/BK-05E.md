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
