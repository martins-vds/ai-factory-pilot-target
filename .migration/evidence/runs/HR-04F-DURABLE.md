# Run journal: HR-04F-DURABLE

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-04T21:28:27+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-04T21:30:02+00:00 | pinned-harness-checkout | 1 | 0.03 | `python -c 'from pathlib import Path; paths=[Path("/home/vinima/repos/ai-factory-swarm"), Path("/home/runner/work/ai-factory-swarm")]; matches=[p for p in paths if (p/"tools/bootstrap.py").is_file() and (p/"stacks/java-to-django.json").is_file()]; print("clean pinned checkout found:", matches); raise SystemExit(0 if matches else 1)'` | `280ebc4fcb0ad6ce` |  |  |
| 2026-11-04T21:30:06+00:00 | installed-integrity | 0 | 0.07 | `python .migration/harness/tools/check_installed.py` | `1b443db2ad5232aa` |  |  |
| 2026-11-04T21:30:11+00:00 | migration-state-validation | 0 | 0.76 | `python .migration/harness/tools/validate.py .migration` | `a55ffa15a38fa513` |  |  |
| 2026-11-04T21:30:19+00:00 | exact-input-preservation | 0 | 0.01 | `bash -c 'git diff --exit-code 5cace249987e3ddd4ce3345a845168ca545bab55 -- src templates tests characterization .migration/profile.yaml .migration/source.lock .migration/capabilities.yaml .migration/slices .migration/graphs .migration/ledger .migration/returns .migration/costs .migration/evidence/HR-04F-HARNESS .migration/evidence/runs ":(exclude).migration/evidence/runs/HR-04F-DURABLE.md"'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-04T21:30:32+00:00 | source-graph-flow | 0 | 0.1 | `python .migration/harness/tools/graph_gate.py --side source --require-graph` | `c070c957323aa7e9` |  | gate=graph side=source verdict=pass failures=0 entry_points=27 reaching_data=18 enriched_edges=1352 |
| 2026-11-04T21:30:36+00:00 | target-graph-flow | 0 | 0.09 | `python .migration/harness/tools/graph_gate.py --side target --require-graph` | `4b734ce13b6fa527` |  | gate=graph side=target verdict=pass failures=0 entry_points=7 reaching_data=3 enriched_edges=510 |
| 2026-11-04T21:30:40+00:00 | graph-freshness | 0 | 0.08 | `python .migration/harness/tools/check_graph_fresh.py --require source,target` | `e58be4641e00fbe4` |  |  |
| 2026-11-04T21:31:28+00:00 | acceptance-installation-state | 1 | 0.03 | `python -c 'import json,os; from pathlib import Path; pin="344241e92256a6048183f99063ca297fb96780de"; m=json.loads(Path(".migration/harness/installed.json").read_text()); t=Path(".migration/harness/tools/afs-acceptance"); w=Path(".github/workflows/afs-acceptance.yml"); checks={"requested_pin":m.get("harness_commit")==pin,"acceptance_executable":t.is_file() and os.access(t,os.X_OK),"manual_acceptanc` | `4e7269a355f1f9f9` |  |  |
| 2026-11-04T21:32:19+00:00 | output-validation | 0 | 0.78 | `python .migration/harness/tools/validate.py .migration` | `a71c6a78c9e8726a` |  |  |
| 2026-11-04T21:32:29+00:00 | return-contract | 0 | 0.13 | `python .migration/harness/tools/check_return_contract.py --base origin/main` | `156481c2d16ac806` |  |  |
| 2026-11-04T21:32:34+00:00 | final-protected-inputs | 0 | 0.01 | `bash -c 'git diff --exit-code 5cace249987e3ddd4ce3345a845168ca545bab55 -- src templates tests characterization .migration/profile.yaml .migration/source.lock .migration/capabilities.yaml .migration/slices .migration/graphs .migration/ledger .migration/returns .migration/costs .migration/evidence/HR-04F-HARNESS .migration/evidence/runs .migration/handoffs .migration/evidence/HR-04F-DURABLE ":(exclu` | `e3b0c44298fc1c14` |  |  |
| 2026-11-04T21:32:54+00:00 | named-pilot-inputs | 0 | 0.03 | `python .migration/harness/tools/check_inputs.py --text 'Inputs: '.migration/source.lock' '.migration/profile.yaml' '.migration/capabilities.yaml''` | `ae14ecefd7578858` |  |  |
| 2026-11-04T21:33:34+00:00 | final-output-validation | 0 | 0.76 | `python .migration/harness/tools/validate.py .migration` | `a71c6a78c9e8726a` |  |  |
| 2026-11-04T21:34:35+00:00 | final-final-validation | 0 | 0.77 | `python .migration/harness/tools/validate.py .migration` | `a71c6a78c9e8726a` |  |  |
