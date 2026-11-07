# Run journal: BK-05A

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-07T03:49:04+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T03:51:07+00:00 | tdd-red | 2 | 2.32 | `pytest -q tests/booking/application` | `6bfd436367a5d41c` | _______ ERROR collecting tests/booking/application/test_registration.py ________ |  |
| 2026-11-07T03:51:45+00:00 | tdd-green | 0 | 1.1 | `pytest -q tests/booking/application` | `53e496b3492d6f07` |  |  |
