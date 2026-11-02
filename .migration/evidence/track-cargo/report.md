# Slice Track Cargo — acceptance evidence

- Tickets: TC-02–TC-15 · Audited target commit: `7b78de8` · Date: 2026-11-02 UTC
- Slice epic: `martins-vds/ai-factory-pilot-target#9` · Decision map: `#3`
- Pinned source: `eclipse-ee4j/cargotracker@f3beacf78de4f6d34edc4971ac87e38a5c6fe59d`

## Verdict

**Gaps remain.** Build, idiom, tests, CRAP and differential checks pass in the available
environment. The browser check found a broken embedded-map flow, ledger approval metadata is
incomplete for two approved rulings, and the declared Python 3.13 target could not be exercised
because only Python 3.12.15 is installed. The human legacy/Django side-by-side comparison remains
pending; its procedure and checklist are in [side-by-side-check.md](../../../docs/side-by-side-check.md).

## Gates

All shell gates were run through `.migration/harness/tools/afs-run`. The committed journal
`.migration/evidence/runs/TC-15.md` records commands, exits and log digests. Raw logs are temporary.

| Gate | Command | Exit / result | Evidence |
|---|---|---|---|
| Build | `python -m compileall -q src`; `python manage.py check` | 0; 0 | `build-compile`, `build-django-check` |
| Idiom | `ruff check`; `ruff format --check` | 0; 0; 108 files already formatted | `idiom-ruff-check`, `idiom-ruff-format` |
| Behavior / regression | `pytest -q` | 0; **172 passed** with PostgreSQL 17 | `tests-postgres17` |
| CRAP | `lizard --csv src`; `crap.py .migration/runs/lizard.csv --lcov coverage.lcov --max 30` | 0; maximum **14**, zero methods above 30 | `crap` |
| Differential | `python -m pytest -q tests/differential/test_track_cargo.py` | 0; **8 passed** | `differential` |
| Approved rulings | Five named target tests for #12, #13, #14, #17 and #52 | 0; **5 passed** | `ruling-tests` |
| Changed mutation | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | 0; no mutable code changed | `mutation-changed` |
| Full mutation | `python .migration/harness/tools/afs-mutation --all` | Initial invocation: **0.602** (381 killed, 252 survived), below 0.8; configured rerun was in progress when this report was drafted | `mutation-full`, `mutation-full-configured` |
| Browser / UI | Interactive browser check of the target tracking page and map iframe | **Fail:** tracking result renders; iframe request returns 200 with `X-Frame-Options: DENY`, so browser refuses the map | Browser observation below; no browser command is defined in `profile.yaml` |

The first full-suite attempt could not connect to PostgreSQL; after starting PostgreSQL 17 and
setting the local connection variables, the complete suite passed. The first mutation invocation
did not inherit those database variables, so its score is not a clean measurement of database-backed
mutants. The configured rerun is recorded separately rather than hiding that attempt. All automated
gate commands used Python **3.12.15**; the profile specifies Python 3.13, which is not installed in
this environment. Therefore the profile-runtime gate result remains unverified.

## Characterization and differential evidence

The tier-A characterization has eight source goldens: `ABC123`, `JKL567`, `DEF789`, `MNO456`,
padded ID, lowercase ID, empty ID and unknown ID. The fresh target differential run passed all
eight cases. Result, history and map-frame data were compared; date values use UTC and the source
format. See `.migration/evidence/track-cargo/characterization/report.md` and
`.migration/evidence/track-cargo/differential/report.md`.

The four approved fixes and preserved ruling are pinned by named tests and were rerun in this
session:

