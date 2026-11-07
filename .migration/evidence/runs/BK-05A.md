# Run journal: BK-05A

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-07T03:49:04+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T03:51:07+00:00 | tdd-red | 2 | 2.32 | `pytest -q tests/booking/application` | `6bfd436367a5d41c` | _______ ERROR collecting tests/booking/application/test_registration.py ________ |  |
| 2026-11-07T03:51:45+00:00 | tdd-green | 0 | 1.1 | `pytest -q tests/booking/application` | `53e496b3492d6f07` |  |  |
| 2026-11-07T03:53:08+00:00 | build-compile | 0 | 0.04 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T03:53:09+00:00 | build-check | 0 | 0.24 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T03:53:09+00:00 | idiom-lint | 1 | 0.01 | `ruff check` | `2aac03cc572db868` |  |  |
| 2026-11-07T03:53:22+00:00 | idiom-lint-rerun | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T03:53:22+00:00 | idiom-format | 0 | 0.01 | `ruff format --check` | `8f54ec861a76fc44` |  |  |
| 2026-11-07T03:53:52+00:00 | tests | 0 | 26.07 | `pytest -q` | `1c835f6c11e32a26` |  |  |
| 2026-11-07T03:54:23+00:00 | crap-coverage | 0 | 26.71 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `dde1f9736f10ab32` |  |  |
| 2026-11-07T03:54:23+00:00 | crap-lizard | 0 | 0.08 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T03:54:23+00:00 | crap-threshold | 0 | 0.03 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `df94388d8dc116c8` |  | gate=crap max=19.0 threshold=30 over=0 methods=139 |
| 2026-11-07T03:54:38+00:00 | mutation-changed | 0 | 10.14 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `bbaa364119793b1e` |  | gate=mutation score=0.944 threshold=0.8 killed=17 survived=1 files=2 base=origin/main |
| 2026-11-07T03:55:18+00:00 | tdd-edge | 0 | 1.08 | `pytest -q tests/booking/application` | `81e259044c81c485` |  |  |
| 2026-11-07T03:55:32+00:00 | mutation-changed-rerun | 0 | 9.63 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `bbaa364119793b1e` |  | gate=mutation score=0.944 threshold=0.8 killed=17 survived=1 files=2 base=origin/main |
| 2026-11-07T03:56:09+00:00 | mutation-changed-final | 0 | 9.48 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `bbaa364119793b1e` |  | gate=mutation score=0.944 threshold=0.8 killed=17 survived=1 files=2 base=origin/main |
| 2026-11-07T03:57:06+00:00 | behavior-final | 0 | 23.16 | `pytest -q` | `4d458973569f6c45` |  |  |
| 2026-11-07T03:57:06+00:00 | idiom-lint-final | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T03:57:06+00:00 | idiom-format-final | 0 | 0.01 | `ruff format --check` | `8f54ec861a76fc44` |  |  |
| 2026-11-07T03:57:31+00:00 | crap-coverage-final | 0 | 24.46 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `e3734c9281b15347` |  |  |
| 2026-11-07T03:57:31+00:00 | crap-lizard-final | 0 | 0.07 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T03:57:31+00:00 | crap-threshold-final | 0 | 0.02 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `df94388d8dc116c8` |  | gate=crap max=19.0 threshold=30 over=0 methods=139 |
| 2026-11-07T04:14:40+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T04:16:28+00:00 | build-compile | 0 | 0.07 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T04:16:29+00:00 | build-check | 0 | 0.77 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T04:17:09+00:00 | behavior | 0 | 40.01 | `pytest -q` | `880a9bf72b6de8b8` |  |  |
| 2026-11-07T04:17:09+00:00 | idiom-lint | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T04:17:09+00:00 | idiom-format | 0 | 0.02 | `ruff format --check` | `8f54ec861a76fc44` |  |  |
| 2026-11-07T04:17:48+00:00 | crap-coverage | 0 | 39.06 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `8ca3826fceab0153` |  |  |
| 2026-11-07T04:17:49+00:00 | crap-lizard | 0 | 0.11 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T04:17:49+00:00 | crap-threshold | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `df94388d8dc116c8` |  | gate=crap max=19.0 threshold=30 over=0 methods=139 |
| 2026-11-07T04:18:02+00:00 | mutation-changed | 0 | 12.91 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `bbaa364119793b1e` |  | gate=mutation score=0.944 threshold=0.8 killed=17 survived=1 files=2 base=origin/main |
| 2026-11-07T04:18:41+00:00 | regression | 0 | 39.16 | `pytest -q` | `417c6a0ab9eb99f0` |  |  |
| 2026-11-07T04:22:55+00:00 | verifier-legacy-fields | 0 | 1.72 | `pytest -q tests/booking/application/test_registration.py tests/booking/application/test_specification.py` | `ff8b70c9209cc2a9` |  |  |
