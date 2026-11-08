# BK-05G Handoff: Dashboard Template Dialog Integration

**From:** BK-05G (afs-specialist-migrator, ui)  
**To:** BK-05E (afs-specialist-migrator, ui)  
**Reason:** Scope correction; dashboard template is owned by BK-05E

## Required Changes to BK-05E's `templates/booking/dashboard/not_routed_table.html`

BK-05G implements destination and deadline dialogs (`templates/booking/dialogs/*.html` and view handlers). These dialogs must be triggered from the not-routed cargo table. BK-05G's current diff includes integration changes to `not_routed_table.html` that belong in BK-05E's scope.

**Add to the not-routed table:**

1. **Destination cell (line ~28):** wrap `{{ cargo.route_specification.destination.name }}...` in a button with:
   - `hx-get="/admin/cargo/{{ cargo.tracking_id.value }}/destination/"`
   - `hx-target="#cargo-edit-dialog-content"` 
   - `hx-swap="innerHTML"`
   - `aria-controls="cargo-edit-dialog"` and `aria-haspopup="dialog"`

2. **Deadline cell (line ~41):** same button pattern for deadline endpoint

3. **After the table (line ~62):** add the shared `<dialog>` container with ID `cargo-edit-dialog` and content div ID `cargo-edit-dialog-content`

4. **Dialog management script (lines ~73–89):** htmx event listeners to showModal/close and autofocus

Reference commit `4e75b7d` in BK-05G for exact markup.

## Files Affected

- `templates/booking/dashboard/not_routed_table.html` — owned by BK-05E, not BK-05G
