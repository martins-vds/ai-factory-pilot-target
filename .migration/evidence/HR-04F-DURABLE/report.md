# HR-04F-DURABLE — pinned acceptance harness rollout

- Issue: [martins-vds/ai-factory-pilot-target#185](https://github.com/martins-vds/ai-factory-pilot-target/issues/185)
- Acceptance issue: [martins-vds/ai-factory-pilot-target#132](https://github.com/martins-vds/ai-factory-pilot-target/issues/132)
- Setup PR: [#186](https://github.com/martins-vds/ai-factory-pilot-target/pull/186)
- Requested pilot main: `5cace249987e3ddd4ce3345a845168ca545bab55`
- Requested harness pin: `344241e92256a6048183f99063ca297fb96780de`
- Outcome: **blocked** — the public harness checkout was acquired and verified at the requested clean pin, but normal bootstrap could not fetch a pinned skill dependency without GitHub credentials.

## Evidence

The committed journal at `../runs/HR-04F-DURABLE.md` contains each command, exit code and log fingerprint.

| Check | Result |
|---|---|
| Named pilot inputs | Pass — source lock, existing profile, and capability checklist all exist. |
| Public harness acquisition and preflight | Pass — fresh clone at `/tmp/afs-HR-04F-DURABLE.E63zhQ/harness`; `HEAD=344241e92256a6048183f99063ca297fb96780de`, clean worktree, `tools/bootstrap.py` and `stacks/java-to-django.json` present. See run `clone-and-pin-harness`. |
| Normal pinned bootstrap | **Blocked** — exit 1 while fetching skill source `martins-vds/code-migration-hackathon` at `4de661a9a830aaef70ff55e879c0cc540599cad8`. See run `bootstrap`. The bootstrap traceback reports Git exit 128. |
| Exact dependency fetch diagnostic | **Blocked** — recorded fetch command exited 128 with `fatal: unable to get password from user`. See run `dependency-fetch-diagnostic`. No credentials were copied or supplied, and the dependency was not skipped. |
| Partial bootstrap rollback | Pass — bootstrap's partial `.github/skills/` changes were restored to requested pilot main. The post-failure installed integrity check passes: existing pin `9b805e17624c50d1e74cb008b3f1b0454c1be177`, 77 entries / 387 files, zero problems. |
| Migration-state validation | Pass — final post-rollback validation checked 86 files, zero errors (run `refreshed-output-validation`). |
| Protected input and prior-output preservation | Pass — final `git diff --exit-code` against requested main found no changes to application/test/characterization files, profile, source lock, capabilities, slices, graphs, ledger, `.github/skills/`, prior returns, prior costs, or prior HR-04F-HARNESS evidence/journals. The check excludes only this session's expected cost record and this ticket's own journal. |
| Source graph flow | Pass — 0 failures; 27 entry points, 18 reaching data. |
| Target graph flow | Pass — 0 failures; 7 entry points, 3 reaching data. |
| Both graph freshness | Pass — source and target graphs fresh. No graph was edited or rebuilt. |
| Requested acceptance installation | **Not installed** — current manifest pin is `9b805e17624c50d1e74cb008b3f1b0454c1be177`; requested pin check, executable `afs-acceptance` check, and `afs-acceptance.yml` existence check all fail. |

The clean public harness checkout was used with the existing profile, capability checklist, and Java-to-Django stack pack through the normal bootstrap command. Bootstrap stopped at its pinned skill dependency fetch; no retry with alternate credentials, dependency skip, or hand-edit of generated files was used. Consequently, the generated workflow's profile-derived Python, manual-only/read-only behavior, timeout, and failure/cancellation artifact upload cannot be verified.

An earlier workspace-location probe returned no checkout, but was not treated as an access failure; the later public clone and exact-pin preflight succeeded. An initial preservation command also included this session's newly generated cost record and failed; the corrected preservation check excluding only that expected record passed.

The initial CI run [41916185215](https://github.com/martins-vds/ai-factory-pilot-target/actions/runs/41916185215) failed only because the plan-only commit did not yet contain the required return file. Its logs show migration-state, graph and changed-code gates passed. This return is added in the blocked handoff.

## Scope and acceptance boundary

No application, tests, templates, thresholds, source lock, capability decisions, slices, graphs, ledger, other-role returns, prior journals, or cost records were changed. No acceptance workflow was dispatched, no full mutation run was started, and no slice acceptance or human flow signoff is claimed.

## Next step

Provide approved GitHub access for fetching the pinned `martins-vds/code-migration-hackathon` dependency at `4de661a9a830aaef70ff55e879c0cc540599cad8`, or make that exact pinned input fetchable without credentials. Then rerun normal bootstrap from the already verified clean harness checkout and complete the generated-installation checks. Do not merge without separate named approval.
