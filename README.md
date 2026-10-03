# ai-docs

A portable, version-controlled copy of my agent configuration: global orchestration instructions, a sub-agent roster, and on-demand skills.

Everything here is plain Markdown. The goal is to keep the working configuration reviewable, shareable, and easy to point Pi at with symlinks.

## Layout

```text
global/AGENTS.md        Global orchestration instructions for the parent agent
agents/                 Named sub-agent definitions
skills/                 On-demand skills
reference/standards/    Supporting coding standards and reference docs
```

Skills may carry supporting files beside `SKILL.md`:

```text
skills/<name>/SKILL.md       The skill itself
skills/<name>/references/    Detail loaded only when the skill needs it
skills/<name>/scripts/       Deterministic helpers the skill calls
skills/<name>/agents/        Harness-specific agent metadata
```

## Concepts

The setup follows one loop regardless of harness:

**Plan → delegate → verify → synthesize.**

A single parent agent keeps the high-level reasoning and coordination. It breaks work into bounded tasks, hands those tasks to scoped sub-agents when useful, treats the results as untrusted evidence, and integrates the outcome. Detailed skills and standards are loaded only when a task calls for them.

## Current agents

These live in [`agents/`](./agents).

| Agent | Purpose |
| --- | --- |
| `dev` | Implementation, refactors, fixes, and targeted verification |
| `publisher` | Change summaries and publication / PR handoff workflows |
| `researcher` | External-knowledge research with sourced findings |
| `review` | Read-only correctness, maintainability, and risk review |

## Current skills

These live in [`skills/`](./skills).

| Skill | What it does |
| --- | --- |
| `code-review-and-quality` | Multi-axis code review across correctness, readability, architecture, security, and performance |
| `commit` | Create polished commits with good staging and message structure |
| `dev-task-orchestrator` | End-to-end task workflow through scout / dev / review / publish stages. Commits once the reviewer returns `APPROVED`; the human PR review is the single approval gate. |
| `factory-supervisor` | Intake-and-dispatch supervisor that orchestrates a fleet of child threads over a durable ledger. See [Factory supervisor](#factory-supervisor). |
| `find-skills` | Discover installable skills for new capabilities |
| `frontend-ai-review` | AI-first frontend review for Vue/Nuxt and related UI work |
| `frontend-ui-engineering` | Production-quality user-facing UI work with accessibility and responsive behavior |
| `frontend-ui-engineering-global` | Shared frontend engineering guidance for broader UI tasks |
| `github-issues` | GitHub issue workflows through `gh` |
| `legacy-ui-migrator` | Migrate legacy UI into a modern app with parity checks |
| `manual-review` | Human-in-the-loop review workflow using terminal tooling |
| `subagent-dev-guidance` | Shared implementation guidance for the `dev` sub-agent |
| `subagent-review-guidance` | Shared read-only review guidance for the `review` sub-agent |
| `wrike` / `wrike-ai-safe` | Safe Wrike CLI workflows with confirmation and scope guardrails |
| `write-todos` | Break plans into independently executable todos with constraints and acceptance criteria |
| `work-planning` | Decompose upcoming work into right-sized deliverables with estimates, ranges, and a sequenced plan |

## Portability

| Layer | Status |
| --- | --- |
| `skills/` | Portable. Each skill is a Markdown package with frontmatter, plus optional `references/` and `scripts/`. |
| `reference/standards/` | Portable. Plain reference docs. |
| `agents/` | Mostly portable. The role prompts transfer well; frontmatter may need mapping by harness. |
| `global/AGENTS.md` | Least portable. It is written for my orchestration workflow and current tool conventions. |

The concepts transfer more easily than the wiring. Skills and standards are straightforward to reuse; agents and global instructions may need tool-name or frontmatter adjustments in another harness.

## Factory supervisor

`factory-supervisor` is the one piece here with real cross-machine setup, because
half of it is a BB fleet and BB state is host-local.

**The skill is portable.** Clone this repo on another machine and the skill,
its references, and its helper script all arrive intact. It resolves its own
directory per session, so it works from any checkout path with no edits.

**The wiring is per-machine.** Four things do not travel:

| Piece | Why |
| --- | --- |
| Wake automation | A BB database row on that host |
| Project IDs | Host-local BB identifiers |
| Provider and model | Depends on what that machine runs |
| Intake source | GitHub at home, Wrike at work |

**State is the same path, different contents.** Every machine uses
`~/.bb/state/factory/`, but the contents are deliberately machine-specific:
each machine runs its own factories. Nothing syncs, and nothing should — merging
two ledgers would duplicate task IDs and make state ambiguous. The ledger is
append-only and is the restart-proof truth; a supervisor can rebuild its entire
fleet picture from disk, so context exhaustion and restarts lose nothing.

Setup on a new machine is a short checklist rather than a port. See
[`skills/factory-supervisor/references/setup.md`](./skills/factory-supervisor/references/setup.md).

### How it fits together

The supervisor never implements. It reconciles from the ledger, intakes
scope-filtered work, and dispatches one child thread per task. Each child runs
the existing `dev-task-orchestrator` workflow in its own isolated worktree, so
the fleet reuses the single-task path rather than duplicating it. Implementation
lives in this repo; runtime state never does.

## Wiring into Pi

Pi treats global instructions, agents, and skills separately.

The symlink approach below is the intended setup: it keeps the live configuration
and this repo the same files, so they cannot drift. If your machine is currently
running a **copy** instead, check with `readlink -f ~/.pi/agent/skills` — a path
resolving outside this repo means you will need to re-copy after every pull.

### Global instructions

```bash
ln -sfn ~/Dev/ai-docs/global/AGENTS.md ~/.pi/agent/AGENTS.md
```

### Agents

```bash
ln -sfn ~/Dev/ai-docs/agents ~/.pi/agent/agents
```

### Skills

If you want this repo to be the main Pi skills source:

```bash
ln -sfn ~/Dev/ai-docs/skills ~/.pi/agent/skills
```

If you also use `~/.agents/skills`, you can point that at the same repo copy too:

```bash
ln -sfn ~/Dev/ai-docs/skills ~/.agents/skills
```

If you prefer additive configuration, keep your existing directories and point Pi at this repo through `~/.pi/agent/settings.json` instead.

## Verifying

```bash
ls -la ~/.pi/agent/ | grep -E 'AGENTS|agents|skills'
ls -la ~/.agents | grep skills
```

Inside a session, confirm that skills register and that your sub-agent tooling can discover the agent files.

If the harness **copies** rather than symlinks, re-copy after every pull so the
live config and the repo do not drift. Check which mode you are in with
`readlink -f ~/.pi/agent/skills`: a resolved path outside this repo means it is a
copy, not a link.

To verify a factory setup specifically:

```bash
SKILL_DIR=<absolute path to the factory-supervisor skill directory>
python3 "$SKILL_DIR/scripts/factory-state.py" init   # idempotent, safe to re-run
python3 "$SKILL_DIR/scripts/factory-state.py" list   # empty until work is admitted
bb automation list --project <project-id> --json     # the wake automation
```

## Notes

- This repository is public. Review skill contents before pushing anything sensitive.
- Some skills reference local tooling or paths on my machine. Those references are intentional and may need adjustment elsewhere. Skill helper scripts live in the repo under `skills/<name>/scripts/` and are invoked relative to the skill directory, never by absolute path.
- Runtime state never lives in this repo. The factory supervisor keeps its ledger, task cache, and decision record under `~/.bb/state/factory/`, which is machine-local and unversioned by design.
- The intended workflow is to edit the repo and point the harness at it so the live configuration and the version-controlled copy do not drift.
