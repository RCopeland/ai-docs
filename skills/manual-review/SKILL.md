---
name: manual-review
description: Launches or resumes a human-in-the-loop code review workflow using tmux and Hunk. Use when the user wants Pi to open hunk diff in tmux for manual review, then later inspect the user's Hunk comments and evaluate them against the live diff.
compatibility: Requires tmux, hunk, and a local Hunk session daemon. Best in repos with git changes to review.
---

# Manual Review

This skill is a higher-level wrapper around the `hunk-review` skill.

Always load and follow the `hunk-review` skill first when using this workflow by resolving its path with:

```bash
hunk skill path
```

Then read that `SKILL.md` and treat `manual-review` as the orchestration layer that adds tmux launch/resume flow and human-comment evaluation on top of `hunk-review`'s live-session commands.

Use this skill for a two-phase workflow:

1. Pi opens or reloads a Hunk review session in tmux for the user.
2. The user leaves Hunk **user comments** manually.
3. Pi comes back later, reads those comments through `hunk session` commands, and reviews them.

Do **not** try to drive Hunk's interactive TUI directly. Launch it for the user, then inspect and control the live session through `hunk session ...` commands.

Because this workflow depends on Hunk live-session operations, explicitly resolve and read the `hunk-review` skill with `hunk skill path` before proceeding. Reuse its command patterns, constraints, and error handling throughout.

## Requirements

Before doing anything else, load the `hunk-review` skill via:

```bash
hunk skill path
```

Before using this workflow, confirm these tools exist:

```bash
which tmux
which hunk
```

If `hunk session list` fails because no session exists, launch one in tmux first.

## Phase 1: Start manual review

When the user asks to start a manual review:

0. First run `hunk skill path`, read the returned `hunk-review` skill file, and use it as the source of truth for Hunk session operations.

1. Decide whether a matching Hunk session already exists:

```bash
hunk session list --json
```

2. If no suitable session exists, open a new tmux window in the target repo:

```bash
tmux new-window -n hunk-review -c "$PWD" 'hunk diff'
```

If the user wants a specific diff range, open Hunk with that command instead:

```bash
tmux new-window -n hunk-review -c "$PWD" 'hunk diff main...HEAD'
```

Tracked-only review:

```bash
tmux new-window -n hunk-review -c "$PWD" 'hunk diff --exclude-untracked'
```

3. Tell the user to switch to that tmux window, review changes, and leave **user comments** in Hunk.

Suggested wording:

- "I opened Hunk in a tmux window named `hunk-review`. Leave your inline user comments there, then come back and ask me to review them."

## Phase 2: Resume and review the user's comments

When the user returns and asks you to review their comments:

0. Reload or re-check the `hunk-review` skill via `hunk skill path` if needed, and follow its live-session guidance while evaluating the user's comments.

1. Find the active session for the repo:

```bash
hunk session get --repo . --json
```

2. List the user's comments:

```bash
hunk session comment list --repo . --type user
```

3. Inspect review structure first without pulling full patch text unless needed:

```bash
hunk session review --repo . --json
hunk session context --repo . --json
```

4. For each meaningful user comment, inspect the relevant file/hunk. Prefer structure first; add patch text only when needed:

```bash
hunk session navigate --repo . --file <path> --new-line <line>
hunk session review --repo . --include-patch --json
```

5. Evaluate each comment against the diff and classify it. Use categories like:

- valid
- valid but weakly justified
- redundant
- incorrect
- outdated after later edits
- actionable follow-up

6. Return a concise review summary. For each comment, include:

- file and line
- the user's comment summary
- your evaluation
- recommended next step

## Optional follow-ups

If the user wants, after reviewing their comments you may:

- convert approved findings into agent comments with `hunk session comment add` or `comment apply`
- turn approved findings into implementation tasks
- fix issues directly in the repo
- write a summary file such as `.review/manual-review.md`

## Operating rules

- `hunk-review` is the operational dependency; this skill should defer to it for exact Hunk CLI behavior.

- Human comments are the source material; do not overwrite or clear them unless the user asks.
- Prefer `--type user` when reviewing human-authored notes.
- Keep Pi's evaluation separate from the user's original wording.
- Do not spam comments on every hunk; focus on whether the user's comments are sound and useful.
- If multiple Hunk sessions match, ask the user which one to use or select by explicit session id.
- If the session already exists, prefer reusing it over launching a second review window.

## Common commands

Check sessions:

```bash
hunk session list --json
hunk session get --repo . --json
```

Launch Hunk in tmux:

```bash
tmux new-window -n hunk-review -c "$PWD" 'hunk diff'
```

Read user comments:

```bash
hunk session comment list --repo . --type user
```

Inspect focus and structure:

```bash
hunk session context --repo . --json
hunk session review --repo . --json
```

## Common errors

- **No active Hunk sessions**: open a tmux Hunk window first.
- **Multiple active sessions match**: use the exact session id.
- **No visible diff file matches**: the file is not in the currently loaded review; reload or confirm the repo/session.
- **tmux not found**: ask the user to install tmux or launch Hunk manually.
- **hunk not found**: ask the user to install Hunk.

## Skill relationship

Use `manual-review` to decide *when* to launch Hunk, *when* to resume, and *how* to evaluate human comments.

Use `hunk-review` to decide *how* to talk to the live Hunk session.

In practice, that means:

1. run `hunk skill path` and read/load `hunk-review`
2. launch or inspect the session
3. let the human review in Hunk
4. read `--type user` comments
5. evaluate them against the live diff

## Response patterns

When starting review, be brief and action-oriented.

Example:

- "Opened `hunk diff` in a new tmux window named `hunk-review`. Leave your Hunk user comments there, then come back and ask me to review them."

When reviewing comments, summarize clearly.

Example:

- "I found 4 Hunk user comments. 2 are solid, 1 is redundant with an existing change, and 1 appears incorrect because the null check already happens earlier in the hunk."
