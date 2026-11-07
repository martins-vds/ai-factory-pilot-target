# Run journal: DM-05C

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-07T05:14:19+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T05:15:05+00:00 | snapshot | 0 | 0.06 | `python .migration/harness/tools/data_reconcile.py snapshot .migration/data/snapshot` | `bee2f0acd5234102` |  | gate=data-snapshot tables=7 problems=0 |
| 2026-11-07T05:16:58+00:00 | loader-red | 1 | 3.13 | `pytest -q tests/data_migration/test_load.py` | `c29933f1f16abc82` | E               KeyError: 'load_data_snapshot' |  |
| 2026-11-07T05:18:03+00:00 | loader-green | 1 | 1.64 | `pytest -q tests/data_migration/test_load.py` | `24aadeb264b70940` | # Daft, but matches old exception sans the err msg. |  |
| 2026-11-07T05:18:23+00:00 | loader-green-2 | 0 | 1.56 | `pytest -q tests/data_migration/test_load.py` | `d44de49cc8aa128c` |  |  |
| 2026-11-07T05:18:31+00:00 | data-load | 1 | 0.39 | `python manage.py load_data_snapshot --snapshot .migration/data/snapshot --mapping .migration/data/mapping.yaml` | `3d0e4f7dc207cab6` | Traceback (most recent call last): |  |
| 2026-11-07T05:18:38+00:00 | migrate-db | 0 | 0.47 | `python manage.py migrate --noinput` | `56d728c244009843` |  |  |
| 2026-11-07T05:18:42+00:00 | data-load-2 | 0 | 0.39 | `python manage.py load_data_snapshot --snapshot .migration/data/snapshot --mapping .migration/data/mapping.yaml` | `102e06696c233e34` |  |  |
| 2026-11-07T05:19:43+00:00 | data-load-rerun | 0 | 0.42 | `python manage.py load_data_snapshot --snapshot .migration/data/snapshot --mapping .migration/data/mapping.yaml` | `102e06696c233e34` |  |  |
| 2026-11-07T05:19:47+00:00 | build-compile | 0 | 0.04 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T05:19:50+00:00 | build-check | 0 | 0.34 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T05:19:53+00:00 | idiom-ruff | 1 | 0.02 | `ruff check` | `996a433aeb71085f` |  |  |
| 2026-11-07T05:20:27+00:00 | idiom-ruff-2 | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T05:20:30+00:00 | idiom-format | 1 | 0.02 | `ruff format --check` | `307b7d568fbd28b7` | 158 \|     except OSError as error: |  |
| 2026-11-07T05:20:44+00:00 | idiom-format-2 | 0 | 0.01 | `ruff format --check` | `c98b86154f37b741` |  |  |
| 2026-11-07T05:20:54+00:00 | loader-regression | 0 | 1.57 | `pytest -q tests/data_migration/test_load.py` | `b29404b0332b987b` |  |  |
| 2026-11-07T05:21:39+00:00 | behavior | 1 | 41.18 | `pytest -q` | `5c979d86dc6e3f05` | assert settings.BASE_DIR == Path(__file__).resolve().parents[1] |  |
| 2026-11-07T05:51:33+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T05:53:04+00:00 | behavior | 0 | 26.57 | `pytest -q` | `dca0ba4d21778cac` |  |  |
| 2026-11-07T05:53:18+00:00 | build-compile | 0 | 0.03 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T05:53:21+00:00 | build-check | 0 | 0.22 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T05:53:24+00:00 | idiom-ruff-check | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T05:53:26+00:00 | idiom-format-check | 0 | 0.01 | `ruff format --check` | `c98b86154f37b741` |  |  |
| 2026-11-07T05:53:53+00:00 | crap-coverage | 0 | 24.0 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `679cce7877933639` |  |  |
| 2026-11-07T05:53:57+00:00 | crap-lizard | 0 | 0.08 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T05:54:00+00:00 | crap-score | 1 | 0.03 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `5cfa4d5970f1aefc` |  | gate=crap max=64.2 threshold=30 over=2 methods=151 |
| 2026-11-07T05:57:13+00:00 | mutation-changed | 1 | 176.75 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `3d5674fad37a0529` | afs-mutation: FAILED score=0.590 threshold=0.8 killed=174 survived=121 skipped=0 files=3 jobs=3 base=origin/main | gate=mutation score=0.590 threshold=0.8 killed=174 survived=121 files=3 base=origin/main |
| 2026-11-07T05:59:16+00:00 | loader-transform-tests | 0 | 1.18 | `pytest -q tests/data_migration/test_load.py` | `fc9523279c6881ef` |  |  |
| 2026-11-07T05:59:30+00:00 | build-compile-rerun | 0 | 0.03 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T05:59:33+00:00 | build-check-rerun | 0 | 0.23 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T06:00:02+00:00 | behavior-rerun | 0 | 27.3 | `pytest -q` | `a8682e0ff1abea49` |  |  |
| 2026-11-07T06:00:05+00:00 | idiom-ruff-check-rerun | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T06:00:08+00:00 | idiom-format-check-rerun | 0 | 0.01 | `ruff format --check` | `c98b86154f37b741` |  |  |
| 2026-11-07T06:00:37+00:00 | crap-coverage-rerun | 0 | 26.42 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `dba06c00c1425134` |  |  |
| 2026-11-07T06:00:40+00:00 | crap-lizard-rerun | 0 | 0.09 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T06:00:43+00:00 | crap-score-rerun | 1 | 0.03 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `f2855acf53916c15` |  | gate=crap max=38.7 threshold=30 over=2 methods=151 |
| 2026-11-07T06:01:54+00:00 | regression | 0 | 28.26 | `pytest -q` | `06bcc17a3b5b930b` |  |  |
| 2026-11-07T12:46:07+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T12:48:04+00:00 | lizard-baseline | 0 | 0.12 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T12:48:50+00:00 | snapshot-preflight | 0 | 0.05 | `python .migration/harness/tools/data_reconcile.py snapshot .migration/data/snapshot` | `bee2f0acd5234102` |  | gate=data-snapshot tables=7 problems=0 |
| 2026-11-07T12:51:43+00:00 | loader-contract-tests | 1 | 2.03 | `pytest -q tests/data_migration/test_load.py` | `6cca45e03831a965` | E           ValueError: invalid literal for int() with base 10: '2026-11-07 00:40:40.322' |  |
| 2026-11-07T12:51:53+00:00 | mutation-baseline | 1 | 228.66 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `5dd8e6d641b379dc` | afs-mutation: FAILED score=0.620 threshold=0.8 killed=183 survived=112 skipped=0 files=3 jobs=3 base=origin/main | gate=mutation score=0.620 threshold=0.8 killed=183 survived=112 files=3 base=origin/main |
| 2026-11-07T12:52:03+00:00 | loader-contract-tests-rerun | 0 | 1.58 | `pytest -q tests/data_migration/test_load.py` | `9e1f2780037dd611` |  |  |
| 2026-11-07T12:52:26+00:00 | loader-refactor-tests | 0 | 1.57 | `pytest -q tests/data_migration/test_load.py` | `ff8b70c9209cc2a9` |  |  |
| 2026-11-07T12:53:01+00:00 | idiom-ruff-check | 0 | 0.03 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T12:53:01+00:00 | build-compile | 0 | 0.1 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T12:53:01+00:00 | idiom-format-check | 0 | 0.03 | `ruff format --check` | `c98b86154f37b741` |  |  |
| 2026-11-07T12:53:01+00:00 | build-check | 0 | 0.33 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T12:53:40+00:00 | behavior | 0 | 35.22 | `pytest -q` | `e985152d42537a5c` |  |  |
| 2026-11-07T12:54:22+00:00 | crap-coverage | 0 | 31.5 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `115a29d13e876923` |  |  |
| 2026-11-07T12:54:25+00:00 | crap-lizard | 0 | 0.12 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T12:54:28+00:00 | crap-score | 1 | 0.03 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `a93e4685bc36891b` |  | gate=crap max=37.4 threshold=30 over=2 methods=157 |
| 2026-11-07T12:56:11+00:00 | mapping-contract-tests | 0 | 1.99 | `pytest -q tests/data_migration/test_load.py` | `dee50331f3550c6e` |  |  |
| 2026-11-07T12:56:52+00:00 | crap-coverage-mapping-tests | 0 | 34.36 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `2dcb1fdf03ad43e2` |  |  |
| 2026-11-07T12:56:56+00:00 | crap-lizard-mapping-tests | 0 | 0.11 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T12:56:59+00:00 | crap-score-mapping-tests | 0 | 0.03 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `40067e260b62dacd` |  | gate=crap max=29.8 threshold=30 over=0 methods=157 |
| 2026-11-07T12:57:42+00:00 | mutation-changed | 2 | 7.06 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `fabf0357e6de9435` | afs-mutation: mutmut failed on src/cargotracker/data_migration/loader.py; its mutants were not tested: | gate=mutation score=n/a error=mutmut-failed failed_files=2 files=3 base=origin/main |
| 2026-11-07T12:58:28+00:00 | unparameterized-mapping-tests | 0 | 1.84 | `pytest -q tests/data_migration/test_load.py` | `38c73c4aa6537238` |  |  |
| 2026-11-07T13:01:29+00:00 | behavior-final | 0 | 34.18 | `pytest -q` | `9ac7c865f4698fc2` |  |  |
| 2026-11-07T13:02:10+00:00 | crap-coverage-final | 0 | 35.04 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `f350e371861115c9` |  |  |
| 2026-11-07T13:02:19+00:00 | crap-lizard-final | 0 | 0.12 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T13:02:23+00:00 | crap-score-final | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `40067e260b62dacd` |  | gate=crap max=29.8 threshold=30 over=0 methods=157 |
| 2026-11-07T13:02:45+00:00 | build-compile-final | 0 | 0.06 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T13:02:45+00:00 | idiom-ruff-final | 0 | 0.03 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T13:02:45+00:00 | idiom-format-final | 0 | 0.02 | `ruff format --check` | `c98b86154f37b741` |  |  |
| 2026-11-07T13:02:45+00:00 | build-check-final | 0 | 0.32 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T13:03:02+00:00 | mutation-changed-rerun | 1 | 254.17 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `97de1a65a8a41610` | afs-mutation: FAILED score=0.682 threshold=0.8 killed=206 survived=96 skipped=0 files=3 jobs=3 base=origin/main | gate=mutation score=0.682 threshold=0.8 killed=206 survived=96 files=3 base=origin/main |
| 2026-11-07T15:07:11+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T15:11:18+00:00 | fixture-tests-red | 1 | 4.33 | `pytest -q tests/data_migration/test_load.py` | `f32e6a773551c5b5` | options = {'verbosity': 1, 'settings': None, 'pythonpath': None, 'traceback': False, ...} |  |
| 2026-11-07T15:11:43+00:00 | fixture-tests-green | 0 | 1.66 | `pytest -q tests/data_migration/test_load.py` | `6789680c21af067c` |  |  |
| 2026-11-07T15:12:02+00:00 | fixture-tests-final | 0 | 1.67 | `pytest -q tests/data_migration/test_load.py` | `2b485f61c9190426` |  |  |
| 2026-11-07T15:12:02+00:00 | fixture-snapshot-check | 0 | 0.04 | `python .migration/harness/tools/data_reconcile.py snapshot tests/data_migration/fixtures/DM-05C` | `525bd2128fe2515f` |  | gate=data-snapshot tables=6 problems=0 |
| 2026-11-07T15:12:26+00:00 | build-compile-fixture | 0 | 0.05 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T15:12:27+00:00 | build-check-fixture | 0 | 0.27 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T15:12:27+00:00 | idiom-ruff-fixture | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T15:12:27+00:00 | idiom-format-fixture | 0 | 0.01 | `ruff format --check` | `c98b86154f37b741` |  |  |
| 2026-11-07T15:12:58+00:00 | behavior-fixture | 0 | 31.54 | `pytest -q` | `79266cbb1f4c0a83` |  |  |
| 2026-11-07T15:13:27+00:00 | crap-coverage-fixture | 0 | 28.51 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `fd7f78a890141da6` |  |  |
| 2026-11-07T15:13:27+00:00 | crap-lizard-fixture | 0 | 0.09 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T15:13:27+00:00 | crap-score-fixture | 0 | 0.03 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `40067e260b62dacd` |  | gate=crap max=29.8 threshold=30 over=0 methods=157 |
| 2026-11-07T15:17:39+00:00 | mutation-changed-fixture | 1 | 247.28 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `56bc2d213a40121c` | afs-mutation: FAILED score=0.695 threshold=0.8 killed=210 survived=92 skipped=0 files=3 jobs=3 base=origin/main | gate=mutation score=0.695 threshold=0.8 killed=210 survived=92 files=3 base=origin/main |
| 2026-11-07T15:20:46+00:00 | survivor-tests | 1 | 2.27 | `pytest -q tests/data_migration/test_load.py` | `f8c38f4e16b0c5a5` | E           AssertionError: Regex pattern did not match. |  |
| 2026-11-07T15:20:56+00:00 | survivor-tests-final | 1 | 2.31 | `pytest -q tests/data_migration/test_load.py` | `89bf4fcf039b210b` | E           AssertionError: Regex pattern did not match. |  |
| 2026-11-07T15:21:07+00:00 | survivor-tests-verified | 0 | 2.39 | `pytest -q tests/data_migration/test_load.py` | `e2f3094058850728` |  |  |
| 2026-11-07T15:21:10+00:00 | fixture-snapshot-final | 0 | 0.04 | `python .migration/harness/tools/data_reconcile.py snapshot tests/data_migration/fixtures/DM-05C` | `525bd2128fe2515f` |  | gate=data-snapshot tables=6 problems=0 |
| 2026-11-07T15:21:10+00:00 | idiom-ruff-survivors | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T15:21:10+00:00 | idiom-format-survivors | 0 | 0.01 | `ruff format --check` | `c98b86154f37b741` |  |  |
| 2026-11-07T15:21:19+00:00 | build-compile-survivors | 0 | 0.03 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T15:21:19+00:00 | build-check-survivors | 0 | 0.25 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T15:21:45+00:00 | behavior-survivors | 0 | 26.08 | `pytest -q` | `f098e7852bfabc00` |  |  |
| 2026-11-07T15:22:13+00:00 | crap-coverage-survivors | 0 | 27.25 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `ce3a07b68ddd0f87` |  |  |
| 2026-11-07T15:22:13+00:00 | crap-lizard-survivors | 0 | 0.08 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T15:22:13+00:00 | crap-score-survivors | 0 | 0.03 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `0ee29d308b3e0f2c` |  | gate=crap max=29.8 threshold=30 over=0 methods=157 |
| 2026-11-07T15:26:39+00:00 | mutation-changed-final | 1 | 262.47 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `c2bf76a9c8992d0d` | afs-mutation: FAILED score=0.752 threshold=0.8 killed=227 survived=75 skipped=0 files=3 jobs=3 base=origin/main | gate=mutation score=0.752 threshold=0.8 killed=227 survived=75 files=3 base=origin/main |
| 2026-11-07T17:27:38+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T17:33:19+00:00 | mutation-changed | 1 | 329.27 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `c2bf76a9c8992d0d` | afs-mutation: FAILED score=0.752 threshold=0.8 killed=227 survived=75 skipped=0 files=3 jobs=3 base=origin/main | gate=mutation score=0.752 threshold=0.8 killed=227 survived=75 files=3 base=origin/main |
| 2026-11-07T17:37:25+00:00 | loader-mutant-tests | 1 | 3.57 | `pytest -q tests/data_migration/test_load.py` | `8743d56608027081` | with pytest.raises(CommandError) as error: |  |
| 2026-11-07T17:37:42+00:00 | loader-mutant-tests-rerun | 0 | 3.56 | `pytest -q tests/data_migration/test_load.py` | `e38475f21a06abc9` |  |  |
