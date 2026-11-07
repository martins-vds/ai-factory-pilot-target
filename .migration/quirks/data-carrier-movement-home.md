# CARRIER_MOVEMENT has no target persistence home

## Question
The source persists voyage schedules as CARRIER_MOVEMENT child rows, but the target has no corresponding database table or migration. Should the target preserve these schedule rows, replace their storage, or intentionally regenerate them?

## Evidence
- Source: `.source/src/main/java/org/eclipse/cargotracker/domain/model/voyage/CarrierMovement.java:25-57`; `Schedule.java:21-36`.
- Characterization: the validated snapshot manifest records 13 rows; no row values were inspected.
- Why it looks wrong: ADR-0003 calls for mirrored source tables and columns, while target `VoyageRecord` stores only the voyage number and target migrations create no carrier-movement table.

## Impact
- Ledger capabilities: `data.carrier-movement`
- Blocks: follow-on data-migration mapping decision (not yet ticketed)

## Options
1. Preserve exactly by introducing target storage and pinning the imported schedule behavior.
2. Replace with an approved target representation or explicitly regenerate schedule data.
3. Other
