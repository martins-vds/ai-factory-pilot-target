# Run journal: HR-04B

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-03T18:18:40+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-03T18:21:43+00:00 | behavior-red | 2 | 4.31 | `pytest -q tests/handling/test_registration_attempt_repository.py` | `78a2800ff80d2d93` | ___ ERROR collecting tests/handling/test_registration_attempt_repository.py ____ |  |
| 2026-11-03T18:22:56+00:00 | behavior-accepted | 0 | 1.23 | `pytest -q tests/handling/test_registration_attempt_repository.py` | `4e221273d861ce0e` |  |  |
| 2026-11-03T18:23:44+00:00 | repository-tests | 0 | 1.31 | `pytest -q tests/handling/test_registration_attempt_repository.py` | `ecde7e16d7742946` |  |  |
| 2026-11-03T18:24:56+00:00 | skip-locked-test | 0 | 1.33 | `pytest -q tests/handling/test_registration_attempt_repository.py` | `3d84880b5ebc05a9` |  |  |
| 2026-11-03T18:26:42+00:00 | idiom-format-check | 0 | 0.02 | `ruff format --check` | `291d91fd4256e9a8` |  |  |
| 2026-11-03T18:26:42+00:00 | idiom-ruff-check | 1 | 0.05 | `ruff check` | `623066115990c6d8` |  |  |
| 2026-11-03T18:26:42+00:00 | build-compile | 0 | 0.05 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-03T18:26:43+00:00 | build-django-check | 0 | 0.36 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-03T18:26:55+00:00 | behavior | 0 | 12.81 | `pytest -q` | `3f68bd8949118397` |  |  |
| 2026-11-03T18:27:36+00:00 | idiom-format-check | 0 | 0.02 | `ruff format --check` | `291d91fd4256e9a8` |  |  |
| 2026-11-03T18:27:36+00:00 | idiom-ruff-check | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-03T18:27:37+00:00 | migration-drift | 0 | 0.36 | `python manage.py makemigrations handling --check --dry-run` | `f91468a08ee08a1e` |  |  |
