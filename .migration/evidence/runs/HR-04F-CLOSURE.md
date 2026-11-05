# Run journal: HR-04F-CLOSURE

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-05T14:07:18+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-05T14:09:03+00:00 | bootstrap-inputs | 1 | 0.03 | `python .migration/harness/tools/check_inputs.py --text 'Normal bootstrap requires '.migration/profile.yaml' '.migration/capabilities.yaml' '.migration/source.lock' '.migration/harness/tools/bootstrap.py' 'stacks/java-to-django.json''` | `32bef833d26e0f61` |  |  |
| 2026-11-05T14:13:17+00:00 | coordinator-normal-bootstrap | 0 | 30.48 | `python3 /home/vinima/.copilot/session-state/c53b1a7f22614cd4814a2ad82cbfa0a9/files/harness71-approved-source/tools/bootstrap.py --target . --profile .migration/profile.yaml --capabilities .migration/capabilities.yaml --stack-pack /home/vinima/.copilot/session-state/c53b1a7f22614cd4814a2ad82cbfa0a9/files/harness71-approved-source/stacks/java-to-django.json` | `1d84e142872f1d03` |  |  |
| 2026-11-05T14:13:50+00:00 | coordinator-preservation | 0 | 0.13 | `python3 /home/vinima/.copilot/session-state/c53b1a7f22614cd4814a2ad82cbfa0a9/files/hr04f-closure-coordinator-check.py` | `146263dc17cee507` |  |  |
| 2026-11-05T14:13:50+00:00 | coordinator-integrity | 0 | 0.06 | `python3 .migration/harness/tools/check_installed.py` | `586f410745c430a3` |  |  |
| 2026-11-05T14:13:51+00:00 | coordinator-state | 0 | 0.5 | `python3 .migration/harness/tools/validate.py .migration` | `eead015f60953286` |  |  |
| 2026-11-05T14:13:51+00:00 | coordinator-graph-freshness | 0 | 0.06 | `python3 .migration/harness/tools/check_graph_fresh.py --require source,target` | `e58be4641e00fbe4` |  |  |
| 2026-11-05T14:13:51+00:00 | coordinator-graph-source | 0 | 0.06 | `python3 .migration/harness/tools/graph_gate.py --side source --require-graph` | `c070c957323aa7e9` |  | gate=graph side=source verdict=pass failures=0 entry_points=27 reaching_data=18 enriched_edges=1352 |
| 2026-11-05T14:13:51+00:00 | coordinator-graph-target | 0 | 0.06 | `python3 .migration/harness/tools/graph_gate.py --side target --require-graph` | `4b734ce13b6fa527` |  | gate=graph side=target verdict=pass failures=0 entry_points=7 reaching_data=3 enriched_edges=510 |
| 2026-11-05T14:13:53+00:00 | coordinator-epic-guard | 0 | 2.46 | `python3 .migration/harness/tools/check_slice_returns.py --repo martins-vds/ai-factory-pilot-target --epic 113` | `dce44c9177986af3` |  | gate=slice-returns epic=113 verdict=pass tickets=9 failures=0 |
