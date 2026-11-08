# Run journal: BK-ACCEPT

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-08T22:11:41+00:00 | runtime | 0 | 0.04 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.migration/harness/tools/check_runtime.py` | `96436ba39c5ef665` |  |  |
| 2026-11-08T22:11:41+00:00 | harness-integrity | 0 | 0.05 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.migration/harness/tools/check_installed.py` | `e129c16b4dc28ce5` |  |  |
| 2026-11-08T22:11:41+00:00 | services | 0 | 0.1 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.migration/harness/tools/afs-services check` | `274667623a156426` |  |  |
| 2026-11-08T22:11:41+00:00 | graph-freshness | 0 | 0.05 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.migration/harness/tools/check_graph_fresh.py --require source,target` | `77c677c7f49c1cf5` |  |  |
| 2026-11-08T22:11:41+00:00 | graph-source | 0 | 0.14 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.migration/harness/tools/graph_gate.py --side source --require-graph` | `97aa7c12f0569f31` |  | gate=graph side=source verdict=pass failures=0 entry_points=27 reaching_data=19 enriched_edges=1350 |
| 2026-11-08T22:11:42+00:00 | graph-target | 0 | 0.14 | `/opt/hostedtoolcache/Python/3.13.18/x64/bin/python /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.migration/harness/tools/graph_gate.py --side target --require-graph --enforce-ownership` | `3a6761967ba1ee56` |  | gate=graph side=target verdict=pass failures=0 entry_points=34 reaching_data=19 enriched_edges=782 |
| 2026-11-08T22:11:42+00:00 | build-0 | 0 | 0.06 | `bash -c 'python -m compileall -q src'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-08T22:11:42+00:00 | build-1 | 0 | 0.61 | `bash -c 'python manage.py check'` | `1e3e63f221bde888` |  |  |
| 2026-11-08T22:11:42+00:00 | idiom-0 | 0 | 0.02 | `bash -c 'ruff check'` | `82b3e6a6c090a576` |  |  |
| 2026-11-08T22:11:42+00:00 | idiom-1 | 0 | 0.02 | `bash -c 'ruff format --check'` | `2f72b17f517480b5` |  |  |
| 2026-11-08T22:12:30+00:00 | tests-0 | 0 | 47.25 | `bash -c 'pytest -q'` | `3073a523b044eb29` |  |  |
| 2026-11-08T22:13:16+00:00 | crap-0 | 0 | 46.67 | `bash -c 'pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov'` | `1243c388fcca7ebd` |  |  |
| 2026-11-08T22:13:17+00:00 | crap-1 | 0 | 0.09 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-08T22:13:17+00:00 | crap-2 | 0 | 0.05 | `bash -c 'python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30'` | `ac684dec6ba288ff` |  | gate=crap max=26.0 threshold=30 over=0 methods=213 |
| 2026-11-08T23:13:49+00:00 | mutation_full-0 | 0 | 3632.56 | `bash -c 'python .migration/harness/tools/afs-mutation --all'` | `99d5ec4b76d024a3` |  | gate=mutation score=0.931 threshold=0.8 killed=2065 survived=153 files=83 base=all |
