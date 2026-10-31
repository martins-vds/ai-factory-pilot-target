# What should the page show for empty and unknown tracking IDs?

## Question
An empty submission is rejected by the required field and an unknown ID adds an ERROR FacesMessage, but neither message is rendered; additionally, the empty-events label can render with a null cargo and its value references cargo.trackingId. Preserve, fix, or something else?

## Evidence
- Source: `src/main/java/org/eclipse/cargotracker/interfaces/tracking/web/Track.java:65-78`; `src/main/webapp/public/track.xhtml:16-25,71-73`; `src/main/webapp/WEB-INF/templates/common/public.xhtml:22-49`.
- Characterization: Static source trace only. A blank value fails the `required="true"` input; an unknown ID adds `Cargo with tracking ID: {id} not found.` to FacesContext and clears cargo. The page/template have no `<h:message>`/`<h:messages>` component. When cargo is null, `empty cargo.events` is true and the empty-history label's value references `cargo.trackingId`; runtime null-resolution behavior has not been characterized.
- Why it looks wrong: Empty/unknown lookup feedback is not displayed, and the empty-state value may dereference a missing cargo.

## Impact
- Ledger capabilities: `track-cargo.tracking-id-entry`, `track-cargo.not-found`, `track-cargo.handling-history`
- Blocks: `martins-vds/ai-factory-pilot-target#10`

## Options
1. Preserve exactly (target reproduces the quirk; a test pins it)
2. Fix (target diverges; the divergence is recorded in the ledger with this ticket as approval)
3. Other
