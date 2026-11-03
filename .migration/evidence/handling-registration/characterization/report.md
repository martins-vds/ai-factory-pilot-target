# Handling registration characterization

- Ticket: HR-03 · source: `eclipse-ee4j/cargotracker@f3beacf78de4f6d34edc4971ac87e38a5c6fe59d`
- Run journal: [HR-03](../../runs/HR-03.md)
- Tier-A suite: `characterization/handling-registration/test_handling_registration.py`
- Tier-B suite: `characterization/handling-registration/tier_b/HandlingRegistrationCharacterizationTest.java`, run by `characterization/handling-registration/run-tier-b.sh`

## Tier A — running Payara

The source was copied to a scratch directory, built and deployed with Java 8 and
Payara 4.1.2.181. The first page probe returned HTTP 200. The 21-test pytest
suite passed on both the golden-record and clean replay runs. Its 28 golden
cases cover 29 POSTs; all 28 predictions matched the observed output.

| Cases | Predicted behavior | Observed behavior |
|---|---|---|
| 4 missing required fields; 9 malformed-length inputs | HTTP 400 | HTTP 400 |
| Unparseable 16-character time; unknown 7-character event type | HTTP 500 | HTTP 500 |
| RECEIVE, CUSTOMS, LOAD, UNLOAD, destination UNLOAD, CLAIM; off-itinerary UNLOAD | HTTP 204; event history and cargo state follow the seeded itinerary, with the off-route event misdirected | HTTP 204; public tracking history and `GET /rest/cargo` matched the expected state |
| Two quick reports for DEF789 with reversed submission/completion order | HTTP 204 for both; history sorted by completion time | HTTP 204 for both; the earlier completion appeared first |
| Unknown tracking ID, voyage, location, and LOAD without voyage | HTTP 204 at the door; no visible cargo/history change | HTTP 204; no visible trace within the bounded two-second observation window |

The individual inputs, predictions, comparison flags, and normalized public
observations are committed in `characterization/handling-registration/golden/`.
Dates are represented as signed offsets from today. Error bodies and other
volatile server output are intentionally omitted.

The source's one-second registration-attempt TTL is not asserted with a timing
race. The tier-B producer test observed `setTimeToLive(1000)` and verified the
registration-attempt queue is declared in `web.xml`. Unknown-reference HTTP
cases reproduce the accepted-at-the-door/no-visible-trace behavior; source
inspection shows the registration consumer rethrows failures and the declared
rejected-attempts queue has no producer.

## Tier B — unreachable branches and source tests

The scratch-copy suite ran 27 tests successfully: 10 focused characterization
tests plus the source-owned `HandlingEventTest` (6), `HandlingHistoryTest` (2),
and `CargoTest` (9).

- `DefaultCargoInspectionService.inspectCargo`: missing cargo returns without
  lookups or side effects; existing cargo is re-derived, stored, and emits the
  inspection event; misdirected and destination-unload conditions emit their
  respective application notifications.
- `HandlingEventFactory`: known cargo/location resolves; unknown cargo,
  voyage, and location fail with their typed exceptions; LOAD without a voyage
  fails during event construction.
- The source's no-voyage event accessor returns `Voyage.NONE`.
- `HandlingHistoryTest` confirms distinct completion-time ordering and the most
  recently completed event. `HandlingEventTest` confirms event/voyage
  construction rules. `CargoTest` confirms misdirection and destination-unload
  domain outcomes.
- `HandlingEventServiceTest.testRegisterEvent` and
  `CargoLifecycleScenarioTest.testCargoFromHongkongToStockholm` are present in
  the source tree but are not JUnit-discoverable (no test annotations or
  `TestCase` superclass); their setups/expectations are commented out. They
  were inventoried but not treated as executable evidence.

## Ruled behaviors and findings

- #94: attempt expiry is 1,000 ms at the JMS producer boundary; not timed
  through the live endpoint because it is not reliably reproducible.
- #95: unknown references are accepted by REST and produce no public trace;
  internal rejection is not surfaced to the submitter.
- #88: invalid field lengths return 400, while an unparseable time or unknown
  event type returns 500.
- No prediction mismatches or new quirks were found. Existing decision tickets
  #94, #95, and #88 cover the observed quirks.
