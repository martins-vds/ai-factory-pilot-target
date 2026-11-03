# Run journal: HR-04B

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-03T18:18:40+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-03T18:21:43+00:00 | behavior-red | 2 | 4.31 | `pytest -q tests/handling/test_registration_attempt_repository.py` | `78a2800ff80d2d93` | ___ ERROR collecting tests/handling/test_registration_attempt_repository.py ____ |  |
| 2026-11-03T18:22:56+00:00 | behavior-accepted | 0 | 1.23 | `pytest -q tests/handling/test_registration_attempt_repository.py` | `4e221273d861ce0e` |  |  |
| 2026-11-03T18:23:44+00:00 | repository-tests | 0 | 1.31 | `pytest -q tests/handling/test_registration_attempt_repository.py` | `ecde7e16d7742946` |  |  |
| 2026-11-03T18:24:56+00:00 | skip-locked-test | 0 | 1.33 | `pytest -q tests/handling/test_registration_attempt_repository.py` | `3d84880b5ebc05a9` |  |  |
| 2026-11-03T18:26:42+00:00 | idiom-format-check | 0 | 0.02 | `ruff format --check` | `291d91fd4256e9a8` |  |  |
| 2026-11-03T18:26:42+00:00 | idiom-ruff-check | 1 | 0.05 | `ruff check` | `623066115990c6d8` |  |  |
| 2026-11-03T18:26:42+00:00 | build-compile | 0 | 0.05 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-03T18:26:43+00:00 | build-django-check | 0 | 0.36 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-03T18:26:55+00:00 | behavior | 0 | 12.81 | `pytest -q` | `3f68bd8949118397` |  |  |
| 2026-11-03T18:27:36+00:00 | idiom-format-check | 0 | 0.02 | `ruff format --check` | `291d91fd4256e9a8` |  |  |
| 2026-11-03T18:27:36+00:00 | idiom-ruff-check | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-03T18:27:37+00:00 | migration-drift | 0 | 0.36 | `python manage.py makemigrations handling --check --dry-run` | `f91468a08ee08a1e` |  |  |
| 2026-11-03T18:28:17+00:00 | idiom-format | 0 | 0.02 | `ruff format --check` | `291d91fd4256e9a8` |  |  |
| 2026-11-03T18:28:17+00:00 | idiom-lint | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-03T18:28:17+00:00 | build-compile | 0 | 0.05 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-03T18:28:17+00:00 | build-check | 0 | 0.38 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-03T18:28:35+00:00 | behavior | 0 | 13.16 | `pytest -q` | `ad86665461dd644d` |  |  |
| 2026-11-03T18:28:52+00:00 | regression | 0 | 13.01 | `pytest -q` | `660f5da137eb5c4b` |  |  |
| 2026-11-03T18:29:10+00:00 | crap | 1 | 13.03 | `bash -c 'pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov && lizard --csv src > .migration/runs/lizard.csv && python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30'` | `221a633c6afdffe9` |  | gate=crap max=35.5 threshold=30 over=1 methods=106 |
| 2026-11-03T18:29:39+00:00 | domain-validation | 0 | 1.39 | `pytest -q tests/handling/test_registration_attempt_repository.py` | `95f02f21446da0e9` |  |  |
| 2026-11-03T18:29:56+00:00 | crap | 0 | 13.23 | `bash -c 'pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov && lizard --csv src > .migration/runs/lizard.csv && python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30'` | `8881d78cb4d58890` |  | gate=crap max=15.0 threshold=30 over=0 methods=106 |
| 2026-11-03T18:30:58+00:00 | mutation-changed | 1 | 56.56 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `8940110e5a33976d` | afs-mutation: FAILED score=0.658 threshold=0.8 killed=79 survived=41 skipped=0 files=6 jobs=4 base=origin/main | gate=mutation score=0.658 threshold=0.8 killed=79 survived=41 files=6 base=origin/main |
| 2026-11-03T18:32:00+00:00 | mutation-focused-tests | 0 | 1.43 | `pytest -q tests/handling/test_registration_attempt_repository.py` | `5142a9263e6ef808` |  |  |
| 2026-11-03T18:33:01+00:00 | mutation-changed | 1 | 56.53 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `d2fd9d1e54769698` | afs-mutation: FAILED score=0.742 threshold=0.8 killed=89 survived=31 skipped=0 files=6 jobs=4 base=origin/main | gate=mutation score=0.742 threshold=0.8 killed=89 survived=31 files=6 base=origin/main |
| 2026-11-03T18:34:14+00:00 | mutation-focused-tests | 0 | 1.56 | `pytest -q tests/handling/test_registration_attempt_repository.py` | `00005cb364919a1d` |  |  |
| 2026-11-03T18:35:16+00:00 | mutation-changed | 0 | 58.38 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `dc2a91257150fbc1` |  | gate=mutation score=0.850 threshold=0.8 killed=102 survived=18 files=6 base=origin/main |
| 2026-11-03T18:35:32+00:00 | idiom-lint | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-03T18:35:32+00:00 | idiom-format | 0 | 0.02 | `ruff format --check` | `291d91fd4256e9a8` |  |  |
| 2026-11-03T18:35:32+00:00 | build-compile | 0 | 0.04 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-03T18:35:32+00:00 | build-check | 0 | 0.4 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-03T18:35:50+00:00 | behavior | 0 | 13.8 | `pytest -q` | `cc1cce794a27e71b` |  |  |
| 2026-11-03T18:36:08+00:00 | regression | 0 | 13.41 | `pytest -q` | `9b0d1f309d4fd838` |  |  |
| 2026-11-03T18:36:25+00:00 | crap | 0 | 13.14 | `bash -c 'pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov && lizard --csv src > .migration/runs/lizard.csv && python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30'` | `61a9ebb5c369a3f7` |  | gate=crap max=15.0 threshold=30 over=0 methods=106 |
| 2026-11-03T18:52:10+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
