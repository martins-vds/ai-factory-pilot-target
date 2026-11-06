# External routing test method lacks a JUnit annotation

## Question
Should the source's unannotated `testCalculatePossibleRoutes` method be treated as legacy test coverage?

## Evidence
- Source: `src/test/java/org/eclipse/cargotracker/infrastructure/routing/ExternalRoutingServiceTest.java:42-44` has a TODO comment followed by `public void testCalculatePossibleRoutes()` with no `@Test` annotation.
- Characterization: graph analysis identifies this method as a route test, but the source method declaration is not annotated for JUnit; its assertions therefore are not automatically discovered as a JUnit test.
- Why it looks wrong: the method name and assertions suggest coverage, but standard JUnit discovery will not execute it as written.

## Impact
- Ledger capabilities: `booking.routing.candidates`
- Blocks: relying on this method as executable legacy evidence; the routing implementation inventory itself is not blocked.

## Options
1. Preserve the source test inventory as-is and do not claim this method as executed coverage.
2. Correct the source test in a separately approved source-maintenance task and then use it as evidence.
3. Other
