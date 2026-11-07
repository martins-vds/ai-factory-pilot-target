# Admin live-map marker behavior

**Ticket:** AM-04A · **Slice:** `martins-vds/ai-factory-pilot-target#202`  
**Plan:** `.migration/plan/admin-live-map.md` (approved in [#260](https://github.com/martins-vds/ai-factory-pilot-target/pull/260), revised in [#266](https://github.com/martins-vds/ai-factory-pilot-target/pull/266))

This design turns the characterized admin map into a test-first checklist for AM-04B–E. Source observations are in `.migration/characterization/admin-live-map/`; target status behavior currently lives in `src/cargotracker/cargo/application/map_status.py` and `src/cargotracker/cargo/interfaces/tracking/map/views.py`.

## Approved decisions

| Decision | Required target behavior |
|---|---|
| [#90 / ADR-0005](https://github.com/martins-vds/ai-factory-pilot-target/issues/90) | Poll a server-rendered markers partial with htmx at `CARGO_MAP_POLL_SECONDS` (default 10). Committed cargo changes appear by the next poll. The source WebSocket and online/offline label are dropped. |
| [#205](https://github.com/martins-vds/ai-factory-pilot-target/issues/205) | Use the exact configured coordinates for a known city; omit the source's random southwest offset. |
| [#206](https://github.com/martins-vds/ai-factory-pilot-target/issues/206) | A cargo whose selected location has no configured coordinates gets no marker or invented point. Show it in a separate Unknown/unmapped list with its real tracking link; keep other valid markers. |
| [#207](https://github.com/martins-vds/ai-factory-pilot-target/issues/207) | Render the normalized `In port` tooltip label, without the source's accidental leading space. |
| [#253](https://github.com/martins-vds/ai-factory-pilot-target/issues/253) | Fix the `NOT_RECEIVED` + `Unknown` sentinel: keep the marker at a mappable origin and show `Last known location: Unknown`, never `undefined`. If the selected origin has no coordinates, use #206's unmapped list. |

The approved #253 ruling supersedes the older open-question text in the plan (#260, revised by #266). Do not defer this case or classify it as a new decision.

## Decision tables

### Cargo location and marker placement

| Cargo state / selected location | Marker location | Coordinates / fallback |
|---|---|---|
| `NOT_RECEIVED`, origin is configured | Origin | Exact configured origin coordinates. Keep the marker even when `lastKnownLocation` is `Unknown`; report `Unknown` in the tooltip. (#253) |
| `NOT_RECEIVED`, origin is not configured | No marker | Add cargo to the separate unmapped list with its tracking link. Do not fall back to `Unknown` or fabricate a point. (#206, #253) |
| Any other transport status, last-known location is configured | Last-known location | Exact configured coordinates. (#205) |
| Any other transport status, last-known location is missing or unmapped | No marker | Add cargo to the separate unmapped list with its tracking link. Keep other known-location markers. (#206) |
| Mixed known and unmapped cargo | Known cargo only | Render every known marker and every unmapped list item independently; never discard valid markers because another location is unmapped. |

The origin selection for `NOT_RECEIVED` is the characterized legacy rule (`edge-cases.json`, `unknown_sentinel_not_received`) and is now approved by #253. The list is for cargo whose **selected** location cannot be mapped, not for every cargo whose last-known-location field says `Unknown`.

### Status precedence and marker colors

Resolve one status per cargo in the following order; apply the color for the first matching row. This preserves the source's conflicting-flag cases in `edge-cases.json:2-58`.

| Priority | Condition | Color |
|---:|---|---|
| 1 | Not routed (`NOT_ROUTED`) | Grey |
| 2 | Misrouted or misdirected | Red, including when also at destination |
| 3 | At destination | Black |
| 4 | Otherwise `NOT_RECEIVED` | Gold |
| 5 | Otherwise `IN_PORT` or `ONBOARD_CARRIER` | Green |
| 6 | Otherwise `CLAIMED` | Black |
| 7 | Unknown or unrecognized status | Red |

Pin the characterized combinations as well as each isolated precedence rule: not-routed beats misdirected/at-destination; misdirected beats at-destination; at-destination beats ordinary transport status. In particular, the source matrix expects red for both `MISROUTED + misdirected + atDestination` and `ROUTED + misdirected + atDestination`, while `NOT_ROUTED + misdirected + atDestination` is grey.

**Shared-status constraint:** reuse cargo/domain status values and the existing status behavior where it agrees, but do not blindly call `map_status_code` for the admin map. The current target helper checks destination before misdirection (`map_status.py:4-11`), which conflicts with the admin source cases above. AM-04B/D must preserve the admin precedence with a small, explicitly tested resolver/adapter; any change to shared tracking behavior must also pass its existing tests. The color lookup can remain a separate, simple mapping.

### Tooltip

| Field / case | Required rendering |
|---|---|
| Every known marker | Tracking ID, routing status, misdirected flag, transport status, at-destination flag, origin, and last-known location, in the characterized order. |
| `IN_PORT` | `In port` (one normalized space; #207). |
| `NOT_RECEIVED` with unknown last-known location and known origin | Show the origin marker and `Last known location: Unknown`; never interpolate `undefined` (#253). |
| Unmapped selected location | Do not put an unmapped marker/tooltip on the map; show the cargo in the separate list with its real tracking link (#206). |

Other source labels and values remain unchanged unless separately approved. Characterization records source tooltip text and visible browser behavior separately; the target tests assert the required text, not incidental HTML whitespace collapsing.

### Empty and failure behavior

| Condition | Required result |
|---|---|
| No cargos | Empty markers; keep the map shell/controls; show no user-facing empty-state message (source `empty_response`). |
| HTTP error with an empty JSON array | Render zero markers and no user-facing message; do not treat the body as a successful cargo result (source `http_500_with_json_array`). |
| Network or server-side cargo-query failure | Log the failure, do not synthesize cargo or marker data, and do not show a user-facing error message. The response must not be mistaken for successful cargo data. |
| Valid and unmapped cargo together | Keep valid markers and render only the unmapped cargo in the separate list (#206). |

The source's empty and HTTP-500-with-JSON-array observations both have zero markers and no user message; network failure is logged and produces no markers (`edge-cases.json`). The target's server-side failure response must be tested at the endpoint boundary; the htmx view must not manufacture a successful marker partial from failed data.

### Marker navigation

| Action | Required result |
|---|---|
| Activate a cargo marker | Open that cargo's BK-05 admin cargo-details page, carrying the same tracking ID. Resolve the URL through the target route; do not hard-code the source JSF URL. |
| Destination route | Remains provisional until the revised booking plan names BK-05's route. AM-04D is blocked on BK-05; do not implement against a guessed URL. |

The source observation opens `/admin/show.xhtml?trackingId=…` in the named `winMap` window (`browser-observations.json:navigation`). Preserve the user-visible click-through to the selected cargo. AM-04D should use a semantic link to the resolved booking route and test its tracking ID; do not couple the test to popup dimensions or an unapproved target URL.

## Test-first inventory for AM-04B–E

Write the focused test first in the ticket named below, then implement only enough to pass it. The listed paths are from the approved plan.

| Ticket / test file | Test checklist |
|---|---|
| **AM-04B** — `tests/cargo/interfaces/test_admin_live_map_data.py` | Query all cargos through the existing repository; preserve the fields needed for marker status, tooltip, and location selection. Test `NOT_RECEIVED` selects origin and other statuses select last-known location. Test exact configured coordinates and that an unmapped selected location has no coordinates. Assert `CARGO_MAP_POLL_SECONDS` defaults to 10. |
| **AM-04C** — `tests/cargo/interfaces/test_admin_live_map_templates.py` | Render the server-side page and Leaflet/OpenStreetMap shell. Assert the htmx trigger uses the configured interval, including a non-default setting. Assert there is no WebSocket endpoint or online/offline label (#90). |
| **AM-04D** — `tests/cargo/interfaces/test_admin_live_map_markers.py` | Table-test the status/color cases and conflicting-flag precedence above; exact coordinates with no offset; tooltip field order, `In port`, and `Unknown` sentinel text; empty results; HTTP-error and query-failure handling with no fabricated markers or user message; mixed known/unmapped cargo with its real tracking link and no invented point; marker link opens the correct BK-05 cargo detail using its tracking ID. |
| **AM-04E** — `tests/cargo/interfaces/test_admin_live_map_processing.py` | Process the characterized `DEF789` `RECEIVE` at `CNHKG` through the real handling flow, then request the markers partial. Assert `CNHKG`, `IN_PORT`, and red misrouted precedence appear. Assert the page's actual htmx interval equals the configured non-default `CARGO_MAP_POLL_SECONDS`. Do not mutate cargo directly or mock the processing step. |

## Complexity boundary

- Keep the view focused on querying/building context and rendering; keep marker projection, selected-location lookup, status precedence/color lookup, tooltip data, and unmapped-list projection in small, single-purpose helpers.
- Reuse existing cargo/location repositories, configured coordinate mappings, and shared status values; avoid a duplicate persistence path or a monolithic template/view with nested conditionals.
- Add focused tests for each helper and the end-to-end poll flow. Every changed target method must remain at CRAP ≤ 30; split a method before it crosses the profile limit.

## Evidence references

- Characterized source behavior: `.migration/characterization/admin-live-map/test_admin_live_map.py`, `edge-cases.json`, `browser-observations.json`, `cargo-before-handling.json`, and `cargo-after-handling.json`.
- Shared target status behavior and tests: `src/cargotracker/cargo/application/map_status.py`, `src/cargotracker/cargo/interfaces/tracking/map/views.py`, and `tests/cargo/interfaces/test_map.py`.
- Approved plan and cross-slice dependency: `.migration/plan/admin-live-map.md`, [#260](https://github.com/martins-vds/ai-factory-pilot-target/pull/260), and [#266](https://github.com/martins-vds/ai-factory-pilot-target/pull/266).
