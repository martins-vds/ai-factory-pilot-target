# Lesson Card Template

Use this exact structure when writing a card to `docs/lessons/<id>.md`. The YAML
frontmatter fields are validated during capture — keep them well-formed.

```markdown
---
id: <YYYYMMDD>-<semantic-slug>-<4hex>   # equals the filename, without .md
date: <YYYY-MM-DD>                       # ISO date the lesson was captured
scope: <project | module | feature>      # applicability
tags: [<tag-1>, <tag-2>, <tag-3>]        # 3-6 lowercase tags for recall matching
source: <user-correction | bug-fix | retrospective>
confidence: <0.0-0.9>                    # recall ranking signal; 0.0 = excluded from normal recall
related: [<[[other-card-id]]>]           # 0-2 high-relevance references, or omit / leave empty
---

# <One-line summary of the lesson>

## Context
<What was happening when the mistake occurred.>

## Mistake
<What went wrong.>

## Lesson
<The extracted rule or best practice.>

## When to Apply
<Future situations where this lesson matters. State a concrete trigger, not broad advice.>
```

## Worked example

```markdown
---
id: db-migration-run-order
date: 2026-06-05
scope: project
tags: [database, migrations, ordering, deploy]
source: user-correction
confidence: 0.7
related: []
---

# Run schema migrations before data migrations, never the reverse

## Context
Adding a data backfill alongside a new column during the same deploy.

## Mistake
Ran the data migration first; it failed because the target column did not exist yet.

## Lesson
Schema migrations must complete before any data migration that depends on the new
shape. Sequence them explicitly in the deploy step rather than relying on filename
ordering.

## When to Apply
Any deploy that introduces a new column/table *and* backfills it in the same release.
```

## Field rules

| Field        | Rule                                                                                                  |
| ------------ | ----------------------------------------------------------------------------------------------------- |
| `id`         | Semantic kebab-case slug; must equal the filename.                                                    |
| `date`       | ISO `YYYY-MM-DD`.                                                                                     |
| `scope`      | One of `project`, `module`, `feature`.                                                                |
| `tags`       | 3–6 lowercase tags.                                                                                   |
| `source`     | One of `user-correction`, `bug-fix`, `retrospective`.                                                 |
| `confidence` | Numeric, inclusive `0.0`–`0.9`. Source defaults: user-correction=0.7, bug-fix=0.5, retrospective=0.3. |
| `related`    | 0–2 `[[card-id]]` links; every target must resolve to an existing card.                               |

Keep this template subordinate to `SKILL.md`. If anything here conflicts with the
canonical limits or validation rules in `SKILL.md`, `SKILL.md` wins.
