# ADR-0003: The database schema mirrors the source's JPA mapping

- Status: accepted (martins-vds, 2026-11-01; decision map #3)
- Context: the golden files and any later Derby → PostgreSQL copy (#1) are easiest to compare when
  the tables line up.

## Decision
Django ORM models in each context's `infrastructure/` map to the **same tables and columns** that
Cargo Tracker's JPA mapping generates (EclipseLink defaults plus explicit `@Column`/`@JoinColumn`
names). For example:
- `tracking_id`
- `origin_id`
- `spec_origin_id`, `spec_destination_id`, `spec_arrival_deadline`
- `transport_status`, `routing_status`
- `last_known_location_id`, `current_voyage_id`
- `next_expected_handling_event_type`
- `load_time`, `unload_time`
- `completionTime`, `registration`
- `voyage_number`

Embedded values (`Delivery`, `RouteSpecification`, `HandlingActivity`) are stored as columns of
their owning table, as in the source. Django migrations create the schema on PostgreSQL 17; the seed
reproduces `SampleDataGenerator`.

## Consequences
- The domain model and the table layout are decoupled through repositories (ADR-0001), so mirroring
  doesn't leak into the domain.
