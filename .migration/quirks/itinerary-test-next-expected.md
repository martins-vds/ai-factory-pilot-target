# Quirk: Itinerary next-activity test is an empty TODO

## Question
The source's `ItineraryTest.testNextExpectedEvent` contains no assertions; should this legacy-test coverage gap be tracked as a quirk, or retired after the new characterization test is accepted?

## Evidence
- Source: `src/test/java/org/eclipse/cargotracker/domain/model/cargo/ItineraryTest.java:85-88` at the pinned SHA.
- Characterization: `ItineraryTest::testNextExpectedEvent` passes but performs no setup or assertions.
- Why it looks wrong: the ledger says this test covers next-activity predictions, but the method is an empty TODO.

## Impact
- Ledger capabilities: `track-cargo.next-activity`, `track-cargo.domain-route-state`
- Blocks: `martins-vds/ai-factory-pilot-target#10`

## Options
1. Preserve the empty legacy test and rely on the new tier-B characterization coverage.
2. Fix the source test in a separate source change.
3. Other
