# Run journal: HR-04A

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-03T18:18:32+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-03T18:24:29+00:00 | build-compile | 0 | 0.08 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-03T18:24:30+00:00 | build-django-check | 0 | 1.44 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-03T18:24:35+00:00 | idiom-ruff-check | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-03T18:24:35+00:00 | idiom-ruff-format | 0 | 0.02 | `ruff format --check` | `1a9301f4cf03fa0d` |  |  |
| 2026-11-03T18:24:57+00:00 | behavior | 0 | 17.39 | `pytest -q` | `cc5d1b24884b0ab9` |  |  |
| 2026-11-03T18:25:22+00:00 | crap-coverage | 0 | 16.59 | `python -m pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `6384506cb2579a44` |  |  |
| 2026-11-03T18:25:27+00:00 | crap-lizard | 0 | 0.12 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-03T18:25:30+00:00 | crap-threshold | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `680306b0c08d8ed8` |  | gate=crap max=14.0 threshold=30 over=0 methods=98 |
| 2026-11-03T18:25:55+00:00 | regression | 0 | 16.86 | `pytest -q` | `c2cd3a8b7c5840fd` |  |  |
| 2026-11-03T18:25:59+00:00 | mutation-changed | 0 | 0.08 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `36603172da4a0d74` |  | gate=mutation score=n/a reason=no-mutable-code-changed base=origin/main |
