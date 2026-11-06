# Route selection redirects to a non-Faces suffix

## Question
Should the route-assignment result preserve or correct its redirect to `show.html`?

## Evidence
- Source: `src/main/java/org/eclipse/cargotracker/interfaces/booking/web/ItinerarySelection.java:64-69` returns `show.html?faces-redirect=true&trackingId=...`; the page is `src/main/webapp/admin/show.xhtml`, and `src/main/webapp/WEB-INF/web.xml:46-54` maps the Faces Servlet only to `*.xhtml`.
- Characterization: after assigning a route, the bean returns the `.html` outcome; the existing cargo-detail page and Faces mapping use `.xhtml`.
- Why it looks wrong: the return outcome does not match the page suffix handled by JSF and may fail to reach the intended cargo-detail page.

## Impact
- Ledger capabilities: `booking.routing.assign`
- Blocks: implementation of the route-assignment return flow in slice `booking` until a human decides.

## Options
1. Preserve exactly (the target reproduces the `.html` outcome; a test pins it).
2. Fix (the target returns to the cargo-detail page; the divergence is recorded in the ledger with this ticket as approval).
3. Other
