# Run journal: COORDINATOR-L0-VALIDATION

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-06T04:40:34+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-06T04:44:19+00:00 | output-validation | 0 | 0.9 | `python .migration/harness/tools/validate.py .migration` | `1f4ff7e5cda8e1f6` |  |  |
| 2026-11-06T04:44:58+00:00 | final-validation | 0 | 0.9 | `python .migration/harness/tools/validate.py .migration` | `1f4ff7e5cda8e1f6` |  |  |
