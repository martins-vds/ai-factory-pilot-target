---
name: self-learning
description: Autonomous skill generator that researches a technology from the web and turns it into a reusable local skill. Use this skill whenever the user wants to learn, research, or document a new library, framework, API, CLI, or tool; asks to "create a skill for X", "learn X", or invokes the `/learn` command with a topic; or needs current usage patterns synthesized from official documentation. It uses the host's web-fetch and browser tools (VS Code, Copilot CLI, Copilot coding agent and others) to discover and extract authoritative docs, then delegates skill authoring to the skill-creator skill.
---

# Self-Learning Skill Generator

Autonomously research and learn a new technology from the web, then generate a
reusable skill that captures what was learned. The goal is to transform official
documentation into a self-contained skill another agent can trigger later.

It works in any agent host. Steps name the *capability* they need (fetch a web
page, render a page in a browser, write a file); use whichever tool your host
provides for it (see the tool table). All skill-authoring standards come from the
**skill-creator** skill rather than a bundled guide.

## Usage

```
/learn <topic>
```

If `<topic>` is missing, show this usage. If the topic is ambiguous, ask one
clarifying question before researching, because researching the wrong target
wastes time and produces a misleading skill. In an unattended session (no one to
answer), pick the most likely reading, state it at the top of the generated
skill, and say so in your summary:

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

Find authoritative documentation with your host's **web-fetch** tool (search
results or known documentation pages). Fall back to a **browser** (the host's
browser tools or the `agent-browser` skill) for interactive search when needed.

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

For each selected URL, call the **web-fetch** tool with a focused query describing
what to pull out. Extract only the sections that make the skill useful:

**Keep:** installation / setup, core concepts, API reference / key functions,
common patterns and examples, version information.

**Skip:** navigation, ads, login prompts, unrelated sidebars, comments, forums.

If web-fetch fails or returns little (common on JavaScript-heavy sites), render
the page in a **browser** (the host's browser tools or the `agent-browser` skill)
and read its main content.

Record the scrape date for each source (current date, `YYYY-MM-DD`) so the
generated skill carries provenance and can be refreshed later.

### 4. Generate the skill

**Invoke the `skill-creator` skill and follow it as the single source of truth for
skill structure and quality.** Load it through your host's skill mechanism (or
read `skill-creator/SKILL.md` from the skills directory found in step 5) and apply
its guidance on anatomy,
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

### 5. Save the skill

Decide **where** first, in this order:

1. **The repository says where.** If the repo's agent instructions name a location
   for new or generated skills (for example `.github/copilot-instructions.md`,
   `AGENTS.md` or `CLAUDE.md`; an AI Factory Swarm target says
   `.migration/skills-proposed/`), save there. Such repos often pin their skill
   folders and reject edits to them; a proposal folder is reviewed and promoted by
   a human.
2. **Otherwise, the project skills folder your host loads:**
   - GitHub Copilot (CLI, coding agent, VS Code): `.github/skills/<topic>/`
   - Claude Code: `.claude/skills/<topic>/`
   - Other hosts that read `.agents/skills/`: `.agents/skills/<topic>/`

   If more than one exists in the repo, use the one the repo already uses for its
   own skills.

Then create `<skills-folder>/<topic>/SKILL.md` (and any `references/` subfolder)
with your host's file-writing tool. If `<topic>/` already exists, do not overwrite
it: ask the user, or in an unattended session save as `<topic>-<YYYYMMDD>/` and say
so in the summary.

### 6. Confirm to the user

Report a concise summary:

```
✓ Created skill: <topic>
  Sources scraped: <N> (as of <YYYY-MM-DD>)
  Saved to: <skills-folder>/<topic>/SKILL.md
  This skill will trigger when working with <topic>.
```

## Tool Reference

Use the tool your host provides for each capability. Examples:

| Capability | VS Code | Copilot CLI / coding agent | Other hosts |
| --- | --- | --- | --- |
| Fetch a web page or search results | `fetch_webpage` | `web_fetch` | the host's web-fetch tool |
| Render a JS-heavy page | integrated browser (`open_browser_page`, `read_page`) | `agent-browser` skill | browser tool or `agent-browser` |
| Author the skill to standard | `skill-creator` skill | `skill-creator` skill | `skill-creator` skill |
| Create folders and files | `create_directory`, `create_file` | `create` / shell | the host's file-writing tool |
| Check for an existing skill | `list_dir`, `file_search`, `read_file` | `view` / shell | the host's file tools |

## Critical Rules

1. **Never hallucinate documentation.** Include only information drawn from
   sources you actually fetched.
2. **Never invent APIs.** If the documentation is unclear or incomplete, ask the
   user how to proceed instead of guessing.
3. **Ask for URLs when discovery fails.** If automated search turns up nothing
   credible, request specific URLs from the user.
4. **Verify sources.** Prefer official documentation over third-party tutorials.
5. **Use the host's own tools.** Use only the capabilities listed above, through
   the tools your host provides; do not install external tooling or call other
   services.
6. **Delegate authoring standards.** Let the `skill-creator` skill define skill
   structure and quality; do not restate or fork those rules here.
7. **Record provenance.** Note the scrape date so the generated skill can be
   audited and refreshed.
