---
name: self-learning
description: Autonomous skill generator that researches a technology from the web and turns it into a reusable local skill. Use this skill whenever the user wants to learn, research, or document a new library, framework, API, CLI, or tool; asks to "create a skill for X", "learn X", or invokes the `/learn` command with a topic; or needs current usage patterns synthesized from official documentation. It uses VS Code web-fetch and browser tools to discover and extract authoritative docs, then delegates skill authoring to the skill-creator skill.
---

# Self-Learning Skill Generator

Autonomously research and learn a new technology from the web, then generate a
reusable skill that captures what was learned. The goal is to transform official
documentation into a self-contained skill another agent can trigger later.

This is a local, VS Code-native adaptation: all research uses VS Code tools, and
all skill-authoring standards come from the **skill-creator** skill rather than a
bundled guide. Nothing here depends on services outside VS Code.

## Usage

```
/learn <topic>
```

If `<topic>` is missing, show this usage. If the topic is ambiguous, ask one
clarifying question before researching, because researching the wrong target
wastes time and produces a misleading skill:

- "react" → "React for web, React Native, or a specific library like react-query?"
- "apollo" → "Apollo GraphQL client, Apollo Server, or Apollo Federation?"
- "aws" → "Which AWS service? (S3, Lambda, DynamoDB, etc.)"

Normalize the resolved topic to **kebab-case** for the skill folder and filename
(e.g., `react-query`, `apollo-server`).

## Workflow

Follow these steps in order. Each step feeds the next, so do not skip ahead.

### 1. Parse the topic

Resolve the topic to a single, unambiguous target and its kebab-case name. Keep a
short note of the canonical name and any aliases — you will reuse them in the
description so the generated skill triggers reliably.

### 2. Discover sources

Find authoritative documentation. In VS Code, use `fetch_webpage` to pull search
results or known documentation pages, and fall back to the integrated browser
(`open_browser_page` + `read_page`) or the `agent-browser` skill for interactive
search when needed.

**Search queries to try:**

1. `<topic> official documentation`
2. `<topic> getting started guide`
3. `<topic> API reference`
4. `<topic> GitHub repository`

**Source prioritization (highest first):**

1. Official docs sites (e.g., `docs.*`, `*.dev`)
2. Official GitHub repositories (README, `/docs`)
3. Official blogs / release notes / announcements

Select **3–5 high-quality URLs** maximum. Prefer fewer authoritative sources over
many shallow ones. If no credible sources are found, ask the user to provide a URL
instead of guessing.

### 3. Extract content

For each selected URL, call `fetch_webpage` with a focused query describing what
to pull out. Extract only the sections that make the skill useful:

**Keep:** installation / setup, core concepts, API reference / key functions,
common patterns and examples, version information.

**Skip:** navigation, ads, login prompts, unrelated sidebars, comments, forums.

If `fetch_webpage` fails or returns little (common on JavaScript-heavy sites),
fall back to the integrated browser tools (`open_browser_page`, `navigate_page`,
`read_page`, `screenshot_page`) or the `agent-browser` skill to render the page
and read its main content.

Record the scrape date for each source (current date, `YYYY-MM-DD`) so the
generated skill carries provenance and can be refreshed later.

### 4. Generate the skill

**Invoke the `skill-creator` skill and follow it as the single source of truth for
skill structure and quality.** Read it from
`.agents/skills/skill-creator/SKILL.md` and apply its guidance on anatomy,
frontmatter, description writing, progressive disclosure, and what *not* to
include. Do not embed or duplicate skill-authoring rules here — the skill-creator
skill owns those standards so they stay consistent across every generated skill.

Then synthesize the extracted information into the new skill:

- **Trigger / description:** Write a description that clearly states what the
  skill does *and* the contexts that should trigger it (per skill-creator
  guidance). Fold in the canonical topic name and common aliases from step 1.
- **Workflow:** Turn the learned material into clear, imperative, step-by-step
  instructions.
- **Resources:** Move long reference material (API tables, schemas, large
  examples) into `references/` files and link them from `SKILL.md`, following the
  skill-creator's progressive-disclosure pattern. Keep `SKILL.md` lean.
- **Format:** Ensure valid YAML frontmatter (`name`, `description` only) and a
  proper folder structure.

### 5. Save the skill locally

Save the generated skill into the workspace skills directory so VS Code can
discover it:

```
.agents/skills/<topic>/SKILL.md
```

Use `create_directory` for the folder (and any `references/` subfolder), then
`create_file` for each file. Before writing, check whether
`.agents/skills/<topic>/` already exists (`list_dir` or `file_search`); if it
does, warn the user and confirm before overwriting their existing skill.

### 6. Confirm to the user

Report a concise summary:

```
✓ Created skill: <topic>
  Sources scraped: <N> (as of <YYYY-MM-DD>)
  Saved to: .agents/skills/<topic>/SKILL.md
  This skill will trigger when working with <topic>.
```

## VS Code Tool Reference

Use only tools available in VS Code. This skill assumes no external CLIs or
services beyond VS Code itself.

| Purpose | VS Code tool |
| --- | --- |
| Discover documentation URLs | `fetch_webpage` (search-results or doc URLs); integrated browser (`open_browser_page` + `read_page`) or the `agent-browser` skill for interactive search |
| Extract content from static pages | `fetch_webpage` |
| Extract content from JS-heavy / interactive sites | Integrated browser (`open_browser_page`, `navigate_page`, `read_page`, `screenshot_page`) or the `agent-browser` skill |
| Author the skill to standard | The `skill-creator` skill (`.agents/skills/skill-creator/SKILL.md`) |
| Create folders | `create_directory` |
| Save the generated skill | `create_file` |
| Check for an existing skill before overwriting | `list_dir` / `file_search` / `read_file` |

## Critical Rules

1. **Never hallucinate documentation.** Include only information drawn from
   sources you actually fetched.
2. **Never invent APIs.** If the documentation is unclear or incomplete, ask the
   user how to proceed instead of guessing.
3. **Ask for URLs when discovery fails.** If automated search turns up nothing
   credible, request specific URLs from the user.
4. **Verify sources.** Prefer official documentation over third-party tutorials.
5. **Stay within VS Code.** Use only the tools listed above; do not rely on
   external tooling or services.
6. **Delegate authoring standards.** Let the `skill-creator` skill define skill
   structure and quality; do not restate or fork those rules here.
7. **Record provenance.** Note the scrape date so the generated skill can be
   audited and refreshed.
