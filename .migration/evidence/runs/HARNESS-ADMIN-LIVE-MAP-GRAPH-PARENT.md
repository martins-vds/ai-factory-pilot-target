# Run journal: HARNESS-ADMIN-LIVE-MAP-GRAPH-PARENT

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-06T14:58:12+00:00 | parent-normal-bootstrap | 0 | 56.63 | `python3 /home/vinima/.copilot/session-state/c53b1a7f22614cd4814a2ad82cbfa0a9/files/harness-admin-map-approved-source/tools/bootstrap.py --target /home/vinima/.copilot/session-state/c53b1a7f22614cd4814a2ad82cbfa0a9/files/pilot209-parent-bootstrap --profile /home/vinima/.copilot/session-state/c53b1a7f22614cd4814a2ad82cbfa0a9/files/pilot209-parent-bootstrap/.migration/profile.yaml --capabilities /hom` | `733e4536dac6c3e2` |  |  |
| 2026-11-06T14:59:18+00:00 | parent-preservation-and-parity | 0 | 0.14 | `python3 /home/vinima/.copilot/session-state/c53b1a7f22614cd4814a2ad82cbfa0a9/files/verify-pilot209-install.py` | `fdfdb75fb61481b8` |  |  |
| 2026-11-06T14:59:18+00:00 | parent-installed-integrity | 0 | 0.06 | `python3 .migration/harness/tools/check_installed.py` | `3cc4ff5ba9f911a0` |  |  |
| 2026-11-06T14:59:19+00:00 | parent-migration-validation | 0 | 0.81 | `python3 .migration/harness/tools/validate.py .migration` | `cefb166b037d28b2` |  |  |
