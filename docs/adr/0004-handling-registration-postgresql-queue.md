# ADR-0004: Handling-event registration runs through a PostgreSQL-backed queue

- Status: accepted (martins-vds, 2026-11-02; decision map #3)
- Rulings: "Quirk: handling-event registrations expire after one second and can be silently dropped" (#94),
  "Quirk: rejected handling-event registrations go nowhere visible; the rejected-attempts queue is never fed"
  (#95), "Must the target preserve "accepted now, processed later" for handling events, and with which
  mechanism?" (#87). Facts: [async-flows research](https://github.com/martins-vds/ai-factory-pilot-target/blob/research/async-flows/docs/research/async-flows.md) (#86).

## Decision
The source registers handling events through JMS. Three front doors queue a registration attempt and
return: REST `POST /handling/reports`, the event logger and the upload folder. Consumers later register
the event and then, in a second asynchronous step, re-derive the cargo's delivery. Attempts expire after
one second, and rejections leave no trace. The target keeps the asynchronous **acceptance** and replaces
everything behind it.

- **Accepted attempts are rows.** A front door validates an attempt and inserts it into an attempts
  table in PostgreSQL, in the request's own transaction, before answering "accepted". The row's ID is the
  attempt's identity.
- **A worker processes them.** It claims pending rows (`FOR UPDATE SKIP LOCKED`). In **one transaction**,
  it registers the handling event and re-derives the cargo's delivery (the source's "inspection"), then
  marks the row *registered*. The admin map shows the change on its next poll after the commit
  (ADR-0005).
- **Worker choice: hand-rolled Django management-command loop.** PostgreSQL attempts already provide
  durable work and `SKIP LOCKED` claims, so another queue dependency or broker is unnecessary.
- **Guarantees.**
  - An accepted attempt is never lost: no time-to-live.
  - Processing is at least once, and registration is idempotent per attempt.
  - Attempts are processed in no promised order; handling history is ordered by completion time.
- **Rejections.** An attempt that can never succeed (unknown cargo, voyage or location, or invalid data)
  is marked *rejected* immediately, with a reason code and message. The rejected row is the rejection
  record, kept indefinitely and logged. No UI shows it (an admin view is out of scope).
- **Temporary failures** (database or broker down, timeouts) retry indefinitely with backoff, log an
  error after about 15 minutes of retrying, and never become rejections.
- **"Misdirected" and "delivered"** are log lines written during inspection. The source's queues for
  them, and its never-fed rejected-attempts queue, are not carried over.
- **Running and testing.** The worker is its own `worker` service in `compose.yaml`. Tests call the
  processing step directly, so CI's test services stay `[db]`. The worker library (hand-rolled loop or a
  PostgreSQL task queue such as Procrastinate) is the slice's choice, within these rules.

## Considered options
- **Celery with Redis or RabbitMQ**: a new broker to run, and "never lost once accepted" would still need
  the attempt written to the database first (an outbox). That means two stores to keep consistent, and
  rejections stored separately again.
- **Processing after commit in the web process**: a crash between the response and the processing
  would lose an accepted attempt.

## Consequences
- **Divergences from the source,** each approved by its ruling: no expiry (#94); rejections recorded and
  the rejected-attempts queue dropped (#95); registration and inspection in one transaction, so tracking
  never shows a new event next to an out-of-date status (#87).
- **Terms:** *accepted*, *registered* and *rejected* are defined in the Handling glossary.
