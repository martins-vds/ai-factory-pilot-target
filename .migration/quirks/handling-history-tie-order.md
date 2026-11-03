# Handling history has no completion-time tie-breaker

## Question
When two distinct handling events have the same completion time, the source's final event depends on set iteration because its comparator returns equality for the tie. Preserve this, define a stable tie-breaker, or something else?

## Evidence
- Source: `class:src/main/java/org/eclipse/cargotracker/domain/model/handling/HandlingHistory.java:HandlingHistory`; `.source/src/main/java/org/eclipse/cargotracker/domain/model/handling/HandlingHistory.java:32-49,75-79` at pinned SHA `f3beacf78de4f6d34edc4971ac87e38a5c6fe59d`.
- Characterization: `.migration/evidence/handling-registration/characterization/report.md` records distinct completion-time ordering, but does not characterize equal-time ordering.
- Why it looks wrong: the last event drives the persisted Delivery and its misdirected/destination-unload outcomes, yet the source does not define which tied event is last.

## Impact
- Ledger capabilities: `handling.history-ordering`, `handling.cargo-inspection`, `handling.misdirected-queue`, `handling.delivered-queue`.
- Blocks: `martins-vds/ai-factory-pilot-target#130` for equal-completion-time test cases and outcome behavior.

## Options
1. Preserve exactly (target reproduces the quirk; a test pins it)
2. Fix (target diverges; the divergence is recorded in the ledger with this ticket as approval)
3. Other
