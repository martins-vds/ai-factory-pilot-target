# Quirk: Claimed cargo retains a past ETA

## Question
After a cargo has been claimed, should tracking continue to display its scheduled arrival date when that date is in the past?

## Evidence
- Source: `src/main/java/org/eclipse/cargotracker/domain/model/cargo/Delivery.java:256-261,328-330` at the pinned SHA.
- Characterization: `characterization/track-cargo/golden/mno456.json`; MNO456 is claimed but displays `<TODAY-28> 12:00 AM UTC` as its ETA.
- Why it looks wrong: a completed delivery still displays its historical scheduled arrival as an ETA.

## Impact
- Ledger capabilities: `track-cargo.eta`, `track-cargo.domain-route-state`
- Blocks: `martins-vds/ai-factory-pilot-target#10`

## Options
1. Preserve the historical ETA after claim.
2. Hide or replace the ETA after claim.
3. Other
