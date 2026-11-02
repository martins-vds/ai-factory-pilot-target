# Track Cargo side-by-side check

Compare behavior, not visual styling. Keep both applications open in separate terminals and
browser tabs. Use UTC and the source date format (`MM/dd/yyyy hh:mm a UTC`) when comparing times;
normalize dates to `<TODAY>` or a signed day offset if the clock changes between runs.

## Start the legacy application

Prerequisites: Java 8, Maven, `curl`, `unzip`, and network access to Maven Central. The runner
builds a writable scratch copy of the pinned, read-only source, starts Payara 4.1.2.181, and checks
the initial page. Keep it alive by passing a long-running command; without one, the runner cleans
up Payara as soon as the initial probe completes.

In terminal 1, from the repository root:

```bash
export JAVA_HOME="${JAVA_HOME:-/usr/lib/jvm/temurin-8-jdk-amd64}"
bash characterization/legacy-runtime/run-payara.sh sleep 3600
```

Open <http://localhost:8080/cargo-tracker/>. Leave the command running while comparing. Stop it
with Ctrl-C when finished; the runner's cleanup trap stops Payara and removes its scratch copy.

## Start the Django application

Prerequisites: the project Python environment, PostgreSQL 17, and the project's Tailwind CLI.
For a disposable local database, start PostgreSQL in a separate terminal (use only a throwaway
local password):

```bash
docker run --rm --name track-cargo-check-db \
  -e POSTGRES_DB=cargotracker \
  -e POSTGRES_USER=cargotracker \
  -e POSTGRES_PASSWORD=local-only \
  -p 5432:5432 postgres:17-alpine
```

In terminal 2, from the repository root:

```bash
export POSTGRES_DB=cargotracker
export POSTGRES_USER=cargotracker
export POSTGRES_PASSWORD=local-only
export POSTGRES_HOST=127.0.0.1
export POSTGRES_PORT=5432
export DJANGO_DEBUG=true
python manage.py migrate --noinput
python manage.py seed_sample_data
make tailwind-build
python manage.py runserver 127.0.0.1:8001
```

Open <http://127.0.0.1:8001/> in the second browser tab. Keep the same host (`127.0.0.1`) for
the page and its map iframe. Do not compare screenshots pixel-for-pixel; compare the listed
observable values and flows.

## Capability checklist

For each known tracking ID below, submit the same input to both applications. Record the displayed
value or a mismatch in the notes column. The approved differences are intentional and should not
be reported as regressions.

| Checked | Capability | Observable behavior to compare | Approved difference |
|---|---|---|---|
| [ ] | `track-cargo.data-cargo` | Found tracking ID, route endpoints, delivery status and fields used by the result. | None |
| [ ] | `track-cargo.data-handling-event` | Event type, event location, voyage when present, completion time and relation to the cargo. | None |
| [ ] | `track-cargo.data-leg` | Ordered route legs, voyages, load/unload locations and scheduled times. | None |
| [ ] | `track-cargo.data-location` | Location names and UN/LOCODEs used by route, history and map markers. | None |
| [ ] | `track-cargo.data-voyage` | Voyage number shown for onboard status, history and next activity. | None |
| [ ] | `track-cargo.domain-event-expectation` | Each history event's expected/unexpected marker for its itinerary location and voyage. | None |
| [ ] | `track-cargo.domain-history-order` | History is deduplicated and ordered by completion time; latest event drives the current state. | None |
| [ ] | `track-cargo.domain-route-state` | Routed/unrouted state, misdirection, arrival state and next activity for the cargo. | #52 is preserved: next activity uses the first route leg matching the event location, not the event voyage. |
| [ ] | `track-cargo.domain-transport-status` | No event → Not received; LOAD → Onboard; UNLOAD/RECEIVE/CUSTOMS → In port; CLAIM → Claimed. | None |
| [ ] | `track-cargo.eta` | Unknown ETA is `?`; otherwise compare the UTC date in source format. | #17: target hides ETA after CLAIM; source shows the past scheduled arrival. |
| [ ] | `track-cargo.handling-history` | Empty-history text, event descriptions, order, UTC times and expected markers. | #12: target renders no history section when no cargo is found. |
| [ ] | `track-cargo.map-frame` | Found cargo embeds a map frame with status, origin, destination and last-known location. | #14: target marker positions use exact configured coordinates instead of random offsets. |
| [ ] | `track-cargo.map-integration` | Leaflet map, location markers, tooltips and OpenStreetMap tiles load in the embedded frame. | #14: exact configured coordinates are intentional. |
| [ ] | `track-cargo.map-status-code` | Map status is NOT_ROUTED, AT_DESTINATION, MISDIRECTED or the transport status as appropriate. | None |
| [ ] | `track-cargo.misdirected-indicator` | Misdirected cargo shows the warning and corresponding status. | None |
| [ ] | `track-cargo.next-activity` | Expected activity text includes event type, location and voyage when applicable; absent when none. | #52 is preserved as described above. |
| [ ] | `track-cargo.not-found` | Unknown ID leaves the entered ID and does not render cargo-dependent content. | #12: target shows a visible not-found message; source feedback is not rendered. |
| [ ] | `track-cargo.status-text` | Status text identifies the latest transport state and relevant location/voyage. | #13: target says `In port {last-known location}`; source names the route destination. |
| [ ] | `track-cargo.tracking-id-entry` | Form accepts a tracking ID, trims surrounding whitespace, and remains case-sensitive. | #12: target shows a visible required message for an empty ID. |

## Golden-case checklist

Compare result text, ETA, next activity, misdirection, ordered history, map status and marker
coordinates. Compare all displayed dates in UTC using the normalization above.

| Checked | Golden input | Expected comparison |
|---|---|---|
| [ ] | `ABC123` | Three expected history events; IN_PORT; target says `In port New York` while source says `In port Helsinki` (#13); target ETA is the same normalized scheduled date; map coordinates differ only by the approved #14 offset removal. |
| [ ] | `JKL567` | Onboard and misdirected; four history events with the final event unexpected; MISDIRECTED map status; target uses exact configured marker coordinates (#14). |
| [ ] | `DEF789` | Not received, no ETA or next activity, empty history, and NOT_ROUTED map status; target uses exact configured marker coordinates (#14). |
| [ ] | `MNO456` | Claimed with five history events; source shows its past scheduled ETA, target hides it (#17); target map status is CLAIMED; target uses exact configured coordinates (#14). |
| [ ] | ` ABC123 ` | Whitespace is trimmed and the cargo is found; apply the #13 status-text and #14 map-coordinate differences. |
| [ ] | `abc123` | Case-sensitive lookup is not found; target shows the #12 message and no cargo, history or map. |
| [ ] | empty ID | Target shows the #12 required-ID message and no cargo, history or map; source's required-field behavior does not render a feedback message. |
| [ ] | `NOPE000` | Target shows the #12 not-found message and no cargo, history or map; source feedback is not rendered. |

## Auditor's browser observation (2026-11-02 UTC)

The target form and ABC123 result rendered in a browser, including the #13 status, ETA, next
activity and history. The unknown-ID message also rendered without cargo-dependent content.
The map request returned HTTP 200, but the response included `X-Frame-Options: DENY`; the browser
refused to display the map iframe. Therefore the map-frame and map-integration checks above remain
unchecked until that integration issue is resolved and rechecked. The automated map data and
coordinate assertions do not substitute for a visible browser-rendered map.

This is a human comparison checklist, not evidence that a person has completed the side-by-side
review. Record the reviewer, UTC date, observations and follow-up issue links here after the
comparison.
