# HR-04E handling-registration differential

- Ticket: HR-04E (#131) · correction issue: #168
- Source: `eclipse-ee4j/cargotracker@f3beacf78de4f6d34edc4971ac87e38a5c6fe59d`
- Replay: `pytest -q tests/differential/test_handling_registration.py`, journal entry `differential-corrected`
- Source goldens were not modified. The replay has 13 failing and 15 matching golden cases; the other two differential-test cases pass.

## Approved replacements applied

| Decision | Explicit target expectation |
|---|---|
| #12 | `unknown_tracking_id`: assert no cargo/status section, no history section, and no empty-history label. |
| #13 | Replace source destination-based IN_PORT text with the last-known-location text: `event_receive`, `event_customs` → New York; `event_unload` → Dallas; `misdirected_off_itinerary` → Tokyo; `two_reports_ordered_by_completion_time`, `load_without_voyage`, `unknown_location`, `unknown_voyage` → Hong Kong. Other status fields remain compared. This matches the explicit #13 comparison in `tests/differential/test_track_cargo.py`. |
| #17 | `event_claim`: assert ETA is absent; pre-claim cases retain their characterized ETA. |
| #87 / ADR-0004 | `two_reports_ordered_by_completion_time`: the source cargo snapshot says `NOT_RECEIVED`/`Unknown`, while its independently observed history contains RECEIVE and CUSTOMS and its tracking map says Hong Kong. For the atomic target, expect `IN_PORT`/`CNHKG`. In the three rejected-reference cases (`load_without_voyage`, `unknown_location`, `unknown_voyage`), the source cargo snapshot says `MISROUTED` while its tracking map says `NOT_ROUTED`; preserve `NOT_ROUTED`, consistent with the no-itinerary delivery rule and the atomic snapshot. |
| #88 | Preserve each malformed input shape; assert target 400 JSON field errors, including the approved replacement for source 500s on `unparseable_time` and `unknown_event_type`. Valid reports remain 204 with UTC inputs. No approval covers accepted-response Content-Type. |
| #136 | The two-report golden has distinct completion dates (+1 and +2), so it does not exercise a tie. The target's tie replacement remains asserted by `tests/handling/test_domain.py::test_handling_history_breaks_completion_time_ties_by_registration_time_then_id` and the two equal-time processing tests; all four parameterized checks passed in `ruling-136`. |

The test now uses one fixed reference instant for sample seeding, submitted-date substitution, and date normalization. Deliberately malformed values remain untouched by substitution.

## Remaining case/field differences

Every listed POST is an accepted 204. Source goldens record an empty Content-Type; target Django responses expose `text/html`. This is not waived by #88.

| Case | Remaining field | Expected | Observed |
|---|---|---|---|
| `event_claim` | `post.content_type` | `''` | `text/html` |
| `event_customs` | `post.content_type` | `''` | `text/html` |
| `event_load` | `post.content_type` | `''` | `text/html` |
| `event_load_dallas` | `post.content_type` | `''` | `text/html` |
| `event_receive` | `post.content_type` | `''` | `text/html` |
| `event_unload` | `post.content_type` | `''` | `text/html` |
| `load_without_voyage` | `post.content_type` | `''` | `text/html` |
| `misdirected_off_itinerary` | `post.content_type` | `''` | `text/html` |
| `two_reports_ordered_by_completion_time` | `posts[0].content_type`, `posts[1].content_type` | `''`, `''` | `text/html`, `text/html` |
| `unknown_location` | `post.content_type` | `''` | `text/html` |
| `unknown_tracking_id` | `post.content_type` | `''` | `text/html` |
| `unknown_voyage` | `post.content_type` | `''` | `text/html` |
| `unload_at_destination` | `post.content_type` | `''` | `text/html` |

The following history fields also differ. In each listed row, source expects `<TODAY…> 12:00 PM UTC`; target observes the same date at `12:00 AM UTC`.

| Case | Remaining fields |
|---|---|
| `event_claim` | `tracking.history.rows[1,2,5,6,7,8,9].time` |
| `event_customs` | `tracking.history.rows[1,2].time` |
| `event_load` | `tracking.history.rows[1,2,5].time` |
| `event_load_dallas` | `tracking.history.rows[1,2,5,6,7].time` |
| `event_receive` | `tracking.history.rows[1].time` |
| `event_unload` | `tracking.history.rows[1,2,5,6].time` |
| `load_without_voyage` | `tracking.history.rows[0,1].time` |
| `misdirected_off_itinerary` | `tracking.history.rows[1,2,5,6,7,8,9,10].time` |
| `two_reports_ordered_by_completion_time` | `tracking.history.rows[0,1].time` |
| `unknown_location` | `tracking.history.rows[0,1].time` |
| `unknown_voyage` | `tracking.history.rows[0,1].time` |
| `unload_at_destination` | `tracking.history.rows[1,2,5,6,7,8].time` |

Pinned source `HandlingEvent.java` maps completion and registration with `@Temporal(TemporalType.DATE)`, while immediate runtime goldens retain noon values. Target `HandlingEventRecord` stores both as dates and reconstructs midnight. The evidence does not establish why those source runtime observations retain noon; no root cause is asserted. Target date persistence also collapses distinct same-day completion times into ties, and date-only registration persistence can remove the #136 registration-time distinction before event ID is considered. This remains unresolved for implementation review.

## Gate outcome

`build-compile`, `build-django-check`, both idiom commands, CRAP calculation, and the final mutation invocation exited 0. `behavior`, the coverage command, and `regression` each exited 1 with the same 13 timestamp/Content-Type differential cases (305 passed, 13 failed for the full suite). The coverage command's failure is not the CRAP metric: `crap-score` independently reported max CRAP `19.0` against threshold `30`. Mutation reported `n/a: no mutable code changed` after the shallow checkout's `origin/main` history was fetched.

Full gate rows and hashes: `.migration/evidence/runs/HR-04E.md`.
