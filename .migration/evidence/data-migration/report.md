# Data-migration capability audit — DM-AUDIT

Scope: every `.migration/ledger/data.*.yaml` entry (7 capabilities). Audit date: 2026-11-07.
Target revision under audit: `fbe311648f83eef709ca262c7cf06e29dfdadfa9`.

## A. Graph refresh

Ran `check_graph_fresh.py --require source,target`; both full graphs were fresh. The source graph gate and target graph gate (`--require-graph`) both passed. The source graph has the six mapped table anchors. `SEQUENCE` has no source graph node, as already documented in the data-migration plan (lines 34–38).

The target graph's `command=load_data_snapshot` path ends at `location`; it does not reach `voyage`, `cargo`, `HandlingEvent`, `leg`, or `carrier_movement`. The plan requires the command to reach every mapped target table (data-migration plan, lines 34–38). This is a target-graph inconsistency, although the graph gate itself passes. The source graph's missing `SEQUENCE` node is a documented inventory discrepancy, not an unresolved capability: ruling #255 approves the target-native sequence replacement.

## B. Top-down findings

No screen or route is owned by this data-migration slice. The audited entry point is the `load_data_snapshot` management command.

## C. Bottom-up findings

The loader prepares and inserts each table from the mapping (`src/cargotracker/data_migration/loader.py:172–226, 277–323`). The mapping lists six tables and excludes `SEQUENCE` under ruling #255 (`.migration/data/mapping.yaml:3–129`).

Fresh execution through `afs-run` loaded 54 rows across the six mapped tables, exported them, and reconciled with `tables=6 rows=54 mismatched_tables=0`. The generated reconciliation reported matching row counts and checksums for `location`, `voyage`, `cargo`, `HandlingEvent`, `leg`, and `carrier_movement`, with no reference problems. The four DM-05F tests passed, covering derived cargo delivery, connected itinerary legs, event references, and ordered carrier movements (`tests/data_migration/test_invariants.py:266–323`). The sequence realignment test also passed (`tests/data_migration/test_load.py::test_load_snapshot_realigns_each_sequence_to_max_plus_one`).

Full acceptance evidence is not yet available. Run [42424618848](https://github.com/martins-vds/ai-factory-pilot-target/actions/runs/42424618848) is for the exact target revision above, attempt 1, and uses the acceptance workflow at that revision. At the latest check it remained `in_progress` and had no artifact. No artifact verification or import was possible; full mutation and the acceptance gate therefore remain unproven. Do not infer a pass from partial progress.

The committed audit journal is `.migration/evidence/runs/DM-AUDIT.md`. It records the fresh graph checks, invariant and sequence tests, and load/export/reconciliation commands, including the first load attempt that correctly failed before the local database schema was migrated.

## D. Capability coverage

| Ledger ID | Target component / disposition | Evidence passing in this audit | Graph result |
|---|---|---|---|
| `data.location` | `LocationRecord` | Reconciliation; load | Reached |
| `data.voyage` | `VoyageRecord` | Reconciliation; load; carrier-movement invariant | Missing target graph path |
| `data.cargo` | `CargoRecord` | Reconciliation; load; delivery-history invariant | Missing target graph path |
| `data.handling-event` | `HandlingEventRecord` | Reconciliation; load; handling-event reference invariant | Missing target graph path |
| `data.leg` | `LegRecord` | Reconciliation; load; connected-itinerary invariant | Missing target graph path |
| `data.carrier-movement` | `CarrierMovementRecord` | Reconciliation; load; schedule-order invariant | Missing target graph path |
| `data.sequence` | Replaced by target-native sequence realignment, approved by #255 | Ledger approval and fresh sequence realignment test | No source `SEQUENCE` graph node; discrepancy documented in the plan |

No missing target component, misplaced responsibility, missing integration, or untested runtime path was found. The five `broken-flow` findings below refer specifically to the required graph representation; fresh load, reconciliation, and invariant results demonstrate that the runtime data flow works for these tables.

## E. Tickets created

No follow-up issue could be created with the GitHub tools available to this read-only audit. The graph-enrichment follow-up is therefore unfiled; the five gap records carry a null ticket and require operator tracking.

## F. Final gap list

| Class | Ledger ID | Finding | Follow-up |
|---|---|---|---|
| `broken-flow` | `data.voyage` | Target graph path from `load_data_snapshot` does not reach `voyage`; runtime reconciliation passes. | Graph enrichment issue needed |
| `broken-flow` | `data.cargo` | Target graph path from `load_data_snapshot` does not reach `cargo`; runtime reconciliation and invariant test pass. | Graph enrichment issue needed |
| `broken-flow` | `data.handling-event` | Target graph path from `load_data_snapshot` does not reach `HandlingEvent`; runtime reconciliation and invariant test pass. | Graph enrichment issue needed |
| `broken-flow` | `data.leg` | Target graph path from `load_data_snapshot` does not reach `leg`; runtime reconciliation and invariant test pass. | Graph enrichment issue needed |
| `broken-flow` | `data.carrier-movement` | Target graph path from `load_data_snapshot` does not reach `carrier_movement`; runtime reconciliation and invariant test pass. | Graph enrichment issue needed |

The acceptance workflow is an additional gate blocker, not a capability-class gap: it is still running and has not produced a verifiable artifact.

## G. Assessment

**Verdict: gaps remain.** Capability components, current reconciliation, DM-05F invariants, and approved sequence replacement were verified. Slice acceptance cannot be called complete until the target graph represents the loader's paths to every mapped table and the AFS acceptance workflow finishes with an artifact that passes independent verification. This audit does not rely on the separate Slice Coordinator acceptance work. No human flow sign-off was obtained in this audit.
