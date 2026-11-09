# Slice booking — re-audit evidence

- Tickets: BK-05A–BK-05J · Audited `main`: `218309906ad44369a69eb118cd714a1a38499687` · Date: 2026-11-09
- Acceptance execution: `135c70a276d4b20d377d701e064c9c819de4151c`
- Source: `f3beacf78de4f6d34edc4971ac87e38a5c6fe59d`

## A. Graph refresh

The pinned source graph is fresh. In this audit, `check_graph_fresh.py --require source` and `graph_gate.py --side source` passed through `afs-run`; the source gate reports 27 entry points, 19 reaching data, and 1,350 enriched edges.

The current checkout's committed target graph remains stale, but it is not used as acceptance evidence. GitHub Actions run [42528425964, attempt 1](https://github.com/martins-vds/ai-factory-pilot-target/actions/runs/42528425964) completed successfully for `main` at `135c70a276d4b20d377d701e064c9c819de4151c`. I checked the repository, branch, revision, successful conclusion, and artifact name against GitHub; fetched the artifact; and ran `afs-acceptance verify` at that exact commit in a detached worktree. Verification passed. Its target graph snapshot names the same `src/` and `templates/` trees as the accepted commit, and those paths have not changed through audited `main`. The target graph gate passed with 34 entry points, 19 reaching data, 782 enriched edges, 564 nodes, and 1,373 edges.

Verification from the current `main` checkout itself rejects the artifact because the post-run coordinator reconciliation changed `booking.screen-not-routed-table.yaml`. That change adds evidence for existing dashboard/dialog tests; the application, tests, graph inputs, profile, source lock, and installed harness inputs are unchanged from the execution commit. The reconciled entry and the accepted code evidence were reviewed independently below.

The target graph reports some template-page nodes without a direct data path; the booking endpoints and domain flows do reach the relevant data, and their rendered UI behavior is covered by the cited tests. This is a leaf-page modeling limitation, not a broken booking flow or a graph-gate failure.

## B. Top-down findings

All booking screens and entry points have target counterparts and evidence in the 25-entry coverage table below. The registration wizard preserves its defaults, step state, validation and registration; dashboard tables preserve grouping, order, fields, empty states and links; route selection and cargo details preserve candidate display, assignment and not-found behavior; and destination/deadline dialogs preserve validation, updates and dashboard refresh.

