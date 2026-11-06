# Routed-cargo table contains an orphan test dialog

## Question
Should the unused tracking dialog with test placeholders be preserved or removed from the routed-cargo table?

## Evidence
- Source: `src/main/webapp/admin/tables/listRouted.xhtml:54-59` declares a `ShowTrackingDialog` with literal `Test -->` and `Id -->` labels bound to `currentTracking.test` and `currentTracking.id`; the scoped page has no control that opens this widget.
- Characterization: the markup is present in the routed table, while the declared content is test/debug text and is not connected to a page action in this file.
- Why it looks wrong: a dormant dialog exposes test placeholders and references a bean not otherwise bound by the scoped table.

## Impact
- Ledger capabilities: `booking.screen-routed-table`
- Blocks: implementing the routed-table dialog behavior in slice `booking` until a human decides.

## Options
1. Preserve exactly (retain the dialog and placeholders; pin behavior if reachable).
2. Fix (remove the unused markup or implement an intentional dialog; record the divergence in the ledger with this ticket as approval).
3. Other
