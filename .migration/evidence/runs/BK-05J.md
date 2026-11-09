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
| 2026-11-09T03:28:26+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-09T03:28:42+00:00 | graph-source-fresh | 0 | 0.05 | `python .migration/harness/tools/check_graph_fresh.py --require source` | `90cd01282d340dfc` |  |  |
| 2026-11-09T03:28:51+00:00 | graph-source-gate | 0 | 0.14 | `python .migration/harness/tools/graph_gate.py --side source` | `97aa7c12f0569f31` |  | gate=graph side=source verdict=pass failures=0 entry_points=27 reaching_data=19 enriched_edges=1350 |
| 2026-11-09T03:29:25+00:00 | acceptance-fetch | 0 | 0.31 | `python .migration/harness/tools/afs-acceptance fetch --run-id 42528425964 --attempt 1 --dest .migration/runs/acceptance-42528425964-1` | `15c2f15c155f27d8` |  |  |
| 2026-11-09T03:29:28+00:00 | acceptance-verify | 2 | 0.05 | `python .migration/harness/tools/afs-acceptance verify .migration/runs/acceptance-42528425964-1 --commit 135c70a276d4b20d377d701e064c9c819de4151c --run-id 42528425964 --attempt 1` | `1d432f27f2d34ce2` |  |  |
| 2026-11-09T03:32:02+00:00 | booking-ledger-review | 0 | 0.05 | `python -c 'from pathlib import Path; import yaml; entries=[]; missing=[]; bad=[]
for p in sorted(Path(".migration/ledger").glob("booking.*.yaml")):
 d=yaml.safe_load(p.read_text());
 if not isinstance(d,dict) or not d.get("id"): continue
 entries.append(d)
 if d.get("status") != "migrated": bad.append((d["id"],d.get("status")))
 for c in d.get("target",{}).get("components",[]):
  if not Path(c).ex` | `8b5e8fb8d12c9274` |  |  |
