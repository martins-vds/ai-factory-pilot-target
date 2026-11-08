
## Handoff — afs-auditor · 2026-11-08T01:38:48Z
**State:** blocked  ·  **Branch / PR:** copilot/dm-audit-gate-7-data-migration  ·  **Last commit:** 1cc2d63
### Done
- See this branch's commits and `afs-run` journal.
### Remaining
- [ ] You changed another role's or ticket's return file: `.migration/returns/BK-05F.afs-specialist-migrator.yaml`. A session writes only its own return (`.migration/returns/DM-AUDIT.afs-auditor.yaml`). Restore each one exactly as it was on your base branch (`git checkout <base> -- <file>`) and commit.
### Blockers / questions
- self-check failed: `afs-finish-check` still found 1 problem(s) after its retry budget (ADR-0034). Written by the stop hook, not by the agent.
### Next step for the next session
Fix the items under Remaining, run `afs-finish-check`, and commit. Scope items need the operator.
