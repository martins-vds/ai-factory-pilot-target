# Run journal: TC-15c

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-02T03:44:36+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-02T03:46:19+00:00 | postgres-smoke | 0 | 5.3 | `pytest -q tests/cargo/test_repository.py` | `5f7522f05e8f426e` |  |  |
| 2026-11-02T04:09:45+00:00 | mutation-full-before | 0 | 1402.57 | `python .migration/harness/tools/afs-mutation --all` | `bc1419259b9c8c1b` |  |  |
| 2026-11-02T04:11:21+00:00 | targeted-tests | 0 | 4.02 | `pytest -q tests/cargo/test_domain_calculations.py tests/cargo/test_sample_data.py` | `93c5f7295963172b` |  |  |
| 2026-11-02T04:12:01+00:00 | regression | 0 | 14.17 | `pytest -q` | `c2c5558921a137d5` |  |  |
| 2026-11-02T04:12:10+00:00 | build-compile | 0 | 0.04 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-02T04:12:10+00:00 | build-django-check | 0 | 0.41 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-02T04:12:14+00:00 | idiom-ruff-check | 1 | 0.02 | `ruff check` | `1037884d37bac97f` | Found 1 error. |  |
| 2026-11-02T04:12:24+00:00 | idiom-ruff-autofix | 0 | 0.01 | `ruff check --fix tests/cargo/test_sample_data.py` | `aac3a0503d8b9505` | Found 1 error (1 fixed, 0 remaining). |  |
| 2026-11-02T04:12:28+00:00 | idiom-ruff-check-rerun | 0 | 0.01 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-02T04:12:29+00:00 | idiom-ruff-format | 0 | 0.02 | `ruff format --check` | `1a9301f4cf03fa0d` |  |  |
| 2026-11-02T04:12:34+00:00 | crap | 0 | 0.15 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv && python .migration/harness/tools/crap.py .migration/runs/lizard` | `13717159e2ec6f9a` |  |  |
| 2026-11-02T04:36:13+00:00 | mutation-full-after | 0 | 1387.77 | `python .migration/harness/tools/afs-mutation --all` | `400df51dc21b802b` |  |  |
| 2026-11-02T13:46:12+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-02T14:04:03+00:00 | mutation-full | 0 | 1033.19 | `python .migration/harness/tools/afs-mutation --all` | `3803c3be97be4858` |  | gate=mutation score=0.822 threshold=0.8 killed=426 survived=92 files=53 base=all |

## Mutation context

The `mutation-full` row is the profile's full `--all` run, executed after `afs-services check` reported `services OK: db`; the Compose service is `postgres:17`. The gate result is copied exactly from `AFS-RESULT`: score 0.822 against 0.8, 426 killed and 92 survived across 53 files. The preceding run in this journal scored 0.810 (792 killed, 186 survived) on a manually started PostgreSQL 16 cluster; the issue cites the Auditor's 0.797 (779 killed, 198 survived). The mutant totals differ substantially, and no pre-test run was repeated on this same revision and PostgreSQL 17, so the exact cause of the score discrepancy cannot be isolated; the current full-run result is the comparable acceptance evidence available here.
| 2026-11-02T15:27:08+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-02T15:53:26+00:00 | mutation-full | 0 | 1547.62 | `python .migration/harness/tools/afs-mutation --all` | `5a5f5f4bd11bce96` |  | gate=mutation score=0.819 threshold=0.8 killed=801 survived=177 files=53 base=all |
