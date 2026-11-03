# Run journal: HR-04C

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-03T20:42:52+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-03T20:45:35+00:00 | accepted-red | 1 | 3.76 | `pytest -q tests/handling/interfaces/test_registration_reports.py` | `10121c1874c20288` | E           cargotracker.handling.infrastructure.models.RegistrationAttemptRecord.DoesNotExist: RegistrationAttemptRecor |  |
| 2026-11-03T20:45:51+00:00 | accepted-green | 0 | 1.56 | `pytest -q tests/handling/interfaces/test_registration_reports.py` | `b458571cf7530567` |  |  |
| 2026-11-03T20:46:31+00:00 | validation-red | 1 | 3.13 | `pytest -q tests/handling/interfaces/test_registration_reports.py` | `208fc20a69ca4ab8` | /opt/hostedtoolcache/Python/3.13.17/x64/lib/python3.13/site-packages/django/core/handlers/exception.py:55: in inner |  |
| 2026-11-03T20:46:57+00:00 | validation-green | 0 | 1.69 | `pytest -q tests/handling/interfaces/test_registration_reports.py` | `69385c30e2675f23` |  |  |
| 2026-11-03T20:47:24+00:00 | view-tests | 0 | 1.77 | `pytest -q tests/handling/interfaces/test_registration_reports.py` | `1cc2d6832916b25d` |  |  |
| 2026-11-03T20:47:58+00:00 | idiom-lint | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-03T20:48:02+00:00 | idiom-format | 0 | 0.02 | `ruff format --check` | `67e4bf8f396fefa7` |  |  |
| 2026-11-03T20:48:06+00:00 | build-compile | 0 | 0.05 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-03T20:48:06+00:00 | build-check | 0 | 0.37 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-03T20:48:27+00:00 | behavior | 0 | 16.9 | `pytest -q` | `f0b7109cda161201` |  |  |
| 2026-11-03T20:48:43+00:00 | regression | 0 | 16.33 | `pytest -q` | `4240a8bab01c7847` |  |  |
| 2026-11-03T20:49:04+00:00 | crap | 0 | 16.58 | `bash -c 'pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov && lizard --csv src > .migration/runs/lizard.csv && python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30'` | `af23510cc94bf8ea` |  | gate=crap max=15.0 threshold=30 over=0 methods=114 |
| 2026-11-03T20:50:23+00:00 | mutation-changed | 1 | 72.66 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `432ff283f4da0f16` | afs-mutation: FAILED score=0.624 threshold=0.8 killed=53 survived=32 skipped=0 files=3 jobs=3 base=origin/main | gate=mutation score=0.624 threshold=0.8 killed=53 survived=32 files=3 base=origin/main |
| 2026-11-03T20:52:07+00:00 | mutation-tests | 0 | 1.79 | `pytest -q tests/handling/interfaces/test_registration_reports.py` | `722d512f3a364801` |  |  |
| 2026-11-03T20:52:38+00:00 | verify-ruff | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-03T20:52:38+00:00 | verify-format | 0 | 0.01 | `ruff format --check` | `67e4bf8f396fefa7` |  |  |
| 2026-11-03T20:53:58+00:00 | mutation-changed | 0 | 73.41 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `5769be606373f536` |  | gate=mutation score=0.800 threshold=0.8 killed=68 survived=17 files=3 base=origin/main |
| 2026-11-03T20:55:19+00:00 | final-build-compile | 0 | 0.04 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-03T20:55:20+00:00 | final-build-check | 0 | 0.37 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-03T20:55:20+00:00 | final-idiom-lint | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-03T20:55:20+00:00 | final-idiom-format | 0 | 0.01 | `ruff format --check` | `67e4bf8f396fefa7` |  |  |
| 2026-11-03T20:55:35+00:00 | final-behavior | 0 | 14.92 | `pytest -q` | `53354221590a50d3` |  |  |
| 2026-11-03T20:55:50+00:00 | final-regression | 0 | 14.89 | `pytest -q` | `687cb4ac00522ee1` |  |  |
| 2026-11-03T20:56:05+00:00 | final-crap | 0 | 15.06 | `bash -c 'pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov && lizard --csv src > .migration/runs/lizard.csv && python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30'` | `553149513bca08a8` |  | gate=crap max=15.0 threshold=30 over=0 methods=114 |
| 2026-11-03T21:00:38+00:00 | composition-view-tests | 0 | 1.75 | `pytest -q tests/handling/interfaces/test_registration_reports.py` | `8ce99aa40a756baf` |  |  |
| 2026-11-03T21:00:55+00:00 | composition-lint | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-03T21:00:55+00:00 | composition-format | 0 | 0.01 | `ruff format --check` | `002dcbe5e1c568f6` |  |  |
| 2026-11-03T21:01:16+00:00 | final2-build-compile | 0 | 0.04 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-03T21:01:16+00:00 | final2-build-check | 0 | 0.36 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-03T21:01:16+00:00 | final2-idiom-lint | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-03T21:01:16+00:00 | final2-idiom-format | 0 | 0.01 | `ruff format --check` | `002dcbe5e1c568f6` |  |  |
| 2026-11-03T21:01:33+00:00 | final2-behavior | 0 | 16.43 | `pytest -q` | `9cc094bcef1cebc1` |  |  |
| 2026-11-03T21:01:50+00:00 | final2-regression | 0 | 16.66 | `pytest -q` | `871e05f72c711951` |  |  |
| 2026-11-03T21:02:06+00:00 | final2-crap | 0 | 16.14 | `bash -c 'pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov && lizard --csv src > .migration/runs/lizard.csv && python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30'` | `b77918b7b73e573f` |  | gate=crap max=15.0 threshold=30 over=0 methods=116 |
| 2026-11-03T21:03:21+00:00 | mutation-changed | 0 | 74.48 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `f60e3f9e013eb808` |  | gate=mutation score=0.800 threshold=0.8 killed=68 survived=17 files=4 base=origin/main |
| 2026-11-03T21:45:20+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-03T21:46:37+00:00 | zero-year-red | 4 | 3.57 | `pytest -q tests/handling/interfaces/test_registration_reports.py::test_accepts_zero_padded_year_in_completion_time` | `6b35bd0b0d860837` | ERROR: not found: /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/tests/handling/interfaces/test_regis |  |
| 2026-11-03T21:47:43+00:00 | zero-year-red | 1 | 1.8 | `pytest -q tests/handling/interfaces/test_registration_reports.py::test_accepts_zero_padded_year_in_completion_time` | `d7c3e83daa68776f` | >       assert response.status_code == 204 |  |
| 2026-11-03T21:48:10+00:00 | zero-year-green | 0 | 1.53 | `pytest -q tests/handling/interfaces/test_registration_reports.py::test_accepts_zero_padded_year_in_completion_time` | `910de278ff7c60fe` |  |  |
| 2026-11-03T21:48:15+00:00 | handling-report-tests | 0 | 1.8 | `pytest -q tests/handling/interfaces/test_registration_reports.py` | `0af08ce93d3ef3d6` |  |  |
| 2026-11-03T21:49:48+00:00 | final-build-compile | 0 | 0.05 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-03T21:49:48+00:00 | final-build-check | 0 | 0.37 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-03T21:49:48+00:00 | final-idiom-lint | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-03T21:49:48+00:00 | final-idiom-format | 0 | 0.02 | `ruff format --check` | `67e4bf8f396fefa7` |  |  |
| 2026-11-03T21:50:07+00:00 | final-behavior | 0 | 15.49 | `pytest -q` | `5aa355058dd222f6` |  |  |
| 2026-11-03T21:50:22+00:00 | final-regression | 0 | 14.81 | `pytest -q` | `253a7d318d53803b` |  |  |
| 2026-11-03T21:50:45+00:00 | final-crap | 0 | 16.58 | `bash -c 'pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov && lizard --csv src > .migration/runs/lizard.csv && python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30'` | `2de7606bf820ab7b` |  | gate=crap max=15.0 threshold=30 over=0 methods=116 |
| 2026-11-03T21:50:49+00:00 | final-mutation-changed | 1 | 0.08 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `3ff11adc524e78cf` |  |  |
| 2026-11-03T21:52:18+00:00 | final-mutation-changed | 1 | 72.88 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `87e32d4d48adc891` | afs-mutation: FAILED score=0.795 threshold=0.8 killed=66 survived=17 skipped=0 files=2 jobs=2 base=origin/main | gate=mutation score=0.795 threshold=0.8 killed=66 survived=17 files=2 base=origin/main |
| 2026-11-03T21:54:18+00:00 | null-voyage-test | 0 | 1.58 | `pytest -q tests/handling/interfaces/test_registration_reports.py::test_null_voyage_number_is_accepted_as_optional` | `ed580d2d4796cc63` |  |  |
| 2026-11-03T21:55:50+00:00 | final2-mutation-changed | 1 | 72.59 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `87e32d4d48adc891` | afs-mutation: FAILED score=0.795 threshold=0.8 killed=66 survived=17 skipped=0 files=2 jobs=2 base=origin/main | gate=mutation score=0.795 threshold=0.8 killed=66 survived=17 files=2 base=origin/main |
| 2026-11-03T22:34:04+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-03T22:34:41+00:00 | mutation-changed | 1 | 0.35 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `3ff11adc524e78cf` |  |  |
| 2026-11-03T22:35:12+00:00 | mutation-changed | 1 | 0.12 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `3ff11adc524e78cf` |  |  |
| 2026-11-03T22:37:10+00:00 | mutation-changed | 1 | 85.57 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `0d8e0e3e0f88cce0` | afs-mutation: FAILED score=0.795 threshold=0.8 killed=66 survived=17 skipped=0 files=3 jobs=3 base=origin/main | gate=mutation score=0.795 threshold=0.8 killed=66 survived=17 files=3 base=origin/main |
