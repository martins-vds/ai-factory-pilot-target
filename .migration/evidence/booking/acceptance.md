# Booking slice acceptance evidence

- Tickets: BK-05A–BK-05J · Acceptance ticket: #473 · Date: 2026-11-09
- Acceptance run: [42528425964, attempt 1](https://github.com/martins-vds/ai-factory-pilot-target/actions/runs/42528425964)
- Executed commit: `135c70a276d4b20d377d701e064c9c819de4151c`
- Artifact: `afs-acceptance-135c70a276d4b20d377d701e064c9c819de4151c-42528425964-1` (retained until 2026-12-08T23:13:50Z)
- Verified result: `.migration/evidence/acceptance-runs/42528425964-1.json`

The issue text named an artifact using SHA `4462a706...`; GitHub's run artifact list and the fetched, verified branch identify the artifact above, matching the executed commit SHA.

## Gates

The verified durable Actions run passed the profile gates. Its committed journal rows are appended unchanged to `.migration/evidence/runs/BK-ACCEPT.md`.

| Gate | Result |
|---|---|
| Runtime and harness integrity | Pass |
| Services and graph freshness | Pass |
| Source graph | Pass; 27 entry points, 19 reaching data, 1,350 enriched edges |
| Target graph | Pass: `verdict=pass`, 0 failures; 34 entry points, 19 reaching data, 782 enriched edges; built under `graph/target/full` and gated for commit `135c70a276d4b20d377d701e064c9c819de4151c` |
| Build | Pass: `compileall` and `manage.py check` |
| Idiom | Pass: Ruff check and format |
| Behavior | Pass: `pytest -q` |
| CRAP | Pass: max 26.0, threshold 30, 0 over-threshold methods |
| Full mutation | Pass: score 0.931, threshold 0.8, 2,065 killed, 153 survived, 83 files, `base=all` |

No build, test, CRAP, or mutation gates were rerun in this coordinator session.

## Characterization and audit

BK-05I's tier-A replay records **24 prediction matches** and one prediction difference: route assignment redirects to cargo details, the approved divergence in #236. It records the other approved rulings and preserved routing quirk separately; the replay and its field-level comparisons are in `.migration/evidence/booking/replay.md`.

BK-05J checked 25 capabilities and returned `gaps-remain`. Its report found the stale `booking.screen-not-routed-table` status and a stale target graph, while its return also records one additional `untested` gap with both `ledger_id` and `ticket` null. This report reconciles the named ledger entry from BK-05E/BK-05G evidence, and the verified acceptance run supplies the target graph and full-mutation results missing from that earlier audit. The anonymous audit gap is not attributable to a booking ledger entry from the available evidence; it remains unresolved pending Auditor clarification. No new independent gate-7 audit was run.

## Booking ledger status

Every booking ledger entry is now `migrated`; the `screen-not-routed-table` entry was reconciled using its dashboard, dialog-action, update, and refresh tests.

| Ledger entry | Status |
|---|---|
| `booking.cargo-not-found` | migrated |
| `booking.dashboard-chain` | migrated |
| `booking.dashboard-filters` | migrated |
| `booking.deadline-change` | migrated |
| `booking.destination-change` | migrated |
| `booking.dialog-chain` | migrated |
| `booking.dialog-deadline` | migrated |
| `booking.dialog-destination` | migrated |
| `booking.registration` | migrated |
| `booking.routing-assign` | migrated |
| `booking.routing-candidates` | migrated |
| `booking.routing-chain` | migrated |
| `booking.routing-pathfinder-api` | migrated |
| `booking.screen-cargo-details` | migrated |
| `booking.screen-claimed-table` | migrated |
| `booking.screen-dashboard` | migrated |
| `booking.screen-deadline` | migrated |
| `booking.screen-destination` | migrated |
| `booking.screen-not-routed-table` | migrated |
| `booking.screen-origin` | migrated |
| `booking.screen-route` | migrated |
| `booking.screen-routed-table` | migrated |
| `booking.screen-select-itinerary` | migrated |
| `booking.wizard-chain` | migrated |
| `booking.wizard-input-rules` | migrated |

## Human check

The operator should compare the pinned legacy application with the target side by side:

- **Registration wizard:** origin and destination defaults/options (including excluding the selected origin), Back/Cancel/Next state preservation, date minimum and same-day booking-disabled behavior, and successful registration plus dashboard redirect.
- **Dashboard and cargo details:** routed, not-routed, and claimed row membership/order and displayed fields; route/details links; empty states; claimed-cargo link destination; and unknown or stale tracking IDs returning 404.
- **Routing:** candidate itineraries' endpoints, connected legs, voyages and date ordering; deadline filtering in booking; selection persistence and the approved #236 redirect to cargo details. Compare pathfinder response field names/order, date format, validation status/body, and the preserved #89 item 5 behavior that accepts but ignores `deadline`.
- **Destination/deadline dialogs:** initial values, filtered destination choices without mutation, visible invalid-deadline errors, successful updates preserving the other specification fields and resetting route state, and refreshed not-routed rows.

The operator reports that **"Everything [matched]. All good"** (martins-vds, 2026-11-08), covering all four side-by-side comparisons above: the registration wizard; dashboard and cargo details; routing and pathfinder API; and destination and deadline dialogs.
