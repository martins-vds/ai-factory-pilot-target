# Program Orchestrator validation — issue #196

Ticket: `COORDINATOR-L0-VALIDATION`  
Role: `afs-program-orchestrator`  
Owning proposal: [PR #201](https://github.com/martins-vds/ai-factory-pilot-target/pull/201)  
Assessment baseline: target `main` `b62f324bb095f2554e4ef0a051ce256d0462af64`, tree `114eca66d75d559ba3c48eb6c65ef7235b76153a`. The task checkout began at `bd2a87b398f3b34d2ad449806af741213b5f53ad`, whose parent is that main commit and whose tree is identical.

## Setup and evidence boundary

Loaded the migration contract and completed the Program Orchestrator setup checks. Target history is complete (`git rev-parse --is-shallow-repository` → `false`); migration validation reported 98 files and zero errors; ticket inputs reported three named local paths and zero missing; RTK is 1.1.0; Python is 3.13.17; installed-harness integrity reports pin `e51998d716c229930e1e072cdcb05be0a872b4ef`, 77 entries, 388 files and zero problems. The role's own `setup-probe` passed and is recorded in [the own journal](runs/COORDINATOR-L0-VALIDATION.md). Source checks and service health checks were skipped as directed for this non-source-reading, non-test-running role.

The assessment used landed target artifacts and live GitHub issue, PR and Actions records. Historical `.migration/returns/HR-00.afs-program-orchestrator.yaml` is coordinator-authored schema evidence, not proof this role ran; it and all inherited returns, cost records, journals and evidence remain unchanged. This session did not use a parent-written substitute for this role or copy an authenticated parent guard execution into its journal. The application's source remains pinned at `f3beacf78de4f6d34edc4971ac87e38a5c6fe59d`; source checks were skipped for this role. [The own return](../returns/COORDINATOR-L0-VALIDATION.afs-program-orchestrator.yaml) records this role's phase and decisions.

## L1 outcome and landing proof

The same real Slice Coordinator assigned issue #194 / ticket `COORDINATOR-L1-VALIDATION`, returned its evidence in PR #195, and was independently reviewed and merged by the parent at 04:32:19Z. PR #195's final role head was `66269186372dfb8557a2c12208e9b4d9236e4260`; its merged content is present on the assessed main commit. The landed [L1 return](../returns/COORDINATOR-L1-VALIDATION.afs-slice-coordinator.yaml), [machine reconciliation](ticket-reconciliation/113.yaml), [role review](ticket-reconciliation/COORDINATOR-L1-VALIDATION-review.md), [own journal](runs/COORDINATOR-L1-VALIDATION.md), and [chronological handoff](../handoffs/COORDINATOR-L1-VALIDATION.md) show 21 recursive descendants: 20 completed landings, one superseded disposition, zero open descendants, and no remaining ticket blocker. Superseded and earlier nonpassing verifier history remain explicit in the machine reconciliation and review.

The L1 worker's GitHub CLI was unauthenticated. Its own guard attempts failed before reading the report; the role did not present them as passes. After its explicit handoff, the parent ran the two unchanged installed read-only guards against candidate `f52f560dab700b73fba0c09c8da210c34bda7948` with installed pin `e51998d716c229930e1e072cdcb05be0a872b4ef`. Both parent executions ended with 21 tickets and zero failures. Their full outputs, hashes and attribution are preserved in [parent review comment 6676715139](https://github.com/martins-vds/ai-factory-pilot-target/pull/195#issuecomment-6676715139) and the landed L1 role review; they are not this L0 session's executions. Historical parent results of 21/16 and 21/6 failures at the older commit/pin remain historical and unaltered. This L0 session did not perform the earlier L1 dispatch.

The required post-merge check was run on current main: AFS harness run [42163100368](https://github.com/martins-vds/ai-factory-pilot-target/actions/runs/42163100368) completed successfully at `b62f324bb095f2554e4ef0a051ce256d0462af64`. All applicable checks passed, including current graph validation. The gate job reports 323 tests passed and CRAP maximum 19 against threshold 30; mutation is `n/a: no mutable code changed`. Separate ticket-guard workflow [42163104512](https://github.com/martins-vds/ai-factory-pilot-target/actions/runs/42163104512) also succeeded. These are current CI checks, not a new acceptance or full-mutation run.

Two earlier PR-triggered AFS runs on the L1 final head, [42163078708](https://github.com/martins-vds/ai-factory-pilot-target/actions/runs/42163078708) and [42163095548](https://github.com/martins-vds/ai-factory-pilot-target/actions/runs/42163095548), failed in the return-contract job because `origin/main` had advanced beyond the event's expected base `93aaa937873ad948699ae9525bb57e03416d9339`. Their logs preserve that exact base-mismatch diagnostic. The later exact-main post-merge run above passed; the earlier failures are not erased or described as passing. No new reusable harness defect was established by this L0 review.

## Program phase and remaining frontier

The accepted handling-registration slice #113 completed through Phase 6. Its generated fog re-walk #189 is closed; the decision map #3 is open with no remaining “Not yet specified” entries. The program is between slices. The next unstarted frontier is **Phase 4 planning** for the three open `wayfinder:task` issues #99 (admin live map), #101 (handling-event file upload), and #112 (mobile event logger). They are legitimate future work, not stale tickets or current `afs:slice` epics. This review dispatched no Planner, worker or application work.

The map has concrete decisions for these tasks; the applicable next human gate is to prioritize/authorize a future slice plan and approve it before its tickets are published. The map and its remaining tasks may stay open. The only other open program issue outside this bounded work is research #172 with draft PR #173; both remain excluded and untouched.

Current `.migration/capabilities.yaml` lists required capabilities as `met` or `not-applicable`. Stored source and target graph artifacts pass their historical graph gates; the post-merge current-main workflow also passed its graph checks. This is readiness evidence, not a graph rebuild or a new claim of whole-project coverage. The installed harness repairs are confirmed landed: source PRs #78 and #81 are merged in martins-vds/ai-factory-swarm, and normal target rollout PR #198 is merged with the approved `e51998d716c229930e1e072cdcb05be0a872b4ef` pin. No repair is merely proposed or locally hotpatched. This consumed rollout approval grants no authority for future merges; the parent must independently review this role-evidence proposal and current CI.

## Historical acceptance and human sign-off

Issue #113 remains accepted. Its closure and the merged Auditor PR #184 support that status. The historical acceptance workflow [41924854967, attempt 1](https://github.com/martins-vds/ai-factory-pilot-target/actions/runs/41924854967) is independently confirmed as a successful `workflow_dispatch` on exact commit `7e3d6d5427064c67b951a29ac9f8cfabfa77e3db`. Its existing artifact is ID `13371474656` with Actions-reported digest `sha256:1f023eab634c89321869c3aec907c59428222746466010356dfacde3501dd60b`; the committed acceptance result records 15/15 planned steps, 321 tests, CRAP max 19/30, and full mutation score 0.869/0.8. The historical Auditor return records 19 capabilities and no established gaps.

The genuine human attestation is [PR #184 comment 6645381666](https://github.com/martins-vds/ai-factory-pilot-target/pull/184#issuecomment-6645381666), where the operator said, “I completed the human flow check and sign off” for reviewed revision `7e3d6d5427064c67b951a29ac9f8cfabfa77e3db`. Its creation time is the attestation timestamp, not an asserted execution time. The human performed that check; this role did not. The historical acceptance, mutation score and sign-off do not establish whole-application acceptance or authorize future slice work.

## Decisions and next step

- Keep #113 accepted and #189 closed; preserve their reports, return files, human sign-off and historical acceptance artifact unchanged.
- Keep #3, #99, #101 and #112 open until future planning and human approvals justify further work.
- Keep #172 / draft PR #173 excluded.
- No application code, worker or slice/Planner dispatch, issue closure/reopening, graph rebuild, acceptance or mutation rerun, profile/capability/threshold change, research action, inherited-output rewrite, or merge occurred.
- `dispatched` is empty for this L0 execution. PR #195's earlier L1 dispatch belonged to the parent; it is not attributed to this session.
- No blocking handoff is needed. The parent must still independently review this role's own finished exact-head evidence and current CI before deciding the role-evidence-only merge. This role does not self-merge.
