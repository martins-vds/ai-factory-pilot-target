# Run journal: HR-04F-CLOSURE

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-05T14:07:18+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-05T14:09:03+00:00 | bootstrap-inputs | 1 | 0.03 | `python .migration/harness/tools/check_inputs.py --text 'Normal bootstrap requires '.migration/profile.yaml' '.migration/capabilities.yaml' '.migration/source.lock' '.migration/harness/tools/bootstrap.py' 'stacks/java-to-django.json''` | `32bef833d26e0f61` |  |  |
