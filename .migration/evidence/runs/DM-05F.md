# Run journal: DM-05F

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-07T18:23:25+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T18:24:55+00:00 | snapshot-preflight | 0 | 0.07 | `python .migration/harness/tools/data_reconcile.py snapshot .migration/data/snapshot` | `bee2f0acd5234102` |  | gate=data-snapshot tables=7 problems=0 |
| 2026-11-07T18:25:01+00:00 | data-load | 1 | 1.47 | `python manage.py load_data_snapshot --snapshot .migration/data/snapshot --mapping .migration/data/mapping.yaml` | `a06a9a1326808ba6` | Traceback (most recent call last): |  |
| 2026-11-07T18:25:08+00:00 | schema-migrate | 0 | 0.64 | `python manage.py migrate --noinput` | `56d728c244009843` |  |  |
| 2026-11-07T18:25:09+00:00 | data-load | 0 | 0.56 | `python manage.py load_data_snapshot --snapshot .migration/data/snapshot --mapping .migration/data/mapping.yaml` | `102e06696c233e34` |  |  |
| 2026-11-07T18:27:56+00:00 | invariants-red | 1 | 3.43 | `pytest -q tests/data_migration/test_invariants.py` | `09e0ee6d31763de3` | E           ValueError: 'AAA01' is not a valid UN/LOCODE |  |
| 2026-11-07T18:28:08+00:00 | invariants-green | 1 | 2.65 | `pytest -q tests/data_migration/test_invariants.py` | `6b1991a96cb39e50` | assert len(cargos) == CargoRecord.objects.count() == 2 |  |
| 2026-11-07T18:28:25+00:00 | invariants-green-2 | 0 | 2.58 | `pytest -q tests/data_migration/test_invariants.py` | `df589a78f8a8b32b` |  |  |
| 2026-11-07T18:28:44+00:00 | build-compile | 0 | 0.06 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T18:28:45+00:00 | build-check | 0 | 0.42 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T18:28:45+00:00 | idiom-ruff | 1 | 0.03 | `ruff check` | `2eb5cc1c405d57dd` | 318 \|         assert len(movements) == 2 |  |
| 2026-11-07T18:28:55+00:00 | idiom-ruff-rerun | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T18:28:55+00:00 | idiom-format | 0 | 0.02 | `ruff format --check` | `1e2a3e2494e870c6` |  |  |
| 2026-11-07T18:28:57+00:00 | invariants-final | 0 | 2.61 | `pytest -q tests/data_migration/test_invariants.py` | `28456d16762f935e` |  |  |
| 2026-11-07T18:30:19+00:00 | behavior | 0 | 54.63 | `pytest -q` | `52585893b369b562` |  |  |
| 2026-11-07T18:31:09+00:00 | crap-coverage | 0 | 50.34 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `cd07715b21d6c105` |  |  |
| 2026-11-07T18:31:10+00:00 | crap-lizard | 0 | 0.15 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T18:31:10+00:00 | crap-score | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `7f9a11255491989c` |  | gate=crap max=26.0 threshold=30 over=0 methods=177 |
| 2026-11-07T18:31:10+00:00 | mutation-changed | 0 | 0.08 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `36603172da4a0d74` |  | gate=mutation score=n/a reason=no-mutable-code-changed base=origin/main |
| 2026-11-07T18:31:59+00:00 | regression | 0 | 49.15 | `pytest -q` | `aa1a98242ef7e30f` |  |  |
| 2026-11-07T20:44:24+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T20:45:44+00:00 | invariants-independent | 0 | 5.12 | `pytest -q tests/data_migration/test_invariants.py` | `55107bafcfbdb7c1` |  |  |
| 2026-11-07T20:45:58+00:00 | broken-itinerary-fixture | 1 | 1.87 | `pytest -q tests/data_migration/test_invariants.py::test_loaded_itinerary_legs_connect` | `b65cbfed9c72af84` | assert len(routed_cargo.itinerary.legs) == 2 |  |
| 2026-11-07T20:46:26+00:00 | invariants-restored | 0 | 2.18 | `pytest -q tests/data_migration/test_invariants.py` | `f007a127784409c8` |  |  |
| 2026-11-07T20:47:27+00:00 | build-compile-verifier | 0 | 0.07 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T20:47:28+00:00 | build-check-verifier | 0 | 0.37 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T20:47:28+00:00 | idiom-ruff-verifier | 0 | 0.03 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T20:47:28+00:00 | idiom-format-verifier | 0 | 0.02 | `ruff format --check` | `27b0eb549ee60b2d` |  |  |
| 2026-11-07T20:48:35+00:00 | behavior-verifier | 0 | 59.02 | `pytest -q` | `ba8a02c08057ead5` |  |  |
| 2026-11-07T20:49:31+00:00 | crap-coverage-verifier | 0 | 56.18 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `b126736d5eae8c4e` |  |  |
| 2026-11-07T20:49:31+00:00 | crap-lizard-verifier | 0 | 0.16 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T20:49:31+00:00 | crap-score-verifier | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `5ae953a68cbe67c7` |  | gate=crap max=26.0 threshold=30 over=0 methods=194 |
| 2026-11-07T20:49:31+00:00 | mutation-changed-verifier | 0 | 0.08 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `36603172da4a0d74` |  | gate=mutation score=n/a reason=no-mutable-code-changed base=origin/main |
| 2026-11-07T20:50:27+00:00 | regression-verifier | 0 | 56.06 | `pytest -q` | `7eeba45991bc4bb5` |  |  |
| 2026-11-07T20:53:50+00:00 | regression-final | 0 | 55.25 | `pytest -q` | `4742483f5c6e4435` |  |  |
