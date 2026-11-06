# Run journal: HARNESS-ADMIN-LIVE-MAP-DOMAIN-PARENT

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-06T16:28:30+00:00 | parent-normal-bootstrap | 0 | 108.13 | `python3 /home/vinima/.copilot/session-state/c53b1a7f22614cd4814a2ad82cbfa0a9/files/harness-domain-approved-source/tools/bootstrap.py --target /home/vinima/.copilot/session-state/c53b1a7f22614cd4814a2ad82cbfa0a9/files/pilot211-parent-bootstrap --profile /home/vinima/.copilot/session-state/c53b1a7f22614cd4814a2ad82cbfa0a9/files/pilot211-parent-bootstrap/.migration/profile.yaml --capabilities /home/v` | `fa2fbd6a1221ee12` |  |  |
| 2026-11-06T16:28:38+00:00 | parent-installed-integrity | 0 | 0.06 | `python3 .migration/harness/tools/check_installed.py` | `b3204e753b040c28` |  |  |
| 2026-11-06T16:28:38+00:00 | parent-migration-validation | 0 | 0.75 | `python3 .migration/harness/tools/validate.py .migration` | `446108b8fc1c3e05` |  |  |
| 2026-11-06T16:29:34+00:00 | parent-preservation-and-parity | 0 | 0.27 | `python3 /home/vinima/.copilot/session-state/c53b1a7f22614cd4814a2ad82cbfa0a9/files/verify-pilot211-install.py` | `5161bb25ff7bc4ab` |  |  |
| 2026-11-06T16:29:34+00:00 | parent-new-checker-tracing | 0 | 0.04 | `python3 .migration/harness/tools/check_domain_coverage.py --help` | `e1e5d211b67fc6e7` |  |  |
