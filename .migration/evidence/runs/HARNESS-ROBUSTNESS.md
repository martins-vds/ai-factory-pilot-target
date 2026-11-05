# Run journal: HARNESS-ROBUSTNESS

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-05T18:54:39+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-05T18:56:37+00:00 | pinned-normal-bootstrap | 1 | 20.54 | `python /tmp/afs-harness-ee54dfdda8d86b324fa2818aa82c6b5b6456dbd1/tools/bootstrap.py --target /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target --profile /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.migration/profile.yaml --capabilities /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.migration/capabilities.yaml --stack-pack /tmp/afs-harness-e` | `90785a0267781dd5` | Traceback (most recent call last): |  |
| 2026-11-05T18:58:54+00:00 | migration-state-validation | 0 | 0.85 | `python .migration/harness/tools/validate.py .migration` | `c784e0bf7a2d7bdb` |  |  |
| 2026-11-05T18:59:15+00:00 | final-state-validation | 0 | 0.82 | `python .migration/harness/tools/validate.py .migration` | `c784e0bf7a2d7bdb` |  |  |
