# Run journal: BK-05B

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-07T04:09:16+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T04:13:45+00:00 | red-routing | 2 | 1.99 | `pytest -q tests/pathfinder/test_routing.py` | `3c1bad0393671bb2` | ______________ ERROR collecting tests/pathfinder/test_routing.py _______________ |  |
| 2026-11-07T04:14:06+00:00 | routing-service | 0 | 0.77 | `pytest -q tests/pathfinder/test_routing.py` | `689cba347b5af559` |  |  |
| 2026-11-07T04:14:50+00:00 | red-pathfinder-api | 2 | 0.59 | `pytest -q tests/pathfinder/test_api.py` | `e2c8c9cdf835cd06` | ________________ ERROR collecting tests/pathfinder/test_api.py _________________ |  |
| 2026-11-07T04:15:05+00:00 | pathfinder-tests | 0 | 0.87 | `pytest -q tests/pathfinder` | `a97fe8d679efa4e9` |  |  |
| 2026-11-07T04:15:48+00:00 | pathfinder-tests | 0 | 0.8 | `pytest -q tests/pathfinder` | `d5d6c7e3d74efa9f` |  |  |
| 2026-11-07T04:17:33+00:00 | idiom-ruff-check | 1 | 0.02 | `ruff check` | `35e1ef8de2e4d81f` | 44 \|                 assert parsed.utcoffset() == timedelta(0) |  |
| 2026-11-07T04:18:02+00:00 | idiom-ruff-check-diagnostic | 1 | 0.01 | `ruff check` | `35e1ef8de2e4d81f` | 44 \|                 assert parsed.utcoffset() == timedelta(0) |  |
| 2026-11-07T04:18:46+00:00 | idiom-ruff-check | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T04:18:55+00:00 | idiom-format-check | 1 | 0.03 | `ruff format --check` | `a3d3652e21b3aa24` | 26 \|         assert all( |  |
| 2026-11-07T04:19:03+00:00 | idiom-format-check | 0 | 0.01 | `ruff format --check` | `273e81e5999dffa5` |  |  |
| 2026-11-07T04:19:07+00:00 | pathfinder-tests | 0 | 0.8 | `pytest -q tests/pathfinder` | `f891ca4c15593a9c` |  |  |
| 2026-11-07T04:19:43+00:00 | build-compileall | 0 | 0.04 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T04:19:47+00:00 | build-django-check | 0 | 0.21 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T04:20:17+00:00 | full-tests | 0 | 25.82 | `pytest -q` | `a2a77f16747eb24c` |  |  |
| 2026-11-07T04:20:46+00:00 | crap-coverage | 0 | 22.14 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `d6067783288801ad` |  |  |
| 2026-11-07T04:20:50+00:00 | crap-lizard | 0 | 0.07 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T04:20:54+00:00 | crap-check | 0 | 0.02 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `f911be73e221b3f7` |  | gate=crap max=19.0 threshold=30 over=0 methods=138 |
| 2026-11-07T04:21:25+00:00 | mutation-changed | 1 | 25.49 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `c90390068a2c80c6` | afs-mutation: FAILED score=0.596 threshold=0.8 killed=53 survived=36 skipped=0 files=3 jobs=3 base=origin/main | gate=mutation score=0.596 threshold=0.8 killed=53 survived=36 files=3 base=origin/main |
| 2026-11-07T04:23:07+00:00 | pathfinder-tests-expanded | 0 | 0.84 | `pytest -q tests/pathfinder` | `3b5a5e0db37e2ddd` |  |  |
| 2026-11-07T04:23:11+00:00 | idiom-ruff-check | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T04:23:17+00:00 | idiom-format-check | 1 | 0.01 | `ruff format --check` | `72f6c0af28fe2748` | 45  \|         assert all( |  |
| 2026-11-07T04:23:25+00:00 | idiom-format-check | 0 | 0.01 | `ruff format --check` | `273e81e5999dffa5` |  |  |
| 2026-11-07T04:24:00+00:00 | mutation-changed | 0 | 26.46 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `35f6e3518629d5e9` |  | gate=mutation score=0.910 threshold=0.8 killed=81 survived=8 files=3 base=origin/main |
| 2026-11-07T04:24:48+00:00 | pathfinder-tests-final | 0 | 0.94 | `pytest -q tests/pathfinder` | `9737c558e193fb2f` |  |  |
| 2026-11-07T04:24:51+00:00 | idiom-ruff-check | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T04:24:55+00:00 | idiom-format-check | 0 | 0.01 | `ruff format --check` | `273e81e5999dffa5` |  |  |
| 2026-11-07T04:25:30+00:00 | mutation-changed | 0 | 29.94 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `6c9514973e57f8f8` |  | gate=mutation score=0.921 threshold=0.8 killed=82 survived=7 files=3 base=origin/main |
| 2026-11-07T04:26:03+00:00 | full-tests | 0 | 23.33 | `pytest -q` | `ca2271d987fab7f6` |  |  |
| 2026-11-07T04:26:31+00:00 | crap-coverage | 0 | 24.33 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `e3b17e986be8d49b` |  |  |
| 2026-11-07T04:26:36+00:00 | crap-check | 0 | 0.03 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `f911be73e221b3f7` |  | gate=crap max=19.0 threshold=30 over=0 methods=138 |
