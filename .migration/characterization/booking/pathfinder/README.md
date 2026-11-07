# Pathfinder REST response

Captured 2026-11-07 from the pinned source (`f3beacf78de4f6d34edc4971ac87e38a5c6fe59d`) running on Java 8 / Payara 4.1.2.181. The successful startup and requests are recorded in [the BK-03B run journal](../../../evidence/runs/BK-03B.md).

Each case has four files: `.status` is the HTTP status code, `.content-type` is the response `Content-Type` value, `.headers` is the response header block as received, and `.body` is the response body bytes as received. No formatting or normalization was applied to the bodies.

| Case | Request | Status | Content-Type | Body |
|---|---|---:|---|---|
| `normal-1` | `GET /cargo-tracker/rest/graph-traversal/shortest-path?origin=CNHKG&destination=USNYC` | 200 | `application/json` | [`normal-1.body`](normal-1.body) |
| `normal-2` | Same as `normal-1` | 200 | `application/json` | [`normal-2.body`](normal-2.body) |
| `normal-3` | Same as `normal-1` | 200 | `application/json` | [`normal-3.body`](normal-3.body) |
| `deadline` | Same as `normal-1`, with `&deadline=2030-01-01T00:00:00Z` | 200 | `application/json` | [`deadline.body`](deadline.body) |
| `four-character-origin` | `GET /cargo-tracker/rest/graph-traversal/shortest-path?origin=CNHK&destination=USNYC` | 400 | `text/plain` | [`four-character-origin.body`](four-character-origin.body) |
| `missing-destination` | `GET /cargo-tracker/rest/graph-traversal/shortest-path?origin=CNHKG` | 400 | `text/plain` | [`missing-destination.body`](missing-destination.body) |

## JSON contract

The success body is a JSON array of path objects. Each path object's only field is `transitEdges`. Each edge's fields appear in this order:

1. `fromDate`
2. `fromUnLocode`
3. `toDate`
4. `toUnLocode`
5. `voyageNumber`

Both `fromDate` and `toDate` use `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`: exactly three fractional-second digits and a literal UTC `Z`, not a numeric offset. For example, the captured values include `2026-11-08T23:12:13.516Z`.

The three baseline responses each contain four candidate paths; the deadline response contains three. Candidate counts are randomized from three to five, so that count difference does not demonstrate a deadline effect. The `deadline` parameter is accepted but does not affect the response: the source `GraphTraversalService.findShortestPath` does not read it (`.source/src/main/java/org/eclipse/pathfinder/api/GraphTraversalService.java:34-77`). The body still varies between calls because routes and dates are randomized.

The four-character origin body is `size must be between 5 and 5 (path = __EJB31_Generated__GraphTraversalService__Intf____Bean__.findShortestPath.arg0, invalidValue = CNHK)` followed by a newline. The missing-destination body is `may not be null (path = __EJB31_Generated__GraphTraversalService__Intf____Bean__.findShortestPath.arg1, invalidValue = null)` followed by a newline. The `.body` goldens preserve the exact response bytes.

The legacy test `BookingServiceTest.testRouteCandidates` asserts that candidate routes are non-empty; it does not assert the REST serialization.
