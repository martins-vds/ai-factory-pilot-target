# HR-04E-TIME — source timestamp persistence and reload

Research for [#172](https://github.com/martins-vds/ai-factory-pilot-target/issues/172),
under [#131](https://github.com/martins-vds/ai-factory-pilot-target/issues/131), informing
[quirk #171](https://github.com/martins-vds/ai-factory-pilot-target/issues/171).
**No quirk option is selected and no target behavior is changed.**

## Result (measured, tier A)

The pinned source retains time-of-day in its EclipseLink identity maps immediately
after handling, but Derby stores **DATE** values for both completion and registration.
After explicitly clearing those maps, the same source events reload at midnight.
The public history changes from `11/03/2026 12:34 PM UTC` to
`11/03/2026 12:00 AM UTC`. This is not inferred from a second HTTP request alone.

- Source: Eclipse Cargo Tracker `f3beacf78de4f6d34edc4971ac87e38a5c6fe59d`.
- Runtime: Java `1.8.0_504`, Payara `4.1.2.181`, its EclipseLink and embedded
  disk-backed Derby, JVM and client `TZ=UTC`.
- Reference: `2026-11-04T13:34:57.280648+00:00` (clean replay).
- Exact inputs, timestamps, IDs, cached values, SQL values/types, public output and
  reload SELECT: [replay observation](observed-20261104-replay.json).
- The [first successful observation](observed-20261104.json) independently reproduces
  the result. Its `sent_utc` was recorded after the POST response; the replay records
  separate send and response times. Its SQL window also includes observer SQL;
  the replay closes that window **before** the observer's post-reload query.
- Commands and raw-log fingerprints: [append-only journal](../../../.migration/evidence/runs/HR-04E-TIME.md).
- [Characterizer return](../../../.migration/returns/HR-04E-TIME.afs-characterizer.yaml).

## Fixture and demonstrated reload boundary

The source graph was queried first for `HandlingEvent`, `HandlingHistory`,
`JpaHandlingEventRepository`, `SampleDataGenerator`, and `HandlingReportService`,
then for the view adapter and relevant source tests. File reads below settled
details not represented in those graph summaries.

The runner creates a private `/tmp/hr-04e-time.*` directory, a new Payara
`timestamp-reload` domain (port base `19000`, HTTP `19080`, admin `19048`), and a
private database directory. It builds an otherwise unmodified scratch copy of the
read-only source, using the source's existing Maven `webapp.databaseTempDir` property
to select that directory. It also sets the existing graph-traversal URL property
to the private HTTP port. No shared running application/database is contacted.
The domain and private files are stopped/removed on exit.

The separate experiment-only `timestamp-probe.war` runs in that domain. It locates
the **source's** EclipseLink session by its actual HandlingEvent descriptor:

1. `Session.executeSQL` reads the real handling rows, bypassing entity caches.
   `SYS.SYSCOLUMNS` reports both column types as `DATE`; SQL casts show date-only values.
2. The probe reads cached HandlingEvent getters for the same row IDs, without
   creating events or changing rows.
3. POST invokes the source session's
   `getIdentityMapAccessor().initializeAllIdentityMaps()`. Both inspected IDs are
   absent from the maps immediately afterward (`cached: []`, `cache_empty: true`).
   SQL row IDs and values remain unchanged.
4. The tracking helper opens a new HTTP session/view and submits DEF789 through
   the real public tracking form. A source
   `SELECT ID, completionTime, registration, TYPE, cargo_id, location_id, voyage_id
   FROM HANDLINGEVENT WHERE (ID = ?)` is captured during this read, before any
   subsequent observer query. Both event getters now return midnight instants.

This clears the provider cache and obtains fresh source entity reads against the
same database; it does **not** restart or redeploy Cargo Tracker. Restart was
deliberately avoided: `SampleDataGenerator.java:51-81` unconditionally deletes
existing entities and reseeds on startup, which would destroy the submitted events.
The observer is instrumentation in a separate WAR, not a patched source endpoint,
mock, in-memory database, or substitute JPA provider.

## Predicted versus observed

Two format-valid reports are sent sequentially to
`http://127.0.0.1:19080/cargo-tracker/rest/handling/reports` for DEF789 / CNHKG,
both with completion `2026-11-03 12:34`: RECEIVE, then CUSTOMS. Each POST returns
204, and processing/public appearance is confirmed before sending the next report.

| Case / prediction before measurement | Observed on clean replay | Match |
|---|---|---|
| Immediate history retains non-midnight time, like the prior noon goldens | Both rows show `11/03/2026 12:34 PM UTC` | Yes |
| DATE mappings produce date-only persisted completion and registration | IDs 55/56 store completion `2026-11-03`, registration `2026-11-04`; both SQL types DATE | Yes |
| Clearing caches and rereading loses time-of-day | Same IDs and SQL rows; completion `2026-11-03T00:00:00Z`, registration `2026-11-04T00:00:00Z`; public history midnight | Yes |
| Distinct same-day registration instants collapse after reload | Before: `13:34:58.261Z` and `13:34:59.483Z` on November 4; afterward both midnight November 4 | Yes |

These are four checked predictions in one live experiment test, repeated on two
independently created private databases. No prediction mismatch occurred.

### Ordering implications for #136

The completion-time tie uses different event types so source equality does not
deduplicate the pair. The first run shows RECEIVE followed by CUSTOMS, before and
after the clear. The clean replay instead shows CUSTOMS followed by RECEIVE,
before and after the clear, despite RECEIVE having the earlier registration
instant and lower ID. The replay therefore does **not** follow ascending
registration-time or event-ID order. The source comparator uses completion only,
after building a HashSet
(`HandlingHistory.java:32-36,75-79`). Registration and ID are excluded from source
event equality (`HandlingEvent.java:237-246`).

The two distinct registration instants are demonstrably unavailable after reload.
Thus, sorting date-only reloaded values cannot recover their original sub-day
registration order. This fixture does not distinguish a proposed registration-first
target policy from an ID-first target policy, because IDs and registration instants
increase together; the source replay follows neither ascending policy. It does not
amend the approved target rule in #136 or decide how #171 should reconcile it.

## Source-derived explanation and legacy test inventory

All source paths below are relative to the read-only checkout root `.source/`
at the revision above; they explain, rather than replace, the live measurements.

- `src/main/java/org/eclipse/cargotracker/domain/model/handling/HandlingEvent.java:65-72`:
  completion/registration are `@Temporal(TemporalType.DATE)`.
- `src/main/webapp/WEB-INF/web.xml:71-75` and `pom.xml:46-49`: embedded Derby URL and
  the configurable database directory (default `/tmp`).
- `src/main/java/org/eclipse/cargotracker/application/internal/DefaultHandlingEventService.java:33-50`:
  creates the event's registration time at processing and stores it. The REST
  attempt also captures a time (`interfaces/handling/rest/HandlingReportService.java:58-60`);
  the recorded event registration values are **not claimed to be the attempt times**.
- `src/main/java/org/eclipse/cargotracker/infrastructure/persistence/jpa/JpaHandlingEventRepository.java:21-31`:
  persist and named-query history read.
- `src/main/java/org/eclipse/cargotracker/interfaces/tracking/web/Track.java:65-71`:
  public tracking queries handling history.
- `src/main/java/org/eclipse/cargotracker/interfaces/tracking/web/CargoTrackingViewAdapter.java:19,153-158`:
  formats the event's completion time as `MM/dd/yyyy hh:mm a z`.
- `src/test/java/org/eclipse/cargotracker/domain/model/handling/HandlingHistoryTest.java:25-40`:
  constructs events in memory; checks deduplication despite different registration
  times, completion ordering, and the most recent event. No JPA reload.
- `src/test/java/org/eclipse/cargotracker/domain/model/handling/HandlingEventTest.java`:
  event construction/voyage/location rules, not persistence.
- `src/test/java/org/eclipse/cargotracker/application/HandlingEventServiceTest.java:24-52`:
  commented-out setup/expectations; `testRegisterEvent` has no JUnit annotation.
  No direct handling repository/persistence test was found in the source test tree.
- `src/test/java/org/eclipse/cargotracker/application/BookingServiceTest.java:84-90,140-248`:
  Arquillian/JPA integration tests for booking, routing and destination/deadline
  changes; date assertions compare cargo deadline days, not handling completion or
  registration precision across a cleared context. This suite was inventoried,
  not executed in this research.

## Reproduce and limitations

From the repository root, install the **existing** characterization dependencies
from `characterization/track-cargo/requirements.txt`, then run:

```bash
repo=/home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target
cd "$repo"
"$repo/.migration/harness/tools/afs-run" --ticket HR-04E-TIME --name timestamp-reload -- \
  env JAVA_HOME=/usr/lib/jvm/temurin-8-jdk-amd64 \
  HR_04E_TIME_OUTPUT=/tmp/hr-04e-time-new-observation.json \
  bash "$repo/characterization/handling-registration/run-timestamp-reload.sh"
```

Use an unused output path (exclusive creation), free private-domain ports, and a
UTC window in which the two processing instants fall on the same day. The runner
checks the pinned SHA and Java 8. Packaging uses `-DskipTests`; executed evidence is
the nested pytest run, **not** Maven source unit tests. One initial collection
attempt failed because `requests` was absent; installing the already-pinned
requirements resolved it. Both subsequent live runs passed.

The preliminary existing-runner smoke probe used its default database path; it is
only boot/build evidence, not the isolated persistence experiment.
No application-restart result, other provider/database/timezone behavior, duplicate
same-type collapse, reversed-ID registration-order fixture, or midnight-crossing
registration pair is claimed. Full target gates/mutation are not relevant to this
source-only research. Existing source goldens, production files, other roles'
returns and earlier evidence remain unchanged. The operator still owns #171.
