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
| 2026-11-07T19:49:31+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T19:50:46+00:00 | idiom-ruff-format | 0 | 0.03 | `ruff format --check` | `05facc7430ea9711` |  |  |
| 2026-11-07T19:50:46+00:00 | idiom-ruff-check | 0 | 0.04 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T19:50:46+00:00 | build-compileall | 0 | 0.15 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T19:50:47+00:00 | build-django-check | 0 | 1.33 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T19:52:03+00:00 | tests | 0 | 70.08 | `pytest -q` | `47b90de6fc08b869` |  |  |
| 2026-11-07T20:00:03+00:00 | tests-details-targeted | 0 | 3.58 | `pytest -q tests/booking/interfaces/test_cargo_details.py` | `37277f0e56f6c5fe` |  |  |
| 2026-11-07T20:00:09+00:00 | idiom-ruff-format | 0 | 0.02 | `ruff format --check` | `05facc7430ea9711` |  |  |
| 2026-11-07T20:00:09+00:00 | idiom-ruff-check | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T20:00:09+00:00 | build-compileall | 0 | 0.07 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T20:00:10+00:00 | build-django-check | 0 | 0.39 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T20:01:24+00:00 | tests | 0 | 68.03 | `pytest -q` | `a8fdd508a1f5cb70` |  |  |
| 2026-11-07T20:02:39+00:00 | crap-coverage | 0 | 68.11 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `2fa758f1fc5abc30` |  |  |
| 2026-11-07T20:02:42+00:00 | crap-lizard | 0 | 0.16 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T20:02:45+00:00 | crap-score | 0 | 0.05 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `803154894bacca53` |  | gate=crap max=26.0 threshold=30 over=0 methods=188 |
| 2026-11-07T20:04:00+00:00 | mutation-changed | 0 | 48.61 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `afeeedaec6f674d4` |  | gate=mutation score=0.929 threshold=0.8 killed=13 survived=1 files=1 base=origin/main |
| 2026-11-07T20:06:31+00:00 | tests-ui-targeted | 0 | 4.54 | `pytest -q tests/booking/interfaces/test_dashboard.py tests/booking/interfaces/test_cargo_details.py` | `4ec95ac9b4b9a34a` |  |  |
| 2026-11-07T20:06:44+00:00 | idiom-ruff-format | 0 | 0.03 | `ruff format --check` | `05facc7430ea9711` |  |  |
| 2026-11-07T20:06:44+00:00 | build-compileall | 0 | 0.06 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T20:06:44+00:00 | idiom-ruff-check | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T20:06:44+00:00 | build-django-check | 0 | 0.4 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T20:07:46+00:00 | tests | 0 | 56.22 | `pytest -q` | `cee5eaed03f360fe` |  |  |
| 2026-11-07T20:08:46+00:00 | crap-coverage | 0 | 56.19 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `a871214465570e3a` |  |  |
| 2026-11-07T20:08:50+00:00 | crap-lizard | 0 | 0.15 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T20:08:54+00:00 | crap-score | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `803154894bacca53` |  | gate=crap max=26.0 threshold=30 over=0 methods=188 |
| 2026-11-07T20:09:47+00:00 | mutation-changed | 0 | 49.64 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `afeeedaec6f674d4` |  | gate=mutation score=0.929 threshold=0.8 killed=13 survived=1 files=1 base=origin/main |
