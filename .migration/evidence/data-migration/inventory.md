# Legacy relational data inventory — DM-02

- Issue: [martins-vds/ai-factory-pilot-target#248](https://github.com/martins-vds/ai-factory-pilot-target/issues/248)
- Slice: data-migration (#247) · Parent: #223 · Decision map: #3
- Source: `eclipse-ee4j/cargotracker@f3beacf78de4f6d34edc4971ac87e38a5c6fe59d`
- Target: `a302ef8` · ADR: [0003 — schema mirrors source](../../../docs/adr/0003-schema-mirrors-source.md)
- Snapshot: Derby `cargo-tracker`, taken `2026-11-07T00:40:49Z`; validated by the DM-02 `snapshot-validate` run (`tables=7 problems=0`).
- Source files were read through the file-view gate after graph inspection. Only CSV headers and manifest counts were read; no snapshot data rows were inspected or copied.

## Graph and table coverage

The checked-in full source graph has 1009 nodes, 2093 edges and one domain flow. Its seven `table` nodes comprise six JPA entities plus a test CSV fixture; the graph has no `SEQUENCE` node, although the database snapshot manifest includes that table. The graph itself was not rebuilt. `SEQUENCE` is recorded as a graph discrepancy, not inferred to be an entity.

The manifest reports:

| Legacy table | Rows |
|---|---:|
| CARGO | 4 |
| LEG | 7 |
| HANDLINGEVENT | 12 |
| LOCATION | 13 |
| VOYAGE | 5 |
| CARRIER_MOVEMENT | 13 |
| SEQUENCE | 1 |

These are manifest counts only. The snapshot verifier confirmed all seven files and manifest checksums; this inventory does not make row-level claims about orphans or sentinel values.

## Mapping conventions

- The source entities use `Long` generated identifiers and JPA's implicit entity table names, except `CarrierMovement`, explicitly mapped to `carrier_movement`. The CSV exporter reports unquoted Derby identifiers in uppercase. The target uses Django `BigAutoField` primary keys and the `db_table` names below.
- Embedded values are flattened into the owning row: `TrackingId` → `tracking_id`; `RouteSpecification` → `spec_origin_id`, `spec_destination_id`, `spec_arrival_deadline`; `Delivery` → delivery columns on CARGO; `HandlingActivity` → its `next_expected_*` columns; `VoyageNumber` → `voyage_number`. `Itinerary` is represented by LEG child rows, and `Schedule` by CARRIER_MOVEMENT child rows.
- `HandlingEvent.Type`, `Delivery.transportStatus`, `Delivery.routingStatus`, and `HandlingActivity.type` use `EnumType.STRING`; these are enum names, not ordinals. Target fields are character fields. No ordinal conversion is indicated.
- JPA `TemporalType.DATE` source fields are calendar dates. `TemporalType.TIMESTAMP` source fields are timestamps; the data mapping has not been authored, and the profile's UTC default should be applied to naive source timestamps. Django's date and datetime fields are listed as they exist at target commit `a302ef8`.
- The target's current HandlingEvent model uses `DateTimeField` for `completionTime` and `registration`. Migration `0003_preserve_handling_event_instants.py` converts the earlier date columns to `timestamp with time zone` at UTC; a source DATE value therefore enters at UTC midnight. This preserves the approved target behavior; reverse migration truncates to DATE.
- Source SQL types for basic Java fields follow the JPA mappings/defaults; the CSV snapshot contains headers but no typed schema. For provider-owned SEQUENCE, neither key constraints nor SQL types are declared by an in-scope JPA entity, so they remain unverified here.

## Table-by-table inventory

### CARGO → `cargo` / `CargoRecord`

Owner: `Cargo` (`.source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Cargo.java:57-78`). The row has generated `ID` as PK. Embedded mappings are in `TrackingId.java:14-20`, `RouteSpecification.java:24-37`, `Delivery.java:40-77`, and `HandlingActivity.java:24-36`; the itinerary join is in `Itinerary.java:20-36`.

| Snapshot column | Source property and type | Target column / field | Keys, relation, or conversion |
|---|---|---|---|
| ID | `Cargo.id`, `Long`, `@Id @GeneratedValue` | `id`, `BigAutoField` | PK |
| TRACKING_ID | `TrackingId.id`, `String` | `tracking_id`, `CharField(255)` | Unique |
| ORIGIN_ID | `Cargo.origin`, `Location` | `origin_id`, FK to `location` | FK to LOCATION |
| SPEC_ORIGIN_ID | `RouteSpecification.origin`, `Location` | `spec_origin_id`, FK to `location` | FK to LOCATION |
| SPEC_DESTINATION_ID | `RouteSpecification.destination`, `Location` | `spec_destination_id`, FK to `location` | FK to LOCATION |
| SPEC_ARRIVAL_DEADLINE | `RouteSpecification.arrivalDeadline`, `Date @Temporal(DATE)` | `spec_arrival_deadline`, `DateField` | DATE; no time conversion |
| TRANSPORT_STATUS | `Delivery.transportStatus`, enum `@Enumerated(STRING)` | `transport_status`, `CharField(255)` | Enum name, not ordinal |
| LAST_KNOWN_LOCATION_ID | `Delivery.lastKnownLocation`, `Location` | `last_known_location_id`, nullable FK to `location` | FK to LOCATION |
| CURRENT_VOYAGE_ID | `Delivery.currentVoyage`, `Voyage` | `current_voyage_id`, nullable FK to `voyage` | FK to VOYAGE |
| MISDIRECTED | `Delivery.misdirected`, `boolean` | `misdirected`, `BooleanField` | Boolean |
| ETA | `Delivery.eta`, `Date @Temporal(DATE)` | `eta`, nullable `DateField` | DATE |
| NEXT_EXPECTED_HANDLING_EVENT_TYPE | `HandlingActivity.type`, `HandlingEvent.Type @Enumerated(STRING)` | `next_expected_handling_event_type`, nullable `CharField(255)` | Enum name; nullable |
| NEXT_EXPECTED_LOCATION_ID | `HandlingActivity.location`, `Location` | `next_expected_location_id`, nullable FK to `location` | FK to LOCATION |
| NEXT_EXPECTED_VOYAGE_ID | `HandlingActivity.voyage`, `Voyage` | `next_expected_voyage_id`, nullable FK to `voyage` | FK to VOYAGE |
| UNLOADED_AT_DEST | `Delivery.isUnloadedAtDestination`, `boolean` | `unloaded_at_dest`, `BooleanField` | Boolean |
| ROUTING_STATUS | `Delivery.routingStatus`, enum `@Enumerated(STRING)` | `routing_status`, `CharField(255)` | Enum name, not ordinal |
| CALCULATED_AT | `Delivery.calculatedAt`, `Date @Temporal(TIMESTAMP)` | `calculated_at`, `DateTimeField` | Timestamp; interpret naive source time as UTC |
| LAST_EVENT_ID | `Delivery.lastEvent`, `HandlingEvent` | `last_event_id`, nullable FK to `HandlingEvent` | FK to HANDLINGEVENT; added as a relation in target migration `0002` |

The target model and migration include all snapshot columns. `Itinerary` contributes no scalar CARGO column; its one-to-many `legs` use `cargo_id` in LEG. Cargo's FKs are `origin_id`, `spec_origin_id`, `spec_destination_id`, `last_known_location_id`, `current_voyage_id`, `next_expected_location_id`, `next_expected_voyage_id`, and `last_event_id`.

### LEG → `leg` / `LegRecord`

Owner: `Leg` (`.source/src/main/java/org/eclipse/cargotracker/domain/model/cargo/Leg.java:22-48`); `cargo_id` is the join column on `Cargo.Itinerary.legs` (`Itinerary.java:29-36`). `ID` is the generated PK.

| Snapshot column | Source type | Target column / field | Keys, relation, or conversion |
|---|---|---|---|
| ID | `Long @Id @GeneratedValue` | `id`, `BigAutoField` | PK |
| CARGO_ID | `Cargo` association, join column on itinerary | `cargo_id`, FK to `cargo` | FK to CARGO |
| VOYAGE_ID | `Voyage` association | `voyage_id`, FK to `voyage` | FK to VOYAGE |
| LOAD_LOCATION_ID | `Location` association | `load_location_id`, FK to `location` | FK to LOCATION |
| UNLOAD_LOCATION_ID | `Location` association | `unload_location_id`, FK to `location` | FK to LOCATION |
| LOAD_TIME | `Date @Temporal(TIMESTAMP)` | `load_time`, `DateTimeField` | Timestamp; naive source time → UTC |
| UNLOAD_TIME | `Date @Temporal(TIMESTAMP)` | `unload_time`, `DateTimeField` | Timestamp; naive source time → UTC |

The target migration mirrors all columns. It orders legs by `load_time`; the source uses `@OrderBy("loadTime")` and declares no persisted `leg_index` column.

### HANDLINGEVENT → `HandlingEvent` / `HandlingEventRecord`

Owner: `HandlingEvent` (`.source/src/main/java/org/eclipse/cargotracker/domain/model/handling/HandlingEvent.java:47-78`). `ID` is the generated PK.

| Snapshot column | Source property and type | Target column / field | Keys, relation, or conversion |
|---|---|---|---|
| ID | `Long @Id @GeneratedValue` | `id`, `BigAutoField` | PK |
| TYPE | `HandlingEvent.type`, enum `@Enumerated(STRING)` | `type`, `event_type` (`CharField(255)`) | Enum name, not ordinal |
| VOYAGE_ID | Nullable `Voyage` association | `voyage_id`, nullable FK to `voyage` | FK to VOYAGE |
| LOCATION_ID | Required `Location` association | `location_id`, FK to `location` | FK to LOCATION |
| COMPLETIONTIME | `Date @Temporal(DATE)` | `completionTime`, `completion_time` (`DateTimeField`) | Source DATE → UTC midnight in target |
| REGISTRATION | `Date @Temporal(DATE)` | `registration`, `registration_time` (`DateTimeField`) | Source DATE → UTC midnight in target |
| CARGO_ID | Required `Cargo` association | `cargo_id`, FK to `cargo` | FK to CARGO |

The target schema preserves the source column names (`type`, mixed-case `completionTime`, and `registration`). Its initial migration represented the two dates as `DateField`; migration `0003` converts them to timezone-aware datetimes at UTC. The target model and final migration therefore differ from the source temporal precision, as described above.

### LOCATION → `location` / `LocationRecord`

Owner: `Location` (`.source/src/main/java/org/eclipse/cargotracker/domain/model/location/Location.java:21-37`); embedded `UnLocode` is defined at `UnLocode.java:17-27`. `ID` is the generated PK; there are no FKs.

| Snapshot column | Source property and type | Target column / field | Keys, relation, or conversion |
|---|---|---|---|
| ID | `Long @Id @GeneratedValue` | `id`, `BigAutoField` | PK |
| UNLOCODE | `UnLocode.unlocode`, `String` | `unlocode`, `CharField(255)` | Identity value stored as text |
| NAME | `Location.name`, `String` | `name`, `CharField(255)` | Text |

The target migration mirrors the columns. The source value object validates five-character UN/LOCODE syntax and uppercases values through its constructor; no migration-time normalization is assumed here.

### VOYAGE → `voyage` / `VoyageRecord`

Owner: `Voyage` (`.source/src/main/java/org/eclipse/cargotracker/domain/model/voyage/Voyage.java:13-35`); `VoyageNumber` is embedded (`VoyageNumber.java:11-18`). `ID` is the generated PK; the table has no FKs.

| Snapshot column | Source property and type | Target column / field | Keys, relation, or conversion |
|---|---|---|---|
| ID | `Long @Id @GeneratedValue` | `id`, `BigAutoField` | PK |
| VOYAGE_NUMBER | `VoyageNumber.number`, `String` | `voyage_number`, `CharField(255)` | Text |

The embedded Schedule has no scalar VOYAGE columns. Its carrier-movement children are persisted separately with `voyage_id` (`Schedule.java:21-36`).

### CARRIER_MOVEMENT → no target table

Owner: `CarrierMovement`, explicitly `@Table(name="carrier_movement")` (`.source/src/main/java/org/eclipse/cargotracker/domain/model/voyage/CarrierMovement.java:25-57`). `ID` is the generated PK. `voyage_id` is the parent join from `Schedule.carrierMovements`; `departure_location_id` and `arrival_location_id` reference LOCATION.

| Snapshot column | Source property and type | Target column / field | Keys, relation, or conversion |
|---|---|---|---|
| ID | `Long @Id @GeneratedValue` | No target column | Source PK |
| VOYAGE_ID | Schedule parent association | No target column | FK to VOYAGE |
| DEPARTURE_LOCATION_ID | `Location` association | No target column | FK to LOCATION |
| ARRIVAL_LOCATION_ID | `Location` association | No target column | FK to LOCATION |
| DEPARTURE_TIME | `Date @Temporal(TIMESTAMP)` | No target column | Timestamp |
| ARRIVAL_TIME | `Date @Temporal(TIMESTAMP)` | No target column | Timestamp |

At `a302ef8`, target `VoyageRecord` persists only `id` and `voyage_number`; there is no carrier-movement infrastructure model or migration. Target domain `CarrierMovement`/`Schedule` classes do not provide a database mirror. The 13 snapshot rows therefore have no direct target home. Draft: `.migration/quirks/data-carrier-movement-home.md` (ledger ID `data.carrier-movement`).

### SEQUENCE → no target table

The CSV header is `SEQ_NAME, SEQ_COUNT`; the manifest reports one row. These are provider-style metadata columns, but no scoped JPA entity maps this table, so its entity-defined key, foreign keys, Java types, and DDL are not available in the source model. The six entity classes use generated IDs; target migrations use Django `BigAutoField`, which delegates generated keys to PostgreSQL sequences rather than a SEQUENCE table.

| Snapshot column | Source mapping/type | Target column / field | Keys, relation, or conversion |
|---|---|---|---|
| SEQ_NAME | Provider metadata; no entity field/type declaration | No target column | Key constraint not established from source JPA |
| SEQ_COUNT | Provider metadata; no entity field/type declaration | No target column | No FK identified |

Both legacy columns have no target table home. The follow-on loader must decide how target-native sequences are aligned after importing explicit IDs; this analyst has not authored a mapping or selected a policy. Draft: `.migration/quirks/data-sequence-state.md` (ledger ID `data.sequence`).

## Risk map

Generated under `.migration/risk-map/data-migration/` from 411 methods in pinned Java main sources; no coverage input was available, so CRAP is a complexity ranking with coverage 0. Eight methods exceed the profile threshold of 30. The top hotspots are `Itinerary::isExpected` (182, CCN 13), `Delivery::calculateNextExpectedActivity` (156, CCN 12), `Delivery::calculateTransportStatus` (56, CCN 7), `CargoStatusDtoAssembler::getCargoStatusText` (42, CCN 6), and `TrackingEventsDtoAssembler::descriptionFrom` (42, CCN 6). Profile exclusions do not match the Java-only input. Lizard emitted no method rows for several mapped JPA entities; ledger risk uses the highest emitted method in each entity or embedded-value scope where available. `data.handling-event` uses the handling-domain package proxy `HandlingHistory::equals` (20, CCN 4) because no row was emitted for `HandlingEvent.java`; no fabricated entity score is assigned to SEQUENCE.

## Pending ledger entries and quirk drafts

Seven new entries are pending in `.migration/ledger/data.*.yaml`, all `kind: data`, `slice: data-migration`, and `verification: pending`. Existing track-cargo and handling data entries were not edited.

The two quirk drafts concern verified schema/home gaps, not inferred row values. No orphan, sentinel, or other row-level anomaly is claimed because CSV data rows were not inspected. The drafts list exact ledger IDs; the coordinator should publish them as issues and add issue references to affected ledger entries.
