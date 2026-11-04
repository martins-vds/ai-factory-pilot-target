# Run journal: HR-04E-HARNESS

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-04T16:53:05+00:00 | bootstrap | 0 | 48.29 | `python3 /home/vinima/repos/ai-factory-swarm/tools/bootstrap.py --target . --profile .migration/profile.yaml --capabilities .migration/capabilities.yaml --stack-pack /home/vinima/repos/ai-factory-swarm/stacks/java-to-django.json` | `d80dbce6d21ee32b` |  |  |
| 2026-11-04T16:53:05+00:00 | installed-integrity | 0 | 0.07 | `python3 .migration/harness/tools/check_installed.py` | `47bd0c5b47633064` |  |  |
| 2026-11-04T16:53:05+00:00 | output-validation | 0 | 0.78 | `python3 .migration/harness/tools/validate.py .migration` | `57ec10eac2a7a391` |  |  |
| 2026-11-04T16:53:54+00:00 | preserved-inputs-and-wiring | 0 | 0.06 | `python3 .migration/evidence/HR-04E-HARNESS/check_rollout.py` | `c74c847e2e26cd78` |  |  |
| 2026-11-04T16:53:54+00:00 | stack-ancestry-replay | 0 | 0.05 | `python3 .migration/harness/tools/check_stack_base.py --event .migration/evidence/HR-04E-HARNESS/pr-169-replay.json` | `2e079d35136dae89` |  |  |
| 2026-11-04T16:53:56+00:00 | attribution-169-replay | 0 | 1.84 | `python3 .migration/harness/tools/check_return_contract.py --base origin/copilot/hr-04e-differentially-replay-handling-goldens --event .migration/evidence/HR-04E-HARNESS/pr-169-replay.json` | `99a26c9ec771892b` |  |  |
| 2026-11-04T16:53:57+00:00 | attribution-167-prospective-replay | 0 | 0.78 | `python3 .migration/harness/tools/check_return_contract.py --base origin/main --event .migration/evidence/HR-04E-HARNESS/pr-167-prospective-replay.json` | `66db89dbc975de19` |  |  |
| 2026-11-04T16:53:57+00:00 | existing-evidence-unchanged | 0 | 0.01 | `git diff --exit-code e25ccc8ecb4c0fe979e85116940fe2b6e9ce36ed -- src tests characterization .migration/ledger .migration/costs .migration/returns/HR-04E.afs-verifier.yaml .migration/returns/HR-04E-FIX.afs-specialist-migrator.yaml .migration/evidence/runs/HR-04E.md .migration/evidence/runs/HR-04E-FIX.md` | `e3b0c44298fc1c14` |  |  |
| 2026-11-04T16:55:24+00:00 | final-output-validation | 0 | 0.58 | `python3 .migration/harness/tools/validate.py .migration` | `57ec10eac2a7a391` |  |  |
