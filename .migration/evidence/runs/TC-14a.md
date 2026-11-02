# Run journal: TC-14a

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight |
|---|---|---|---|---|---|---|
| 2026-11-02T00:16:53+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |
| 2026-11-02T00:18:59+00:00 | seed-regression-red | 1 | 3.23 | `pytest -q tests/cargo/test_sample_data.py` | `176dfc6e93b675fe` | E                                                                        [100%] |
| 2026-11-02T00:19:38+00:00 | seed-regression-red | 1 | 1.53 | `pytest -q tests/cargo/test_sample_data.py::test_claimed_sample_cargo_is_not_marked_unloaded_at_destination` | `66db52f9a347a758` | assert seed.events[-1].event_type is HandlingEventType.CLAIM |
| 2026-11-02T00:20:06+00:00 | seed-regression-green | 0 | 1.45 | `pytest -q tests/cargo/test_sample_data.py::test_claimed_sample_cargo_is_not_marked_unloaded_at_destination` | `c8632c1bc7b718eb` |  |
| 2026-11-02T00:21:47+00:00 | targeted-behavior | 0 | 4.65 | `env POSTGRES_DB=app POSTGRES_USER=app POSTGRES_PASSWORD=app POSTGRES_HOST=localhost POSTGRES_PORT=5432 pytest -q tests/c` | `d7d4c9a9f72d6ec9` |  |
| 2026-11-02T00:22:30+00:00 | build | 0 | 0.55 | `bash -lc 'python -m compileall -q src && python manage.py check'` | `1e3e63f221bde888` |  |
| 2026-11-02T00:22:34+00:00 | idiom | 0 | 0.14 | `bash -lc 'ruff check && ruff format --check'` | `2055e6bbf3096e4a` |  |
| 2026-11-02T00:22:37+00:00 | crap | 1 | 0.26 | `bash -lc 'lizard --csv src > .migration/runs/lizard.csv && python .migration/harness/tools/crap.py .migration/runs/lizar` | `70317790ae7cf94b` |  |
| 2026-11-02T00:22:57+00:00 | regression | 0 | 8.19 | `env POSTGRES_DB=app POSTGRES_USER=app POSTGRES_PASSWORD=app POSTGRES_HOST=localhost POSTGRES_PORT=5432 pytest -q` | `5374c140b94215ee` |  |
| 2026-11-02T00:31:31+00:00 | mutation-changed | 0 | 508.11 | `env POSTGRES_DB=app POSTGRES_USER=app POSTGRES_PASSWORD=app POSTGRES_HOST=localhost POSTGRES_PORT=5432 python .migration` | `3a4ab68a5a39f989` |  |
| 2026-11-02T00:36:04+00:00 | differential-pr61 | 0 | 4.87 | `bash -lc 'cd /tmp/tc14a-pr61-test && env POSTGRES_DB=app POSTGRES_USER=app POSTGRES_PASSWORD=app POSTGRES_HOST=localhost` | `7f5a128402b1b286` |  |
