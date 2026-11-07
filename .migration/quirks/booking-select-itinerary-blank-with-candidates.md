# Select Itinerary page is blank when routes exist

## Question
Should the source preserve or change the `selectItinerary.xhtml` page's blank content when candidate routes are non-empty?

## Evidence
- Source: `.source/src/main/webapp/admin/selectItinerary.xhtml:15-23` renders only the empty-candidate message.
- Characterization: `DEF789` had four route candidates on `route.xhtml`; opening `selectItinerary.xhtml?trackingId=DEF789` returned HTTP 200 with only the admin navigation and no route content.
- Why it looks wrong: the page loads candidate routes but renders no content when the list is non-empty.

## Impact
- Ledger capabilities: `booking.screen-select-itinerary`
- Blocks: implementing the `selectItinerary.xhtml` content branch in slice `booking` until a human decides.

## Options
1. Preserve exactly (the page stays blank when candidates exist).
2. Fix (render candidate routes or redirect to the populated route page; record the divergence with the human decision).
3. Other
