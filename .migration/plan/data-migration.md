# Data-migration slice plan

- Slice epic: [#247](https://github.com/martins-vds/ai-factory-pilot-target/issues/247)
- Planning ticket: [DM-04 / #258](https://github.com/martins-vds/ai-factory-pilot-target/issues/258)
- Parent workstream: [#223](https://github.com/martins-vds/ai-factory-pilot-target/issues/223)
- Decision map: [#3](https://github.com/martins-vds/ai-factory-pilot-target/issues/3)
- Status: draft for review; tickets are not published.

## Evidence and scope

The newest local snapshot is the Derby `cargo-tracker` export taken at `2026-11-07T00:40:49Z`. The DM-02 inventory records its manifest validation as `tables=7 problems=0`; its seven table counts total 55 rows. The CSV data rows are not included in this plan or committed.

The target schema at the inventory's recorded target revision (`a302ef8`) has persistence tables for `LOCATION → location`, `VOYAGE → voyage`, `CARGO → cargo`, `LEG → leg`, and `HANDLINGEVENT → HandlingEvent`. `CARRIER_MOVEMENT` has no target persistence home (#254), and `SEQUENCE` has no target table or entity mapping (#255). Both remain unresolved; the mapping must not silently drop either table or assert a fate before the human rulings.

The source graph has table nodes for the six entity-backed tables, including `carrier_movement`, but no `SEQUENCE` node. The missing `SEQUENCE` node is the graph discrepancy recorded by the inventory, not a reason to infer a source entry point or target mapping.

## Draft specialist tickets

These are five one-session-sized tickets for `afs-specialist-migrator` with `specialty: data`. Ticket creation/publication waits for approval of this plan.

1. **Define the snapshot mapping.** Create `.migration/data/mapping.yaml` from the inventory, with explicit source keys, target keys, column transforms, references, and a dependency-aware table order. Use the existing source identifiers and the inventory's UTC handling for naive timestamps, date handling, and enum-name values. Do not normalize values beyond declared transforms. This ticket is blocked on human rulings for #254 and #255 and on the CARGO/HANDLINGEVENT reference-cycle question below; do not mark unresolved tables as excluded without an approved disposition.
2. **Implement the idempotent loader.** Add a management command named `load_data_snapshot` that reads the profile mapping and snapshot, preserves explicit source IDs, resolves references, and reloads transactionally or otherwise guarantees an identical rerun. The target relations include a cycle: `HANDLINGEVENT.cargo_id` requires CARGO while nullable `CARGO.last_event_id` references HANDLINGEVENT. The mapping and loader must preserve both references using an approved strategy.
3. **Implement the mapped target export.** Add `export_data_snapshot`, using the same mapping as the loader and writing one headered CSV per mapped target table to `{out}`, with SQL NULL represented as `\N`.
4. **Reconcile the snapshot.** Run the configured load and export through `afs-run`, then run `data_reconcile.py reconcile` through `afs-run` with the snapshot, export, and mapping. Commit the reconciliation report; require matching row counts and checksums and no dangling references for every mapped table.
5. **Test business invariants on loaded data.** Add focused tests against the loaded relational state, including cargo delivery-state consistency with its handling history and connected itinerary legs. Keep these tests distinct from row/checksum reconciliation.

### Blocking edges

- Within this slice: mapping → loader and export; loader + export → reconciliation; mapping + loader → business-invariant tests.
- No application slice is blocked by these data tickets, consistent with the current workstream decision in #223.
- The mapping/loader completion is blocked by human answers to #254 and #255 and the reference-cycle question above. Those do not create an application-slice dependency.
- The Verifier independently reruns reconciliation on its own verification issue. The Auditor verifies capability coverage at slice acceptance.

## Data-path anchors

The source anchors are the six existing source table nodes: `table=Cargo`, `table=Leg`, `table=HandlingEvent`, `table=Location`, `table=Voyage`, and `table=carrier_movement`. These anchors represent the snapshot's source tables and reach their table nodes directly. `SEQUENCE` cannot currently be anchored because it has no source graph node; record this as the inventory's existing graph discrepancy.

The planned target anchor is `command=load_data_snapshot`. At implementation and acceptance, the target graph must show this command reaching every mapped target table (currently `location`, `voyage`, `cargo`, `leg`, and `HandlingEvent`; any additional table approved for #254 must also be reached). The export command is a separate target entry point and is listed in `.migration/slices/data-migration.yaml`.

## Awaiting human approval

Do not edit `.migration/profile.yaml` in this planning ticket. After approval, propose these exact single-command arrays:

- `profile.data.load`: `python manage.py load_data_snapshot --snapshot {snapshot} --mapping .migration/data/mapping.yaml`
- `profile.data.export`: `python manage.py export_data_snapshot --mapping .migration/data/mapping.yaml --out {out}`

## Open questions

- Resolve #254: preserve CARRIER_MOVEMENT in target storage, replace it with an approved representation, or explicitly regenerate it.
- Resolve #255: decide how to handle source SEQUENCE metadata after importing explicit IDs, including target-native sequence alignment.
- Approve the mapping/loader strategy for the nullable CARGO.last_event_id ↔ HANDLINGEVENT.cargo_id cycle.
- Approve the proposed `profile.data.load` and `profile.data.export` commands above.
