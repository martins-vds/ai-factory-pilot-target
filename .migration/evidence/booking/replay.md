# BK-05I — Booking characterization replay

- Source: Eclipse Cargo Tracker, tier A, `f3beacf78de4f6d34edc4971ac87e38a5c6fe59d`
- Target replay revision: `d416b89` (the revision whose focused replay run passed)
- Recordings: `.migration/characterization/booking/observations.json` and the raw Pathfinder captures under `.migration/characterization/booking/pathfinder/`
- Focused replay: `pytest -q tests/characterization/booking` — 17 passed; durable run journal: `.migration/evidence/runs/BK-05I.md`

## Result

The characterization records **24 prediction matches** and **one prediction difference**: route assignment. The target redirects to cargo details, the approved replacement in #236. Replay comparisons passed for all recorded fields exercised below; no target defect was found. Approved changes in other branches are reported individually and are not counted as prediction matches or defects.

The randomized pathfinder was compared by response fields and route properties, not by requiring the target to reproduce captured random values or candidate counts. Its captured invalid-request status, content type and body bytes were compared exactly. The target's assigned route was checked against the captured Hong Kong–Melbourne candidate fields.

## Capability replay

| Capability | Tier-A cases replayed | Target fields compared | Result |
|---|---|---|---|
| `booking.cargo-not-found` | `unknown-cargo-error` | Unknown detail, route and dialog-update HTTP status | Approved divergence — #232: explicit 404 replaces the source null-dereference 500, including updates. |
| `booking.dashboard-chain` | `dashboard` | Dashboard response and three sections in recorded order | Match |
| `booking.dashboard-filters` | `dashboard` | Tracking IDs assigned to routed, not-routed and claimed tables | Match |
| `booking.deadline-change` | `deadline-dialog` | Updated deadline, preserved origin/destination, refreshed row | Match; invalid input's field error is the approved #234 change. |
| `booking.destination-change` | `destination-dialog` | Updated destination, preserved origin/deadline and unrouted state | Match |
| `booking.dialog-chain` | `destination-dialog`, `deadline-dialog` | Dialog requests, successful update responses and dashboard refresh | Approved divergence — #251 removes the unavailable-widget warning while preserving updates. |
| `booking.dialog-deadline` | `deadline-dialog` | Initial route/deadline, invalid-date field error, successful update | Approved divergences — #234 field error and #251 warning removal. |
| `booking.dialog-destination` | `destination-dialog` | Origin/current destination, filtered choices, repeat-render stability, update | Approved divergences — #235 avoids mutating options; #251 removes the warning. |
| `booking.registration` | `wizard-origin`, `wizard-destination`, `wizard-deadline`, `registration` | Origin, destination, deadline, generated ID format, initial delivery state and empty itinerary | Match |
| `booking.routing-assign` | `route-assignment` | Selected candidate's persisted legs, resulting details page and redirect | Approved divergence — #236 redirects to cargo details. |
| `booking.routing-candidates` | `route-candidates`, `unknown-cargo-error` | Candidate endpoints/legs, deadline filtering, zero-route state and unknown ID | Preserved quirk — #89 item 5 / #238: pathfinder accepts but ignores deadline; booking filters by arrival deadline. #232 governs unknown IDs. |
| `booking.routing-chain` | `route-candidates`, `route-assignment` | Candidate display, selected itinerary persistence and final page | Approved divergence — #236 redirect within the otherwise matching route flow. |
| `booking.routing-pathfinder-api` | `route-candidates` | Recorded JSON envelope/edge fields, endpoints, connected legs, dates and exact validation goldens | Preserved quirk — #89: randomized routes and ignored deadline; #238 is recorded as #89 item 5. |
| `booking.screen-cargo-details` | `cargo-details`, `route-assignment` | Origin, destination, deadline, itinerary and absence of history | Match |
| `booking.screen-claimed-table` | `dashboard`, `cargo-details` | Claimed row and details destination | Approved divergence — #233 changes only the link label; it still opens details, not history. |
| `booking.screen-dashboard` | `dashboard` | Section names, order and empty-state behavior | Match |
| `booking.screen-deadline` | `wizard-deadline` | Date minimum, same-day message, next-day message and Book Cargo disabled state | Match |
| `booking.screen-destination` | `wizard-destination` | Selected destination, option count and origin exclusion | Match |
| `booking.screen-not-routed-table` | `dashboard`, `destination-dialog`, `deadline-dialog` | New cargo row, route link, origin/destination/deadline and refreshed values | Match |
| `booking.screen-origin` | `wizard-origin` | Default location, selected UN/LOCODE, offered location count and actions | Match |
| `booking.screen-route` | `route-candidates` | Candidate count, numbered route, voyage and leg endpoint fields; empty result | Match |
| `booking.screen-routed-table` | `dashboard` | Routed rows and displayed field columns | Approved divergence — #237 drops the unreachable debug dialog. |
| `booking.screen-select-itinerary` | `select-itinerary-with-candidates`, `select-itinerary-without-candidates` | Populated candidate fields and no-route guidance | Approved divergence — #252 renders candidates when present; empty-case guidance remains. |
| `booking.wizard-chain` | `wizard-origin`, `wizard-destination`, `wizard-deadline`, `registration` | Step transitions, selections, Back/Cancel and successful registration | Match |
| `booking.wizard-input-rules` | `wizard-destination`, `wizard-deadline` | Destination exclusion and same-day/non-bookable versus next-day/bookable state | Match |

## Approved rulings

| Issue | Recorded outcome and replay assertion |
|---|---|
| #232 | Explicit HTTP 404 for unknown or stale IDs, including destination/deadline updates; replay asserts 404. |
| #233 | Change only the claimed-cargo link label to “Click to see details”; keep the cargo-details destination and add no history page. |
| #234 | Invalid deadline is a visible field error; replay checks the error and invalid-field marker. |
| #235 | Filter destination choices without mutating the backing location list; replay compares repeated option lists and retained inputs. |
| #236 | Successful route assignment redirects to the cargo-details page; replay checks redirect chain and persisted selected legs. |
| #237 | Drop the unreachable debug dialog; replay checks its markup is absent. |
| #251 | Drop the unavailable-widget warning while preserving successful updates and refresh; replay checks update responses and refreshed fields. |
| #252 | Render candidate routes when available; replay checks populated itineraries and retains the empty-candidate guidance. |
| #238 | Apply #89 item 5: accept and ignore `deadline` in the pathfinder; filter candidates by arrival deadline in booking. |

## Source-test inventory boundary

`ExternalRoutingServiceTest.testCalculatePossibleRoutes` (#239) and `CargoLifecycleScenarioTest.testCargoFromHongkongToStockholm` (#250) remain unannotated inventory. Neither was run nor counted as executed legacy evidence. The executed source-test inventory remains the 16 tests recorded in `source-tests.json`.

## Ledger follow-up

`booking.screen-not-routed-table` remains `in-progress` in its ledger entry. This replay does not edit that status; the Slice Coordinator owns reconciling it.
