# Unknown sentinel tooltip and marker location

## Question
For a `NOT_RECEIVED` cargo whose API `lastKnownLocation` is `Unknown`, the source places its marker at its origin but renders `Last known location: undefined` in the tooltip. Preserve, fix, or something else?

## Evidence
- Source: `src/main/webapp/admin/tracking/mapFrame.xhtml:20-34,172-195,215-226` at `f3beacf78de4f6d34edc4971ac87e38a5c6fe59d`.
- Characterization: `DEF789` returned `NOT_RECEIVED`, origin `CNHKG`, last-known `Unknown`; browser showed one gray marker at the origin and tooltip ending `Last known location: undefined`. `.migration/characterization/admin-live-map/edge-cases.json`.
- Why it looks wrong: the cargo is located at an unknown last-known position, yet the source pins it to its origin and exposes an undefined lookup rather than an Unknown label. Ruling #206 already specifies a separate Unknown/unmapped list for the target.

## Impact
- Ledger capabilities: `admin-live-map.cargo-source`, `admin-live-map.marker-coordinates`, `admin-live-map.marker-tooltip`.
- Blocks: `martins-vds/ai-factory-pilot-target#202` (map implementation decision only; characterization is complete).

## Options
1. Preserve exactly (target reproduces the quirk; a test pins it)
2. Fix (target diverges; the divergence is recorded in the ledger with this ticket as approval)
3. Other
