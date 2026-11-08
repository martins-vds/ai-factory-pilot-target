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
