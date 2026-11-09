# Run journal: BK-05J

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-08T14:02:40+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-08T14:05:59+00:00 | idiom-ruff-format | 0 | 0.04 | `ruff format --check` | `c799b224f99851f8` |  |  |
| 2026-11-08T14:05:59+00:00 | idiom-ruff-check | 0 | 0.04 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-08T14:05:59+00:00 | build-compile | 0 | 0.12 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-08T14:06:01+00:00 | build-django-check | 0 | 1.7 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-08T14:07:01+00:00 | tests | 0 | 56.54 | `pytest -q` | `f477d2be76098dc5` |  |  |
| 2026-11-08T14:07:57+00:00 | crap-coverage | 0 | 51.12 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `4583ff68924c4c30` |  |  |
| 2026-11-08T14:08:00+00:00 | crap-lizard | 0 | 0.12 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-08T14:08:03+00:00 | crap-report | 0 | 0.03 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `46edc5c319c80c3b` |  | gate=crap max=26.0 threshold=30 over=0 methods=213 |
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
| 2026-11-09T03:28:26+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-09T03:28:42+00:00 | graph-source-fresh | 0 | 0.05 | `python .migration/harness/tools/check_graph_fresh.py --require source` | `90cd01282d340dfc` |  |  |
| 2026-11-09T03:28:51+00:00 | graph-source-gate | 0 | 0.14 | `python .migration/harness/tools/graph_gate.py --side source` | `97aa7c12f0569f31` |  | gate=graph side=source verdict=pass failures=0 entry_points=27 reaching_data=19 enriched_edges=1350 |
| 2026-11-09T03:29:25+00:00 | acceptance-fetch | 0 | 0.31 | `python .migration/harness/tools/afs-acceptance fetch --run-id 42528425964 --attempt 1 --dest .migration/runs/acceptance-42528425964-1` | `15c2f15c155f27d8` |  |  |
| 2026-11-09T03:29:28+00:00 | acceptance-verify | 2 | 0.05 | `python .migration/harness/tools/afs-acceptance verify .migration/runs/acceptance-42528425964-1 --commit 135c70a276d4b20d377d701e064c9c819de4151c --run-id 42528425964 --attempt 1` | `1d432f27f2d34ce2` |  |  |
| 2026-11-09T03:30:18+00:00 | acceptance-verify-executed-tree | 0 | 0.08 | `python .migration/harness/tools/afs-acceptance verify /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.migration/runs/acceptance-42528425964-1 --commit 135c70a276d4b20d377d701e064c9c819de4151c --run-id 42528425964 --attempt 1` | `36cc4a271fd56ca9` |  | gate=acceptance-evidence status=verified commit=135c70a276d4b20d377d701e064c9c819de4151c run_id=42528425964 attempt=1 |
| 2026-11-09T03:32:02+00:00 | booking-ledger-review | 0 | 0.05 | `python -c 'from pathlib import Path; import yaml; entries=[]; missing=[]; bad=[]
for p in sorted(Path(".migration/ledger").glob("booking.*.yaml")):
 d=yaml.safe_load(p.read_text());
 if not isinstance(d,dict) or not d.get("id"): continue
 entries.append(d)
 if d.get("status") != "migrated": bad.append((d["id"],d.get("status")))
 for c in d.get("target",{}).get("components",[]):
  if not Path(c).ex` | `8b5e8fb8d12c9274` |  |  |
| 2026-11-09T03:34:16+00:00 | validate-audit-outputs | 0 | 1.13 | `python .migration/harness/tools/validate.py .migration` | `bf7e7b29be6a839d` |  |  |
