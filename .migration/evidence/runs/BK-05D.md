# Run journal: BK-05D

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-07T15:31:33+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T15:35:17+00:00 | origin-test-red | 2 | 1.32 | `pytest -q tests/booking/interfaces/test_wizard.py` | `d71e403d5ad97e03` | ___________ ERROR collecting tests/booking/interfaces/test_wizard.py ___________ |  |
| 2026-11-07T15:35:34+00:00 | origin-test-green | 0 | 2.09 | `pytest -q tests/booking/interfaces/test_wizard.py` | `7eb11104642b7dc0` |  |  |
