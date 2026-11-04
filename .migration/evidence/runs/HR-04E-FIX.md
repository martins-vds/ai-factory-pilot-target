# Run journal: HR-04E-FIX

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-04T14:37:33+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-04T14:42:02+00:00 | targeted-red | 1 | 33.5 | `pytest -q tests/handling/test_repository.py tests/handling/interfaces/test_registration_reports.py tests/handling/test_registration_processing.py tests/differential/test_handling_registration.py` | `fb641bb8c9fec417` | assert set(columns) == { |  |
| 2026-11-04T14:43:25+00:00 | targeted-green | 0 | 35.44 | `pytest -q tests/handling/test_repository.py tests/handling/interfaces/test_registration_reports.py tests/handling/test_registration_processing.py tests/differential/test_handling_registration.py` | `00a4240d1c4b1db7` |  |  |
| 2026-11-04T14:43:55+00:00 | postgres-migration | 1 | 2.21 | `pytest -q tests/handling/test_migration.py` | `8eb1918e468b6420` | assert connection.vendor == 'postgresql' |  |
| 2026-11-04T14:44:29+00:00 | postgres-migration-recheck | 0 | 2.16 | `pytest -q tests/handling/test_migration.py` | `859684cbbffbdeee` |  |  |
| 2026-11-04T14:47:25+00:00 | targeted-verification | 0 | 36.32 | `pytest -q tests/handling/test_repository.py tests/handling/test_migration.py tests/handling/interfaces/test_registration_reports.py tests/handling/test_registration_processing.py tests/differential/test_handling_registration.py` | `8c2fd7602707a5d3` |  |  |
| 2026-11-04T14:52:19+00:00 | migration-state | 0 | 0.4 | `python manage.py makemigrations --check --dry-run` | `a2bfa7b376c38062` |  |  |
| 2026-11-04T14:52:45+00:00 | differential-28-golden | 0 | 21.13 | `pytest -q tests/differential/test_handling_registration.py` | `b16160f36422d474` |  |  |
| 2026-11-04T14:53:04+00:00 | handling-regression | 0 | 13.53 | `pytest -q tests/handling` | `026a57cd4690da46` |  |  |
| 2026-11-04T14:53:27+00:00 | build-compile | 0 | 0.04 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-04T14:53:33+00:00 | build-django-check | 0 | 0.37 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-04T14:53:38+00:00 | idiom-ruff-check | 1 | 0.02 | `ruff check` | `4a6ccd902536d886` |  |  |
| 2026-11-04T14:53:57+00:00 | idiom-migration-diagnostic | 1 | 0.01 | `ruff check src/cargotracker/handling/migrations/0003_preserve_handling_event_instants.py` | `4a6ccd902536d886` |  |  |
| 2026-11-04T14:54:05+00:00 | idiom-migration-concise | 1 | 0.01 | `ruff check --output-format concise src/cargotracker/handling/migrations/0003_preserve_handling_event_instants.py` | `bb38bed0c37fc30c` |  |  |
| 2026-11-04T14:54:27+00:00 | idiom-ruff-check-retry | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-04T14:54:32+00:00 | idiom-ruff-format | 1 | 0.02 | `ruff format --check` | `803efbd0b1376ce2` | 385 \|                 assert attempt.status == 'registered' |  |
| 2026-11-04T14:54:50+00:00 | idiom-ruff-format-recheck | 0 | 0.01 | `ruff format --check` | `13e464c51f06111c` |  |  |
| 2026-11-04T14:55:00+00:00 | postgres-migration-final | 0 | 2.15 | `pytest -q tests/handling/test_migration.py` | `2ebbc522705b242d` |  |  |
| 2026-11-04T14:55:48+00:00 | behavior | 0 | 42.65 | `pytest -q` | `0943a796bd4fcaf8` |  |  |
| 2026-11-04T14:57:26+00:00 | behavior-final | 0 | 42.76 | `pytest -q` | `aaad25a5cb0a7f33` |  |  |
| 2026-11-04T14:58:16+00:00 | crap-coverage | 0 | 41.01 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `adc2c9863e91dec6` |  |  |
| 2026-11-04T14:58:21+00:00 | crap-lizard | 0 | 0.13 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-04T14:58:27+00:00 | crap-score | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `34d1ce024bdfe792` |  | gate=crap max=19.0 threshold=30 over=0 methods=132 |
| 2026-11-04T14:58:34+00:00 | mutation-changed | 1 | 0.09 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `3ff11adc524e78cf` |  |  |
| 2026-11-04T15:02:06+00:00 | mutation-changed | 0 | 164.82 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `37eba6c3c44ac951` |  | gate=mutation score=0.902 threshold=0.8 killed=129 survived=14 files=3 base=origin/main |
| 2026-11-04T15:03:12+00:00 | regression | 0 | 41.44 | `pytest -q` | `e8a82a4e800cc5a3` |  |  |
| 2026-11-04T15:03:50+00:00 | build-compile-final | 0 | 0.05 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-04T15:04:17+00:00 | build-django-check-final | 0 | 0.36 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-04T15:04:24+00:00 | idiom-ruff-check-final | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-04T15:04:30+00:00 | idiom-ruff-format-final | 0 | 0.01 | `ruff format --check` | `13e464c51f06111c` |  |  |
| 2026-11-04T15:05:04+00:00 | differential-28-golden-final | 0 | 22.93 | `pytest -q tests/differential/test_handling_registration.py` | `3767f6442e5c836b` |  |  |
| 2026-11-04T15:06:05+00:00 | migration-state-final | 0 | 0.39 | `python manage.py makemigrations --check --dry-run` | `a2bfa7b376c38062` |  |  |
| 2026-11-04T15:20:22+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-04T15:20:38+00:00 | return-validation | 0 | 0.54 | `python .migration/harness/tools/validate.py .migration` | `6b979784513aa6bc` |  |  |
