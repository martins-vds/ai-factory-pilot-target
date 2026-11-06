# Run journal: HARNESS-ADMIN-LIVE-MAP-DOMAIN

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-06T16:17:42+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-06T16:20:16+00:00 | source-tree-and-current-state | 0 | 0.06 | `python -c 'import json,pathlib,subprocess,yaml; root=pathlib.Path("/tmp/afs-admin-map-source/tree"); tree=subprocess.check_output(["git","-C",str(root),"write-tree"],text=True).strip(); cap=yaml.safe_load(pathlib.Path(".migration/capabilities.yaml").read_text()); counts={k:sum(c["status"]==k for c in cap["capabilities"]) for k in ("met","gap","waived","not-applicable")}; installed=json.loads(pathl` | `c0ff0ee408693623` |  |  |
| 2026-11-06T16:20:20+00:00 | source-head-metadata | 128 | 0.0 | `git -C /tmp/afs-admin-map-source/tree rev-parse HEAD` | `e000a2af1ee89f0a` | fatal: ambiguous argument 'HEAD': unknown revision or path not in the working tree. |  |
| 2026-11-06T16:20:54+00:00 | migration-state-validation | 0 | 0.96 | `python .migration/harness/tools/validate.py .migration` | `446108b8fc1c3e05` |  |  |
| 2026-11-06T16:21:16+00:00 | final-migration-state-validation | 0 | 0.95 | `python .migration/harness/tools/validate.py .migration` | `446108b8fc1c3e05` |  |  |
| 2026-11-06T16:32:55+00:00 | resume-setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
