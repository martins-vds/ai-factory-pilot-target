# Track Cargo — characterization evidence

- Ticket: `martins-vds/ai-factory-pilot-target#15`
- Pinned source: `eclipse-ee4j/cargotracker@f3beacf78de4f6d34edc4971ac87e38a5c6fe59d`
- Characterization: tier A for 14 capabilities; tier B for 5 capabilities
- Ledger entries updated: all 19 `track-cargo.*.yaml` capabilities

## Tier A black-box characterization

`characterization/track-cargo/test_tracking.py` submits JSF forms using one `requests.Session`
per case, including the rendered `javax.faces.ViewState`. The eight golden cases record input,
source-derived prediction, prediction comparison, and observed status text, destination, ETA,
next activity, misdirected indicator, history rows and map-frame query parameters:

| Case | Input | Seed/result |
|---|---|---|
| `abc123` | `ABC123` | In port, three expected events |
| `jkl567` | `JKL567` | Onboard, misdirected, final event unexpected |
| `def789` | `DEF789` | Not received, unrouted, empty history |
| `mno456` | `MNO456` | Claimed, five expected events |
| `padded-id` | ` ABC123 ` | Input is trimmed and found |
| `lowercase-id` | `abc123` | Not found |
| `empty-id` | empty | Required validation prevents lookup |
| `unknown-id` | `NOPE000` | Not found |

Dates in the goldens are represented by `<TODAY>` or a signed day offset. The MNO456 comparison
records the one prediction mismatch: the initial prediction was that a claimed cargo has no ETA;
the page displays the scheduled final-arrival date, 28 days in the past. The source calculates ETA
while routing is `ROUTED` and the cargo is not misdirected, and a valid `CLAIM` leaves those
conditions true. This behavior is recorded for human review in
`.migration/quirks/claimed-cargo-past-eta.md`.

The ruled quirks are pinned by named tests:

- `test_quirk12_unknown_id_message_is_not_rendered`: the FacesMessage is not displayed; the
  no-events label can render with an empty tracking ID when no cargo is found. Empty-ID validation
  also leaves the page without a result or map.
- `test_quirk13_in_port_names_route_destination`: ABC123 says “In port Helsinki” while its last
  known location is New York.
- `test_quirk14_map_offsets_are_random_and_in_range`: the served map frame contains six uses of
  `Math.floor((Math.random() * 3) - 3)`; sampled offsets remain in `[-3, -1]` and differ between
  simulated loads. No specific offset is pinned.

## Tier B hot domain characterization

`characterization/track-cargo/tier_b/TrackCargoCharacterizationTest.java` adds five source-unit
tests to a writable temporary copy of `.source/`. They cover empty-itinerary expectation,
transport status for each declared event type, next activity from no event through receive/load/
unload/claim, and no activity for unrouted/off-track cargo. The switch defaults for event
expectation and transport status cannot be reached with the source's declared event enum values.

The five source domain test classes were run unchanged: `CargoTest` (9), `ItineraryTest` (3),
`RouteSpecificationTest` (4), `HandlingEventTest` (6), and `HandlingHistoryTest` (2), 24 tests
total. The `ItineraryTest::testNextExpectedEvent` method is an empty TODO and therefore is not
counted as coverage; the discrepancy is recorded in
`.migration/quirks/itinerary-test-next-expected.md`.

## Run evidence

| Run | Command scope | Result |
|---|---|---|
| Tier A | Payara runtime + `pytest -q characterization/track-cargo/test_tracking.py` | 12 passed; HTTP 200; `.migration/runs/15/20261031T181017511302Z-tier-a-characterization-final.log` and `.migration/runs/15/20261031T181040428604Z-tier-a-pytest-final.log` |
| Tier B | `bash characterization/track-cargo/run-tier-b.sh` | 29 passed (24 legacy + 5 characterization); `.migration/runs/15/20261031T180806878653Z-tier-b-domain.log` |
| Ledger validation | `python .migration/harness/tools/validate.py .migration` | 21 files checked, 0 errors; `.migration/runs/15/20261031T181255687813Z-ledger-validate-final.log` |

Commands and transient setup corrections are summarized in
`.migration/evidence/track-cargo/characterization/run-summary.md`.
