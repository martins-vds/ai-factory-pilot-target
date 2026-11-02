# Slice Track Cargo — acceptance evidence

- Tickets: TC-02–TC-15 · Audited target commit: `7b78de8` · Date: 2026-11-02 UTC
- Slice epic: `martins-vds/ai-factory-pilot-target#9` · Decision map: `#3`
- Pinned source: `eclipse-ee4j/cargotracker@f3beacf78de4f6d34edc4971ac87e38a5c6fe59d`

## Verdict

**Gaps remain.** Build, idiom, tests, CRAP and differential checks pass in the available
environment, but the configured full mutation run scores **0.797**, below the required 0.8. The
browser check found a broken embedded-map flow, ledger approval metadata is incomplete for two
approved rulings, and the source graph metadata does not match the pinned SHA. The declared Python
3.13 target could not be exercised because only Python 3.12.15 is installed. The human
legacy/Django side-by-side comparison remains pending; its procedure and checklist are in
[side-by-side-check.md](../../../docs/side-by-side-check.md).

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
| Full mutation | `python .migration/harness/tools/afs-mutation --all` | First invocation: **0.602** without DB variables; configured run: **0.797** (779 killed, 198 survived, 0 skipped; 53 files), exit 1 vs. 0.8 threshold | `mutation-full`, `mutation-full-configured` |
| Browser / UI | Interactive browser check of the target tracking page and map iframe | **Fail:** tracking result renders; iframe request returns 200 with `X-Frame-Options: DENY`, so browser refuses the map | Browser observation below; no browser command is defined in `profile.yaml` |

The first full-suite attempt could not connect to PostgreSQL; after starting PostgreSQL 17 and
setting the local connection variables, the complete suite passed. The first mutation invocation
did not inherit those database variables, so its score is not a clean measurement of database-backed
mutants. The configured run inherited the PostgreSQL settings and is the authoritative full-run
result; it missed the threshold by 0.003. All automated gate commands used Python **3.12.15**; the
profile specifies Python 3.13, which is not installed in this environment. Therefore the
profile-runtime gate result remains unverified.

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
| `untested` | — | The configured full mutation score is 0.797, below 0.8 (198 mutants survived); the Python 3.13 profile runtime is unavailable here. | Follow-up not filed |
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

The source knowledge/domain graph metadata and `graph-check.md` identify analyzed commit
`a8cdf52effc852af7a9218b40bedb98b8451d4ae`, while `SNAPSHOT.txt` and `.migration/source.lock`
identify the pinned source as `f3beacf78de4f6d34edc4971ac87e38a5c6fe59d`. The graph is therefore not
fresh for the pinned source. No target graph artifact is present under `.migration/graphs`.
Target components and flows were checked directly against code, tests, goldens and differential
evidence; the graph discrepancy remains unresolved.

## Re-audit — 2026-11-02 UTC

- Re-audited target revision: `1ff3974d115b42f19e6af77433f8f6ca85dd5d7e`
- Source: `.source` and `.migration/source.lock` both resolve to
  `f3beacf78de4f6d34edc4971ac87e38a5c6fe59d`; `afs-services check` reported `services OK: db`.
- Fresh gate records are in `.migration/evidence/runs/TC-15.md`. The profile declares Python 3.13;
  this environment executes Python 3.12.15 and has no `python3.13` executable.

### Fresh gates

| Gate | Profile command | Exit / result |
|---|---|---|
| Build: compile | `python -m compileall -q src` | 0 |
| Build: Django | `python manage.py check` | 0 |
| Idiom: lint | `ruff check` | 0 |
| Idiom: format | `ruff format --check` | 0; 108 files already formatted |
| Tests | `pytest -q` | 0; 188 passed |
| CRAP | `lizard --csv src`; `crap.py .migration/runs/lizard.csv --lcov coverage.lcov --max 30` | 0; journal result `gate=crap max=14.0 threshold=30 over=0 methods=98` |
| Changed mutation | `python .migration/harness/tools/afs-mutation --changed-since origin/main` | 0; journal result `gate=mutation score=n/a reason=no-mutable-code-changed base=origin/main` |
| Full mutation | `python .migration/harness/tools/afs-mutation --all` | 0; journal result `gate=mutation score=0.815 threshold=0.8 killed=797 survived=181 files=53 base=all` |

