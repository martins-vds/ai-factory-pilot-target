# Run journal: HR-04F-HARNESS

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-04T18:58:45+00:00 | bootstrap | 0 | 36.27 | `python3 /home/vinima/repos/ai-factory-swarm/tools/bootstrap.py --target . --profile .migration/profile.yaml --capabilities .migration/capabilities.yaml --stack-pack /home/vinima/repos/ai-factory-swarm/stacks/java-to-django.json` | `556428bcaf7d8405` |  |  |
| 2026-11-04T18:58:45+00:00 | installed-integrity | 0 | 0.21 | `python3 .migration/harness/tools/check_installed.py` | `1b443db2ad5232aa` |  |  |
| 2026-11-04T18:58:46+00:00 | preserved-inputs-and-evidence | 0 | 0.06 | `git diff --exit-code d3453215147cdad68a9cfbd8cf187a3e9d4d6e34 -- src templates tests characterization .migration/profile.yaml .migration/source.lock .migration/slices .migration/graphs .migration/ledger .migration/returns .migration/costs` | `e3b0c44298fc1c14` |  |  |
| 2026-11-04T18:59:36+00:00 | reviewed-pin-and-method-inference | 0 | 0.17 | `python3 .migration/evidence/HR-04F-HARNESS/check_rollout.py` | `8c96cb6a509915da` |  |  |
| 2026-11-04T18:59:37+00:00 | output-validation | 0 | 0.71 | `python3 .migration/harness/tools/validate.py .migration` | `a55ffa15a38fa513` |  |  |
| 2026-11-04T18:59:37+00:00 | previous-returns-and-journals-unchanged | 0 | 0.0 | `git diff --exit-code d3453215147cdad68a9cfbd8cf187a3e9d4d6e34 -- .migration/returns .migration/evidence/runs ':(exclude).migration/returns/HR-04F-HARNESS.afs-bootstrapper.yaml' ':(exclude).migration/evidence/runs/HR-04F-HARNESS.md'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-04T18:59:53+00:00 | attributed-return-validation | 0 | 0.76 | `python3 .migration/harness/tools/validate.py .migration` | `a55ffa15a38fa513` |  |  |
