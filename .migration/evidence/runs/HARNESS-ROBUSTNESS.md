# Run journal: HARNESS-ROBUSTNESS

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-05T18:54:39+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-05T18:56:37+00:00 | pinned-normal-bootstrap | 1 | 20.54 | `python /tmp/afs-harness-ee54dfdda8d86b324fa2818aa82c6b5b6456dbd1/tools/bootstrap.py --target /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target --profile /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.migration/profile.yaml --capabilities /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.migration/capabilities.yaml --stack-pack /tmp/afs-harness-e` | `90785a0267781dd5` | Traceback (most recent call last): |  |
| 2026-11-05T18:58:54+00:00 | migration-state-validation | 0 | 0.85 | `python .migration/harness/tools/validate.py .migration` | `c784e0bf7a2d7bdb` |  |  |
| 2026-11-05T18:59:15+00:00 | final-state-validation | 0 | 0.82 | `python .migration/harness/tools/validate.py .migration` | `c784e0bf7a2d7bdb` |  |  |
| 2026-11-05T19:06:06+00:00 | coordinator-pinned-bootstrap | 0 | 86.75 | `python3 ../harness75-approved-source/tools/bootstrap.py --target . --profile .migration/profile.yaml --capabilities .migration/capabilities.yaml --stack-pack ../harness75-approved-source/stacks/java-to-django.json --create-gap-issues` | `3cf68dfe01025a9d` |  |  |
| 2026-11-05T19:06:23+00:00 | coordinator-install-integrity | 0 | 0.06 | `python3 .migration/harness/tools/check_installed.py` | `84be7e50875f2269` |  |  |
| 2026-11-05T19:06:24+00:00 | coordinator-installed-state | 1 | 0.72 | `python3 .migration/harness/tools/validate.py .migration` | `d1cb431a977bc0f6` | 92 file(s) checked, 2 error(s) |  |
| 2026-11-05T19:07:48+00:00 | coordinator-source-preservation | 1 | 0.42 | `python3 ../verify-pilot193-install.py` | `582049862d083df8` | Traceback (most recent call last): |  |
| 2026-11-05T19:08:01+00:00 | coordinator-source-preservation | 0 | 0.1 | `python3 ../verify-pilot193-install.py` | `4fd7dfbb93c3bdb4` |  |  |
| 2026-11-05T19:08:02+00:00 | coordinator-committed-state | 0 | 0.76 | `python3 .migration/harness/tools/validate.py .migration` | `c784e0bf7a2d7bdb` |  |  |
| 2026-11-05T19:09:28+00:00 | coordinator-final-preservation | 0 | 0.1 | `python3 ../verify-pilot193-install.py` | `4fd7dfbb93c3bdb4` |  |  |
| 2026-11-05T19:09:28+00:00 | coordinator-final-state | 0 | 0.68 | `python3 .migration/harness/tools/validate.py .migration` | `c784e0bf7a2d7bdb` |  |  |
| 2026-11-05T19:11:42+00:00 | resumed-setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
