# ADR-0001: DDD layers per bounded context

- Status: accepted (martins-vds, 2026-11-01; decision map #3)
- Context: Cargo Tracker is a DDD application. It has the cargo, handling, voyage and location
  aggregates, repositories and domain services. Its riskiest logic (`Itinerary.isExpected`,
  `Delivery.calculateNextExpectedActivity`, `Delivery.calculateTransportStatus`) is pure domain code.

## Decision
- One Django project (`cargotracker`): code under `src/`, `manage.py` at the repo root, matching the profile's gates.
- One package per bounded context (`cargo`, `handling`, `voyage`, `location`, and later `booking` and
  `routing`). Each has these layers:
  - `domain/`: plain Python. Aggregates, entities and value objects (`dataclass(frozen=True)` for value
    objects), plus domain services. It never imports Django.
  - `application/`: use-case services. These are the entry points for views, REST handlers and jobs.
  - `infrastructure/`: Django ORM models and repository implementations that map to and from the
    domain. Each repository has a protocol in `domain/`.
  - `interfaces/`: views, templates, forms and URL routes (the web adapters, like the source's
    `interfaces/` packages).
- Dependencies point inward only: interfaces → application → domain ← infrastructure. Wiring happens
  through constructor injection, composed in one module per context.
- Tests: domain tests run without a database; repository and view tests use pytest-django.

## Consequences
- The source's domain logic ports nearly one to one, and its characterization cases apply directly to
  the domain layer.
- There is more structure than plain Django apps, so new contributors need this ADR.
