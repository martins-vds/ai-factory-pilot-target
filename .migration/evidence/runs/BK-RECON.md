# Run journal: BK-RECON

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-09T02:22:02+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-09T02:23:57+00:00 | initial-reconciliation | 1 | 0.09 | `python .migration/harness/tools/ticket_guard.py --repo martins-vds/ai-factory-pilot-target --reconcile-epic 224` | `03ce2407bca175e4` |  |  |
