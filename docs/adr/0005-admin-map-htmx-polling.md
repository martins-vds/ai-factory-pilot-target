# ADR-0005: The admin dashboard map refreshes by htmx polling

- Status: accepted (martins-vds, 2026-11-02; decision map #3)
- Ruling: "How does the admin dashboard receive real-time cargo updates in the target?" (#90).
  Implementation: "Admin dashboard live map: plan and run the slice" (#99).

## Decision
In the source, `RealtimeCargoTrackingService` (`@ServerEndpoint("/tracking")`) sends a JSON message to
every open WebSocket session each time a cargo is inspected. Its only client is the admin map frame
(`admin/tracking/mapFrame.xhtml`). The frame ignores the message's content: on any message it reloads
the whole page (`location.reload(true)`), and the reload fetches `/rest/cargo` again.

The behaviour preserved is: **after a cargo's state changes, the open admin map shows it within
`CARGO_MAP_POLL_SECONDS` seconds, without a manual reload.** The message's JSON fields are not part of
the contract, because no client reads them.

- **Mechanism.** The map's markers are a server-rendered partial. The page polls it with htmx
  (`hx-trigger="every Ns"`) and swaps it in, with no full-page reload.
- **Interval.** `CARGO_MAP_POLL_SECONDS` in settings, default 10. Registration is already
  asynchronous (ADR-0004), so the source's map was never instant either.
- **Works across processes.** Inspection runs in the `worker` service (ADR-0004). The next poll reads
  the committed state, so the web and worker processes need no channel between them.
- **Testing.** Tests inspect a cargo (calling the processing step directly), request the partial and
  assert the new location and status are there. A second test asserts the page's `hx-trigger` interval
  equals the setting.

## Considered options
- **Django Channels (ASGI with Redis):** the closest match to a WebSocket, but it adds Redis and an
  ASGI server to run, only for this page.
- **Server-sent events fed by PostgreSQL `LISTEN/NOTIFY`:** a real push with no new service, but it
  needs async views and long-lived connections, and its tests are timing-dependent.

## Consequences
- **Divergences from the source,** approved by the ruling (#90):
  - The map shows **every** change to cargo state (booking, routing, misdirection, handling) on the
    next poll, not only inspections. This can only remove stale views, not add wrong ones.
  - The `ws://…/tracking` endpoint is dropped; nothing outside the app used it.
  - The online/offline status label (debug scaffolding) is dropped.
  - Updates arrive up to `CARGO_MAP_POLL_SECONDS` later than a push would.
- The admin map slice (#99) lists these drops in its ledger, so the parity audit doesn't flag them.
- ADR-0004's "dashboard push follows the commit" is realised by this ADR: the push becomes the next
  poll after the commit.
