# Run journal: TC-14a

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight |
|---|---|---|---|---|---|---|
| 2026-11-02T00:16:53+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |
| 2026-11-02T00:18:59+00:00 | seed-regression-red | 1 | 3.23 | `pytest -q tests/cargo/test_sample_data.py` | `176dfc6e93b675fe` | E                                                                        [100%] |
| 2026-11-02T00:19:38+00:00 | seed-regression-red | 1 | 1.53 | `pytest -q tests/cargo/test_sample_data.py::test_claimed_sample_cargo_is_not_marked_unloaded_at_destination` | `66db52f9a347a758` | assert seed.events[-1].event_type is HandlingEventType.CLAIM |
