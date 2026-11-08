# Slice booking — acceptance evidence

- Tickets: BK-05A–BK-05J · Audited tree: `c7f6a95f0e6a80593e980eae02c0939ce6dab761` · Date: 2026-11-08
- Source: `f3beacf78de4f6d34edc4971ac87e38a5c6fe59d`

## Gates

| Gate | Command / evidence | Result |
|---|---|---|
| Source graph freshness | `check_graph_fresh.py --require source` | Pass; source graph is fresh. |
| Source graph | `graph_gate.py --side source` | Pass: 1,054 nodes, 2,139 edges, 1,350 enriched edges. All declared booking anchors reach source data. |
| Target graph | `check_graph_fresh.py --require source` reported stale target `src/` and `templates/` hashes. | Blocked: no target graph built and gated for this audited tree. The committed target graph is stale and is not acceptance evidence. |
| Build | `python -m compileall -q src`; `python manage.py check` | Pass; both run through `afs-run`. |
| Idiom | `ruff check`; `ruff format --check` | Pass; both run through `afs-run`. |
| Behavior / regression | `pytest -q` | Pass: 523 tests; run through `afs-run`. |
| CRAP | Coverage pytest, Lizard CSV, then `crap.py --max 30` | Pass: 523 tests; max CRAP 26.0, threshold 30, 0 over-threshold methods, 213 methods. All commands run through `afs-run`. |
| Full mutation | Profile command: `python .migration/harness/tools/afs-mutation --all` | Not run. No current-commit acceptance result establishes full mutation. |
| Current run evidence | `.migration/evidence/runs/BK-05J.md` | Contains fresh build, idiom, tests, and CRAP gate rows and hashes. |

The successful Actions acceptance run #42427856017 is for commit `3d1fcec13586c2d89b7a079bfd14ca011e2522c0`, not this audited tree. `origin/main` is `692c625b29e603780366a5d21e37bd27411fbb8f`; 122 files differ between the acceptance-run commit and current main, including application, test, ledger, and harness inputs. That run and its artifact therefore cannot establish current target-graph or full-mutation acceptance. A fresh acceptance workflow run on the audited commit is required.

## Characterization and rulings

Tier-A replay evidence in `.migration/evidence/booking/replay.md` records 24 prediction matches and one prediction difference: route assignment redirects to cargo details, as approved by #236. It records the approved outcomes for #232–#237, #251, and #252; #238 applies #89 item 5 (the pathfinder accepts but ignores `deadline`, while booking filters candidate arrivals). Decision #92 keeps booking/admin pages unauthenticated. The #239 pathfinder test and #250 cargo-lifecycle scenario remain inventory only and were not executed as legacy evidence; the source inventory records 16 executed tests.

The replay's source anchors are backed by the fresh source graph:

- Booking page → `Booking.init` → `BookingServiceFacade.listShippingLocations` → `LocationRepository.findAll` → `Location`.
- Dashboard routed/not-routed pages → `ListCargo.init` → `BookingServiceFacade.listAllCargos` → `CargoRepository.findAll` → `Cargo`.
- Route and itinerary-selection pages → `CargoDetails.load` → `BookingServiceFacade.loadCargoForRouting` → `CargoRepository.find` → `Cargo`.

The booking graph paths reach the five source data nodes `Cargo`, `HandlingEvent`, `Leg`, `Location`, and `Voyage`. Current target code and tests are represented below, but target graph paths cannot be independently accepted until the current-commit graph is built and gated.

Test-first evidence was inspected in BK-05A–BK-05H journals. They record named RED runs followed by green runs; examples include BK-05A registration/destination/deadline assertions, BK-05D wizard validation/navigation, BK-05E cargo details, BK-05F route assignment, BK-05G dialog behavior, and BK-05H URL resolution. Some early RED entries are collection/import failures; those alone are not treated as behavioral proof. The current 523-test suite passes, and BK-05I's replay journal records the characterization replay passing.

## Capability coverage

Each evidence reference below is recorded in the corresponding `.migration/ledger/booking.*.yaml`; the current passing full suite is in `.migration/evidence/runs/BK-05J.md`.

