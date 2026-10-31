# Linking Heuristics

Deterministic procedure for choosing the 0–2 `related` links on a lesson card.
Keep links rare and high-value — speculative links create churn and noise during
recall, and every link is a future maintenance cost when cards are updated or retired.

## Eligibility gate

Only consider a related link when at least **2 of these 4** conditions are true:

1. **Reusable** — the candidate applies across different tasks, not just this one.
2. **High-cost** — the candidate captures a mistake that took multiple attempts or significant time.
3. **Parameter-critical** — the candidate depends on a specific config / parameter / decision detail.
4. **Well-connected** — the candidate naturally connects to at least two existing lesson cards.

If fewer than 2 conditions hold, add no link.

## Deterministic ranking

When more than 2 candidates pass the gate, rank them and keep the top 2 using this
strict, total order (each tiebreaker only applies when the previous ones are equal):

1. **Shared tags (desc)** — more overlapping tags rank higher.
2. **Same scope** — a candidate with the same `scope` as the current card outranks a different scope.
3. **Confidence (desc)** — higher-confidence cards rank higher.
4. **Date (desc)** — newer cards rank higher.
5. **ID (asc)** — alphabetical by `id` as the final tiebreaker, so the result is fully deterministic.

Because step 5 always breaks remaining ties, two runs over the same card set always
produce the same two links.

## Constraints

- Add 0–2 links per card, never more.
- Never link a card to itself.
- Prefer active cards. A card excluded from normal recall (`confidence: 0.0`) may still
  be linked for historical traceability, but only when no active card is a better fit.
- A broken / missing related target is non-blocking: ignore it, warn, and continue the
  recall or capture flow.

This file is subordinate to `SKILL.md`. If anything here conflicts with the canonical
limits or the Linking Rule in `SKILL.md`, `SKILL.md` wins.
