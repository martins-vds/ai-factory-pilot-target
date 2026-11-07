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
| 2026-11-07T19:53:05+00:00 | fixture-snapshot-check | 0 | 0.05 | `python .migration/harness/tools/data_reconcile.py snapshot tests/data_migration/fixtures/DM-05C` | `525bd2128fe2515f` |  | gate=data-snapshot tables=6 problems=0 |
| 2026-11-07T19:53:06+00:00 | fixture-load | 1 | 0.47 | `python manage.py load_data_snapshot --snapshot tests/data_migration/fixtures/DM-05C --mapping .migration/data/mapping.yaml` | `a06a9a1326808ba6` | Traceback (most recent call last): |  |
| 2026-11-07T19:53:06+00:00 | fixture-export | 1 | 0.34 | `python manage.py export_data_snapshot --mapping .migration/data/mapping.yaml --out .migration/runs/DM-05D/fixture-export` | `447ea869025774ba` | Traceback (most recent call last): |  |
| 2026-11-07T19:53:06+00:00 | fixture-reconcile | 1 | 0.06 | `python .migration/harness/tools/data_reconcile.py reconcile --snapshot tests/data_migration/fixtures/DM-05C --target .migration/runs/DM-05D/fixture-export --mapping .migration/data/mapping.yaml --report /tmp/DM-05D-reconciliation.md` | `8d1d1bb79118b271` | ::error::location: rows: snapshot 2, target 0; content differs: only in snapshot: id=101; only in snapshot: id=102 | gate=data-reconcile tables=6 rows=2 mismatched_tables=6 |
| 2026-11-07T19:53:15+00:00 | fixture-database-migrate | 0 | 0.38 | `python manage.py migrate --noinput` | `56d728c244009843` |  |  |
| 2026-11-07T19:53:20+00:00 | fixture-load | 0 | 0.33 | `python manage.py load_data_snapshot --snapshot tests/data_migration/fixtures/DM-05C --mapping .migration/data/mapping.yaml` | `1853e482c3557f1c` |  |  |
| 2026-11-07T19:53:20+00:00 | fixture-export | 0 | 0.34 | `python manage.py export_data_snapshot --mapping .migration/data/mapping.yaml --out .migration/runs/DM-05D/fixture-export` | `ed5f1d08e822887e` |  |  |
| 2026-11-07T19:53:20+00:00 | fixture-reconcile | 0 | 0.06 | `python .migration/harness/tools/data_reconcile.py reconcile --snapshot tests/data_migration/fixtures/DM-05C --target .migration/runs/DM-05D/fixture-export --mapping .migration/data/mapping.yaml --report /tmp/DM-05D-reconciliation.md` | `cc4f9b78ce7ba0ae` |  | gate=data-reconcile tables=6 rows=7 mismatched_tables=0 |
| 2026-11-07T19:53:36+00:00 | build-compileall | 0 | 0.05 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T19:53:37+00:00 | build-django-check | 0 | 0.32 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T19:54:19+00:00 | behavior | 0 | 42.03 | `pytest -q` | `a0e80345a1334237` |  |  |
| 2026-11-07T19:54:19+00:00 | idiom-ruff-check | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T19:54:19+00:00 | idiom-ruff-format | 1 | 0.02 | `ruff format --check` | `1d6e46749efb98d7` | -     assert {path.stem for path in output.glob('*.csv')} == { |  |
| 2026-11-07T19:54:59+00:00 | crap-coverage | 0 | 40.48 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `8a2d24c45a000490` |  |  |
| 2026-11-07T19:54:59+00:00 | crap-lizard | 0 | 0.12 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T19:55:00+00:00 | crap-score | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `a7bfc7f045556709` |  | gate=crap max=26.0 threshold=30 over=0 methods=194 |
| 2026-11-07T19:56:14+00:00 | mutation-changed | 0 | 74.58 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `79c3a4699244dc73` |  | gate=mutation score=0.951 threshold=0.8 killed=98 survived=5 files=2 base=origin/main |
| 2026-11-07T19:56:56+00:00 | regression | 0 | 41.99 | `pytest -q` | `8f3abf5dea89f691` |  |  |
| 2026-11-07T19:57:38+00:00 | verifier-focused-tests-rerun | 0 | 1.72 | `pytest -q tests/data_migration/test_export.py` | `bb0617a4d5262ac3` |  |  |
| 2026-11-07T19:57:54+00:00 | build-compileall-final | 0 | 0.04 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T19:57:55+00:00 | build-django-check-final | 0 | 0.32 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T19:58:38+00:00 | behavior-final | 0 | 42.94 | `pytest -q` | `7ef9221bd3fa85d3` |  |  |
| 2026-11-07T19:58:38+00:00 | idiom-ruff-check-final | 1 | 0.01 | `ruff check` | `66d6f816be595f42` | Found 1 error. |  |
| 2026-11-07T19:58:38+00:00 | idiom-ruff-format-final | 0 | 0.01 | `ruff format --check` | `05facc7430ea9711` |  |  |
| 2026-11-07T19:59:26+00:00 | crap-coverage-final | 0 | 48.64 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `289f50c5a7c322a5` |  |  |
| 2026-11-07T19:59:27+00:00 | crap-lizard-final | 0 | 0.12 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T19:59:27+00:00 | crap-score-final | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `5ae953a68cbe67c7` |  | gate=crap max=26.0 threshold=30 over=0 methods=194 |
| 2026-11-07T20:00:45+00:00 | mutation-changed-final | 0 | 78.04 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `841b87b4fab049ab` |  | gate=mutation score=0.981 threshold=0.8 killed=101 survived=2 files=2 base=origin/main |
| 2026-11-07T20:01:27+00:00 | regression-final | 0 | 42.43 | `pytest -q` | `e462ca77758f3f21` |  |  |
| 2026-11-07T20:01:51+00:00 | verifier-focused-tests-final | 0 | 1.84 | `pytest -q tests/data_migration/test_export.py` | `d1ead8e694c6a06d` |  |  |
| 2026-11-07T20:01:51+00:00 | idiom-ruff-check-final-rerun | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T20:01:51+00:00 | idiom-ruff-format-final-rerun | 0 | 0.01 | `ruff format --check` | `05facc7430ea9711` |  |  |
