# Run journal: HR-04D

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-03T20:42:19+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-03T20:47:32+00:00 | processing-red | 2 | 1.45 | `pytest -q tests/handling/test_registration_processing.py` | `5c3a97d3a9f4c611` | _______ ERROR collecting tests/handling/test_registration_processing.py ________ |  |
| 2026-11-03T20:48:38+00:00 | processing-idempotence-initial-green | 1 | 2.18 | `pytest -q tests/handling/test_registration_processing.py` | `5f92992c72f95b1e` | >       assert process_registration_attempt() is True |  |
| 2026-11-03T20:48:55+00:00 | processing-idempotence-green | 0 | 2.12 | `pytest -q tests/handling/test_registration_processing.py` | `1969d567e72eca2c` |  |  |
| 2026-11-03T20:49:25+00:00 | processing-and-history | 0 | 2.29 | `pytest -q tests/handling/test_registration_processing.py tests/handling/test_domain.py` | `2fbde5a0adf1ca5d` |  |  |
| 2026-11-03T20:49:39+00:00 | rejection-tests | 0 | 3.63 | `pytest -q tests/handling/test_registration_processing.py` | `98acbf2a18d506b5` |  |  |
| 2026-11-03T20:50:00+00:00 | delivery-outcome | 1 | 4.34 | `pytest -q tests/handling/test_registration_processing.py` | `c09ab50b669c30ac` | assert process_registration_attempt() is True |  |
| 2026-11-03T20:50:18+00:00 | delivery-outcome-green | 0 | 4.25 | `pytest -q tests/handling/test_registration_processing.py` | `6d7b18ffc96fdcfb` |  |  |
| 2026-11-03T20:50:47+00:00 | retry-red | 1 | 4.85 | `pytest -q tests/handling/test_registration_processing.py` | `6e875cf9b28076c8` | raise OperationalError('temporary database failure') |  |
| 2026-11-03T20:51:13+00:00 | retry-green | 0 | 7.18 | `pytest -q tests/handling/test_registration_processing.py` | `2f5ca87d4c05825e` |  |  |
| 2026-11-03T20:51:32+00:00 | concurrent-claim | 0 | 7.64 | `pytest -q tests/handling/test_registration_processing.py` | `34eca3bbb34c2cc9` |  |  |
| 2026-11-03T20:53:18+00:00 | handling-processing-tests | 0 | 8.33 | `pytest -q tests/handling/test_registration_processing.py tests/handling/test_domain.py` | `57e58251ed246694` |  |  |
