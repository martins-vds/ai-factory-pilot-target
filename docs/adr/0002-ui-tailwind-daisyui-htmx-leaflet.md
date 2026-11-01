# ADR-0002: UI uses Tailwind CSS, daisyUI and htmx; the map uses Leaflet with OpenStreetMap

- Status: accepted (martins-vds, 2026-11-01; decision map #3)
- Context: the UI is always rewritten. Functional fidelity is mandatory and the visual direction is
  a human decision (harness ADR-0014).

## Decision
- **Look:** modernized with Tailwind CSS and daisyUI, built with the Tailwind standalone CLI via
  `pytailwindcss` (no Node toolchain). `ui-ux-pro-max` guides layout within daisyUI.
- **Interactivity:** server-rendered Django templates. htmx swaps the result fragment on a tracking
  lookup (the source posts a JSF form), and the page also works without JavaScript.
- **Map:** Leaflet with OpenStreetMap tiles; no API key is needed. Markers sit at each location's
  configured coordinates, with no random offset (#14).

## Consequences
- Every observable behavior in the ledger (texts, states, messages, history rows, map status) is
  still reproduced. Only the look and layout change, and the human side-by-side check compares
  behavior, not pixels.
