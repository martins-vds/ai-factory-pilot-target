# Run journal: HR-04F

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-04T19:28:17+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-04T19:28:38+00:00 | graph-source | 0 | 0.1 | `python .migration/harness/tools/graph_gate.py --side source` | `c070c957323aa7e9` |  | gate=graph side=source verdict=pass failures=0 entry_points=27 reaching_data=18 enriched_edges=1352 |
| 2026-11-04T19:28:38+00:00 | graph-target | 0 | 0.08 | `python .migration/harness/tools/graph_gate.py --side target --require-graph` | `4b734ce13b6fa527` |  | gate=graph side=target verdict=pass failures=0 entry_points=7 reaching_data=3 enriched_edges=510 |
| 2026-11-04T19:29:41+00:00 | build-compileall | 0 | 0.09 | `python -m compileall -q src` | `e3b0c44298fc1c14` |  |  |
| 2026-11-04T19:29:43+00:00 | build-django-check | 0 | 1.8 | `python manage.py check` | `1e3e63f221bde888` |  |  |
| 2026-11-04T19:29:43+00:00 | idiom-ruff-check | 0 | 0.02 | `ruff check` | `82b3e6a6c090a576` |  |  |
| 2026-11-04T19:29:43+00:00 | idiom-ruff-format | 0 | 0.02 | `ruff format --check` | `13e464c51f06111c` |  |  |
| 2026-11-04T19:30:28+00:00 | tests | 0 | 44.94 | `pytest -q` | `29ae69f512e05c95` |  |  |
| 2026-11-04T19:31:09+00:00 | crap | 0 | 40.76 | `bash -c 'pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov && lizard --csv src > .migration/runs/lizard.csv && python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30'` | `60d2ec6e1107695c` |  | gate=crap max=19.0 threshold=30 over=0 methods=132 |
| 2026-11-04T19:31:09+00:00 | mutation-changed | 0 | 0.08 | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | `36603172da4a0d74` |  | gate=mutation score=n/a reason=no-mutable-code-changed base=origin/main |
| 2026-11-04T20:32:57+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |

## Bounded recovery record — 2026-11-04 (not a gate-run row)

- The coordinator-confirmed full mutation invocation was externally cancelled in [Actions run 41896926094](https://github.com/martins-vds/ai-factory-pilot-target/actions/runs/41896926094). It has no completed result. No `afs-run` completion row or score is recorded for it.
- Output inspection found no completed HR-04F full-mutation result in the journal, no full-mutation artifact in `.migration/runs/HR-04F` (the local files there are setup probes only), and no `.migration/evidence/mutants/HR-04F.md`.
- The prior successful graph, build, idiom, tests, CRAP, and changed-mutation rows above are historical and unchanged.
- Bounded recovery output validation: `python .migration/harness/tools/validate.py .migration` exited 0 (86 files checked, 0 errors); all four HR-04F report, return, handoff, and journal paths existed; `git diff --check` exited 0. This validates the return schema and durable outputs, not the interrupted mutation gate.
| 2026-11-04T23:39:31+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |

## Imported durable acceptance journal

Source: verified artifact `13371474656` from [Actions run 41924854967, attempt 1](https://github.com/martins-vds/ai-factory-pilot-target/actions/runs/41924854967), ZIP SHA-256 `1f023eab634c89321869c3aec907c59428222746466010356dfacde3501dd60b`. The following 15 data rows are copied unchanged from `journals/HR-04F.md` in that artifact; they are workflow evidence, not local reruns.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-04T22:24:06+00:00 | runtime | 0 | 0.06 | `/opt/hostedtoolcache/Python/3.13.17/x64/bin/python /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.migration/harness/tools/check_runtime.py` | `d07c895212ff2443` |  |  |
| 2026-11-04T22:24:06+00:00 | harness-integrity | 0 | 0.08 | `/opt/hostedtoolcache/Python/3.13.17/x64/bin/python /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.migration/harness/tools/check_installed.py` | `1b22ec25ad38f843` |  |  |
| 2026-11-04T22:24:06+00:00 | services | 0 | 0.16 | `/opt/hostedtoolcache/Python/3.13.17/x64/bin/python /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.migration/harness/tools/afs-services check` | `274667623a156426` |  |  |
| 2026-11-04T22:24:06+00:00 | graph-freshness | 0 | 0.09 | `/opt/hostedtoolcache/Python/3.13.17/x64/bin/python /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.migration/harness/tools/check_graph_fresh.py --require source,target` | `e58be4641e00fbe4` |  |  |
| 2026-11-04T22:24:06+00:00 | graph-source | 0 | 0.1 | `/opt/hostedtoolcache/Python/3.13.17/x64/bin/python /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.migration/harness/tools/graph_gate.py --side source --require-graph` | `c070c957323aa7e9` |  | gate=graph side=source verdict=pass failures=0 entry_points=27 reaching_data=18 enriched_edges=1352 |
| 2026-11-04T22:24:07+00:00 | graph-target | 0 | 0.08 | `/opt/hostedtoolcache/Python/3.13.17/x64/bin/python /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.migration/harness/tools/graph_gate.py --side target --require-graph` | `4b734ce13b6fa527` |  | gate=graph side=target verdict=pass failures=0 entry_points=7 reaching_data=3 enriched_edges=510 |
| 2026-11-04T22:24:07+00:00 | build-0 | 0 | 0.08 | `bash -c 'python -m compileall -q src'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-04T22:24:08+00:00 | build-1 | 0 | 0.92 | `bash -c 'python manage.py check'` | `1e3e63f221bde888` |  |  |
| 2026-11-04T22:24:08+00:00 | idiom-0 | 0 | 0.02 | `bash -c 'ruff check'` | `82b3e6a6c090a576` |  |  |
| 2026-11-04T22:24:08+00:00 | idiom-1 | 0 | 0.02 | `bash -c 'ruff format --check'` | `13e464c51f06111c` |  |  |
| 2026-11-04T22:24:55+00:00 | tests-0 | 0 | 47.31 | `bash -c 'pytest -q'` | `27f3c19d8f5d95ff` |  |  |
| 2026-11-04T22:25:42+00:00 | crap-0 | 0 | 46.54 | `bash -c 'pytest -q --cov=src --cov-report=lcov:.migration/runs/crap.lcov'` | `8a710fdb81cc1ec5` |  |  |
| 2026-11-04T22:25:42+00:00 | crap-1 | 0 | 0.13 | `bash -c 'lizard --csv src > .migration/runs/lizard.csv'` | `e3b0c44298fc1c14` |  |  |
| 2026-11-04T22:25:42+00:00 | crap-2 | 0 | 0.06 | `bash -c 'python .migration/harness/tools/crap.py .migration/runs/lizard.csv --lcov .migration/runs/crap.lcov --max 30'` | `34d1ce024bdfe792` |  | gate=crap max=19.0 threshold=30 over=0 methods=132 |
| 2026-11-04T23:26:04+00:00 | mutation_full-0 | 0 | 3621.5 | `bash -c 'python .migration/harness/tools/afs-mutation --all'` | `2782f48811001bc5` |  | gate=mutation score=0.869 threshold=0.8 killed=1126 survived=169 files=61 base=all |

Artifact import verification (not a gate-run row): the installed `afs-acceptance verify` command
exited 0 with `gate=acceptance-evidence status=verified` for commit
`7e3d6d5427064c67b951a29ac9f8cfabfa77e3db`, run `41924854967`, attempt `1`. The imported
`.migration/evidence/acceptance-runs/41924854967-1.json` and
`.migration/evidence/mutants/HR-04F.md` are byte-for-byte copies of the verified artifact files.
