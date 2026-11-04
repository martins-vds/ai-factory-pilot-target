# Run journal: HR-04F

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-04T19:28:17+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-04T19:28:38+00:00 | graph-source | 0 | 0.1 | `python .migration/harness/tools/graph_gate.py --side source` | `c070c957323aa7e9` |  | gate=graph side=source verdict=pass failures=0 entry_points=27 reaching_data=18 enriched_edges=1352 |
| 2026-11-04T19:28:38+00:00 | graph-target | 0 | 0.08 | `python .migration/harness/tools/graph_gate.py --side target --require-graph` | `4b734ce13b6fa527` |  | gate=graph side=target verdict=pass failures=0 entry_points=7 reaching_data=3 enriched_edges=510 |
| 2026-11-04T19:29:41+00:00 | build-compileall | 0 | 0.09 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-04T19:29:43+00:00 | build-django-check | 0 | 1.8 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-04T19:29:43+00:00 | idiom-ruff-check | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-04T19:29:43+00:00 | idiom-ruff-format | 0 | 0.02 | `ruff format --check` | `13e464c51f06111c` |  |  |
| 2026-11-04T19:30:28+00:00 | tests | 0 | 44.94 | `pytest -q` | `29ae69f512e05c95` |  |  |
| 2026-11-04T19:31:09+00:00 | crap | 0 | 40.76 | `bash -c 'pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov && lizard --csv src > .migration/runs/lizard.csv && python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30'` | `60d2ec6e1107695c` |  | gate=crap max=19.0 threshold=30 over=0 methods=132 |
| 2026-11-04T19:31:09+00:00 | mutation-changed | 0 | 0.08 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `36603172da4a0d74` |  | gate=mutation score=n/a reason=no-mutable-code-changed base=origin/main |
