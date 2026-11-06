# Run journal: HARNESS-COORDINATOR-FIXES

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-06T02:34:39+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-06T02:45:12+00:00 | parent-normal-bootstrap | 0 | 46.51 | `python3 /home/vinima/.copilot/session-state/c53b1a7f22614cd4814a2ad82cbfa0a9/files/harness-coordinator-approved-source/tools/bootstrap.py --target /home/vinima/.copilot/session-state/c53b1a7f22614cd4814a2ad82cbfa0a9/files/pilot198-rollout-review --profile .migration/profile.yaml --capabilities .migration/capabilities.yaml --stack-pack /home/vinima/.copilot/session-state/c53b1a7f22614cd4814a2ad82cb` | `4779d84e85763652` |  |  |
| 2026-11-06T02:45:39+00:00 | parent-preservation-parity | 0 | 0.15 | `python3 ../verify-pilot198-install.py` | `8234ea78516a3e92` |  |  |
| 2026-11-06T02:45:39+00:00 | parent-installed-integrity | 0 | 0.07 | `python3 .migration/harness/tools/check_installed.py` | `ded3aadcd399f8e6` |  |  |
| 2026-11-06T02:45:40+00:00 | parent-state-validation | 0 | 0.82 | `python3 .migration/harness/tools/validate.py .migration` | `ee0d254997a7a3b1` |  |  |
| 2026-11-06T02:53:29+00:00 | resume-setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-06T02:53:29+00:00 | verified-installed-integrity | 0 | 0.04 | `python .migration/harness/tools/check_installed.py` | `ded3aadcd399f8e6` |  |  |
| 2026-11-06T02:53:29+00:00 | verified-source-parity | 0 | 0.03 | `python -c 'import hashlib,json,pathlib; r=pathlib.Path(".").resolve(); s=pathlib.Path("/tmp/afs-source-e51998d716c229930e1e072cdcb05be0a872b4ef"); m=json.loads((r/".migration/harness/installed.json").read_text()); l=json.loads((s/"skills.lock.json").read_text()); sl={x["name"]:x["path"] for x in l["skills"] if x["install"]=="harness"}; es=[e for e in m["entries"] if e["kind"] in ("agent","tools","` | `fcc445722b1b5b27` |  |  |
| 2026-11-06T02:53:31+00:00 | verified-preservation | 0 | 1.17 | `python -c 'import subprocess,pathlib; b="a284b840e97e06452ca5370b941d22c4c6ae4f2d"; p=subprocess.check_output(["git","ls-tree","-r","--name-only",b],text=True).splitlines(); a={".github/agents/afs-program-orchestrator.agent.md",".github/agents/afs-slice-coordinator.agent.md",".github/skills/afs-setup-check/SKILL.md",".github/workflows/afs-acceptance.yml",".github/workflows/afs-costs.yml",".github/` | `2aee1fd75b2a6175` |  |  |
| 2026-11-06T02:53:31+00:00 | verified-state-validation | 0 | 0.55 | `python .migration/harness/tools/validate.py .migration` | `ee0d254997a7a3b1` |  |  |