| Ruling | Decision and target assertion | Named target test |
|---|---|---|
| #12 | Fix: visible required/not-found feedback and no cargo-dependent result without a cargo | `tests/cargo/test_tracking.py::test_empty_and_unknown_ids_show_messages_without_cargo_result_or_map` |
| #13 | Fix: IN_PORT names the last-known location, not the route destination | `tests/cargo/interfaces/test_status_text.py::test_in_port_status_names_last_known_location` |
| #14 | Fix: markers use configured coordinates without random offsets | `tests/cargo/interfaces/test_map.py::test_map_markers_use_exact_configured_coordinates` |
| #17 | Fix: claimed cargo has no displayed ETA | `tests/cargo/interfaces/test_eta.py::test_claimed_cargo_hides_eta` |
| #52 | Preserve: repeated-location lookup uses the first matching location/leg, without voyage matching | `tests/cargo/test_domain_calculations.py::test_quirk52_next_activity_uses_first_matching_location` |

The characterization tests continue to pin the source behavior for the fixed rulings. The target
results are approved divergences, not unexplained differential exclusions.

## Capability coverage (gate 7)

All 19 `track-cargo.*` ledger entries have `status: migrated`, non-empty `target.components`,
implementation-ticket links and evidence. The target component references resolve to source or
template paths. The table records the primary counterpart and a representative passing target test;
each full component/evidence list remains in its named ledger entry.

| Ledger capability | Ticket(s) | Primary target counterpart | Passing target evidence |
|---|---|---|---|
| `track-cargo.data-cargo` | #10, #25, #26, #64 | `CargoRecord`, `DjangoCargoRepository` | `tests/cargo/test_repository.py::test_repository_reads_cargo_embedded_fields_and_legs_by_tracking_id`; sample seed test |
| `track-cargo.data-handling-event` | #25, #26 | `HandlingEventRecord`, `DjangoHandlingEventRepository` | `tests/handling/test_repository.py::test_repository_reads_and_orders_deduplicated_handling_history` |
| `track-cargo.data-leg` | #10, #26 | `LegRecord`, `Itinerary` | `tests/cargo/test_repository.py::test_cargo_and_leg_schema_matches_source_jpa_tables_and_relations` |
| `track-cargo.data-location` | #10, #26 | `LocationRecord`, `DjangoLocationRepository` | `tests/location/test_domain.py`; `tests/location/test_repository.py` |
| `track-cargo.data-voyage` | #10, #26 | `VoyageRecord`, `DjangoVoyageRepository` | `tests/voyage/test_domain.py`; `tests/voyage/test_repository.py` |
| `track-cargo.domain-event-expectation` | #10, #28 | `Itinerary.is_expected` | `tests/cargo/test_domain_calculations.py::test_itinerary_matches_only_expected_event_location_and_voyage` |
| `track-cargo.domain-history-order` | #25 | `HandlingHistory` | `tests/handling/test_domain.py::test_handling_history_deduplicates_and_orders_events_by_completion_time` |
| `track-cargo.domain-route-state` | #10, #28, #33 | `Delivery.derived_from` | `tests/cargo/test_domain_calculations.py::test_delivery_matches_golden_states_for_abc_jkl_def_and_mno` |
| `track-cargo.domain-transport-status` | #10, #28 | `Delivery.derived_from` | `tests/cargo/test_domain_calculations.py::test_delivery_derives_transport_status_from_latest_event` |
| `track-cargo.eta` | #31 | `format_eta` | `tests/cargo/interfaces/test_eta.py::test_claimed_cargo_hides_eta`; UTC format test |
| `track-cargo.handling-history` | #10, #33 | `get_history_rows`, tracking result template | `tests/cargo/interfaces/test_tracking_result.py::test_tracking_result_renders_ordered_history_with_utc_times_and_expectation_markers` |
| `track-cargo.map-frame` | #32 | `map_frame_url`, `map_frame` | `tests/cargo/interfaces/test_map.py::test_map_frame_url_carries_status_and_cargo_locations`; differential suite |
| `track-cargo.map-integration` | #32 | `LOCATION_COORDINATES`, Leaflet/OpenStreetMap map template | `tests/cargo/interfaces/test_map.py::test_map_markers_use_exact_configured_coordinates` |
| `track-cargo.map-status-code` | #32 | `map_status_code` | `tests/cargo/interfaces/test_map.py::test_map_status_code_preserves_source_branch_precedence` |
| `track-cargo.misdirected-indicator` | #10, #33 | tracking result view/template | `tests/cargo/interfaces/test_tracking_result.py::test_misdirected_warning_and_absent_next_activity` |
| `track-cargo.next-activity` | #10, #33 | `get_next_activity_text` | `tests/cargo/interfaces/test_tracking_result.py::test_next_activity_text_matches_source_descriptions`; #52 test |
| `track-cargo.not-found` | #10, #29 | `TrackingLookup`, tracking view | `tests/cargo/test_tracking.py::test_empty_and_unknown_ids_show_messages_without_cargo_result_or_map` |
| `track-cargo.status-text` | #10, #30 | `get_status_text` | `tests/cargo/interfaces/test_status_text.py::test_in_port_status_names_last_known_location` |
| `track-cargo.tracking-id-entry` | #10, #29 | `TrackingForm`, tracking view | `tests/cargo/test_tracking.py::test_tracking_page_has_a_progressive_tracking_form`; padded-ID test |

