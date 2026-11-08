# BK-05G Scope Extension Handoff

## Handoff — afs-handoff · 2026-11-08T00:31:25Z

**Issue:** #401 – Operator scope extension authorization

## Authorization

Issue #401 (Operator scope extension, 2026-11-07):
> **Operator scope extension (2026-11-07):**
> AFS-SCOPE: templates/booking/dashboard/not_routed_table.html
>
> Change that template only to open the dialogs; keep BK-05E's table behaviour and tests green.

## Rationale

The destination and deadline dialogs cannot function without buttons to open them. The not-routed table is the required integration point per plan line 94. Destination and deadline dialogs must launch from the not-routed table's respective cells per BK-05G specification.

## Changes

- Added HTMX dialog-open buttons to destination and deadline columns
- Preserved all route-specification fields and row structure
- Added dialog shell and HTMX event handlers
- All BK-05E table tests remain green

## Files Affected

- `templates/booking/dashboard/not_routed_table.html` – authorized by issue #401 for scope extension

## Handoff — afs-specialist-migrator · 2026-11-08T00:31:55Z
**State:** blocked  ·  **Branch / PR:** copilot/bk-05g-continue-dialogs-not-routed-table  ·  **Last commit:** 148883f
### Done
- See this branch's commits and `afs-run` journal.
### Remaining
- [ ] CI's validate.py will fail on this: .migration/handoffs/BK-05G.md: handoff section 1 is missing '**State:**'. Fix it and commit.
- [ ] CI's validate.py will fail on this: .migration/handoffs/BK-05G.md: handoff section 1 is missing '### Done'. Fix it and commit.
- [ ] CI's validate.py will fail on this: .migration/handoffs/BK-05G.md: handoff section 1 is missing '### Remaining'. Fix it and commit.
- [ ] CI's validate.py will fail on this: .migration/handoffs/BK-05G.md: handoff section 1 is missing '### Blockers / questions'. Fix it and commit.
- [ ] CI's validate.py will fail on this: .migration/handoffs/BK-05G.md: handoff section 1 is missing '### Next step for the next session'. Fix it and commit.
- [ ] Your return reports a handoff (`martins-vds/ai-factory-pilot-target#401`) but this branch didn't commit it. Write the `## Handoff` section with afs-handoff and commit `martins-vds/ai-factory-pilot-target`.
- [ ] These files are outside ticket BK-05G's planned files: `.migration/handoffs/BK-05G.bk05e-dashboard-template.md`. Don't widen your own scope: revert them, or, if the work truly needs them, write a handoff (afs-handoff) that names each file and why, set `handoff:` in your return, and stop. The operator decides.
### Blockers / questions
- self-check failed: `afs-finish-check` still found 7 problem(s) after its retry budget (ADR-0034). Written by the stop hook, not by the agent.
### Next step for the next session
Fix the items under Remaining, run `afs-finish-check`, and commit. Scope items need the operator.
