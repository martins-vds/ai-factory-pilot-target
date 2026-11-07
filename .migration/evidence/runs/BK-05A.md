# Run journal: BK-05A

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-07T03:49:04+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T03:51:07+00:00 | tdd-red | 2 | 2.32 | `pytest -q tests/booking/application` | `6bfd436367a5d41c` | _______ ERROR collecting tests/booking/application/test_registration.py ________ |  |
| 2026-11-07T03:51:45+00:00 | tdd-green | 0 | 1.1 | `pytest -q tests/booking/application` | `53e496b3492d6f07` |  |  |
| 2026-11-07T03:53:08+00:00 | build-compile | 0 | 0.04 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T03:53:09+00:00 | build-check | 0 | 0.24 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T03:53:09+00:00 | idiom-lint | 1 | 0.01 | `ruff check` | `2aac03cc572db868` |  |  |
| 2026-11-07T03:53:22+00:00 | idiom-lint-rerun | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T03:53:22+00:00 | idiom-format | 0 | 0.01 | `ruff format --check` | `8f54ec861a76fc44` |  |  |
| 2026-11-07T03:53:52+00:00 | tests | 0 | 26.07 | `pytest -q` | `1c835f6c11e32a26` |  |  |
| 2026-11-07T03:54:23+00:00 | crap-coverage | 0 | 26.71 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `dde1f9736f10ab32` |  |  |
| 2026-11-07T03:54:23+00:00 | crap-lizard | 0 | 0.08 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T03:54:23+00:00 | crap-threshold | 0 | 0.03 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `df94388d8dc116c8` |  | gate=crap max=19.0 threshold=30 over=0 methods=139 |
| 2026-11-07T03:54:38+00:00 | mutation-changed | 0 | 10.14 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `bbaa364119793b1e` |  | gate=mutation score=0.944 threshold=0.8 killed=17 survived=1 files=2 base=origin/main |
| 2026-11-07T03:55:18+00:00 | tdd-edge | 0 | 1.08 | `pytest -q tests/booking/application` | `81e259044c81c485` |  |  |
| 2026-11-07T03:55:32+00:00 | mutation-changed-rerun | 0 | 9.63 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `bbaa364119793b1e` |  | gate=mutation score=0.944 threshold=0.8 killed=17 survived=1 files=2 base=origin/main |
| 2026-11-07T03:56:09+00:00 | mutation-changed-final | 0 | 9.48 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `bbaa364119793b1e` |  | gate=mutation score=0.944 threshold=0.8 killed=17 survived=1 files=2 base=origin/main |
| 2026-11-07T03:57:06+00:00 | behavior-final | 0 | 23.16 | `pytest -q` | `4d458973569f6c45` |  |  |
| 2026-11-07T03:57:06+00:00 | idiom-lint-final | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T03:57:06+00:00 | idiom-format-final | 0 | 0.01 | `ruff format --check` | `8f54ec861a76fc44` |  |  |
| 2026-11-07T03:57:31+00:00 | crap-coverage-final | 0 | 24.46 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `e3734c9281b15347` |  |  |
| 2026-11-07T03:57:31+00:00 | crap-lizard-final | 0 | 0.07 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T03:57:31+00:00 | crap-threshold-final | 0 | 0.02 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `df94388d8dc116c8` |  | gate=crap max=19.0 threshold=30 over=0 methods=139 |
| 2026-11-07T04:14:40+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T04:16:28+00:00 | build-compile | 0 | 0.07 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T04:16:29+00:00 | build-check | 0 | 0.77 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T04:17:09+00:00 | behavior | 0 | 40.01 | `pytest -q` | `880a9bf72b6de8b8` |  |  |
| 2026-11-07T04:17:09+00:00 | idiom-lint | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T04:17:09+00:00 | idiom-format | 0 | 0.02 | `ruff format --check` | `8f54ec861a76fc44` |  |  |
| 2026-11-07T04:17:48+00:00 | crap-coverage | 0 | 39.06 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `8ca3826fceab0153` |  |  |
| 2026-11-07T04:17:49+00:00 | crap-lizard | 0 | 0.11 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T04:17:49+00:00 | crap-threshold | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `df94388d8dc116c8` |  | gate=crap max=19.0 threshold=30 over=0 methods=139 |
| 2026-11-07T04:18:02+00:00 | mutation-changed | 0 | 12.91 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `bbaa364119793b1e` |  | gate=mutation score=0.944 threshold=0.8 killed=17 survived=1 files=2 base=origin/main |
| 2026-11-07T04:18:41+00:00 | regression | 0 | 39.16 | `pytest -q` | `417c6a0ab9eb99f0` |  |  |
| 2026-11-07T04:22:55+00:00 | verifier-legacy-fields | 0 | 1.72 | `pytest -q tests/booking/application/test_registration.py tests/booking/application/test_specification.py` | `ff8b70c9209cc2a9` |  |  |
| 2026-11-07T04:23:28+00:00 | build-compile | 0 | 0.04 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T04:23:28+00:00 | build-check | 0 | 0.39 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T04:24:09+00:00 | behavior | 0 | 40.97 | `pytest -q` | `66684f42dc0c354c` |  |  |
| 2026-11-07T04:24:09+00:00 | idiom-lint | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T04:24:09+00:00 | idiom-format | 0 | 0.01 | `ruff format --check` | `8f54ec861a76fc44` |  |  |
| 2026-11-07T04:24:48+00:00 | crap-coverage | 0 | 38.35 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `807b7a7083b1bcd2` |  |  |
| 2026-11-07T04:24:48+00:00 | crap-lizard | 0 | 0.11 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T04:24:48+00:00 | crap-threshold | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `df94388d8dc116c8` |  | gate=crap max=19.0 threshold=30 over=0 methods=139 |
| 2026-11-07T04:25:01+00:00 | mutation-changed | 0 | 13.06 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `bbaa364119793b1e` |  | gate=mutation score=0.944 threshold=0.8 killed=17 survived=1 files=2 base=origin/main |
| 2026-11-07T04:25:49+00:00 | regression | 0 | 47.63 | `pytest -q` | `6481f0c0ddb30735` |  |  |
| 2026-11-07T04:31:45+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T04:33:47+00:00 | tdd-red-registration | 1 | 3.31 | `pytest -q tests/booking/application/test_registration.py::test_registration_persists_new_cargo_with_generated_id_and_empty_itinerary` | `3d92251b03c2d1bd` | >       assert f'Booked new cargo with tracking ID {tracking_id.value}' in caplog.messages |  |
| 2026-11-07T04:34:00+00:00 | tdd-green-registration | 0 | 1.61 | `pytest -q tests/booking/application/test_registration.py::test_registration_persists_new_cargo_with_generated_id_and_empty_itinerary` | `d44de49cc8aa128c` |  |  |
| 2026-11-07T04:34:10+00:00 | tdd-red-destination | 1 | 1.7 | `pytest -q tests/booking/application/test_specification.py::test_change_destination_preserves_other_specification_fields_and_resets_route_state` | `91282aa6b4b8fe13` | >       assert f'Changed destination for cargo {original.tracking_id} to {destination}' in caplog.messages |  |
| 2026-11-07T04:34:20+00:00 | tdd-green-destination | 0 | 1.62 | `pytest -q tests/booking/application/test_specification.py::test_change_destination_preserves_other_specification_fields_and_resets_route_state` | `e953d66aa32df0e1` |  |  |
| 2026-11-07T04:34:28+00:00 | tdd-red-deadline | 1 | 1.69 | `pytest -q tests/booking/application/test_specification.py::test_change_deadline_preserves_other_specification_fields_and_resets_route_state` | `c7f7e53fc0a2032d` | >       assert f'Changed deadline for cargo {original.tracking_id} to {earlier_deadline}' in caplog.messages |  |
| 2026-11-07T04:34:40+00:00 | tdd-green-deadline | 0 | 1.62 | `pytest -q tests/booking/application/test_specification.py::test_change_deadline_preserves_other_specification_fields_and_resets_route_state` | `b29404b0332b987b` |  |  |
| 2026-11-07T04:34:41+00:00 | tdd-green-registration-final | 0 | 1.56 | `pytest -q tests/booking/application/test_registration.py::test_registration_persists_new_cargo_with_generated_id_and_empty_itinerary` | `a558b8376cd28466` |  |  |
| 2026-11-07T04:35:31+00:00 | build-compile-final | 0 | 0.06 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T04:35:31+00:00 | build-check-final | 0 | 0.36 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T04:35:31+00:00 | idiom-lint-final | 1 | 0.02 | `ruff check` | `ef035980c42a113c` |  |  |
| 2026-11-07T04:35:42+00:00 | idiom-lint-final-rerun | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T04:35:42+00:00 | idiom-format-final | 1 | 0.02 | `ruff format --check` | `2784e02ac8461810` | -     assert f'Changed destination for cargo {original.tracking_id} to {destination}' in caplog.messages |  |
| 2026-11-07T04:35:46+00:00 | idiom-format-final-rerun | 0 | 0.01 | `ruff format --check` | `8f54ec861a76fc44` |  |  |
| 2026-11-07T04:36:48+00:00 | behavior-final | 0 | 51.35 | `pytest -q` | `3677a12cb5e4e760` |  |  |
| 2026-11-07T04:37:30+00:00 | crap-coverage-final | 0 | 42.15 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `c25e047f91cc7a33` |  |  |
| 2026-11-07T04:37:36+00:00 | crap-lizard-final | 0 | 0.13 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T04:37:36+00:00 | crap-threshold-final | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `df94388d8dc116c8` |  | gate=crap max=19.0 threshold=30 over=0 methods=139 |
| 2026-11-07T04:37:55+00:00 | mutation-changed-final | 0 | 18.53 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `abc43bad9b9c9ce0` |  | gate=mutation score=0.960 threshold=0.8 killed=24 survived=1 files=2 base=origin/main |
| 2026-11-07T04:38:46+00:00 | regression-final | 0 | 41.43 | `pytest -q` | `a8703e3a6ed4fc20` |  |  |
| 2026-11-07T04:39:32+00:00 | build-compile-rerun | 0 | 0.04 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T04:39:33+00:00 | build-check-rerun | 0 | 0.36 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T04:52:32+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T04:53:41+00:00 | verifier-unknown-deadline | 0 | 1.26 | `pytest -q tests/booking/application/test_specification.py::test_change_deadline_raises_lookup_error_for_unknown_cargo` | `f17ef6e2702e9118` |  |  |
| 2026-11-07T04:53:49+00:00 | build-compile | 0 | 0.04 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T04:53:53+00:00 | build-check | 0 | 0.22 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-07T04:53:56+00:00 | idiom-lint | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-07T04:53:58+00:00 | idiom-format | 0 | 0.01 | `ruff format --check` | `8f54ec861a76fc44` |  |  |
| 2026-11-07T04:54:31+00:00 | behavior | 0 | 30.79 | `pytest -q` | `e2d01a672027679c` |  |  |
| 2026-11-07T04:55:00+00:00 | crap-coverage | 0 | 26.02 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `90003f167d7bbade` |  |  |
| 2026-11-07T04:55:04+00:00 | crap-lizard | 0 | 0.08 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T04:55:06+00:00 | crap-threshold | 0 | 0.03 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `df94388d8dc116c8` |  | gate=crap max=19.0 threshold=30 over=0 methods=139 |
| 2026-11-07T04:55:24+00:00 | mutation-changed | 0 | 13.04 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `abc43bad9b9c9ce0` |  | gate=mutation score=0.960 threshold=0.8 killed=24 survived=1 files=2 base=origin/main |
| 2026-11-07T04:56:03+00:00 | regression | 0 | 31.69 | `pytest -q` | `2c9f3089c4d8ec28` |  |  |
| 2026-11-07T05:06:16+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T05:06:46+00:00 | validate-return-pr | 0 | 1.27 | `python .migration/harness/tools/validate.py .migration` | `5b9d79e0f06ef348` |  |  |
