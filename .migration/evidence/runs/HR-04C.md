# Run journal: HR-04C

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-03T20:42:52+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-03T20:45:35+00:00 | accepted-red | 1 | 3.76 | `pytest -q tests/handling/interfaces/test_registration_reports.py` | `10121c1874c20288` | E           cargotracker.handling.infrastructure.models.RegistrationAttemptRecord.DoesNotExist: RegistrationAttemptRecor |  |
| 2026-11-03T20:45:51+00:00 | accepted-green | 0 | 1.56 | `pytest -q tests/handling/interfaces/test_registration_reports.py` | `b458571cf7530567` |  |  |
