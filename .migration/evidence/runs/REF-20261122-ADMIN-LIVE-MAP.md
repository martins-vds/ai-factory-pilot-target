# Run journal: REF-20261122-ADMIN-LIVE-MAP

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-22T23:43:22+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-22T23:44:14+00:00 | baseline | 0 | 5.33 | `pytest -q tests/cargo/interfaces/test_admin_live_map_data.py tests/cargo/interfaces/test_admin_live_map_markers.py tests/cargo/interfaces/test_admin_live_map_processing.py tests/cargo/interfaces/test_admin_live_map_templates.py` | `1285d7a318273798` |  |  |
