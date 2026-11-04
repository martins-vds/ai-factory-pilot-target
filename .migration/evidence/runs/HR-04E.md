# Run journal: HR-04E

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-04T12:55:17+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-04T13:00:27+00:00 | differential-initial | 1 | 19.71 | `pytest -q tests/differential/test_handling_registration.py` | `1f543be5709c70ba` | assert response.status_code == 400 |  |
| 2026-11-04T13:01:48+00:00 | differential-replay | 1 | 22.63 | `pytest -q tests/differential/test_handling_registration.py` | `5cafcbbd605a3e5c` | assert response.status_code == 400 |  |
| 2026-11-04T13:02:36+00:00 | idiom-test-ruff | 1 | 0.01 | `ruff check tests/differential/test_handling_registration.py` | `1fab734223aa3c5b` |  |  |
| 2026-11-04T13:02:51+00:00 | idiom-test-ruff-check | 0 | 0.01 | `ruff check tests/differential/test_handling_registration.py` | `82b3e6a6c090a576` |  |  |
| 2026-11-04T13:03:05+00:00 | idiom-test-format | 1 | 0.01 | `ruff format --check tests/differential/test_handling_registration.py` | `fb37725b07825bb5` | 156 \|             assert match is not None |  |
| 2026-11-04T13:03:22+00:00 | format-test-file | 0 | 0.01 | `ruff format tests/differential/test_handling_registration.py` | `413a709001976657` |  |  |
| 2026-11-04T13:04:17+00:00 | format-test-file-final | 0 | 0.01 | `ruff format tests/differential/test_handling_registration.py` | `d807f3580f2470a7` |  |  |
| 2026-11-04T13:05:07+00:00 | behavior | 1 | 45.22 | `pytest -q` | `05de0673e3a1e5ec` | assert response.status_code == 400 |  |
| 2026-11-04T13:05:13+00:00 | build-compile | 0 | 0.04 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-04T13:05:18+00:00 | build-django-check | 0 | 0.4 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-04T13:05:23+00:00 | idiom-ruff-check | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-04T13:05:27+00:00 | idiom-ruff-format | 0 | 0.02 | `ruff format --check` | `b1589e558de12a68` |  |  |
| 2026-11-04T13:06:16+00:00 | crap-coverage | 1 | 42.82 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `08c688a818489ab6` | assert response.status_code == 400 |  |
| 2026-11-04T13:06:20+00:00 | crap-lizard | 0 | 0.13 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-04T13:06:24+00:00 | crap-score | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `e9b12e0d845de05e` |  | gate=crap max=19.0 threshold=30 over=0 methods=132 |
| 2026-11-04T13:06:29+00:00 | mutation-changed | 0 | 0.09 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `36603172da4a0d74` |  | gate=mutation score=n/a reason=no-mutable-code-changed base=origin/main |
| 2026-11-04T13:08:07+00:00 | regression | 1 | 44.48 | `pytest -q` | `66b39b453af20fa6` | assert response.status_code == 400 |  |
| 2026-11-04T13:21:20+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-04T13:22:12+00:00 | differential-repro | 1 | 28.22 | `pytest -q tests/differential/test_handling_registration.py` | `09fad0aa44968199` | assert response.status_code == 400 |  |
| 2026-11-04T13:26:54+00:00 | differential-corrected | 1 | 22.32 | `pytest -q tests/differential/test_handling_registration.py` | `b65362922d7cce51` | assert expected['cargo']['transportStatus'] == 'NOT_RECEIVED' |  |
| 2026-11-04T13:27:38+00:00 | differential-corrected | 1 | 22.8 | `pytest -q tests/differential/test_handling_registration.py` | `101c113c5b27f623` | assert expected['cargo']['transportStatus'] == 'NOT_RECEIVED' |  |
| 2026-11-04T13:28:19+00:00 | ruling-136 | 0 | 3.9 | `pytest -q tests/handling/test_domain.py::test_handling_history_breaks_completion_time_ties_by_registration_time_then_id tests/handling/test_registration_processing.py::test_equal_completion_time_uses_registration_order_for_delivered_outcome tests/handling/test_registration_processing.py::test_equal_completion_and_registration_times_use_event_id_for_delivery` | `5390c9371eee96e1` |  |  |
| 2026-11-04T13:29:34+00:00 | build-compile | 0 | 0.04 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-04T13:29:35+00:00 | build-django-check | 0 | 0.36 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-04T13:30:16+00:00 | behavior | 1 | 41.37 | `pytest -q` | `3505804471b4c0fb` | assert expected['cargo']['transportStatus'] == 'NOT_RECEIVED' |  |
| 2026-11-04T13:30:16+00:00 | idiom-ruff-check | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-04T13:30:16+00:00 | idiom-ruff-format | 0 | 0.02 | `ruff format --check` | `b1589e558de12a68` |  |  |
| 2026-11-04T13:31:05+00:00 | crap-coverage | 1 | 48.66 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `9ef70848eccb23ba` | assert expected['cargo']['transportStatus'] == 'NOT_RECEIVED' |  |
| 2026-11-04T13:31:05+00:00 | crap-lizard | 0 | 0.13 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-04T13:31:05+00:00 | crap-score | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `e9b12e0d845de05e` |  | gate=crap max=19.0 threshold=30 over=0 methods=132 |
| 2026-11-04T13:31:05+00:00 | mutation-changed | 1 | 0.08 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `3ff11adc524e78cf` |  |  |
| 2026-11-04T13:31:46+00:00 | regression | 1 | 40.76 | `pytest -q` | `1fe9dcb395189121` | assert expected['cargo']['transportStatus'] == 'NOT_RECEIVED' |  |
| 2026-11-04T13:31:59+00:00 | mutation-changed | 1 | 0.09 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `3ff11adc524e78cf` |  |  |
| 2026-11-04T13:32:20+00:00 | mutation-changed | 0 | 0.08 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `36603172da4a0d74` |  | gate=mutation score=n/a reason=no-mutable-code-changed base=origin/main |
| 2026-11-04T13:34:24+00:00 | differential-final | 1 | 23.31 | `pytest -q tests/differential/test_handling_registration.py` | `a0db51468bd9a474` | assert expected['cargo']['transportStatus'] == 'NOT_RECEIVED' |  |
| 2026-11-04T13:34:33+00:00 | build-compile-final | 0 | 0.04 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-04T13:34:33+00:00 | build-django-check-final | 0 | 0.35 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-04T13:35:16+00:00 | behavior-final | 1 | 43.23 | `pytest -q` | `42971eed36809aa8` | assert expected['cargo']['transportStatus'] == 'NOT_RECEIVED' |  |
| 2026-11-04T13:35:16+00:00 | idiom-ruff-check-final | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-04T13:35:16+00:00 | idiom-ruff-format-final | 0 | 0.01 | `ruff format --check` | `b1589e558de12a68` |  |  |
| 2026-11-04T13:36:07+00:00 | crap-coverage-final | 1 | 50.15 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `8e19a698ea5d60b0` | assert expected['cargo']['transportStatus'] == 'NOT_RECEIVED' |  |
| 2026-11-04T13:36:07+00:00 | crap-lizard-final | 0 | 0.13 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-04T13:36:07+00:00 | crap-score-final | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `e9b12e0d845de05e` |  | gate=crap max=19.0 threshold=30 over=0 methods=132 |
| 2026-11-04T13:36:07+00:00 | mutation-changed-final | 0 | 0.08 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `36603172da4a0d74` |  | gate=mutation score=n/a reason=no-mutable-code-changed base=origin/main |
| 2026-11-04T13:36:48+00:00 | regression-final | 1 | 41.15 | `pytest -q` | `0fec34b1224edd98` | assert expected['cargo']['transportStatus'] == 'NOT_RECEIVED' |  |
