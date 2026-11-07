# Run journal: DM-05D

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-07T18:23:05+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T18:25:57+00:00 | focused-tests-red | 1 | 3.71 | `pytest -q tests/data_migration/test_export.py` | `22ed5e1e4222ac2b` | E               KeyError: 'export_data_snapshot' |  |
| 2026-11-07T18:26:45+00:00 | focused-tests-green | 1 | 1.83 | `pytest -q tests/data_migration/test_export.py` | `4ff492f89c5a2b65` | >           assert reader.fieldnames == ['id', 'unlocode', 'name'] |  |
| 2026-11-07T18:26:59+00:00 | focused-tests-green | 0 | 1.82 | `pytest -q tests/data_migration/test_export.py` | `e72d445d99fd8599` |  |  |
