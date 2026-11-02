# Run journal: TC-14b

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight |
|---|---|---|---|---|---|---|
| 2026-11-02T01:20:43+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |
| 2026-11-02T01:22:41+00:00 | red-snapshot-regression | 1 | 4.23 | `pytest -q tests/cargo/test_sample_data.py::test_sample_cargo_definitions_do_not_include_delivery_snapshots` | `10c77cf34c0e25b7` | >       assert delivery_snapshot_fields.isdisjoint(field.name for field in fields(SAMPLE_CARGOS[0])) |
| 2026-11-02T01:23:19+00:00 | focused-sample-map | 1 | 2.47 | `pytest -q tests/cargo/test_sample_data.py tests/cargo/interfaces/test_map.py` | `9083b5b37f9ee122` | ___ ERROR at setup of test_seeded_deliveries_match_their_handling_histories ____ |
| 2026-11-02T01:23:53+00:00 | seed-contract | 0 | 1.15 | `pytest -q tests/cargo/test_sample_data.py::test_sample_cargo_definitions_do_not_include_delivery_snapshots` | `43a7f3944d7234d4` |  |
| 2026-11-02T01:24:18+00:00 | focused-sample-map | 0 | 5.13 | `pytest -q tests/cargo/test_sample_data.py tests/cargo/interfaces/test_map.py` | `b132010738d1f1be` |  |
| 2026-11-02T01:25:30+00:00 | build-compile | 0 | 0.04 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |
| 2026-11-02T01:25:34+00:00 | build-check | 0 | 0.32 | `python manage.py check` | `1e3e63f221bde888` |  |
| 2026-11-02T01:25:37+00:00 | idiom-ruff-check | 0 | 0.03 | `python -m ruff check` | `82b3e6a6c090a576` |  |
| 2026-11-02T01:25:40+00:00 | idiom-ruff-format | 0 | 0.03 | `python -m ruff format --check` | `e540c8427c224fd6` |  |
| 2026-11-02T01:25:56+00:00 | behavior-tests | 0 | 8.55 | `pytest -q` | `c24c622a87da8afe` |  |
| 2026-11-02T01:26:02+00:00 | crap-lizard | 0 | 0.09 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |
| 2026-11-02T01:26:05+00:00 | crap-threshold | 0 | 0.03 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov coverage.lcov --max 30` | `8e94dfa27054aa92` |  |
| 2026-11-02T01:26:11+00:00 | mutation-changed | 0 | 1.35 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `75d8058f4db9f39b` |  |
| 2026-11-02T01:26:26+00:00 | regression-full-suite | 0 | 7.89 | `pytest -q` | `a1c67c3430598b0d` |  |
