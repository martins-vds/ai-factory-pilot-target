# Run journal: AM-04C

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-07T05:13:52+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T05:51:31+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T05:53:20+00:00 | templates-red | 1 | 3.56 | `pytest -q tests/cargo/interfaces/test_admin_live_map_templates.py` | `61707d02b08cc796` | /opt/hostedtoolcache/Python/3.13.18/x64/lib/python3.13/site-packages/django/core/handlers/exception.py:55: in inner |  |
| 2026-11-07T05:54:11+00:00 | templates-green | 0 | 1.81 | `pytest -q tests/cargo/interfaces/test_admin_live_map_templates.py` | `f96ee49b07b5e48f` |  |  |
| 2026-11-07T05:54:20+00:00 | admin-map-data-tests | 0 | 2.61 | `pytest -q tests/cargo/interfaces/test_admin_live_map_data.py` | `13ecf63495e34b95` |  |  |
| 2026-11-07T05:57:02+00:00 | build-compileall | 0 | 0.04 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T05:57:13+00:00 | build-django-check | 0 | 0.33 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T05:57:16+00:00 | idiom-ruff-check | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T05:57:19+00:00 | idiom-ruff-format | 0 | 0.02 | `ruff format --check` | `5b8e82f27798cc2e` |  |  |
| 2026-11-07T05:58:01+00:00 | behavior-suite | 0 | 38.48 | `pytest -q` | `7dc34705c94783e4` |  |  |
| 2026-11-07T05:58:43+00:00 | crap-coverage | 0 | 37.22 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `1dc3296b11834e35` |  |  |
| 2026-11-07T05:58:47+00:00 | crap-lizard | 0 | 0.1 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T05:58:50+00:00 | crap-threshold | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `6c5a7b5a5f079222` |  | gate=crap max=19.0 threshold=30 over=0 methods=140 |
| 2026-11-07T05:59:31+00:00 | regression-suite | 0 | 37.85 | `pytest -q` | `83ee0c699e1a3c24` |  |  |
| 2026-11-07T05:59:55+00:00 | mutation-changed | 0 | 20.43 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `7db208de9871e676` |  | gate=mutation score=1.000 threshold=0.8 killed=6 survived=0 files=1 base=origin/main |
| 2026-11-07T06:06:40+00:00 | templates-url-assertion | 0 | 1.8 | `pytest -q tests/cargo/interfaces/test_admin_live_map_templates.py` | `f68080226a57b8b1` |  |  |
| 2026-11-07T06:07:05+00:00 | final-build-compileall | 0 | 0.04 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T06:07:09+00:00 | final-build-django-check | 0 | 0.34 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T06:07:13+00:00 | final-idiom-ruff-check | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T06:07:16+00:00 | final-idiom-ruff-format | 0 | 0.01 | `ruff format --check` | `5b8e82f27798cc2e` |  |  |
| 2026-11-07T06:07:58+00:00 | final-behavior-suite | 0 | 38.17 | `pytest -q` | `5809bc37ddfb5232` |  |  |
| 2026-11-07T06:08:39+00:00 | final-crap-coverage | 0 | 36.95 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `f6e597afdb283299` |  |  |
| 2026-11-07T06:08:43+00:00 | final-crap-lizard | 0 | 0.11 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T06:08:47+00:00 | final-crap-threshold | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `6c5a7b5a5f079222` |  | gate=crap max=19.0 threshold=30 over=0 methods=140 |
| 2026-11-07T06:09:37+00:00 | final-regression-suite | 0 | 45.46 | `pytest -q` | `ec1cb039abc92d20` |  |  |
| 2026-11-07T06:10:01+00:00 | final-mutation-changed | 0 | 20.86 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `7db208de9871e676` |  | gate=mutation score=1.000 threshold=0.8 killed=6 survived=0 files=1 base=origin/main |
| 2026-11-07T12:45:39+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T12:49:12+00:00 | verify-build-compileall | 0 | 0.09 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T12:49:12+00:00 | verify-build-django-check | 0 | 0.55 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T12:50:00+00:00 | verify-behavior-suite | 0 | 47.47 | `pytest -q` | `28d4fc2ca55ceeab` |  |  |
| 2026-11-07T12:50:00+00:00 | verify-idiom-ruff-check | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T12:50:00+00:00 | verify-idiom-ruff-format | 0 | 0.02 | `ruff format --check` | `5b8e82f27798cc2e` |  |  |
| 2026-11-07T12:50:45+00:00 | verify-crap-coverage | 0 | 45.04 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `131d061136c9569d` |  |  |
| 2026-11-07T12:50:46+00:00 | verify-crap-lizard | 0 | 0.14 | `lizard --csv src` | `87bd818446e3fd70` |  |  |
| 2026-11-07T12:50:46+00:00 | verify-crap-threshold | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `b34a7b0c580f07b5` |  | gate=crap max=14.0 threshold=30 over=0 methods=5 |
| 2026-11-07T12:51:10+00:00 | verify-mutation-changed | 0 | 23.85 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `7db208de9871e676` |  | gate=mutation score=1.000 threshold=0.8 killed=6 survived=0 files=1 base=origin/main |
| 2026-11-07T12:51:56+00:00 | verify-regression-suite | 0 | 46.36 | `pytest -q` | `60ee151dcc53f2db` |  |  |
| 2026-11-07T12:52:01+00:00 | verify-crap-lizard-corrected | 0 | 0.14 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T12:52:01+00:00 | verify-crap-threshold-corrected | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `6c5a7b5a5f079222` |  | gate=crap max=19.0 threshold=30 over=0 methods=140 |
| 2026-11-07T12:55:06+00:00 | final-verification-suite | 0 | 47.28 | `pytest -q` | `4b50492ad0ad82c6` |  |  |
| 2026-11-07T15:06:53+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T15:08:57+00:00 | templates-red | 1 | 3.53 | `pytest -q tests/cargo/interfaces/test_admin_live_map_templates.py` | `db9fe5e270672cdf` | /opt/hostedtoolcache/Python/3.13.18/x64/lib/python3.13/site-packages/django/core/handlers/exception.py:55: in inner |  |
| 2026-11-07T15:09:27+00:00 | templates-green | 1 | 1.63 | `pytest -q tests/cargo/interfaces/test_admin_live_map_templates.py` | `d86d0431de50f498` | assert response.status_code == 200 |  |
| 2026-11-07T15:09:38+00:00 | templates-green | 0 | 1.55 | `pytest -q tests/cargo/interfaces/test_admin_live_map_templates.py` | `70b912527987b8d6` |  |  |
| 2026-11-07T15:10:42+00:00 | templates-green-final | 0 | 1.65 | `pytest -q tests/cargo/interfaces/test_admin_live_map_templates.py` | `ca3473021cd297f2` |  |  |
| 2026-11-07T15:11:19+00:00 | final-build-compileall | 0 | 0.03 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T15:11:19+00:00 | final-build-django-check | 0 | 0.27 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T15:11:22+00:00 | final-idiom-ruff-check | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T15:11:22+00:00 | final-idiom-ruff-format | 0 | 0.01 | `ruff format --check` | `5b8e82f27798cc2e` |  |  |
| 2026-11-07T15:11:52+00:00 | final-behavior-suite | 0 | 26.29 | `pytest -q` | `9ae6e8d4c9e6b45f` |  |  |
| 2026-11-07T15:12:20+00:00 | final-crap-coverage | 0 | 24.67 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `f5f6eaa15cc6aaab` |  |  |
| 2026-11-07T15:12:20+00:00 | final-crap-lizard | 0 | 0.08 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T15:12:20+00:00 | final-crap-threshold | 0 | 0.03 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `6c5a7b5a5f079222` |  | gate=crap max=19.0 threshold=30 over=0 methods=140 |
| 2026-11-07T15:12:48+00:00 | final-regression-suite | 0 | 25.33 | `pytest -q` | `3dd8801bbd4a9b89` |  |  |
| 2026-11-07T15:13:07+00:00 | final-mutation-changed | 0 | 16.06 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `43cbeda675483b3d` |  | gate=mutation score=1.000 threshold=0.8 killed=6 survived=0 files=1 base=origin/main |
| 2026-11-07T15:51:01+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T15:52:27+00:00 | reverify-build-compileall | 0 | 0.08 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T15:52:29+00:00 | reverify-build-django-check | 0 | 1.57 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T15:52:29+00:00 | reverify-idiom-ruff-check | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T15:52:29+00:00 | reverify-idiom-ruff-format | 0 | 0.02 | `ruff format --check` | `cf764d22188c7061` |  |  |
| 2026-11-07T15:53:14+00:00 | reverify-behavior-suite | 0 | 44.54 | `pytest -q` | `28330d2d5a781d37` |  |  |
| 2026-11-07T15:53:56+00:00 | reverify-crap-coverage | 0 | 42.4 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `1d51516505ed7865` |  |  |
| 2026-11-07T15:53:56+00:00 | reverify-crap-lizard | 0 | 0.13 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T15:53:56+00:00 | reverify-crap-threshold | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `4025a585d6fd1958` |  | gate=crap max=19.0 threshold=30 over=0 methods=147 |
| 2026-11-07T15:54:21+00:00 | reverify-mutation-changed | 0 | 24.59 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `43cbeda675483b3d` |  | gate=mutation score=1.000 threshold=0.8 killed=6 survived=0 files=1 base=origin/main |
| 2026-11-07T15:55:13+00:00 | reverify-regression-suite | 0 | 51.98 | `pytest -q` | `b760313825296c94` |  |  |
| 2026-11-07T15:55:57+00:00 | reverify-focused-admin-map | 0 | 3.81 | `pytest -q tests/cargo/interfaces/test_admin_live_map_templates.py tests/cargo/interfaces/test_admin_live_map_data.py` | `e172eb16c6a9be74` |  |  |
