# Dialog updates log an unavailable PrimeFaces widget

## Question
Should the source preserve or correct the browser-console warning emitted after successful destination and deadline dialog updates?

## Evidence
- Source: `.source/src/main/webapp/admin/tables/listNotRouted.xhtml:30-58` wires dialog-return callbacks to update `tableNotRouted`.
- Characterization: updating destination and deadline persisted the changed values and closed each dialog, while the browser console logged `Widget for var 'mainDash_tableNotRouted_0_toUpdate_dlgwidget' not available!` and `Widget for var 'mainDash_tableNotRouted_0_arrivalDeadlineToUpdate_dlgwidget' not available!`.
- Why it looks wrong: the dialog update succeeds but its generated widget lookup reports a missing widget.

## Impact
- Ledger capabilities: `booking.dialog-destination`, `booking.dialog-deadline`
- Blocks: implementing the corresponding dialog completion callbacks in slice `booking` until a human decides.

## Options
1. Preserve exactly (retain the warning and successful update behavior).
2. Fix (remove the warning while preserving the update behavior; record the divergence with the human decision).
3. Other
