# TC-14 — Track Cargo differential replay

- Ticket: `martins-vds/ai-factory-pilot-target#34`
- Source: all eight records in `characterization/track-cargo/golden/`
- Target: Django tracking view and map frame, seeded with `seed_sample_data`
- Date normalization: UTC dates are rendered in the source format and normalized to `<TODAY>` or a signed day offset.
- Requests: each golden input is submitted through both the regular form and htmx path; observable result, history, and map data are compared field by field.

## Results

| Golden input | Result fields | History | Map query and frame |
|---|---|---|---|
| `abc123` (`ABC123`) | Match except approved ruling #13: status is `In port New York`; destination remains Helsinki, ETA `<TODAY+14> 12:00 AM UTC`, next activity and misdirected flag match. | All 3 rows, text, UTC times, and expectation flags match. | IN_PORT, locations, and exact coordinates match. |
| `def789` (`DEF789`) | Status, destination Melbourne, unknown ETA, no next activity, and misdirected flag match. | Empty-history label and zero rows match. | NOT_ROUTED, location fields, and exact coordinates match. |
| `jkl567` (`JKL567`) | Status, destination Stockholm, unknown ETA, absent next activity, and misdirected flag match. | All 4 rows, including the unexpected final event, match. | MISDIRECTED, location fields, and exact coordinates match. |
| `mno456` (`MNO456`) | Status, destination Dallas, no ETA per ruling #17, no next activity, and misdirected flag match. | All 5 rows, text, UTC times, and expectation flags match. | **Mismatch:** golden status is CLAIMED; both target map query and frame report AT_DESTINATION. Other location fields and marker coordinates match. |
| `padded-id` (` ABC123 `) | Trimmed ID and all result fields match, with approved ruling #13 status text. | All 3 rows match. | IN_PORT, locations, and exact coordinates match. |
| `lowercase-id` (`abc123`) | No cargo result; ruling #12 visible not-found message is present. | No history section is rendered, per ruling #12. | No map query or frame is rendered, per ruling #12. |
| `empty-id` (`""`) | No cargo result; ruling #12 visible required-field message is present. | No history section is rendered, per ruling #12. | No map query or frame is rendered, per ruling #12. |
| `unknown-id` (`NOPE000`) | No cargo result; ruling #12 visible not-found message is present. | No history section is rendered, per ruling #12. | No map query or frame is rendered, per ruling #12. |

Ruling #14 is asserted by comparing each rendered marker coordinate with the configured coordinate for its LOCODE; all markers match. The htmx and regular requests produced identical normalized observable data for all eight inputs. No broad snapshot exclusions are used.

### Finding from initial run — resolved

For MNO456, `map_query.statusCode` and `map_frame.statusCode` should remain `CLAIMED` as recorded in `golden/mno456.json`, but the Django result is `AT_DESTINATION`. The target maps `unloaded_at_destination` before the transport status in `src/cargotracker/cargo/application/map_status.py:7-8`. This is not an approved divergence. It is reported without a production-code change.

PR [#63](https://github.com/martins-vds/ai-factory-pilot-target/pull/63), resolving issue [#62](https://github.com/martins-vds/ai-factory-pilot-target/issues/62), corrected the MNO456 seed snapshot so its last `CLAIM` event is no longer marked unloaded at destination.

### Preserved quirk

Ruling #52 remains preserved; the existing `tests/cargo/test_domain_calculations.py::test_quirk52_next_activity_uses_first_matching_location` passed in the full test run. It is not a divergence in the golden replay.

## Initial pre-#63 gates

| Gate | Command | Exit / result |
|---|---|---|
| Build | `python -m compileall -q src`; `python manage.py check` | 0; 0 |
| Behavior | `pytest -q` | 1 — 169 passed; MNO456 map-status mismatch above |
| Idiom | `ruff check`; `ruff format --check` | 0; 0 |
| CRAP | `lizard --csv src`; `crap.py .migration/runs/lizard.csv --lcov coverage.lcov --max 30` | 0; maximum CRAP 14 (threshold 30) |
| Changed mutation | `afs-mutation --changed-since origin/main` | Exit 0; no mutable production code changed, so no mutation score applies |
| Regression | Full `pytest -q` suite | 1 — same single MNO456 differential failure |

## Re-run after #63

The differential suite was rerun through `afs-run` as
`.migration/runs/TC-14/20261102T012108088993Z-differential-after-pr63.log`:
`python -m pytest -q tests/differential/test_track_cargo.py` — **8 passed**.
The full suite was rerun through `afs-run` as
`.migration/runs/TC-14/20261102T012124191104Z-full-suite-after-pr63.log`:
`pytest -q` — **171 passed**.

| Golden input | Result fields | History rows | Map query/frame |
|---|---|---|---|
| `abc123` (`ABC123`) | Match; ruling #13 status `In port New York`; other result fields match. | All fields match, 3 rows. | All fields and configured marker coordinates match. |
| `def789` (`DEF789`) | Match, including unknown ETA and absent next activity. | Empty-history label and no rows match. | All fields and configured marker coordinates match. |
| `jkl567` (`JKL567`) | Match, including misdirected state and absent next activity. | All fields match, 4 rows including unexpected event. | All fields and configured marker coordinates match. |
| `mno456` (`MNO456`) | Match; ruling #17 hides ETA. | All fields match, 5 rows. | `CLAIMED` status, locations, and configured marker coordinates all match. |
| `padded-id` (` ABC123 `) | Trimmed ID and result fields match; ruling #13 status named. | All fields match, 3 rows. | All fields and configured marker coordinates match. |
| `lowercase-id` (`abc123`) | Ruling #12 visible not-found message, no cargo. | No history rendered. | No map query or frame rendered. |
| `empty-id` (`""`) | Ruling #12 visible required-field message, no cargo. | No history rendered. | No map query or frame rendered. |
| `unknown-id` (`NOPE000`) | Ruling #12 visible not-found message, no cargo. | No history rendered. | No map query or frame rendered. |

Ruling #14 exact-coordinate assertions passed for all rendered markers. Regular and htmx observations match for all eight inputs. No test changes were made for the rerun.

| Gate | Command | Exit / result |
|---|---|---|
| Build | `python -m compileall -q src`; `python manage.py check` | 0; 0 |
| Idiom | `ruff check`; `ruff format --check` | 0; 0 |
| CRAP | `lizard --csv src`; `crap.py .migration/runs/lizard.csv --lcov coverage.lcov --max 30` | 0; maximum CRAP 14 (threshold 30) |
| Changed mutation | `afs-mutation --changed-since origin/main` | 0 — no mutable code changed relative to the fetched base |
| Differential | `python -m pytest -q tests/differential/test_track_cargo.py` | 0 — 8 passed |
| Behavior and regression | `pytest -q` | 0 — 171 passed |

## Ledger

All 19 `track-cargo.*` entries remain `status: migrated`, retain their target components, and reference the differential test and this report with `verification: differential`. The initial `track-cargo.map-status-code` mismatch is resolved by the seed correction in PR #63 / issue #62; all eight cases now match except the explicitly approved divergences.