The not-routed table entry is now `migrated`. Its ledger cites the dashboard rendering test and the dialog open, update and row-refresh tests from BK-05E/BK-05G. The full characterization replay records 24 prediction matches and one approved route-assignment redirect difference (#236). Other approved divergences (#232–#238, #251 and #252) and the preserved ignored-deadline behavior (#89 item 5 / #238) remain separately recorded in the replay.

The operator's side-by-side review is recorded in `.migration/evidence/booking/acceptance.md`: “Everything [matched]. All good,” covering the wizard, dashboard/details, routing/pathfinder, and both edit dialogs.

## C. Bottom-up findings

The target graph's booking flows connect registration, route assignment, route-specification updates, and dashboard rendering to their application services, repositories, and data. Its booking endpoint paths reach `cargo`, `leg`, `HandlingEvent`, `location`, and `voyage` as applicable. Target application boundaries are represented by `CargoRegistration`, `CargoRouting`, `CargoSpecification`, and `CargoDashboard`; Pathfinder remains an in-process integration with its REST contract covered by characterization and API tests. No missing integration, unconnected booking flow, or misplaced responsibility was found.

The verified acceptance run passed runtime and harness integrity, services, both graph gates, build, Ruff, `pytest -q`, CRAP (max 26.0 against 30), and full mutation (0.931 against 0.8; 2,065 killed, 153 survived, 83 files, `base=all`). Its unmodified journal rows are included in `.migration/evidence/runs/BK-05J.md`.

## D. Capability coverage

All 25 booking ledger entries have a target counterpart, migrated status, and evidence references. The acceptance run's full test and mutation gates pass; the tier-A replay provides the end-to-end characterization.

| Capability | Target components | Representative evidence | Status |
|---|---|---|---|
| `booking.cargo-not-found` | `CargoRouting._find_cargo`; dashboard views | routing unknown/stale update and cargo-details 404 tests | migrated |
| `booking.dashboard-chain` | `CargoDashboard`; dashboard views; dashboard template | dashboard partition, ordering and link test | migrated |
| `booking.dashboard-filters` | `CargoDashboard.get_dashboard`; dashboard views | partition and empty-table tests | migrated |
| `booking.deadline-change` | `CargoSpecification.change_deadline` | deadline preservation and route-state reset test | migrated |
| `booking.destination-change` | `CargoSpecification.change_destination` | destination preservation and route-state reset test | migrated |
| `booking.dialog-chain` | dialog views/templates; not-routed table | dialog action, update and refresh tests | migrated |
| `booking.dialog-deadline` | dialog views/templates; not-routed table | invalid-date error and update/refresh tests | migrated |
| `booking.dialog-destination` | dialog views/templates; not-routed table | filtered options and update/refresh tests | migrated |
| `booking.registration` | `CargoRegistration.register` | persisted registration test | migrated |
| `booking.routing-assign` | `CargoRouting.assign_route`; route-selection views | assignment persistence and redirect tests | migrated |
| `booking.routing-candidates` | `CargoRouting.route_candidates` | candidate conversion and deadline filtering test | migrated |
| `booking.routing-chain` | route-selection views; routing application methods | candidate and assignment/redirect tests | migrated |
| `booking.routing-pathfinder-api` | `TransitEdge`; `TransitPath`; `RoutingService`; API and URLs | seeded route, deadline-ignore, validation-golden and port-validation tests | migrated |
| `booking.screen-cargo-details` | dashboard application/views; cargo-details template | details fields and unknown/stale 404 tests | migrated |
| `booking.screen-claimed-table` | claimed-table template | dashboard partition/link test | migrated |
| `booking.screen-dashboard` | dashboard and admin-base templates | dashboard partition/link test | migrated |
| `booking.screen-deadline` | deadline and form templates | wizard date-boundary and deadline-state tests | migrated |
| `booking.screen-destination` | destination template | wizard option filtering and Back-state tests | migrated |
| `booking.screen-not-routed-table` | not-routed table template | dashboard, dialog-action, update and refresh tests | migrated |
| `booking.screen-origin` | origin template | origin default and options test | migrated |
| `booking.screen-route` | route-selection views and templates | populated-route and no-candidate guidance tests | migrated |
| `booking.screen-routed-table` | routed-table template | dashboard partition and cargo-moves-to-routed tests | migrated |
| `booking.screen-select-itinerary` | route-selection views and templates | populated-candidate and no-candidate guidance tests | migrated |
| `booking.wizard-chain` | wizard views and templates | Back/Next preservation and registration/redirect tests | migrated |
| `booking.wizard-input-rules` | wizard views and templates | same-origin/destination and same-day rejection tests | migrated |

## E. Tickets created

None. No new gap was established. The approved divergences and preserved quirk above retain their existing human rulings.

## F. Final gap list

None. The previously named `booking.screen-not-routed-table` status was reconciled with its existing BK-05E/BK-05G evidence. The earlier return's additional `untested` item had no ledger ID or ticket; this re-audit checked all 25 booking entries and their flows and found no separate untested booking capability to which it could be assigned.

Gap classes: missing — none; misplaced — none; broken-flow — none; integration — none; untested — none.

## G. Assessment

**Verdict: complete for the booking slice.** The accepted code revision has verified target-graph and full-mutation evidence, all 25 booking capabilities are migrated with supporting tests and characterization, and the required operator flow review is recorded. This verdict is scoped to booking; it does not assert completion of the full migration.
