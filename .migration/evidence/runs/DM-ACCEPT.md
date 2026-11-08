# Run journal: DM-ACCEPT

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-08T01:32:51+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-08T00:07:00+00:00 | runtime | 0 | 0.06 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.migration/harness/tools/check_runtime.py` | `96436ba39c5ef665` |  |  |
| 2026-11-08T00:07:00+00:00 | harness-integrity | 0 | 0.06 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.migration/harness/tools/check_installed.py` | `d38512e3bf5acce1` |  |  |
| 2026-11-08T00:07:00+00:00 | services | 0 | 0.14 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.migration/harness/tools/afs-services check` | `274667623a156426` |  |  |
| 2026-11-08T00:07:00+00:00 | graph-freshness | 0 | 0.08 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.migration/harness/tools/check_graph_fresh.py --require source,target` | `4cef16213f2824e3` |  |  |
| 2026-11-08T00:07:01+00:00 | graph-source | 0 | 0.21 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.migration/harness/tools/graph_gate.py --side source --require-graph` | `97aa7c12f0569f31` |  | gate=graph side=source verdict=pass failures=0 entry_points=27 reaching_data=19 enriched_edges=1350 |
| 2026-11-08T00:07:01+00:00 | graph-target | 0 | 0.19 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.migration/harness/tools/graph_gate.py --side target --require-graph --enforce-ownership` | `9af5f1ee0e7a8564` |  | gate=graph side=target verdict=pass failures=0 entry_points=22 reaching_data=6 enriched_edges=699 |
| 2026-11-08T00:07:01+00:00 | build-0 | 0 | 0.08 | `bash -c 'python -m compileall -q src'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-08T00:07:02+00:00 | build-1 | 0 | 0.84 | `bash -c 'python manage.py check'` | `1e3e63f221bde888` |  |  |
| 2026-11-08T00:07:02+00:00 | idiom-0 | 0 | 0.02 | `bash -c 'ruff check'` | `82b3e6a6c090a576` |  |  |
| 2026-11-08T00:07:02+00:00 | idiom-1 | 0 | 0.02 | `bash -c 'ruff format --check'` | `dd6674ff09df8dc3` |  |  |
| 2026-11-08T00:08:03+00:00 | tests-0 | 0 | 61.02 | `bash -c 'pytest -q'` | `278a8a04ba78d036` |  |  |
| 2026-11-08T00:09:00+00:00 | crap-0 | 0 | 57.23 | `bash -c 'pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov'` | `21c215211a8e0965` |  |  |
| 2026-11-08T00:09:00+00:00 | crap-1 | 0 | 0.13 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-08T00:09:01+00:00 | crap-2 | 0 | 0.06 | `bash -c 'python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30'` | `ed5d9610a42ebca8` |  | gate=crap max=26.0 threshold=30 over=0 methods=200 |
| 2026-11-08T01:15:36+00:00 | mutation_full-0 | 0 | 3995.62 | `bash -c 'python .migration/harness/tools/afs-mutation --all'` | `82811e94f810b421` |  | gate=mutation score=0.914 threshold=0.8 killed=1895 survived=178 files=80 base=all |
| 2026-11-08T03:01:39+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
