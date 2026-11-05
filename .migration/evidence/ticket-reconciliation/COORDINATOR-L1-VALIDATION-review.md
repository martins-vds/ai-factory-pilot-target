# Coordinator review — handling-registration reconciliation (#113)

Ticket: `COORDINATOR-L1-VALIDATION` · issue [#194](https://github.com/martins-vds/ai-factory-pilot-target/issues/194)  
Role: `afs-slice-coordinator` · base `origin/main` / baseline `a284b840e97e06452ca5370b941d22c4c6ae4f2d`  
Installed harness pin: `ee54dfdda8d86b324fa2818aa82c6b5b6456dbd1`
Review basis: complete local Git ancestry plus live GitHub issue, PR, Actions and comment state queried through GitHub MCP.

## Reconciliation result and boundary

The recursive scope is **21 descendants**: the nine direct children of #113 and 12 nested descendants under #129, #130 and #131. Those 21 issues have no deeper children. None has a `wayfinder:*` research/map label, so none is excluded by the installed `ticket_guard.descendants` filter. Research #173 is not among the descendants and is excluded. Live issue state shows 20 closed as completed and #160 closed as not planned; there are no open descendants.

The actual ADR-0030 candidate is `.migration/evidence/ticket-reconciliation/113.yaml`. `git show origin/main:.migration/evidence/ticket-reconciliation/113.yaml` returned “path does not exist”: this is new branch evidence, not an artifact already landed on main. The role report intentionally records all descendants, their current dispositions, linked landing PRs and relevant existing returns. It does not rewrite issue states or returns.

The installed guard and return checker are **not verified as passing**. The first setup block was resolved by full-history fetch and correcting only this role's quoted scalar; see the continuation correction in `COORDINATOR-L1-VALIDATION.md`. Both required installed commands were run once through this ticket's journal, without `--reopen`; each exited 1 at its first `gh api repos/martins-vds/ai-factory-pilot-target/issues/113` call because the environment lacks `GH_TOKEN`. `gh --version` is `2.103.2`; `gh auth status` confirms no logged-in host. See the run journal and handoff for exact log paths. Do not treat GitHub MCP observations or this candidate report as execution of a passing installed check.

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
| #147 | #129 | Child-work PR #148 is closed unmerged. The actual landed correction is in current owning PR #154; its HR-04C migrator return names parent #129. No same-path return names #147 |
| #149 | #130 | Child-work PR #150 is carried into current owning PR #163. The current HR-04D specialist return at #163 names parent #130, not child #149 |
| #155 | #129 | Child-work PR #156 is carried into current owning PR #154. The current HR-04C migrator return at #154 names parent #129, not child #155 |
| #158 | #129 | Current HR-04C verifier return names #158/PR #159 and passes |
| #160 | #130 | Closed `not_planned`; failed verifier PR #161 is closed unmerged (head `813a215ac3f0fccf1d12916978ef176b6023f365`) and its exact verifier snapshot says `changes-required` but names parent #130, not child #160. Replacement #164 is re-verified in PR #165, whose passing parent-work return also names #130 |
| #162 | #130 | Child fix PR #163 addresses the verifier findings and is the current owning correction PR; the HR-04D specialist return in it names #130, not child #162 |
| #164 | #130 | Child re-verification PR #165 passes the revised work; the HR-04D verifier return in it names #130, not child #164 |
| #168 | #131 | Child-work PR #169 corrects parent HR-04E/#131 verification. Current fix PR #175 and verifier PR #177 carry the final result. Same-path history preserves #131 at `1c8716c7afe972c60b750b36aca91ffa80597a79` then current #176; no return names child #168 |
| #174 | #131 | HR-04E-FIX specialist return names #174/PR #175 |
| #176 | #131 | Current HR-04E verifier return names #176/PR #177 and passes |
| #178 | #131 | HR-04E-HARNESS bootstrapper return names #178/PR #179; normal rollout #188/#193 subsequently landed on main |

PR states and issue-to-PR relationships were cross-checked against live GitHub records. Complete target history is available after `git fetch --unshallow origin`; current `origin/main` is baseline `a284b840e97e06452ca5370b941d22c4c6ae4f2d`. PR #161 is deliberately not merged. For #147/#149/#155/#162/#164/#168, the current report now cites the exact child-work PR plus its owning/correction PR and the actual same-path parent ticket/role return identity. Those parent returns are not passed off as child returns: candidate `returns` is empty for these six child rows because the installed checker requires exact child attribution and no such return exists. #160's exact failed PR-head snapshot likewise names #130 rather than #160; its replacement is accurately identified, but no child-attributed failure return is invented.

The installed guard's current validation also requires a passing role outcome for every returned role listed on a completed disposition. Accordingly, the candidate no longer lists #127/#128 verifier returns as successful witnesses; their exact failed results remain under `observed_nonpassing_reviews`. The successful owning-role returns for those parent work tickets remain cited. The slice Auditor later records no established capability gap, but that historical acceptance does not erase verifier findings or prove the recursive guard will accept the candidate report.

## Historical acceptance, graph/ledger and human sign-off

These are immutable prior acceptance evidence, not newly executed gates in this role:

- GitHub Actions run [41924854967, attempt 1](https://github.com/martins-vds/ai-factory-pilot-target/actions/runs/41924854967) is `workflow_dispatch`, `completed/success`, on `main` at exact SHA `7e3d6d5427064c67b951a29ac9f8cfabfa77e3db`. That revision is an ancestor of current `origin/main`.
- Artifact ID `13371474656`, named `afs-acceptance-7e3d6d5427064c67b951a29ac9f8cfabfa77e3db-41924854967-1`, has API-reported ZIP SHA-256 `1f023eab634c89321869c3aec907c59428222746466010356dfacde3501dd60b` and was unexpired when inspected. The committed HR-04F result/acceptance report records 15/15 planned steps, 321 tests, CRAP max 19.0 (threshold 30), and `afs-mutation --all` 0.869 (threshold 0.8; 1126 killed, 169 survived, 61 files, `base=all`). No run was invented or repeated.
- PR #184's final Auditor return/report records 19 capabilities and no established capability gaps or graph inconsistencies. The preserved graph review says source/target freshness and flow checks passed; the target graph had 374 nodes, 929 edges, five owned and zero unowned entry points. This review reads those historical artifacts only; it does not rebuild graphs or re-audit the ledger.
- Human sign-off is comment [6645381666](https://github.com/martins-vds/ai-factory-pilot-target/pull/184#issuecomment-6645381666), created `2026-11-04T23:45:44Z`. The operator explicitly attested “I completed the human flow check and sign off” for reviewed revision `7e3d6d5427064c67b951a29ac9f8cfabfa77e3db`. The timestamp is the attestation record time, not an invented test execution time; no screenshots or step-by-step manual record were supplied.

The installed setup validator was newly observed passing after the history and return correction: 94 files, zero errors, in `.migration/evidence/runs/COORDINATOR-L1-VALIDATION.md`. Candidate YAML parses with 21 unique issue numbers and passed migration-state validation. The separately journaled afs-run setup probe also passed. Those checks do not substitute for the historical acceptance or the failed live reconciliation CLI result.

## Parent-run checker findings and blockers

The parent ran the unchanged installed commands against this exact candidate with its already-authorized CLI. This is **parent execution**, not a coordinator-role run, and has not been added to this role's afs-run journal:

- `ticket_guard.py --reconcile-epic 113`: 21 tickets, 16 reconciliation failures.
- `check_slice_returns.py --epic 113`: 21 tickets, 6 return failures.
- Parent attribution/review: https://github.com/martins-vds/ai-factory-pilot-target/pull/195#issuecomment-6671481341.

The local role did not repeat these commands: its prior unauthenticated attempts remain separately recorded in the existing journal. The candidate corrects known witness/provenance misstatements but intentionally does not claim that these parent-run failures are resolved.

## Blockers and frontier

1. The local GitHub CLI is not authenticated (`gh auth status` reports no logged-in host). Prior local checker attempts exited before report validation. No auth retry is performed in this bounded provenance session.
2. The source-side inconsistencies isolated by the parent remain real: `handoff: none` is interpreted as both a blocker for successful Migrators and an explicit failed outcome; valid reasoned mutation `n/a` is rejected; and the recursive checkers do not reconcile parent-owned continuation returns to child issues. Harness source work is tracked in ai-factory-swarm#79/#80; setup/example corrections in #78 are unmerged and not installed. Do not copy source proposals or relax this target report to simulate success.
3. Six child continuation rows and the #160 failure record lack exact child-attributed role-return snapshots. The candidate names genuine work/correction PRs and actual parent return identity but leaves child returns absent; parent checker outcomes remain 16 reconciliation and 6 return failures. Independent review and the approved normal pinned rollout are still required.
4. #127 and #128's `changes-required` verifier outcomes remain intact as failed-review context, not passing witnesses. Their actual owning specialist returns and landings remain cited; no new application work is dispatched.

Do not rerun full acceptance or mutation, change issue state, dispatch implementation, rebuild graphs, edit pinned tools/schemas, act on research #173, or merge. Any source-side reusable reconciliation/setup defects should be handled in harness source, not hotpatched into this pilot.
