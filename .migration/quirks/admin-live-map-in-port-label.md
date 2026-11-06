# Admin all-cargo map adds an extra leading space to In port

## Question
The source's `IN_PORT` transport label begins with a leading space, resulting in two spaces after `Transport Status:` in the marker tooltip; should the target preserve or trim it?

## Evidence
- Source: `.source/src/main/webapp/admin/tracking/mapFrame.xhtml:42-48,215-220` at `eclipse-ee4j/cargotracker@f3beacf78de4f6d34edc4971ac87e38a5c6fe59d`.
- Observation: `transportStatusName.IN_PORT` is `" In port"` and the tooltip prefix is `"Transport Status: "`, so the composed label contains two spaces before `In port`.
- Why it looks wrong: the extra whitespace appears accidental, but it is part of the source's visible tooltip text.

## Impact
- Ledger capabilities: `admin-live-map.marker-tooltip`.
- Blocks: implementation of the exact IN_PORT tooltip text until a human decides.

## Options
1. Preserve exactly (including both spaces).
2. Fix (trim the extra space and record the divergence).
3. Other.
