# Run journal: BK-05J

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-08T14:02:40+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-08T14:05:59+00:00 | idiom-ruff-format | 0 | 0.04 | `ruff format --check` | `c799b224f99851f8` |  |  |
| 2026-11-08T14:05:59+00:00 | idiom-ruff-check | 0 | 0.04 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-08T14:05:59+00:00 | build-compile | 0 | 0.12 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-08T14:06:01+00:00 | build-django-check | 0 | 1.7 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-08T14:07:01+00:00 | tests | 0 | 56.54 | `pytest -q` | `f477d2be76098dc5` |  |  |
| 2026-11-08T14:07:57+00:00 | crap-coverage | 0 | 51.12 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `4583ff68924c4c30` |  |  |
| 2026-11-08T14:08:00+00:00 | crap-lizard | 0 | 0.12 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-08T14:08:03+00:00 | crap-report | 0 | 0.03 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `46edc5c319c80c3b` |  | gate=crap max=26.0 threshold=30 over=0 methods=213 |
