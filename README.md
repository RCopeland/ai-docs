# ai-docs

A portable, version-controlled set of agent configuration: orchestration
instructions, a sub-agent roster, on-demand skills, and the coding standards
they reference.

Everything here is plain Markdown with YAML frontmatter. It is written to be
harness-agnostic — the content describes *how to work*, not *which tool to run
it in* — so it can be consumed by any agent harness that supports context
files, skills, and sub-agents.

## Layout

```
global/AGENTS.md        Orchestration instructions for the parent agent
agents/                 6 named sub-agent definitions
skills/                 10 on-demand capability packages
reference/standards/    13 coding standards docs
```

## Concepts

The setup follows one loop, regardless of which agent or model runs it:

**Plan → decompose → delegate → verify → synthesize.**

A single **parent agent** holds the high-level reasoning and coordination. It
breaks work into bounded tasks, hands execution to **sub-agents** with
self-contained briefs, treats what comes back as untrusted evidence, and
integrates the result. Detailed **standards** and **skills** are pulled in
only when a task calls for them.

### `global/AGENTS.md`

The orchestrator instructions, intended to be loaded into every session. It
defines the loop above, the sub-agent roster, model-routing rules, conventions
for shared mutable state (todo files and plan artifacts under the working
directory), and the anti-patterns to avoid — polling for results, fabricating
sub-agent output, delegating trivial work, or letting one agent's output pass
through unverified.

### `agents/`

Named sub-agents. Each is a Markdown file with YAML frontmatter plus a role
prompt, and each is scoped so it cannot spawn further sub-agents.

| Agent | Tools | Purpose |
| --- | --- | --- |
| `dev` | read, bash, edit, write | Implementation: coding, fixes, refactors, targeted verification |
| `frontend-dev` | read, bash, edit, write | Production-quality UI with accessibility and responsive behavior |
| `frontend-review` | read, bash | Read-only review of UI changes (a11y, architecture, UX) |
| `publisher` | read, bash | Review-ready change summaries; opens pull requests when asked |
| `researcher` | read, bash, write, web search, content fetch | External-knowledge research with sources; writes a findings doc |
| `review` | read, bash | Read-only correctness, maintainability, and risk review |

Implementers report what they completed, which files changed, how it was
verified, and any handoff notes. Reviewers are strictly read-only and never
edit code.

