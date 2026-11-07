# Run journal: BK-05D

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-07T15:31:33+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T15:35:17+00:00 | origin-test-red | 2 | 1.32 | `pytest -q tests/booking/interfaces/test_wizard.py` | `d71e403d5ad97e03` | ___________ ERROR collecting tests/booking/interfaces/test_wizard.py ___________ |  |
| 2026-11-07T15:35:34+00:00 | origin-test-green | 0 | 2.09 | `pytest -q tests/booking/interfaces/test_wizard.py` | `7eb11104642b7dc0` |  |  |
| 2026-11-07T15:36:04+00:00 | destination-test-red | 1 | 2.55 | `pytest -q tests/booking/interfaces/test_wizard.py` | `86721a16fb9bf6eb` | assert response.status_code == 200 |  |
| 2026-11-07T15:36:23+00:00 | destination-test-green | 0 | 2.53 | `pytest -q tests/booking/interfaces/test_wizard.py` | `79c4f9b3e3191fc9` |  |  |
| 2026-11-07T15:37:02+00:00 | deadline-test-red | 1 | 3.09 | `pytest -q tests/booking/interfaces/test_wizard.py` | `cc878bab0b77a6b0` | E       ModuleNotFoundError: No module named 'cargotracker.booking.interfaces.wizard.views.timezone'; 'cargotracker.book |  |
| 2026-11-07T15:37:12+00:00 | deadline-test-red | 1 | 3.13 | `pytest -q tests/booking/interfaces/test_wizard.py` | `b75b1493b7f6c863` | assert response.status_code == 200 |  |
| 2026-11-07T15:37:42+00:00 | deadline-test-green | 0 | 3.08 | `pytest -q tests/booking/interfaces/test_wizard.py` | `2415b537910957c0` |  |  |
| 2026-11-07T15:37:59+00:00 | duration-test-red | 1 | 4.01 | `pytest -q tests/booking/interfaces/test_wizard.py` | `c14fd67f1ca7635e` | assert response.status_code == 200 |  |
| 2026-11-07T15:38:17+00:00 | duration-test-green | 0 | 3.93 | `pytest -q tests/booking/interfaces/test_wizard.py` | `b165d8589a83a1d1` |  |  |
| 2026-11-07T15:38:34+00:00 | navigation-test-red | 1 | 4.47 | `pytest -q tests/booking/interfaces/test_wizard.py` | `114dbd82fdb67369` | >       assert 'Set the destination for this new cargo coming from Chicago' in ( |  |
| 2026-11-07T15:38:48+00:00 | navigation-test-green | 0 | 4.36 | `pytest -q tests/booking/interfaces/test_wizard.py` | `ad0d8a2eb7dc0348` |  |  |
| 2026-11-07T15:39:07+00:00 | submit-test-red | 1 | 5.02 | `pytest -q tests/booking/interfaces/test_wizard.py` | `ccbb19055899b215` | E           cargotracker.cargo.infrastructure.models.CargoRecord.DoesNotExist: CargoRecord matching query does not exist |  |
| 2026-11-07T15:39:30+00:00 | submit-test-green | 0 | 4.84 | `pytest -q tests/booking/interfaces/test_wizard.py` | `154757f69803b92f` |  |  |
| 2026-11-07T15:39:51+00:00 | same-origin-test-red | 1 | 5.39 | `pytest -q tests/booking/interfaces/test_wizard.py` | `75d39e20c625de09` | >       assert response.status_code == 200 |  |
| 2026-11-07T15:40:04+00:00 | same-origin-test-green | 0 | 5.14 | `pytest -q tests/booking/interfaces/test_wizard.py` | `ae5426b4e6484c4c` |  |  |
| 2026-11-07T15:41:05+00:00 | wizard-flow-tests | 0 | 6.42 | `pytest -q tests/booking/interfaces/test_wizard.py` | `eb8613fd3fd5a772` |  |  |
| 2026-11-07T15:41:45+00:00 | origin-validation-red | 1 | 7.41 | `pytest -q tests/booking/interfaces/test_wizard.py` | `5f744052c7181855` | >       assert 'Choose the origin of the new cargo' in content |  |
| 2026-11-07T15:42:02+00:00 | origin-validation-green | 0 | 7.27 | `pytest -q tests/booking/interfaces/test_wizard.py` | `310f153101e5cc7c` |  |  |
| 2026-11-07T15:43:11+00:00 | state-preservation-red | 1 | 7.72 | `pytest -q tests/booking/interfaces/test_wizard.py` | `7b78bfebd23acfca` | >       assert 'name="deadline" value="2026-11-09"' in destination_response.content.decode() |  |
| 2026-11-07T15:43:56+00:00 | state-preservation-green | 0 | 7.6 | `pytest -q tests/booking/interfaces/test_wizard.py` | `b00ad2e6bfb0f9ee` |  |  |
| 2026-11-07T15:44:41+00:00 | wizard-flow-refactor-tests | 0 | 7.57 | `pytest -q tests/booking/interfaces/test_wizard.py` | `2bf00bf9836da9c8` |  |  |
| 2026-11-07T15:45:18+00:00 | wizard-final-targeted | 1 | 7.66 | `pytest -q tests/booking/interfaces/test_wizard.py` | `21ca0e1fff511644` | assert response.status_code == 200 |  |
| 2026-11-07T15:45:39+00:00 | wizard-final-targeted | 0 | 7.69 | `pytest -q tests/booking/interfaces/test_wizard.py` | `9dd28b6d77427e6d` |  |  |
| 2026-11-07T15:45:57+00:00 | destination-validation-red | 0 | 8.14 | `pytest -q tests/booking/interfaces/test_wizard.py` | `41e9be429f9687d5` |  |  |
| 2026-11-07T15:46:21+00:00 | idiom-ruff-check | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T15:46:25+00:00 | idiom-ruff-format | 1 | 0.02 | `ruff format --check` | `7739c3d2ee1e69ba` |  |  |
| 2026-11-07T15:46:38+00:00 | idiom-ruff-format | 0 | 0.01 | `ruff format --check` | `3e363a951eafb2bc` |  |  |
| 2026-11-07T15:46:42+00:00 | build-compile | 0 | 0.05 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T15:46:46+00:00 | build-check | 0 | 0.38 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T15:46:50+00:00 | idiom-ruff-check | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T15:47:43+00:00 | behavior-tests | 0 | 48.77 | `pytest -q` | `d1acefce04366214` |  |  |
| 2026-11-07T15:48:38+00:00 | crap-coverage | 0 | 48.55 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `661a0f2d499cdacc` |  |  |
| 2026-11-07T15:48:43+00:00 | crap-lizard | 0 | 0.15 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T15:48:48+00:00 | crap-score | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `c466f686db79d28f` |  | gate=crap max=19.0 threshold=30 over=0 methods=155 |
