# Run journal: HARNESS-ADMIN-LIVE-MAP-GRAPH

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-06T14:48:50+00:00 | setup-validation | 0 | 0.66 | `python .migration/harness/tools/validate.py .migration` | `1f4ff7e5cda8e1f6` |  |  |
| 2026-11-06T14:48:50+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-06T14:48:50+00:00 | setup-services | 0 | 0.12 | `python .migration/harness/tools/afs-services check` | `274667623a156426` |  |  |
| 2026-11-06T14:48:50+00:00 | setup-runtime | 0 | 0.05 | `python .migration/harness/tools/check_runtime.py` | `d07c895212ff2443` |  |  |
| 2026-11-06T14:48:56+00:00 | approved-source-acquisition | 22 | 0.03 | `curl --fail --location --show-error --silent --connect-timeout 15 --max-time 60 --output /tmp/afs-harness-bdf1f43b613f5ed6c7719380cede7c02bca1c778.tar.gz https://api.github.com/repos/martins-vds/ai-factory-swarm/tarball/bdf1f43b613f5ed6c7719380cede7c02bca1c778` | `e85a8cbf6458f846` | curl: (22) The requested URL returned error: 403 |  |
| 2026-11-06T14:49:18+00:00 | installed-integrity | 0 | 0.05 | `python .migration/harness/tools/check_installed.py` | `ded3aadcd399f8e6` |  |  |
| 2026-11-06T14:49:18+00:00 | baseline-preservation | 1 | 0.06 | `bash -c 'git diff --exit-code d77b7bec98d26e7ee291488091d009e89f595117 HEAD && git diff --exit-code && python -c "import collections,json,pathlib,subprocess,yaml; b=\"d77b7bec98d26e7ee291488d009e89f595117\"; paths=subprocess.check_output([\"git\",\"ls-tree\",\"-r\",\"--name-only\",\"HEAD\"],text=True).splitlines(); returns=[p for p in paths if p.startswith(\".migration/returns/\") and p.endswith(\` | `3ed6fbf3a3ca0797` | Traceback (most recent call last): |  |
| 2026-11-06T14:49:33+00:00 | baseline-preservation-corrected | 0 | 0.04 | `bash -c 'git diff --exit-code d77b7bec98d26e7ee291488091d009e89f595117 HEAD && git diff --exit-code && python -c "import collections,json,pathlib,subprocess,yaml; paths=subprocess.check_output([\"git\",\"ls-tree\",\"-r\",\"--name-only\",\"HEAD\"],text=True).splitlines(); returns=[p for p in paths if p.startswith(\".migration/returns/\") and p.endswith(\".yaml\")]; c=collections.Counter(x[\"status\` | `da66f22555192f97` |  |  |
| 2026-11-06T14:50:07+00:00 | setup-ticket-inputs | 1 | 0.02 | `python .migration/harness/tools/check_inputs.py` | `a6ba7e9296076d23` |  |  |
| 2026-11-06T14:50:07+00:00 | application-source-input | 0 | 0.0 | `test -f /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.source/src/main/webapp/admin/tracking/map.xhtml` | `e3b0c44298fc1c14` |  |  |
| 2026-11-06T14:50:57+00:00 | final-validation | 0 | 0.53 | `python .migration/harness/tools/validate.py .migration` | `cefb166b037d28b2` |  |  |
| 2026-11-06T14:50:58+00:00 | final-integrity | 0 | 0.04 | `python .migration/harness/tools/check_installed.py` | `ded3aadcd399f8e6` |  |  |