**Tool names in the table are generic capabilities** (read, edit, search the
web, run commands). Each harness names these differently; map them to whatever
your runtime provides. The frontmatter keys currently in these files
(`spawning`, `auto-exit`, `system-prompt`, `thinking`, `output`) are read by
subagent tooling and are **not part of any public standard** — see
[Portability](#portability) before reusing them elsewhere.

> **Known issue — dangling skill references.** `dev`, `frontend-review`, and
> `review` declare skills named `subagent-dev-guidance` and
> `subagent-review-guidance`, and `publisher` declares `wrike`. None of those
> three names resolve: the `subagent-*-guidance` skills exist nowhere, and the
> Wrike skill's directory is `wrike-ai-safe` while its frontmatter `name` is
> `wrike`. The references are inert but misleading — either add the missing
> skills or drop the entries.

### `skills/`

On-demand capability packages following the
[Agent Skills specification](https://agentskills.io/specification). A skill is
a directory containing a `SKILL.md` with `name` and `description` frontmatter.
Only the description is always in context; the body loads when a task matches.

| Skill | What it does |
| --- | --- |
| `bb-cli` | Inspect and control a task/thread orchestration CLI and its settings |
| `commit` | Conventional commits — staging discipline and message structure |
| `dev-task-orchestrator` | Task → reviewed PR via isolated worktree and staged dev/review/publish |
| `frontend-ai-review` | AI-first frontend review: correctness, architecture, a11y, system impact |
| `frontend-ui-engineering-global` | Build production-quality UI with a11y and responsive behavior |
| `github-issues` | Work GitHub issues via `gh` — pull, split, create, close |
| `legacy-ui-migrator` | Migrate a component or route from a legacy app into a modern one with parity |
| `manual-review` | Human-in-the-loop review in a terminal multiplexer, then evaluate the comments |
| `wrike-ai-safe` | Safely drive the Wrike CLI — scope, dedupe, conversion, secret handling |
| `write-todos` | Break a plan into implementable todos with constraints and acceptance criteria |

`bb-cli` and `frontend-ai-review` carry `references/` subfolders loaded on
demand. `dev-task-orchestrator` ships an `agents/` subfolder describing its
pipeline stages. The rest are single-file skills.

### `reference/standards/`

Coding standards, loaded per the technology context of a task:

| Context | Files to load |
| --- | --- |
| Vue 3 + TypeScript | `vue.md`, `typescript.md`, `component-design.md`, `eslint.md`, `prettier.md` |
| Frontend (any) | `html.md`, `css.md`, `javascript.md`, `accessibility.md` |
| Performance-critical | `performance.md` |
| Plain JavaScript | `javascript.md`, `typescript.md`, `eslint.md`, `prettier.md` |
| Node.js / CLI | `javascript.md`, `typescript.md`, `eslint.md`, `prettier.md` |
| Testing (general) | `testing.md`, `typescript.md` |
| Testing (Vitest) | `vitest.md`, `testing.md`, `typescript.md` |
| Reviewing Vue changes | `vue-review.md` |

`eslint.md` is a hub rather than a standalone standard: it describes how to
detect a project's stack and then read the ESLint section out of each relevant
per-technology file. `vue.md`/`vue-review.md` and `testing.md`/`vitest.md` are
write/review and general/tool-specific pairs.

These standards are language- and framework-specific by design — that is their
subject matter, not a harness dependency. The Vue and Vitest entries reflect
the current stack; the JavaScript, TypeScript, HTML, CSS, testing, and
accessibility files apply broadly.

## Portability

| Layer | Status |
| --- | --- |
| `skills/` | **Portable.** Frontmatter is `name` + `description` per the Agent Skills spec. |
| `reference/standards/` | **Portable.** Plain Markdown, no harness references. |
| `agents/` | **Partly portable.** The role prompts are generic; the frontmatter keys are not. |
| `global/AGENTS.md` | **Least portable.** Names specific tools and state paths directly. |

Skills and standards can be dropped into any harness that reads the Agent
Skills format. Agents and the orchestration doc need a mapping pass: swap
harness-specific tool names for the equivalents your runtime exposes, and
replace or drop frontmatter keys the target harness does not understand.

The concepts are what transfer — orchestrator plus scoped sub-agents plus
lazily-loaded skills. The vocabulary is what needs translating.

## Wiring into Pi

Pi is the harness this configuration was originally built for. To point an
existing Pi install at this repo, you need to handle three things separately,
because Pi treats them differently.

### 1. Global instructions — symlink

Pi loads global instructions from `~/.pi/agent/AGENTS.md`. Replace the existing
file with a symlink:

```bash
ln -sfn ~/Dev/ai-docs/global/AGENTS.md ~/.pi/agent/AGENTS.md
```

### 2. Agents — symlink (required)

Pi discovers agents **only** from `~/.pi/agent/agents/` and a project
`.pi/agents/` found by walking up from the working directory. There is **no
`agents` key in `settings.json`**, so config cannot relocate this — a symlink
is the only option:

```bash
ln -sfn ~/Dev/ai-docs/agents ~/.pi/agent/agents
```

These files define sub-agents, but they do not provide the machinery to run
them. **Subagent tooling is required** — a mechanism that reads agent
definitions, spawns them, and returns their results to the parent session.
This repo is deliberately silent on which one to use: it supplies the agent
definitions, not the runtime.

Without such tooling the agent files are inert — they will be discovered but
nothing can spawn them. The `spawning`, `auto-exit`, and `interactive`
frontmatter keys are conventions read by subagent tooling, not part of any
public standard; expect to map or drop them for a given implementation.

### 3. Skills — symlink or settings

Pi loads skills from `~/.pi/agent/skills/` by default, and additionally from
any path listed in the `skills` array in `~/.pi/agent/settings.json`. Extra
paths are **additive** — they do not replace the default location.

**Option A — symlink** (simplest, replaces the default location):

```bash
ln -sfn ~/Dev/ai-docs/skills ~/.pi/agent/skills
```

**Option B — settings** (keeps the default location active and adds this one):

```jsonc
// ~/.pi/agent/settings.json
{
  "skills": ["~/Dev/ai-docs/skills"]
}
```

Paths resolve relative to `~/.pi/agent`; absolute paths and `~` are supported.
Arrays accept glob patterns, `!pattern` exclusions, `+path` to force-include,
and `-path` to force-exclude.

> Because Option B is additive, a skill present in **both** the default
> directory and this repo will be discovered twice. Use Option A, or an
> exclusion, if you are switching over rather than adding.

### Verifying

```bash
ls -la ~/.pi/agent/ | grep -E 'AGENTS|agents|skills'
pi --help 2>/dev/null | head -1   # confirm the install resolves
```

Inside a session, `/skill:<name>` confirms a skill registered, and the
subagent tool's list action confirms agents were discovered. If a skill does
not appear, check that its `SKILL.md` frontmatter has a non-empty
`description` — skills without one are skipped silently.

### Notes

- `reference/standards/` is **not** wired into Pi by any mechanism. It is
  plain reference material, loaded by the agent reading the files when a
  task's technology context calls for them (see the table above).
- Symlinking the whole directory means edits made in Pi write straight into
  this repo's working tree. That is the intended workflow — commit changes
  here rather than letting the two drift.
- Pi also reads `~/.agents/skills/` and project `.pi/skills/` and
  `.agents/skills/`. Those are separate locations and are unaffected by the
  steps above.

## Syncing

This repo is the reviewable copy. The live configuration lives elsewhere and
is symlinked into place, so edits made through a harness may land outside this
repo:

```
<live config>/AGENTS.md  ->  <source repo>/AGENTS.md
<live config>/agents     ->  <source repo>/agents
<live config>/skills     ->  <source repo>/skills
```

The files here were copied byte-identical from that source. Because skills and
agents change frequently, this copy will drift. When reconciling:

```bash
diff -r <source repo>/skills skills
diff -r <source repo>/agents agents
diff <source repo>/AGENTS.md global/AGENTS.md
```

`reference/standards/` is maintained directly in this repo.

## Notes

- Skills and agents change often and are intended to live outside the dotfiles
  repo, which holds the more stable configuration.
- This repository is public. Some skills reference internal tooling and paths —
  review contents before adding anything sensitive.
