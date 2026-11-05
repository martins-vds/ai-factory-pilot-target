# Run journal: HARNESS-ROBUSTNESS

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-05T18:54:39+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-05T18:56:37+00:00 | pinned-normal-bootstrap | 1 | 20.54 | `python /tmp/afs-harness-ee54dfdda8d86b324fa2818aa82c6b5b6456dbd1/tools/bootstrap.py --target /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target --profile /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.migration/profile.yaml --capabilities /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.migration/capabilities.yaml --stack-pack /tmp/afs-harness-e` | `90785a0267781dd5` | Traceback (most recent call last): |  |
| 2026-11-05T18:58:54+00:00 | migration-state-validation | 0 | 0.85 | `python .migration/harness/tools/validate.py .migration` | `c784e0bf7a2d7bdb` |  |  |
| 2026-11-05T18:59:15+00:00 | final-state-validation | 0 | 0.82 | `python .migration/harness/tools/validate.py .migration` | `c784e0bf7a2d7bdb` |  |  |
| 2026-11-05T19:06:06+00:00 | coordinator-pinned-bootstrap | 0 | 86.75 | `python3 ../harness75-approved-source/tools/bootstrap.py --target . --profile .migration/profile.yaml --capabilities .migration/capabilities.yaml --stack-pack ../harness75-approved-source/stacks/java-to-django.json --create-gap-issues` | `3cf68dfe01025a9d` |  |  |
| 2026-11-05T19:06:23+00:00 | coordinator-install-integrity | 0 | 0.06 | `python3 .migration/harness/tools/check_installed.py` | `84be7e50875f2269` |  |  |
| 2026-11-05T19:06:24+00:00 | coordinator-installed-state | 1 | 0.72 | `python3 .migration/harness/tools/validate.py .migration` | `d1cb431a977bc0f6` | 92 file(s) checked, 2 error(s) |  |
| 2026-11-05T19:07:48+00:00 | coordinator-source-preservation | 1 | 0.42 | `python3 ../verify-pilot193-install.py` | `582049862d083df8` | Traceback (most recent call last): |  |
| 2026-11-05T19:08:01+00:00 | coordinator-source-preservation | 0 | 0.1 | `python3 ../verify-pilot193-install.py` | `4fd7dfbb93c3bdb4` |  |  |
| 2026-11-05T19:08:02+00:00 | coordinator-committed-state | 0 | 0.76 | `python3 .migration/harness/tools/validate.py .migration` | `c784e0bf7a2d7bdb` |  |  |
| 2026-11-05T19:09:28+00:00 | coordinator-final-preservation | 0 | 0.1 | `python3 ../verify-pilot193-install.py` | `4fd7dfbb93c3bdb4` |  |  |
| 2026-11-05T19:09:28+00:00 | coordinator-final-state | 0 | 0.68 | `python3 .migration/harness/tools/validate.py .migration` | `c784e0bf7a2d7bdb` |  |  |
| 2026-11-05T19:11:42+00:00 | resumed-setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-05T19:14:00+00:00 | exact-source-parity-preservation | 1 | 0.33 | `python /tmp/afs-verify-harness-robustness.py` | `d458de7c60e927a6` | FAIL: protected path changed under .migration/costs: .migration/costs/b1766ace-e367-413a-aecc-b040f1de7349.json |  |
| 2026-11-05T19:14:13+00:00 | exact-source-parity-preservation-recheck | 0 | 0.61 | `python /tmp/afs-verify-harness-robustness.py` | `604a11245a1a04de` |  |  |
| 2026-11-05T19:14:23+00:00 | independent-postinstall-gates | 0 | 0.92 | `bash -c 'python .migration/harness/tools/check_installed.py && python .migration/harness/tools/validate.py .migration && python .migration/harness/tools/check_runtime.py && python .migration/harness/tools/check_graph_fresh.py --require source,target && python .migration/harness/tools/graph_gate.py --side source --require-graph && python .migration/harness/tools/graph_gate.py --side target --requir` | `707ea2ae91362278` |  | gate=graph side=target verdict=pass failures=0 entry_points=7 reaching_data=3 enriched_edges=510 |
| 2026-11-05T19:14:39+00:00 | reviewed-attribution-regressions | 0 | 10.17 | `python -c 'import sys,unittest; sys.path.insert(0,"/tmp/afs-harness-resume/tests"); import test_return_contract, test_ticket_guard, test_check_slice_returns; suite=unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromModule(m) for m in (test_return_contract,test_ticket_guard,test_check_slice_returns)]); result=unittest.TextTestRunner(verbosity=2).run(suite); sys.exit(not result.wasSuccessfu` | `4a630de431116a36` |  |  |
| 2026-11-05T19:15:01+00:00 | protected-input-tree-audit | 0 | 0.62 | `python /tmp/afs-verify-harness-robustness.py` | `860f314ca6168e90` |  |  |
| 2026-11-05T19:15:17+00:00 | coordinator-baseline-preservation | 0 | 0.62 | `python /tmp/afs-verify-harness-robustness.py` | `a1408a93ef93fbc3` |  |  |
| 2026-11-05T19:15:31+00:00 | coordinator-baseline-preservation-count | 0 | 0.62 | `python /tmp/afs-verify-harness-robustness.py` | `213393e01370ccd5` |  |  |
