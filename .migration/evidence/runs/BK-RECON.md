# Run journal: BK-RECON

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-09T04:50:02+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |

## GitHub Actions reconciliation check

- Commit: `cb587379722bb602e690c2f31ac3fb0b79526cf2`
- Run: https://github.com/martins-vds/ai-factory-pilot-target/actions/runs/42564426328/job/128987747950
- Gate output: `AFS-RESULT gate=ticket-reconciliation epic=224 verdict=fail tickets=39 failures=4`
- Diagnostics: issues #262, #276, #470 and #477 require return attribution or failure evidence not supported by the committed role returns.
