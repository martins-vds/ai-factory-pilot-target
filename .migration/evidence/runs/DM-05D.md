# Run journal: DM-05D

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-07T18:23:05+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T18:25:57+00:00 | focused-tests-red | 1 | 3.71 | `pytest -q tests/data_migration/test_export.py` | `22ed5e1e4222ac2b` | E               KeyError: 'export_data_snapshot' |  |
| 2026-11-07T18:26:45+00:00 | focused-tests-green | 1 | 1.83 | `pytest -q tests/data_migration/test_export.py` | `4ff492f89c5a2b65` | >           assert reader.fieldnames == ['id', 'unlocode', 'name'] |  |
| 2026-11-07T18:26:59+00:00 | focused-tests-green | 0 | 1.82 | `pytest -q tests/data_migration/test_export.py` | `e72d445d99fd8599` |  |  |
| 2026-11-07T18:27:47+00:00 | idiom-ruff-check | 0 | 0.06 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T18:27:47+00:00 | idiom-ruff-format | 1 | 0.04 | `ruff format --check` | `9579572f2b14114c` |  |  |
| 2026-11-07T18:27:47+00:00 | build-compileall | 0 | 0.12 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T18:27:48+00:00 | build-django-check | 0 | 0.41 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T18:27:55+00:00 | idiom-ruff-format-rerun | 0 | 0.01 | `ruff format --check` | `c7a0bcb17dd5241a` |  |  |
| 2026-11-07T18:28:48+00:00 | behavior | 0 | 50.05 | `pytest -q` | `d0990b68bdbcbeb6` |  |  |
| 2026-11-07T18:29:41+00:00 | crap-coverage | 0 | 46.62 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `18f2ce24c0bac4a6` |  |  |
| 2026-11-07T18:29:44+00:00 | crap-lizard | 0 | 0.16 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T18:29:48+00:00 | crap-score | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `3b66fdac6c140535` |  | gate=crap max=26.0 threshold=30 over=0 methods=186 |
| 2026-11-07T18:31:35+00:00 | snapshot-check | 0 | 0.06 | `python .migration/harness/tools/data_reconcile.py snapshot .migration/data/snapshot/` | `bee2f0acd5234102` |  | gate=data-snapshot tables=7 problems=0 |
| 2026-11-07T18:31:55+00:00 | mutation-changed | 1 | 97.5 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `33aff7a71b52ec31` | afs-mutation: FAILED score=0.660 threshold=0.8 killed=68 survived=35 skipped=0 files=2 jobs=2 base=origin/main | gate=mutation score=0.660 threshold=0.8 killed=68 survived=35 files=2 base=origin/main |
| 2026-11-07T18:32:54+00:00 | focused-ordering-red | 1 | 1.89 | `pytest -q tests/data_migration/test_export.py` | `ee6158c5a9c588e7` | assert reader.fieldnames == [ |  |
| 2026-11-07T18:33:02+00:00 | focused-ordering-green | 0 | 1.81 | `pytest -q tests/data_migration/test_export.py` | `e72d445d99fd8599` |  |  |
| 2026-11-07T18:34:38+00:00 | focused-contract-tests-red | 1 | 2.08 | `pytest -q tests/data_migration/test_export.py` | `05bf36e60dff272d` | with pytest.raises(CommandError) as error: |  |
| 2026-11-07T18:34:49+00:00 | focused-contract-tests-green | 1 | 2.0 | `pytest -q tests/data_migration/test_export.py` | `d6c65eb2f8ce99d2` | assert exit.value.code == 0 |  |
| 2026-11-07T18:35:01+00:00 | focused-contract-tests-green | 0 | 1.96 | `pytest -q tests/data_migration/test_export.py` | `1587aa4746f084ae` |  |  |
| 2026-11-07T18:35:12+00:00 | idiom-ruff-check-rerun | 0 | 0.03 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T18:35:12+00:00 | build-compileall-rerun | 0 | 0.06 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T18:35:12+00:00 | idiom-ruff-format-rerun-2 | 0 | 0.02 | `ruff format --check` | `c7a0bcb17dd5241a` |  |  |
| 2026-11-07T18:35:13+00:00 | build-django-check-rerun | 0 | 0.4 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T18:37:10+00:00 | mutation-changed-rerun | 0 | 95.88 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `39372be25f1abeb0` |  | gate=mutation score=0.903 threshold=0.8 killed=93 survived=10 files=2 base=origin/main |
| 2026-11-07T18:38:18+00:00 | focused-tests-final | 0 | 1.95 | `pytest -q tests/data_migration/test_export.py` | `93d3d3b1534cccb1` |  |  |
| 2026-11-07T18:38:35+00:00 | idiom-final-check | 0 | 0.03 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T18:38:35+00:00 | build-final-compile | 0 | 0.07 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T18:38:35+00:00 | idiom-final-format | 1 | 0.04 | `ruff format --check` | `c952bcfafec2c598` |  |  |
| 2026-11-07T18:39:59+00:00 | mutation-changed-final | 0 | 93.45 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `ee13008ccd6e15ef` |  | gate=mutation score=0.932 threshold=0.8 killed=96 survived=7 files=2 base=origin/main |
| 2026-11-07T18:40:26+00:00 | idiom-final-format-rerun | 0 | 0.01 | `ruff format --check` | `c7a0bcb17dd5241a` |  |  |
| 2026-11-07T18:40:26+00:00 | idiom-final-check-rerun | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T18:41:18+00:00 | behavior-final | 0 | 48.27 | `pytest -q` | `74b720883657388d` |  |  |
| 2026-11-07T18:42:10+00:00 | crap-coverage-final | 0 | 47.86 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `bbca98b03f5f12d6` |  |  |
| 2026-11-07T18:42:14+00:00 | crap-lizard-final | 0 | 0.15 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T18:42:18+00:00 | crap-score-final | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `21b4f85baaf8f356` |  | gate=crap max=26.0 threshold=30 over=0 methods=186 |
| 2026-11-07T18:43:10+00:00 | regression | 0 | 48.1 | `pytest -q` | `2512467a7207958c` |  |  |
| 2026-11-07T18:44:50+00:00 | mutation-changed-final-rerun | 0 | 93.52 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `ee13008ccd6e15ef` |  | gate=mutation score=0.932 threshold=0.8 killed=96 survived=7 files=2 base=origin/main |
| 2026-11-07T19:49:07+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T19:52:18+00:00 | verifier-focused-tests | 0 | 4.1 | `pytest -q tests/data_migration/test_export.py` | `6e894aa45f503752` |  |  |
