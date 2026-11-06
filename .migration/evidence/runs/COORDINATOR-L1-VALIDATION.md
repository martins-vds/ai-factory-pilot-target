# Run journal: COORDINATOR-L1-VALIDATION

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-05T22:08:36+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-05T22:22:06+00:00 | setup-migration-validate | 0 | 0.91 | `python .migration/harness/tools/validate.py .migration` | `ee0d254997a7a3b1` |  |  |
| 2026-11-05T22:31:23+00:00 | candidate-report-validate | 0 | 0.91 | `python .migration/harness/tools/validate.py .migration` | `ee0d254997a7a3b1` |  |  |
| 2026-11-05T22:31:44+00:00 | installed-ticket-reconciliation | 1 | 0.09 | `python .migration/harness/tools/ticket_guard.py --repo martins-vds/ai-factory-pilot-target --reconcile-epic 113` | `af95a491efd07594` |  |  |
| 2026-11-05T22:31:44+00:00 | slice-return-check | 1 | 0.23 | `python .migration/harness/tools/check_slice_returns.py --repo martins-vds/ai-factory-pilot-target --epic 113` | `38a0c2f8af9c6c5f` |  |  |
| 2026-11-05T22:32:29+00:00 | final-migration-validate | 0 | 0.91 | `python .migration/harness/tools/validate.py .migration` | `ee0d254997a7a3b1` |  |  |
| 2026-11-05T23:17:20+00:00 | continuation-setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-05T23:18:04+00:00 | resumed-setup-validate | 0 | 0.64 | `python .migration/harness/tools/validate.py .migration` | `ee0d254997a7a3b1` |  |  |
| 2026-11-05T23:20:28+00:00 | final-provenance-validate | 0 | 0.66 | `python .migration/harness/tools/validate.py .migration` | `ee0d254997a7a3b1` |  |  |
| 2026-11-05T23:20:48+00:00 | final-provenance-validate-2 | 0 | 0.64 | `python .migration/harness/tools/validate.py .migration` | `ee0d254997a7a3b1` |  |  |
| 2026-11-06T03:51:53+00:00 | resumed-main-setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-06T03:57:05+00:00 | resumed-current-main-validation | 0 | 0.87 | `python .migration/harness/tools/validate.py .migration` | `b892cfd2b0409c47` |  |  |
| 2026-11-06T03:57:37+00:00 | final-candidate-validation | 0 | 0.88 | `python .migration/harness/tools/validate.py .migration` | `b892cfd2b0409c47` |  |  |
