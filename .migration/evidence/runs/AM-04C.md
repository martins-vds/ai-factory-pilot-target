# Run journal: AM-04C

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-07T05:13:52+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T05:51:31+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T05:53:20+00:00 | templates-red | 1 | 3.56 | `pytest -q tests/cargo/interfaces/test_admin_live_map_templates.py` | `61707d02b08cc796` | /opt/hostedtoolcache/Python/3.13.18/x64/lib/python3.13/site-packages/django/core/handlers/exception.py:55: in inner |  |
| 2026-11-07T05:54:11+00:00 | templates-green | 0 | 1.81 | `pytest -q tests/cargo/interfaces/test_admin_live_map_templates.py` | `f96ee49b07b5e48f` |  |  |
| 2026-11-07T05:54:20+00:00 | admin-map-data-tests | 0 | 2.61 | `pytest -q tests/cargo/interfaces/test_admin_live_map_data.py` | `13ecf63495e34b95` |  |  |