The mutation score is copied verbatim from the latest profile-command result in the journal. This
fresh full run meets the 0.8 threshold. The differential replay also passed all 8 golden cases, and
the five named tests for approved rulings #12, #13, #14, #17 and #52 passed.

### Browser / end-to-end check

After running the profile migrations, sample seed and Tailwind build through `afs-run`, the tracking
page rendered in a browser with built static assets and no console errors. Submitting `ABC123`
rendered the `In port New York` result, ETA, next activity and three history events. Its
`/tracking/map/` iframe loaded with HTTP 200 and `X-Frame-Options: SAMEORIGIN`; the frame reached
`document.readyState=complete`, rendered the Leaflet map with 3 markers, and loaded OpenStreetMap
tiles and marker assets. An unknown ID showed the visible not-found alert without cargo-dependent
content or a map. The frame route, response header and rendered map resolve the prior broken-flow and
integration findings.

### Earlier findings re-proved

| Earlier finding | Re-audit outcome and evidence |
|---|---|
| Map iframe was blocked by `X-Frame-Options: DENY`; `/tracking/map/` was missing. | **Resolved.** `src/cargotracker/urls.py` routes `/tracking/map/`; `map_frame` has a view-scoped `xframe_options_sameorigin` decorator. Browser observed HTTP 200, `SAMEORIGIN`, Leaflet and 3 markers in the iframe. |
| Ledger approval metadata and map evidence symbols were stale. | **Resolved for the cited entries.** `handling-history` has approval #12; `domain-route-state` and `next-activity` have approval #52. The map-frame and map-status-code symbols now match their test definitions. All 19 ledger entries have tickets, non-empty target components and evidence; all 72 target component references resolve, and no evidence test symbol was stale in the scan. |
| Full mutation score was below 0.8. | **Resolved.** The fresh, configured `--all` run scored 0.815 (see the journal Result column above). |
| `track-cargo.data-voyage` cited absent historical run logs. | **Partially unresolved.** Eleven `.migration/runs/TC-03/...` log paths in that entry do not exist. Its durable TC-03 journal, voyage domain/repository tests, current passing 188-test suite and differential run do exist, so the capability is verified now; the dead historical links remain incorrect ledger evidence. |
| Python 3.13 profile runtime was unavailable. | **Still unverified.** Fresh gates ran on Python 3.12.15; the required 3.13 executable is absent. |
| Human legacy/Django side-by-side comparison was pending. | **Still pending.** `docs/side-by-side-check.md` has unchecked capability and golden-case checklists and explicitly says it is not evidence of human completion. This browser check exercises only the target. |
| Source graph freshness and target graph were unresolved. | **Still unresolved.** `SNAPSHOT.txt` now matches the pinned SHA, but both source graph JSON `project.gitCommitHash` values and `graph-check.md` still identify `a8cdf52effc852af7a9218b40bedb98b8451d4ae`. `check_graph.py` found no endpoint/screen/page/service nodes, no reads/writes/routes edges, and no path from `track.xhtml` or `CargoTrackingViewAdapter` to data. No target graph is tracked under `.migration/graphs`; the graph-refresh plugin and SDK are absent here. |

### Re-audit gap list and verdict

| Class | Ledger entry | Remaining gap |
|---|---|---|
| `untested` | `track-cargo.data-voyage` | Eleven historical raw-log links are dead, although current durable tests and journal evidence pass. |
| `untested` | — | Python 3.13 profile runtime was not exercised; only Python 3.12.15 is available. |
| `untested` | — | Human legacy-versus-target side-by-side review remains unchecked. |
| `graph inconsistency` | — | Source graph metadata is stale against its snapshot marker; the target graph was not refreshed or produced. |

No new source quirk was identified. All 19 capabilities have a target and passing current test or
differential evidence; the browser flow now connects through the embedded map. **Slice gates pass,
but the audit verdict remains gaps-remain** for the stale evidence links, unavailable profile
runtime, pending human comparison and unresolved graph state. No tickets or quirk drafts were filed,
as directed.