Two ledger evidence symbols are stale: `track-cargo.map-frame` names
`test_tracking_map_url_carries_status_and_cargo_locations` (the current test is
`test_map_frame_url_carries_status_and_cargo_locations`), and `track-cargo.map-status-code` names
`test_claimed_sample_cargo_is_not_marked_unloaded_at_destination` (the sample-data assertion is in
`test_seed_sample_data_is_idempotent_and_supports_golden_lookups`). Other passing tests and the
differential suite independently cover these behaviors. The `track-cargo.data-voyage` entry also
references old `.migration/runs/TC-03/...` raw logs that are not present; its durable TC-03 journal,
target tests and current differential evidence are present.

Approval metadata is missing from some affected ledger entries even though the ruling links and
tests exist: `track-cargo.handling-history` lists #12 without an `approval` block, and
`track-cargo.domain-route-state` and `track-cargo.next-activity` list #52 without an `approval`
block. These read-only audit findings were not silently repaired in the ledger.

## Findings by gap class

| Class | Ledger entry | Finding | Ticket |
|---|---|---|---|
| `broken-flow` | `track-cargo.map-frame` | The tracking page requests the frame, but the browser cannot display it because the map response is denied by `X-Frame-Options: DENY`. | Follow-up not filed |
| `integration` | `track-cargo.map-integration` | The map endpoint returns 200, but the browser-level Leaflet/OpenStreetMap map is not integrated into the parent page. | Follow-up not filed |
| `missing` | `track-cargo.handling-history` | #12 is listed as a quirk, but the approved divergence lacks an `approval` block. | #12 |
| `missing` | `track-cargo.domain-route-state` | The preserved #52 ruling is listed as a quirk, but lacks an `approval` block. | #52 |
| `missing` | `track-cargo.next-activity` | The preserved #52 ruling is listed as a quirk, but lacks an `approval` block. | #52 |
| `untested` | — | Full mutation score and the Python 3.13 profile runtime are not yet proven in the required environment. The configured mutation run is still in progress; available Python is 3.12.15. | Follow-up not filed |
| `untested` | — | No human legacy/Django side-by-side comparison has been completed. The target browser run is not a substitute for that review. | Follow-up not filed |

No missing target component or misplaced responsibility was found in the direct code/test audit.
The map finding is a target integration defect, not a source quirk. No issue-creation operation was
available in this session; the two map findings are reported here for follow-up rather than given
invented issue links.

## Human check

The reproducible run instructions and per-capability/per-golden checklist are in
`docs/side-by-side-check.md`. A human has **not** yet performed and recorded the legacy-versus-Django
comparison. The target was exercised in a browser after migrations, sample seeding and Tailwind
build: ABC123 displayed `In port New York`, UTC history, ETA and next activity; an unknown ID showed
the approved message with no cargo/history/map content. The map iframe's response was HTTP 200 but
had `X-Frame-Options: DENY`, so its content was refused in the browser. The map-frame and
map-integration human checks remain pending.

No target graph artifact is present under `.migration/graphs`; the source knowledge and domain
graphs are present. The target components and flows were therefore checked directly against code,
tests, goldens and the differential run, but graph-to-target comparison could not be performed.
