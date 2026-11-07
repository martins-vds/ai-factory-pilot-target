# Cargo lifecycle scenario method is not a JUnit test

## Question
Should `CargoLifecycleScenarioTest.testCargoFromHongkongToStockholm` remain an unannotated scenario method or be made discoverable as a JUnit test?

## Evidence
- Source: `.source/src/test/java/org/eclipse/cargotracker/scenario/CargoLifecycleScenarioTest.java:40,80` declares the class and method without `@Test`; the class does not extend `TestCase` or declare a JUnit runner.
- Characterization: the method contains booking, route-assignment and lifecycle assertions, but standard JUnit discovery does not execute it.
- Why it looks wrong: its `Test` class and method names suggest executed test coverage that is not provided.

## Impact
- Ledger capabilities: `booking.wizard-chain`, `booking.registration`, `booking.routing-assign`
- Blocks: counting this method as executed legacy-test evidence in slice `booking` until a human decides.

## Options
1. Preserve the source test inventory as-is and do not count the method as executed evidence.
2. Add a JUnit annotation in a separately approved source-maintenance task and then use it as executed evidence.
3. Other
