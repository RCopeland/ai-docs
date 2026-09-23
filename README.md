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
| `dev-task-orchestrator` | End-to-end task workflow through scout / dev / review / publish stages |
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

## Portability

| Layer | Status |
| --- | --- |
| `skills/` | Portable. Each skill is a Markdown package with frontmatter. |
| `reference/standards/` | Portable. Plain reference docs. |
| `agents/` | Mostly portable. The role prompts transfer well; frontmatter may need mapping by harness. |
| `global/AGENTS.md` | Least portable. It is written for my orchestration workflow and current tool conventions. |

The concepts transfer more easily than the wiring. Skills and standards are straightforward to reuse; agents and global instructions may need tool-name or frontmatter adjustments in another harness.

## Wiring into Pi

Pi treats global instructions, agents, and skills separately.

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

## Notes

- This repository is public. Review skill contents before pushing anything sensitive.
- Some skills reference local tooling or paths on my machine. Those references are intentional and may need adjustment elsewhere.
- The intended workflow is to edit the repo and symlink Pi to it so the live configuration and the version-controlled copy do not drift.
