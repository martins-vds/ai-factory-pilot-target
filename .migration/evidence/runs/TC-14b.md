# Run journal: TC-14b

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight |
|---|---|---|---|---|---|---|
| 2026-11-02T01:20:43+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |
| 2026-11-02T01:22:41+00:00 | red-snapshot-regression | 1 | 4.23 | `pytest -q tests/cargo/test_sample_data.py::test_sample_cargo_definitions_do_not_include_delivery_snapshots` | `10c77cf34c0e25b7` | >       assert delivery_snapshot_fields.isdisjoint(field.name for field in fields(SAMPLE_CARGOS[0])) |
