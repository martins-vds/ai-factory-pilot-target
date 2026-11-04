# Run journal: HR-04E-FIX

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-04T14:37:33+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-04T14:42:02+00:00 | targeted-red | 1 | 33.5 | `pytest -q tests/handling/test_repository.py tests/handling/interfaces/test_registration_reports.py tests/handling/test_registration_processing.py tests/differential/test_handling_registration.py` | `fb641bb8c9fec417` | assert set(columns) == { |  |
