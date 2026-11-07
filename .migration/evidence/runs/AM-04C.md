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
