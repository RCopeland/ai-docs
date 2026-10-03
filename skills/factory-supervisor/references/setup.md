# Setting up a factory on a new machine

The skill travels in this repo. The wiring does not. Four things are
machine-specific, and each one is deliberate.

State always lives at `~/.bb/state/factory/`. The **path is the same on every
machine; the contents are not.** Each machine runs its own factories, so its
ledger records only its own work. Nothing syncs between machines, and nothing
needs to: a GitHub factory and a Wrike factory never share a task.

## What travels, what does not

| Piece | Where it lives | Travels? |
|---|---|---|
| `SKILL.md`, `references/`, `scripts/factory-state.py` | this repo (git) | **Yes** — clone or pull |
| `ledger.jsonl`, `tasks/`, `decisions.md` | `~/.bb/state/factory/` | **No** — machine-local |
| The wake automation | BB's database on that host | **No** — recreate it |
| Project IDs, provider, model | BB's config on that host | **No** — resolve fresh |

## Checklist

### 1. Get the repo

```bash
git clone <ai-docs-remote> ~/Dev/ai-docs
```

Wire it into the harness the way that machine's harness expects — for Pi, this
repo's README documents symlinking `global/AGENTS.md`, `agents/`, and `skills/`.
Note the existing caveat: if the harness copies rather than symlinks, re-copy
after every pull so the live config does not drift from the repo.

### 2. Initialise state

```bash
SKILL_DIR=<absolute path to the factory-supervisor skill directory>
python3 "$SKILL_DIR/scripts/factory-state.py" init
```

Creates `~/.bb/state/factory/` with a `decisions.md` starter. Idempotent, and it
never touches an existing ledger, so it is safe to re-run.

There is no `wake-prompt.md` to copy — write one for this machine (step 4).

### 3. Register the projects

BB projects are per-host. Register each repository this factory will work on, and
note the resulting project IDs:

```bash
bb project list --include-personal --json
```

Project IDs differ per machine. Never carry an ID from another machine.

### 4. Create the wake automation

Automations are per-host rows. Create one per factory on this machine:

```bash
bb automation create \
  --project <project-id> \
  --name "factory-supervisor wake" \
  --cron "*/15 * * * *" \
  --timezone <this machine's timezone> \
  --target-thread <this supervisor's thread id> \
  --provider <provider available here> \
  --model <a cheap model for this provider> \
  --reasoning none \
  --prompt "$(cat ~/.bb/state/factory/wake-prompt.md)"
```

Notes that cost time the first run:

- `--target-thread` re-prompts one thread rather than spawning new ones, so the
  supervisor keeps its identity and rotates itself at ~60% context.
- `--prompt-file` does **not** exist for automations; pass the prompt inline.
  Keep the prompt free of backticks and `$(...)`, or the shell will run them.
- Use a **cheap** model with `--reasoning none`. A wake is mostly reconciliation
  and most wakes should be near-free.
- `--permission-mode` is provider-dependent. `pi` supports only `full`; if that
  matters on this machine, choose a provider that supports `auto`.
- Get `--provider` and `--model` from `bb provider list --json` and
  `bb provider models <id> --json` on *this* host. Do not copy them.

Then test before trusting it:

```bash
bb automation run <automation-id> --project <project-id>
```

### 5. Confirm the intake source

The skill branches by source, but `references/intake.md` documents the GitHub
query concretely and leaves Wrike to the `wrike-ai-safe` skill. The two machines
are expected to differ here — a personal GitHub factory at home, a Wrike factory
at work.

For a source that is not yet fleshed out, extend `intake.md` in this repo so the
next machine does not rediscover the query. Keep the
`<factory>/<source>-<ref>` task-ID convention.

Intake is read-only. It never labels, comments on, or transitions a source item.

## Verifying the setup

```bash
# State dir exists and the helper runs
python3 "$SKILL_DIR/scripts/factory-state.py" init

# Ledger is readable (empty at first)
python3 "$SKILL_DIR/scripts/factory-state.py" list

# The automation is enabled and scheduled
bb automation show <automation-id> --project <project-id>

# This supervisor owns its children
bb thread list --parent-thread "$BB_THREAD_ID" --json
```

A healthy fresh setup reports an empty ledger, an enabled automation with a
`nextRunAt`, and no children.

## Common mistakes

- **Hardcoding `SKILL_DIR`.** The repo is cloned to different paths on different
  machines. Resolve it per session and verify `scripts/factory-state.py` is
  there.
- **Copying a project ID or automation ID from another machine.** Both are
  host-local; resolve them fresh.
- **Syncing `~/.bb/state/factory/` between machines.** Contents are meant to
  differ. Merging two ledgers creates duplicate task IDs and ambiguous state.
- **Forgetting that the repo and the live config are separate.** A pull changes
  the repo, not the harness's loaded skills.
