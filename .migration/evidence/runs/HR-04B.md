# Run journal: HR-04B

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-03T18:18:40+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-03T18:21:43+00:00 | behavior-red | 2 | 4.31 | `pytest -q tests/handling/test_registration_attempt_repository.py` | `78a2800ff80d2d93` | ___ ERROR collecting tests/handling/test_registration_attempt_repository.py ____ |  |
| 2026-11-03T18:22:56+00:00 | behavior-accepted | 0 | 1.23 | `pytest -q tests/handling/test_registration_attempt_repository.py` | `4e221273d861ce0e` |  |  |
| 2026-11-03T18:23:44+00:00 | repository-tests | 0 | 1.31 | `pytest -q tests/handling/test_registration_attempt_repository.py` | `ecde7e16d7742946` |  |  |
| 2026-11-03T18:24:56+00:00 | skip-locked-test | 0 | 1.33 | `pytest -q tests/handling/test_registration_attempt_repository.py` | `3d84880b5ebc05a9` |  |  |