| Capability | Target components | Representative evidence | Status |
|---|---|---|---|
| `booking.cargo-not-found` | `CargoRouting._find_cargo`; dashboard views | `test_unknown_or_stale_routing_updates_raise_cargo_not_found`; `test_unknown_and_stale_cargo_details_return_http_404` | migrated |
| `booking.dashboard-chain` | `CargoDashboard`; dashboard views; dashboard template | `test_dashboard_partitions_cargo_in_source_order_and_renders_claimed_details_link` | migrated |
| `booking.dashboard-filters` | `CargoDashboard.get_dashboard`; dashboard views | `test_dashboard_partitions_cargos_in_source_order`; `test_dashboard_renders_empty_tables_without_custom_empty_state` | migrated |
| `booking.deadline-change` | `CargoSpecification.change_deadline` | `test_change_deadline_preserves_other_specification_fields_and_resets_route_state` | migrated |
| `booking.destination-change` | `CargoSpecification.change_destination` | `test_change_destination_preserves_other_specification_fields_and_resets_route_state` | migrated |
| `booking.dialog-chain` | dialog views; dialog templates; not-routed table template | `test_not_routed_table_exposes_destination_and_deadline_dialogs`; update/refresh tests | migrated |
| `booking.dialog-deadline` | dialog views; deadline template; not-routed table template | `test_invalid_deadline_shows_field_error_and_keeps_dialog_open`; `test_deadline_update_preserves_route_and_refreshes_not_routed_row` | migrated |
| `booking.dialog-destination` | dialog views; destination template; not-routed table template | `test_destination_dialog_filters_options_without_mutating_locations`; update/refresh test | migrated |
| `booking.registration` | `CargoRegistration.register` | `test_registration_persists_new_cargo_with_generated_id_and_empty_itinerary` | migrated |
| `booking.routing-assign` | `CargoRouting.assign_route`; route-selection views | `test_assign_route_persists_itinerary_and_recalculates_delivery`; redirect/details test | migrated |
| `booking.routing-candidates` | `CargoRouting.route_candidates` | `test_route_candidates_convert_paths_and_filter_by_route_specification` | migrated |
| `booking.routing-chain` | route-selection views; candidate and assignment application methods | populated-candidate and assignment/redirect tests | migrated |
| `booking.routing-pathfinder-api` | `TransitEdge`; `TransitPath`; `RoutingService`; shortest-path API and URLs | seeded route, deadline-ignore, validation-golden, and port-validation tests | migrated |
| `booking.screen-cargo-details` | dashboard application/views; cargo-details template | `test_cargo_details_render_route_fields_and_itinerary`; unknown/stale 404 test | migrated |
| `booking.screen-claimed-table` | claimed-table template | dashboard partition/link test | migrated |
| `booking.screen-dashboard` | dashboard and admin-base templates | dashboard partition/link test | migrated |
| `booking.screen-deadline` | deadline and deadline-form templates | `test_destination_next_opens_deadline_with_today_as_calendar_minimum`; deadline-state test | migrated |
| `booking.screen-destination` | destination template | `test_origin_next_opens_destination_with_dallas_and_excludes_origin`; Back-state test | migrated |
| `booking.screen-not-routed-table` | not-routed table template | dashboard partition/link test; dialog-action/update tests are recorded under the related dialog entries | **in-progress** |
| `booking.screen-origin` | origin template | `test_origin_step_is_open_and_defaults_to_chicago` | migrated |
| `booking.screen-route` | route-selection views; route and candidate templates | populated-route and no-candidate guidance tests | migrated |
| `booking.screen-routed-table` | routed-table template | dashboard partition and cargo-moves-to-routed tests | migrated |
| `booking.screen-select-itinerary` | route-selection views; select-itinerary and candidate templates | populated-candidate and no-candidate guidance tests | migrated |
| `booking.wizard-chain` | wizard views; wizard templates | Back/Next preservation and registration/redirect tests | migrated |
| `booking.wizard-input-rules` | wizard views; wizard templates | same-origin/destination and direct same-day rejection tests | migrated |

All 25 entries have target components and evidence references. However, `booking.screen-not-routed-table` remains `in-progress`; its note assigns dialog actions and refresh to BK-05G, but its own evidence list does not cite BK-05G's dialog-action/update tests. The related dialog capabilities are migrated and tested, but the coordinator must reconcile this ledger entry before claiming all entries complete. No ledger status was changed by this read-only audit.

## Human check and verdict

No operator side-by-side approving review is present in the evidence supplied for this audit. The profile names `martins-vds` as the sign-off approver. That review remains outstanding as required.

**Verdict: gaps remain.** Current build, behavior, idiom, and CRAP gates pass. Slice acceptance is blocked on current-commit target-graph and full-mutation evidence, reconciliation of the in-progress screen capability, and the operator's approving review.
