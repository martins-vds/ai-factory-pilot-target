# Should map markers use the current fixed LOCODE coordinates?

## Question
The map adds a random offset to every marker coordinate, with the offset always between -3 and -1 degrees on each axis; preserve, fix, or something else?

## Evidence
- Source: `src/main/webapp/public/mapFrame.xhtml:149-177`.
- Characterization: Static source trace only. Each origin, destination and last-known coordinate adds `Math.floor(Math.random() * 3 - 3)` to longitude and latitude; this expression can only return -3, -2 or -1, so marker positions shift southwest and vary between page loads.
- Why it looks wrong: Markers do not represent the configured LOCODE coordinates and their displayed positions are nondeterministic.

## Impact
- Ledger capabilities: `track-cargo.map-frame`, `track-cargo.map-integration`
- Blocks: `martins-vds/ai-factory-pilot-target#10`

## Options
1. Preserve exactly (target reproduces the quirk; a test pins it)
2. Fix (target diverges; the divergence is recorded in the ledger with this ticket as approval)
3. Other
