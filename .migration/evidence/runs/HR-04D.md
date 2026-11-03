# Run journal: HR-04D

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-03T20:42:19+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-03T20:47:32+00:00 | processing-red | 2 | 1.45 | `pytest -q tests/handling/test_registration_processing.py` | `5c3a97d3a9f4c611` | _______ ERROR collecting tests/handling/test_registration_processing.py ________ |  |
