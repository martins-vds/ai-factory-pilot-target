# Run journal: BK-05I

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-08T12:47:22+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-08T12:49:43+00:00 | build-compileall | 0 | 0.11 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-08T12:49:44+00:00 | build-django-check | 0 | 1.49 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-08T12:49:44+00:00 | idiom-ruff-check | 0 | 0.03 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-08T12:49:45+00:00 | idiom-ruff-format | 0 | 0.02 | `ruff format --check` | `f971e9aa1333322e` |  |  |
| 2026-11-08T12:50:58+00:00 | behavior | 0 | 72.86 | `pytest -q` | `7883b682283f8b77` |  |  |
| 2026-11-08T12:52:18+00:00 | crap-pytest-cov | 0 | 80.62 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `54abfe75035815b2` |  |  |
| 2026-11-08T12:52:19+00:00 | crap-lizard | 0 | 0.17 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-08T12:52:19+00:00 | crap-report | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `46edc5c319c80c3b` |  | gate=crap max=26.0 threshold=30 over=0 methods=213 |
| 2026-11-08T12:53:28+00:00 | regression | 0 | 69.01 | `pytest -q` | `3c81ea8d762170d0` |  |  |
| 2026-11-08T12:53:28+00:00 | mutation-changed | 0 | 0.08 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `36603172da4a0d74` |  | gate=mutation score=n/a reason=no-mutable-code-changed base=origin/main |
| 2026-11-08T12:53:51+00:00 | booking-characterization-inventory | 0 | 1.71 | `pytest -q tests/characterization/test_booking.py` | `7ce361fd5a320180` |  |  |
| 2026-11-08T13:14:48+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-08T13:18:49+00:00 | booking-replay | 1 | 8.99 | `pytest -q tests/characterization/booking` | `2e7cdc4bbf212632` | assert cargo is not None |  |
| 2026-11-08T13:19:11+00:00 | booking-replay | 1 | 6.38 | `pytest -q tests/characterization/booking` | `0effd933b2fc5343` | assert cargo is not None |  |
| 2026-11-08T13:19:27+00:00 | booking-replay | 0 | 6.24 | `pytest -q tests/characterization/booking` | `0eaa07d048f3d215` |  |  |
| 2026-11-08T13:20:33+00:00 | booking-replay | 0 | 6.33 | `pytest -q tests/characterization/booking` | `f6063177b17f73de` |  |  |
