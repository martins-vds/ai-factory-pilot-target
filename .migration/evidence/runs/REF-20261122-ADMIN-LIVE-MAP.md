# Run journal: REF-20261122-ADMIN-LIVE-MAP

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-22T23:43:22+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-22T23:44:14+00:00 | baseline | 0 | 5.33 | `pytest -q tests/cargo/interfaces/test_admin_live_map_data.py tests/cargo/interfaces/test_admin_live_map_markers.py tests/cargo/interfaces/test_admin_live_map_processing.py tests/cargo/interfaces/test_admin_live_map_templates.py` | `1285d7a318273798` |  |  |
| 2026-11-22T23:44:40+00:00 | targeted-after-refactor | 0 | 4.69 | `pytest -q tests/cargo/interfaces/test_admin_live_map_data.py tests/cargo/interfaces/test_admin_live_map_markers.py tests/cargo/interfaces/test_admin_live_map_processing.py tests/cargo/interfaces/test_admin_live_map_templates.py` | `5fe2eb50b38b6c07` |  |  |
| 2026-11-22T23:44:53+00:00 | build-compile | 0 | 0.05 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-22T23:44:56+00:00 | build-check | 0 | 0.36 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-22T23:46:06+00:00 | behavior | 0 | 66.91 | `pytest -q` | `2d317016fe015d13` |  |  |
| 2026-11-22T23:46:09+00:00 | spec | 0 | 0.06 | `python .migration/harness/tools/afs-spec run` | `1b0b939f3e1e502f` |  | gate=spec cases=0 failed=0 pending=0 |
| 2026-11-22T23:46:11+00:00 | idiom-ruff-check | 1 | 0.03 | `ruff check` | `80d46ad736c8dcbb` |  |  |
| 2026-11-22T23:46:23+00:00 | idiom-ruff-check-rerun | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-22T23:46:25+00:00 | idiom-format | 0 | 0.02 | `ruff format --check` | `b221fa32ed80fb2e` |  |  |
| 2026-11-22T23:46:28+00:00 | idiom-layers | 0 | 0.13 | `python .migration/harness/tools/check_layers.py` | `59bfd54275a9b5a4` | src/cargotracker/booking/application/routing.py:1: known, not failing: use cases don't depend on web adapters or persist | gate=layering contracts=3 violations=0 known=3 |
| 2026-11-22T23:46:30+00:00 | idiom-ui | 0 | 0.26 | `python .migration/harness/tools/check_ui.py` | `b9ae03306fe277bb` |  | gate=ui scope="templates changed since origin/main" templates=0 findings=0 |
| 2026-11-22T23:47:49+00:00 | crap-coverage | 0 | 76.01 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `635444d7860ff048` |  |  |
| 2026-11-22T23:47:51+00:00 | crap-lizard | 0 | 0.13 | `lizard --csv src` | `763307ddb3c7305c` | 16,3,86,6,16,"_origin_step@38-53@src/cargotracker/booking/interfaces/wizard/views.py","src/cargotracker/booking/interfac |  |
| 2026-11-22T23:48:00+00:00 | crap-lizard-csv | 0 | 0.14 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-22T23:48:02+00:00 | crap-threshold | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `dbeb57242d6b2a6b` |  | gate=crap max=26.0 threshold=30 over=0 methods=213 |
| 2026-11-22T23:49:20+00:00 | mutation-changed | 0 | 75.92 | `python .migration/harness/tools/afs-mutation` | `6922f90b80f52850` |  | gate=mutation score=1.000 threshold=0.8 killed=36 survived=0 files=2 base=origin/main |
| 2026-11-22T23:50:38+00:00 | regression | 0 | 65.45 | `pytest -q` | `1187f9f336df0191` |  |  |
| 2026-11-22T23:51:18+00:00 | idiom-format-final | 0 | 0.01 | `ruff format --check` | `b221fa32ed80fb2e` |  |  |
| 2026-11-22T23:51:30+00:00 | build-compile-final | 0 | 0.04 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-22T23:51:32+00:00 | build-check-final | 0 | 0.36 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-22T23:53:06+00:00 | final-ruff-check | 1 | 0.01 | `ruff check` | `8bd8b7309d96680f` |  |  |
| 2026-11-22T23:53:11+00:00 | final-map-tests | 0 | 4.72 | `pytest -q tests/cargo/interfaces/test_admin_live_map_data.py tests/cargo/interfaces/test_admin_live_map_markers.py tests/cargo/interfaces/test_admin_live_map_processing.py tests/cargo/interfaces/test_admin_live_map_templates.py` | `02d129fab13ea9e4` |  |  |
| 2026-11-22T23:53:38+00:00 | final-ruff-check-rerun | 1 | 0.01 | `ruff check` | `35e37249e3119d29` | Found 1 error. |  |
| 2026-11-22T23:55:57+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-23T00:00:05+00:00 | setup-probe-resume | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
