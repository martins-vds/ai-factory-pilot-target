# Run journal: TC-15a

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight |
|---|---|---|---|---|---|---|
| 2026-11-02T03:07:15+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |
| 2026-11-02T03:07:46+00:00 | framing-red | 1 | 2.82 | `pytest -q tests/cargo/interfaces/test_map.py -k only_map_frame_allows_same_origin_framing` | `c0d1755e8cc042b0` | assert response.status_code == 200 |
| 2026-11-02T03:07:56+00:00 | behavior | 1 | 3.42 | `pytest -q tests/cargo/interfaces/test_map.py tests/cargo/test_tracking.py` | `ca1011e62741dc60` | _____ ERROR at setup of test_map_markers_use_exact_configured_coordinates ______ |
| 2026-11-02T03:08:20+00:00 | behavior | 0 | 6.19 | `pytest -q tests/cargo/interfaces/test_map.py tests/cargo/test_tracking.py` | `82d59fd7cfb64799` |  |
| 2026-11-02T03:08:21+00:00 | build | 0 | 0.43 | `bash -c 'python -m compileall -q src && python manage.py check'` | `1e3e63f221bde888` |  |
| 2026-11-02T03:08:21+00:00 | idiom | 0 | 0.03 | `bash -c 'ruff check && ruff format --check'` | `23a089bab5c1e1ce` |  |
| 2026-11-02T03:08:52+00:00 | regression | 0 | 14.36 | `pytest -q` | `0ea33f611943a9b0` |  |
| 2026-11-02T03:08:52+00:00 | crap | 0 | 0.15 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv && python .migration/harness/tools/crap.py .migration/runs/lizard` | `4d7c57f6ead7b75a` |  |
| 2026-11-02T03:12:03+00:00 | mutation_changed | 1 | 205.43 | `python .migration/harness/tools/afs-mutation --paths src/cargotracker/cargo/interfaces/tracking/map/views.py` | `3257ddb06f47faaf` | afs-mutation: FAILED score=0.633 threshold=0.8 killed=31 survived=18 skipped=0 files=1 jobs=1 base=explicit |
| 2026-11-02T03:12:24+00:00 | behavior | 0 | 6.24 | `pytest -q tests/cargo/interfaces/test_map.py tests/cargo/test_tracking.py` | `cbee53c9e0176fd9` |  |
| 2026-11-02T03:13:56+00:00 | mutation_changed | 0 | 91.41 | `python .migration/harness/tools/afs-mutation --paths src/cargotracker/cargo/interfaces/tracking/map/views.py` | `0013ec8f7f7e5347` |  |
| 2026-11-02T03:14:19+00:00 | regression | 0 | 13.45 | `pytest -q` | `04b68eed9ef5bc27` |  |
| 2026-11-02T03:14:19+00:00 | build | 0 | 0.43 | `bash -c 'python -m compileall -q src && python manage.py check'` | `1e3e63f221bde888` |  |
| 2026-11-02T03:14:19+00:00 | idiom | 0 | 0.02 | `bash -c 'ruff check && ruff format --check'` | `23a089bab5c1e1ce` |  |
| 2026-11-02T03:14:19+00:00 | crap | 0 | 0.15 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv && python .migration/harness/tools/crap.py .migration/runs/lizard` | `4d7c57f6ead7b75a` |  |
| 2026-11-02T03:14:20+00:00 | validate | 0 | 0.38 | `python .migration/harness/tools/validate.py .migration` | `5729afdc0c215519` |  |
| 2026-11-02T03:14:29+00:00 | live-http | 0 | 0.09 | `python -c 'from urllib.request import urlopen
for path, expected in [("/tracking/map/?statusCode=IN_PORT&lastKnownLocati` | `0af8aafc9116161e` |  |
