# Run journal: BK-05H

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-08T02:37:59+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-08T02:40:11+00:00 | urls-red | 1 | 2.15 | `pytest -q tests/booking/test_urls.py` | `577cad6222329e51` | E                   KeyError: 'booking' |  |
| 2026-11-08T02:40:28+00:00 | urls-green | 0 | 1.72 | `pytest -q tests/booking/test_urls.py` | `a088da9ede8f1cd2` |  |  |
| 2026-11-08T02:40:37+00:00 | idiom-ruff-check | 1 | 0.05 | `ruff check` | `00f7c3dada987c71` | Found 1 error. |  |
| 2026-11-08T02:40:37+00:00 | idiom-ruff-format | 0 | 0.06 | `ruff format --check` | `f971e9aa1333322e` |  |  |
| 2026-11-08T02:40:47+00:00 | idiom-ruff-check | 0 | 0.03 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-08T02:40:52+00:00 | urls-green-final | 0 | 1.75 | `pytest -q tests/booking/test_urls.py` | `2a527d2368b012db` |  |  |
| 2026-11-08T02:40:56+00:00 | build-compileall | 0 | 0.06 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-08T02:40:59+00:00 | build-django-check | 0 | 0.41 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-08T02:42:13+00:00 | behavior | 0 | 69.32 | `pytest -q` | `c95bfb334e0966bc` |  |  |
| 2026-11-08T02:42:42+00:00 | idiom-ruff-format | 0 | 0.01 | `ruff format --check` | `f971e9aa1333322e` |  |  |
| 2026-11-08T02:43:50+00:00 | crap-pytest-cov | 0 | 65.18 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `7ad65424cf6f51fb` |  |  |
| 2026-11-08T02:43:54+00:00 | crap-lizard | 0 | 0.17 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-08T02:43:57+00:00 | crap-report | 0 | 0.05 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `46edc5c319c80c3b` |  | gate=crap max=26.0 threshold=30 over=0 methods=213 |
| 2026-11-08T02:45:02+00:00 | mutation-changed | 1 | 60.77 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `75e5be3de2e91bef` | afs-mutation: FAILED score=0.289 threshold=0.8 killed=11 survived=27 skipped=0 files=2 jobs=2 base=origin/main | gate=mutation score=0.289 threshold=0.8 killed=11 survived=27 files=2 base=origin/main |
| 2026-11-08T02:46:54+00:00 | urls-strengthened | 0 | 2.81 | `pytest -q tests/booking/test_urls.py` | `a0a74da4d2372618` |  |  |
| 2026-11-08T02:46:59+00:00 | idiom-ruff-check | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-08T02:47:03+00:00 | idiom-ruff-format | 0 | 0.01 | `ruff format --check` | `f971e9aa1333322e` |  |  |
| 2026-11-08T02:48:08+00:00 | mutation-changed | 1 | 59.43 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `8b2b8825c3688892` | afs-mutation: FAILED score=0.763 threshold=0.8 killed=29 survived=9 skipped=0 files=2 jobs=2 base=origin/main | gate=mutation score=0.763 threshold=0.8 killed=29 survived=9 files=2 base=origin/main |
| 2026-11-08T03:54:58+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-08T03:56:07+00:00 | mutation-changed | 1 | 52.42 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `8b2b8825c3688892` | afs-mutation: FAILED score=0.763 threshold=0.8 killed=29 survived=9 skipped=0 files=2 jobs=2 base=origin/main | gate=mutation score=0.763 threshold=0.8 killed=29 survived=9 files=2 base=origin/main |
| 2026-11-08T03:58:24+00:00 | urls-targeted | 0 | 2.36 | `pytest -q tests/booking/test_urls.py` | `f86fdf0efdd6c6d9` |  |  |
| 2026-11-08T03:59:19+00:00 | mutation-changed | 1 | 51.09 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `8b2b8825c3688892` | afs-mutation: FAILED score=0.763 threshold=0.8 killed=29 survived=9 skipped=0 files=2 jobs=2 base=origin/main | gate=mutation score=0.763 threshold=0.8 killed=29 survived=9 files=2 base=origin/main |
| 2026-11-08T04:01:36+00:00 | build-compileall | 0 | 0.05 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-08T04:01:41+00:00 | build-django-check | 0 | 0.36 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-08T04:01:44+00:00 | idiom-ruff-check | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-08T04:01:47+00:00 | idiom-ruff-format | 0 | 0.02 | `ruff format --check` | `f971e9aa1333322e` |  |  |
| 2026-11-08T04:02:53+00:00 | behavior | 0 | 62.28 | `pytest -q` | `0462a074e6b686d5` |  |  |
| 2026-11-08T04:03:54+00:00 | crap-pytest-cov | 0 | 57.07 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `d951f3f1d9a2c3ae` |  |  |
| 2026-11-08T04:03:58+00:00 | crap-lizard | 0 | 0.13 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-08T04:04:01+00:00 | crap-report | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `46edc5c319c80c3b` |  | gate=crap max=26.0 threshold=30 over=0 methods=213 |
| 2026-11-08T04:05:05+00:00 | regression | 0 | 58.43 | `pytest -q` | `1601bb86cdc856ff` |  |  |
