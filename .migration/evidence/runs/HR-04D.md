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
| 2026-11-03T20:56:10+00:00 | handling-regression | 0 | 8.65 | `pytest -q tests/handling` | `8542495a6a514709` |  |  |
| 2026-11-03T20:57:20+00:00 | handling-regression-final | 0 | 9.36 | `pytest -q tests/handling` | `22bcc0dd3bff6f75` |  |  |
| 2026-11-03T20:57:33+00:00 | idiom-ruff-check | 1 | 0.02 | `ruff check` | `f75be1120c69428e` | Found 1 error. |  |
| 2026-11-03T20:57:51+00:00 | idiom-ruff-check | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-03T20:57:55+00:00 | idiom-ruff-format | 1 | 0.02 | `ruff format --check` | `33742bd590d2cf53` | -                 logger.error('Handling attempt processing still failing after 15 minutes: %s', error) |  |
| 2026-11-03T20:59:17+00:00 | handling-regression-injected | 1 | 6.85 | `pytest -q tests/handling` | `ce0a5ac0db40ad73` | raise OperationalError('temporary database failure') |  |
| 2026-11-03T20:59:44+00:00 | handling-regression-injected-green | 0 | 8.39 | `pytest -q tests/handling` | `f855be4d037d66a8` |  |  |
| 2026-11-03T21:00:14+00:00 | build-compile | 0 | 0.05 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-03T21:00:18+00:00 | build-django-check | 0 | 0.36 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-03T21:00:47+00:00 | behavior | 0 | 24.18 | `pytest -q` | `843e0c2c853f9613` |  |  |
| 2026-11-03T21:00:53+00:00 | idiom-ruff-check-final | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-03T21:01:06+00:00 | idiom-ruff-format-final | 0 | 0.01 | `ruff format --check` | `1b6b02b900f11801` |  |  |
| 2026-11-03T21:01:34+00:00 | crap-coverage | 0 | 22.14 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `8b688a3819a4e975` |  |  |
| 2026-11-03T21:01:45+00:00 | crap-lizard | 0 | 0.13 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-03T21:01:50+00:00 | crap-score | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `677beee7579ccc85` |  | gate=crap max=20.0 threshold=30 over=0 methods=119 |
| 2026-11-03T21:07:20+00:00 | mutation-changed | 1 | 324.09 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `bcc9cbaef8e09fcf` | afs-mutation: FAILED score=0.665 threshold=0.8 killed=103 survived=52 skipped=0 files=6 jobs=4 base=origin/main | gate=mutation score=0.665 threshold=0.8 killed=103 survived=52 files=6 base=origin/main |
| 2026-11-03T21:11:24+00:00 | history-id-red | 1 | 1.42 | `pytest -q tests/handling/test_domain.py::test_handling_history_keeps_the_highest_id_when_deduplicating_identical_events` | `2218d6e0392a1955` | assert len(history.events) == 1 |  |
| 2026-11-03T21:12:30+00:00 | remediation-tests | 1 | 9.68 | `pytest -q tests/handling/test_domain.py tests/handling/test_registration_processing.py` | `481a1c926b37bc60` | assert _process() is True |  |
| 2026-11-03T21:13:06+00:00 | remediation-tests-green | 0 | 9.65 | `pytest -q tests/handling/test_domain.py tests/handling/test_registration_processing.py` | `fd5a373639c0809f` |  |  |
| 2026-11-03T21:14:34+00:00 | processing-ports-tests | 0 | 8.93 | `pytest -q tests/handling/test_domain.py tests/handling/test_registration_processing.py` | `6051a056ca483ef0` |  |  |
| 2026-11-03T21:15:04+00:00 | event-id-outcome | 0 | 2.4 | `pytest -q tests/handling/test_registration_processing.py::test_equal_completion_and_registration_times_use_event_id_for_delivery` | `09c7191b036bc2d0` |  |  |
| 2026-11-03T21:15:54+00:00 | history-ids-port-red | 1 | 1.42 | `pytest -q tests/handling/test_domain.py::test_handling_history_breaks_completion_time_ties_by_registration_time_then_id` | `86e367109eaa3649` | E       TypeError: HandlingHistory.__init__() got an unexpected keyword argument 'event_ids'. Did you mean 'events'? |  |
| 2026-11-03T21:16:51+00:00 | history-repository-ids | 1 | 10.4 | `pytest -q tests/handling/test_domain.py tests/handling/test_repository.py tests/handling/test_registration_processing.py` | `d9ea5f1e33e6820f` | assert [event.event_type for event in history.events] == [ |  |
| 2026-11-03T21:17:29+00:00 | history-repository-ids-green | 0 | 10.69 | `pytest -q tests/handling/test_domain.py tests/handling/test_repository.py tests/handling/test_registration_processing.py` | `f9d935407a353649` |  |  |
| 2026-11-03T21:18:35+00:00 | atomic-retry-tests | 0 | 10.48 | `pytest -q tests/handling/test_registration_processing.py tests/handling/test_domain.py` | `76f7dd78c3034232` |  |  |
| 2026-11-03T21:18:50+00:00 | build-compile-final | 0 | 0.05 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-03T21:19:03+00:00 | build-check-final | 0 | 0.37 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-03T21:19:17+00:00 | behavior-handling-final | 0 | 11.62 | `pytest -q tests/handling` | `79772e3284943956` |  |  |
| 2026-11-03T21:19:46+00:00 | tests-full-final | 0 | 22.6 | `pytest -q` | `68416325c2435ed6` |  |  |
| 2026-11-03T21:19:49+00:00 | idiom-ruff-final | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-03T21:19:56+00:00 | idiom-format-final | 0 | 0.01 | `ruff format --check` | `1b6b02b900f11801` |  |  |
| 2026-11-03T21:20:29+00:00 | crap-coverage-final | 0 | 23.58 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `0937a343b0c3ed1c` |  |  |
| 2026-11-03T21:20:43+00:00 | crap-lizard-final | 0 | 0.13 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-03T21:20:46+00:00 | crap-score-final | 1 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `16b1b6c047d0ce2c` |  | gate=crap max=72.0 threshold=30 over=1 methods=122 |
| 2026-11-03T21:21:32+00:00 | worker-command-tests | 0 | 11.43 | `pytest -q tests/handling/test_registration_processing.py` | `cd66f2e3d418ba28` |  |  |
| 2026-11-03T21:22:01+00:00 | crap-coverage-final | 0 | 25.76 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `fd2c2830ab64f4c8` |  |  |
| 2026-11-03T21:22:05+00:00 | crap-lizard-final | 0 | 0.13 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-03T21:22:05+00:00 | crap-score-final | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `47bac2b7ee896840` |  | gate=crap max=19.4 threshold=30 over=0 methods=122 |
| 2026-11-03T21:28:49+00:00 | mutation-changed-final | 1 | 400.06 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `860766f3127759c9` | afs-mutation: FAILED score=0.697 threshold=0.8 killed=136 survived=59 skipped=0 files=6 jobs=4 base=origin/main | gate=mutation score=0.697 threshold=0.8 killed=136 survived=59 files=6 base=origin/main |
| 2026-11-03T21:30:29+00:00 | mutation-remediation-tests | 0 | 11.44 | `pytest -q tests/handling/test_domain.py tests/handling/test_registration_processing.py` | `c77eb0e574ab0dea` |  |  |
| 2026-11-03T21:37:31+00:00 | mutation-changed-final | 1 | 384.61 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `b316ab702b02c0ac` | afs-mutation: FAILED score=0.776 threshold=0.8 killed=159 survived=46 skipped=0 files=7 jobs=4 base=origin/main | gate=mutation score=0.776 threshold=0.8 killed=159 survived=46 files=7 base=origin/main |
| 2026-11-03T22:05:08+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-03T22:05:41+00:00 | mutation-changed | 1 | 0.27 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `3ff11adc524e78cf` |  |  |
| 2026-11-03T22:06:27+00:00 | mutation-changed-current | 1 | 0.1 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `3ff11adc524e78cf` |  |  |
| 2026-11-03T22:13:29+00:00 | mutation-changed-current | 1 | 381.87 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `b316ab702b02c0ac` | afs-mutation: FAILED score=0.776 threshold=0.8 killed=159 survived=46 skipped=0 files=7 jobs=4 base=origin/main | gate=mutation score=0.776 threshold=0.8 killed=159 survived=46 files=7 base=origin/main |
| 2026-11-03T22:15:50+00:00 | mutation-focused-tests | 0 | 10.53 | `pytest -q tests/handling/test_domain.py tests/handling/test_registration_processing.py` | `364bb140db1c32c4` |  |  |
| 2026-11-03T22:24:02+00:00 | mutation-changed-remediated | 1 | 473.36 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `1483b68836219b35` | afs-mutation: FAILED score=0.785 threshold=0.8 killed=161 survived=44 skipped=0 files=7 jobs=4 base=origin/main | gate=mutation score=0.785 threshold=0.8 killed=161 survived=44 files=7 base=origin/main |
| 2026-11-03T22:25:21+00:00 | worker-validation-tests | 1 | 11.17 | `pytest -q tests/handling/test_registration_processing.py` | `d194f6a65a3fe05a` | E               KeyError: 'help' |  |
| 2026-11-03T22:25:44+00:00 | worker-validation-tests | 0 | 11.06 | `pytest -q tests/handling/test_registration_processing.py` | `d8d9e0be8fcdb425` |  |  |
| 2026-11-03T22:26:00+00:00 | focused-remediation-tests-final | 0 | 11.15 | `pytest -q tests/handling/test_domain.py tests/handling/test_registration_processing.py` | `e8bc1a59e840dbf2` |  |  |
| 2026-11-03T22:34:08+00:00 | mutation-changed-final | 1 | 475.46 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `1483b68836219b35` | afs-mutation: FAILED score=0.785 threshold=0.8 killed=161 survived=44 skipped=0 files=7 jobs=4 base=origin/main | gate=mutation score=0.785 threshold=0.8 killed=161 survived=44 files=7 base=origin/main |
| 2026-11-03T22:35:22+00:00 | mutation-command-diagnostic | 1 | 31.58 | `python .migration/harness/tools/afs-mutation --paths src/cargotracker/handling/management/commands/process_handling_attempts.py --jobs 1` | `dab67588130f48ed` | afs-mutation: FAILED score=0.696 threshold=0.8 killed=16 survived=7 skipped=0 files=1 jobs=1 base=explicit | gate=mutation score=0.696 threshold=0.8 killed=16 survived=7 files=1 base=explicit |
| 2026-11-03T22:36:19+00:00 | exact-validation-tests | 0 | 11.28 | `pytest -q tests/handling/test_domain.py tests/handling/test_registration_processing.py` | `6a33328111d02971` |  |  |
| 2026-11-03T22:37:12+00:00 | mutation-command-exact-errors | 0 | 32.26 | `python .migration/harness/tools/afs-mutation --paths src/cargotracker/handling/management/commands/process_handling_attempts.py --jobs 1` | `63f43dcd78217854` |  | gate=mutation score=0.870 threshold=0.8 killed=20 survived=3 files=1 base=explicit |
| 2026-11-03T22:45:18+00:00 | mutation-changed-final | 0 | 477.17 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `cc18867b3ebaaf29` |  | gate=mutation score=0.815 threshold=0.8 killed=167 survived=38 files=7 base=origin/main |
| 2026-11-03T22:45:39+00:00 | final-build-compile | 0 | 0.05 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-03T22:45:46+00:00 | final-build-django-check | 0 | 0.44 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-03T22:46:08+00:00 | final-regression | 0 | 11.44 | `pytest -q tests/handling` | `a4ea8ba3f397a858` |  |  |
| 2026-11-03T22:46:35+00:00 | final-behavior-tests | 0 | 22.63 | `pytest -q` | `1894c53d21a067d7` |  |  |
| 2026-11-03T22:46:40+00:00 | final-idiom-ruff-check | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-03T22:47:05+00:00 | final-idiom-ruff-format | 1 | 0.02 | `ruff format --check` | `c44ac0d80daa1d1c` | -     monkeypatch.setattr(worker, 'sleep', lambda _: pytest.fail('worker slept with invalid settings')) |  |
| 2026-11-03T22:47:30+00:00 | final-idiom-ruff-format | 0 | 0.01 | `ruff format --check` | `1b6b02b900f11801` |  |  |
| 2026-11-03T22:48:07+00:00 | final-crap-coverage | 0 | 23.94 | `pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov` | `8a36300321a835a0` |  |  |
| 2026-11-03T22:48:13+00:00 | final-crap-lizard | 0 | 0.16 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-03T22:48:22+00:00 | final-crap-score | 0 | 0.04 | `python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30` | `7aabe95ab34f288e` |  | gate=crap max=19.0 threshold=30 over=0 methods=122 |
| 2026-11-03T22:49:13+00:00 | final-behavior-tests | 0 | 22.51 | `pytest -q` | `9214b31d881ce3e6` |  |  |
| 2026-11-03T22:49:28+00:00 | final-regression | 0 | 11.49 | `pytest -q tests/handling` | `87ea04280b2c429e` |  |  |
| 2026-11-03T23:48:36+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-03T23:52:43+00:00 | verifier-rest-flow | 0 | 3.97 | `pytest -q tests/handling/test_registration_processing.py::test_rest_accepted_report_is_processed_into_handling_event_and_cargo_delivery` | `1d0e0d67d1aa6a95` |  |  |
