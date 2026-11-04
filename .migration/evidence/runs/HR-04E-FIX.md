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
