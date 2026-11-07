# Run journal: AM-04B

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-07T04:17:05+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T04:19:45+00:00 | red-all-cargo-data | 2 | 2.14 | `pytest -q tests/cargo/interfaces/test_admin_live_map_data.py` | `14ffb7e522c6d9a2` | _____ ERROR collecting tests/cargo/interfaces/test_admin_live_map_data.py ______ |  |
| 2026-11-07T04:20:02+00:00 | green-all-cargo-data | 0 | 1.41 | `pytest -q tests/cargo/interfaces/test_admin_live_map_data.py` | `38e13be45293b3a0` |  |  |
| 2026-11-07T04:20:50+00:00 | red-coordinates-routes-settings | 1 | 1.64 | `pytest -q tests/cargo/interfaces/test_admin_live_map_data.py` | `7b78e92c2138e085` | >       assert cargos[0]['location'] == {'code': 'XXXXX', 'name': 'Unknown'} |  |
| 2026-11-07T04:21:17+00:00 | green-admin-map-data-routes | 0 | 1.63 | `pytest -q tests/cargo/interfaces/test_admin_live_map_data.py` | `e3bc99a1d6726a8f` |  |  |
| 2026-11-07T04:22:22+00:00 | existing-map-regression | 0 | 2.93 | `pytest -q tests/cargo/interfaces/test_map.py` | `b4a1cafe6e9b54e9` |  |  |
| 2026-11-07T04:23:46+00:00 | build-compileall | 0 | 0.03 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T04:23:50+00:00 | build-django-check | 0 | 0.24 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T04:23:53+00:00 | idiom-ruff-check | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T04:23:56+00:00 | idiom-ruff-format | 1 | 0.01 | `ruff format --check` | `ac9ef9c219417344` |  |  |
| 2026-11-07T04:24:05+00:00 | idiom-ruff-format-rerun | 0 | 0.01 | `ruff format --check` | `8f54ec861a76fc44` |  |  |
| 2026-11-07T04:24:35+00:00 | behavior-suite | 0 | 26.45 | `pytest -q` | `e5517dfebb49b885` |  |  |
| 2026-11-07T04:25:04+00:00 | crap-pytest-coverage | 0 | 25.29 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `085f25b64c2fc013` |  |  |
| 2026-11-07T04:25:10+00:00 | crap-lizard | 0 | 0.08 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T04:25:13+00:00 | crap-threshold | 0 | 0.03 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `2d81ffde79cb771b` |  | gate=crap max=19.0 threshold=30 over=0 methods=138 |
| 2026-11-07T04:26:00+00:00 | mutation-changed | 2 | 41.43 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `de3320ae5b3afbb1` | afs-mutation: mutmut failed on src/cargotracker/cargo/interfaces/admin_map/views.py; its mutants were not tested: | gate=mutation score=n/a error=mutmut-failed failed_files=2 files=4 base=origin/main |
| 2026-11-07T04:26:54+00:00 | regression-suite | 0 | 25.04 | `pytest -q` | `74124f79096bf7d6` |  |  |
| 2026-11-07T04:29:25+00:00 | mutation-changed-single-worker | 1 | 122.11 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `543e813a148ef07a` | afs-mutation: FAILED score=0.774 threshold=0.8 killed=41 survived=12 skipped=0 files=4 jobs=1 base=origin/main | gate=mutation score=0.774 threshold=0.8 killed=41 survived=12 files=4 base=origin/main |
| 2026-11-07T04:30:15+00:00 | endpoint-test-strengthening | 0 | 2.19 | `pytest -q tests/cargo/interfaces/test_admin_live_map_data.py` | `15faff48b9bed89c` |  |  |
| 2026-11-07T04:31:42+00:00 | mutation-changed-strengthened | 0 | 80.29 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `9a3b91de6e23666a` |  | gate=mutation score=0.868 threshold=0.8 killed=46 survived=7 files=4 base=origin/main |
| 2026-11-07T04:31:56+00:00 | idiom-final-ruff-check | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T04:31:59+00:00 | idiom-final-format | 0 | 0.01 | `ruff format --check` | `8f54ec861a76fc44` |  |  |
| 2026-11-07T04:32:28+00:00 | behavior-final | 0 | 26.05 | `pytest -q` | `3fd8831d407791af` |  |  |
| 2026-11-07T04:32:57+00:00 | crap-final-coverage | 0 | 25.48 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `353505535bc3c9c4` |  |  |
| 2026-11-07T04:33:00+00:00 | crap-final-lizard | 0 | 0.08 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T04:33:04+00:00 | crap-final-threshold | 0 | 0.03 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `2d81ffde79cb771b` |  | gate=crap max=19.0 threshold=30 over=0 methods=138 |
| 2026-11-07T04:33:33+00:00 | regression-final | 0 | 25.05 | `pytest -q` | `fefc73d2da944e5a` |  |  |
| 2026-11-07T04:38:51+00:00 | composition-wiring-test | 0 | 2.0 | `pytest -q tests/cargo/interfaces/test_admin_live_map_data.py` | `40b6802d60ce19e0` |  |  |
| 2026-11-07T04:39:04+00:00 | composition-ruff-check | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T04:39:07+00:00 | composition-format-check | 0 | 0.01 | `ruff format --check` | `8f54ec861a76fc44` |  |  |
| 2026-11-07T04:39:11+00:00 | composition-build-compileall | 0 | 0.03 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T04:39:15+00:00 | composition-build-django-check | 0 | 0.27 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T04:39:50+00:00 | composition-behavior-suite | 0 | 31.32 | `pytest -q` | `bd5f5041b193e09c` |  |  |
| 2026-11-07T04:40:22+00:00 | composition-crap-coverage | 0 | 28.02 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `745db2e6be42744b` |  |  |
| 2026-11-07T04:40:26+00:00 | composition-crap-lizard | 0 | 0.08 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T04:40:31+00:00 | composition-crap-threshold | 0 | 0.03 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `6c5a7b5a5f079222` |  | gate=crap max=19.0 threshold=30 over=0 methods=140 |
| 2026-11-07T04:41:03+00:00 | composition-regression-suite | 0 | 27.58 | `pytest -q` | `ab5476780a33672b` |  |  |
| 2026-11-07T04:42:33+00:00 | composition-mutation-changed | 0 | 85.34 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `97bf2b3b5204b790` |  | gate=mutation score=0.870 threshold=0.8 killed=47 survived=7 files=4 base=origin/main |
