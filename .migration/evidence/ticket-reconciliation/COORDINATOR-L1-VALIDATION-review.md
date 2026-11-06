# Coordinator review — handling-registration reconciliation (#113)

Ticket: `COORDINATOR-L1-VALIDATION` · issue [#194](https://github.com/martins-vds/ai-factory-pilot-target/issues/194)  
Role: `afs-slice-coordinator` · original baseline `a284b840e97e06452ca5370b941d22c4c6ae4f2d`; current main integrated at `93aaa937873ad948699ae9525bb57e03416d9339`
Installed harness pin: `e51998d716c229930e1e072cdcb05be0a872b4ef`
Review basis: complete local Git ancestry plus live GitHub issue, PR, Actions and comment state queried through GitHub MCP.

## Reconciliation result and boundary

The recursive scope is **21 descendants**: the nine direct children of #113 and 12 nested descendants under #129, #130 and #131. Those 21 issues have no deeper children. None has a `wayfinder:*` research/map label, so none is excluded by the installed `ticket_guard.descendants` filter. Research #173 is not among the descendants and is excluded. Live issue state shows 20 closed as completed and #160 closed as not planned; there are no open descendants. All 20 completed rows have a verified current landing witness. The superseded #160 failure PR is intentionally unmerged; its replacement #164 is completed and landed.

The actual ADR-0030 candidate is `.migration/evidence/ticket-reconciliation/113.yaml`. `git show origin/main:.migration/evidence/ticket-reconciliation/113.yaml` returned “path does not exist”: this is new branch evidence, not an artifact already landed on main. The role report intentionally records all descendants, their current dispositions, linked landing PRs and relevant existing returns. It does not rewrite issue states or returns.

The installed guard and return checker are **not verified as passing**. The earlier attempts in this ticket journal were against the pre-rollout harness and exited before reading the report because `gh api` had no authentication. The current worker still has no authenticated GitHub host (`gh --version` 2.103.2; `gh auth status` confirms this), so no current-pin checker retry was made. Do not treat GitHub MCP observations or this candidate report as execution of a passing installed check.

## Recursive issue and outcome review

| Issue | Parent | Current role outcome and attributable evidence |
|---|---:|---|
| #114 | #113 | HR-02 analyst return, PR #115 |
| #118 | #113 | HR-03 characterizer return, PR #119 |
| #123 | #113 | HR-04 planner return, PR #126 |
| #127 | #113 | Successful owning-role evidence only: HR-04A specialist return at PR #133. PR #137's verifier return remains `changes-required` for the stale quirk-draft link; it is recorded separately as nonpassing review evidence, not a successful witness |
| #128 | #113 | Successful owning-role evidence only: HR-04B specialist return at PR #134. PR #139's verifier return remains `changes-required` for the generated cost artifact; it is recorded separately as nonpassing review evidence, not a successful witness |
| #129 | #113 | HR-04C migrator return names #129/PR #154; final mutation score is 0.855. PR #148 was closed unmerged; its fix is included in #154. Nested verifier #158 passes in PR #159 |
| #130 | #113 | HR-04D specialist return names #130/PR #163; verifier #164 passes in PR #165 |
| #131 | #113 | Current HR-04E verifier return is issue #176/PR #177 and passes. The same-path predecessor at `1c8716c7afe972c60b750b36aca91ffa80597a79` names #131/PR #169 and preserves its earlier `changes-required` verdict. PRs #167, #169 and #175 are in the landed work chain |
| #132 | #113 | HR-04F Auditor return is `complete`, PR #184; this records the historic acceptance and is not new acceptance work here |
| #143 | #129 | Current HR-04C verifier return #158/PR #159 passes; history preserves the initial #143 review and its zero-padded-year finding |
| #147 | #129 | Child-work PR #148 is closed-unmerged, but its exact head `5356b3e386ad16bf1bc577ec1c1b4228b15dbea2` is an ancestor of main and changes the HR-04C migrator return path. Current passing parent return #129 is in owning PR #154; both PRs are cited |
| #149 | #130 | Child-work PR #150 changes the HR-04D specialist return path and closes #149. Current passing parent return #130 is in owning PR #163; both PRs are cited |
| #155 | #129 | Child-work PR #156 changes the HR-04C migrator return path and closes #155. Current passing parent return #129 is in owning PR #154; both PRs are cited |
| #158 | #129 | Current HR-04C verifier return names #158/PR #159 and passes |
| #160 | #130 | Closed `not_planned`; failed verifier PR #161 is closed unmerged (head `813a215ac3f0fccf1d12916978ef176b6023f365`) and its exact verifier snapshot says `changes-required` but names parent #130, not child #160. Replacement #164 is re-verified in PR #165, whose passing parent-work return also names #130 |
| #162 | #130 | PR #163 closes #162, changes the HR-04D specialist return path and owns the current passing parent #130 return; it provides both child-work and current-owner evidence |
| #164 | #130 | PR #165 closes #164, changes the HR-04D verifier return path and owns the current passing parent #130 verifier return |
| #168 | #131 | Child-work PR #169 closes #168 and changes the HR-04E verifier return path; correction PR #175 and current passing verifier PR #177 complete the lineage. The same-path predecessor #131 at `1c8716c7afe972c60b750b36aca91ffa80597a79` and current issue #176 remain distinct |
| #174 | #131 | HR-04E-FIX specialist return names #174/PR #175 |
| #176 | #131 | Current HR-04E verifier return names #176/PR #177 and passes |
| #178 | #131 | HR-04E-HARNESS bootstrapper return names #178/PR #179; normal rollout #188/#193 subsequently landed on main |

PR states and issue-to-PR relationships were cross-checked against live GitHub records; full target ancestry is available. Current `origin/main` is `93aaa937873ad948699ae9525bb57e03416d9339`, tree `cd4d20aab1ec49808d5c2d5ca75c2e6078c1354c`. PR #161 remains deliberately unmerged. For #147/#149/#155/#162/#164/#168, the candidate now cites the exact child-work PR and current owning/correction PR, and lists the actual same-path parent return. I verified the relevant issue-parent relationships, child closure references, return-path changes in child PRs, current return snapshots/outcomes, and owner PR landings. The installed parent-continuation rule now supports these qualified parent returns; these are not represented as child-owned return files. PR #148 is specifically closed-unmerged, but its exact head is present in main ancestry, so it is not misclassified as unlanded. #160's failed #161 snapshot is retained with its true #130 attribution and replacement #164; #161 itself is not represented as landed.

The installed guard's current validation also requires a passing role outcome for every returned role listed on a completed disposition. Accordingly, the candidate no longer lists #127/#128 verifier returns as successful witnesses; their exact failed results remain under `observed_nonpassing_reviews`. The successful owning-role returns for those parent work tickets remain cited. The slice Auditor later records no established capability gap, but that historical acceptance does not erase verifier findings or prove the recursive guard will accept the candidate report.

## Historical acceptance, graph/ledger and human sign-off

These are immutable prior acceptance evidence, not newly executed gates in this role:

- GitHub Actions run [41924854967, attempt 1](https://github.com/martins-vds/ai-factory-pilot-target/actions/runs/41924854967) is `workflow_dispatch`, `completed/success`, on `main` at exact SHA `7e3d6d5427064c67b951a29ac9f8cfabfa77e3db`. That revision is an ancestor of current `origin/main`.
- Artifact ID `13371474656`, named `afs-acceptance-7e3d6d5427064c67b951a29ac9f8cfabfa77e3db-41924854967-1`, has API-reported ZIP SHA-256 `1f023eab634c89321869c3aec907c59428222746466010356dfacde3501dd60b` and was unexpired when inspected. The committed HR-04F result/acceptance report records 15/15 planned steps, 321 tests, CRAP max 19.0 (threshold 30), and `afs-mutation --all` 0.869 (threshold 0.8; 1126 killed, 169 survived, 61 files, `base=all`). No run was invented or repeated.
- PR #184's final Auditor return/report records 19 capabilities and no established capability gaps or graph inconsistencies. The preserved graph review says source/target freshness and flow checks passed; the target graph had 374 nodes, 929 edges, five owned and zero unowned entry points. This review reads those historical artifacts only; it does not rebuild graphs or re-audit the ledger.
- Human sign-off is comment [6645381666](https://github.com/martins-vds/ai-factory-pilot-target/pull/184#issuecomment-6645381666), created `2026-11-04T23:45:44Z`. The operator explicitly attested “I completed the human flow check and sign off” for reviewed revision `7e3d6d5427064c67b951a29ac9f8cfabfa77e3db`. The timestamp is the attestation record time, not an invented test execution time; no screenshots or step-by-step manual record were supplied.

After the normal merge of current main, installed integrity passed: harness `e51998d716c229930e1e072cdcb05be0a872b4ef`, 77 entries, 388 files, zero problems. Migration-state validation passed with 98 files and zero errors; the setup probe passed through this ticket's afs-run journal. Python 3.13.17, db service health, input checks, and source pin/read-only checks passed. The post-merge AFS workflow #42158375241 on exact main `93aaa937873ad948699ae9525bb57e03416d9339` completed successfully; its gate job reported 323 tests, CRAP max 19.0, and no mutable code changed for mutation. This is rollout/main CI evidence, not a coordinator checker result or a substitute for historical accepted epic evidence.

## Parent-run checker findings and blockers

The parent's unchanged installed commands were run on an earlier candidate head `543a9b0d9378571216f609da8deccab7aa7d4438` with the prior harness pin `ee54dfdda8d86b324fa2818aa82c6b5b6456dbd1`. This is **parent execution**, not a coordinator-role run, and has not been added to this role's afs-run journal:

- `ticket_guard.py --reconcile-epic 113`: 21 tickets, 16 reconciliation failures on that earlier candidate and installation.
- `check_slice_returns.py --epic 113`: 21 tickets, 6 return failures on that earlier candidate and installation.
- Parent attribution/review: https://github.com/martins-vds/ai-factory-pilot-target/pull/195#issuecomment-6671481341.

These counts are preserved solely as historical parent results; they do not establish outcomes for the current candidate or installed source repair.

## Blockers and frontier

1. The local GitHub CLI remains unauthenticated. The current installed checker needs `gh api`, and no current-pin checker was run in this session. Parent-owned authorized execution of both read-only commands is needed against the final committed head; those parent results must remain outside this role's journal.
2. The six qualified continuation returns are now represented using the installed parent-ticket rule and genuine current snapshots. The candidate is not yet validated by the installed checker because of the CLI access block; do not infer a pass from local/MCP provenance review alone.
3. #127 and #128's `changes-required` verifier outcomes remain preserved under `observed_nonpassing_reviews`, not passing witnesses. Their successful owning specialist returns and landings remain cited. This is historical review context, not a current checker blocker by itself.
4. The post-merge AFS run and installed integrity/setup checks do not constitute L1 role validation. The actual historical acceptance and human sign-off remain unchanged; no new acceptance work or application dispatch occurred.

Do not rerun full acceptance or mutation, change issue state, dispatch implementation, rebuild graphs, edit pinned tools/schemas, act on research #173, or merge. Do not copy parent guard executions into this role journal. On the exact final commit, an authorized parent should run only the installed read-only reconciliation and slice-return commands without `--reopen`; this role remains blocked until it independently interprets those exact-head results.
