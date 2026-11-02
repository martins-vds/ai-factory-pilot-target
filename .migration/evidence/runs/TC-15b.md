# Run journal: TC-15b

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight |
|---|---|---|---|---|---|---|
| 2026-11-02T03:07:08+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |
| 2026-11-02T03:39:18+00:00 | setup-resume | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |
| 2026-11-02T03:40:30+00:00 | ledger-evidence-tests | 1 | 3.11 | `pytest -q tests/cargo/test_tracking.py::test_empty_and_unknown_ids_show_messages_without_cargo_result_or_map tests/cargo` | `7762f71d41ef822f` | _ ERROR at setup of test_empty_and_unknown_ids_show_messages_without_cargo_result_or_map _ |
| 2026-11-02T03:40:53+00:00 | ledger-evidence-tests-retry | 1 | 1.83 | `pytest -q tests/cargo/test_tracking.py::test_empty_and_unknown_ids_show_messages_without_cargo_result_or_map tests/cargo` | `9b5b9134bdbd0bf4` | _ ERROR at setup of test_empty_and_unknown_ids_show_messages_without_cargo_result_or_map _ |
