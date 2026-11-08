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
