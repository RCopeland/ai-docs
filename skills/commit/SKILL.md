---
name: commit
description: Create polished, descriptive git commits with conventional structure. Use before committing code changes, especially as the final step of an implementation task.
---

# Commit Skill

Load this when your task is done and it's time to commit. A commit is communication: the message should tell a reviewer *what* changed and *why* — without them re-reading the diff.

## Before Committing

1. **Check what's changed:**
   ```bash
   git status --short
   git diff --stat
   git diff            # review unstaged
   git diff --cached   # review staged
   ```

2. **Stage deliberately.** Only stage files related to this task. No unrelated changes in the same commit. If you find unrelated edits, either revert them or commit them separately with their own message.

3. **Verify first.** The code should pass tests/typecheck before you commit:
   ```bash
   npm test 2>/dev/null; npm run typecheck 2>/dev/null
   ```
   (Use the project's actual test command — don't guess. If running tests is expensive, at minimum confirm the change compiles/loads.)

## Writing the Message

**Format (conventional commits):**

```
type(scope): subject

Body — why, not just what.

Refs: <issue/todo ids if known>
```

**Type:** `feat` (new feature), `fix`, `refactor` (no behavior change), `docs`, `test`, `chore` (tooling, deps), `perf`, `style`, `revert`.

**Subject rules:**
- Imperative mood, ≤ ~72 chars: "Add session timeout handling", not "Added..." or "fixes stuff"
- Scope in parens when useful: `feat(auth): require re-login after password change`

**Body rules (when non-trivial):**
- Explain the **why**: the decision, the constraint, the tradeoff — the diff shows the what
- If you made a judgment call ("chose X over Y because..."), say so
- Reference the plan/todo/ISC when relevant

**Anti-patterns:**
- `Update stuff` / `fixes` / `changes` — says nothing
- Committing generated artifacts, secrets, or local config
- Bundling a refactor with a feature in one commit

## Committing

```bash
git add <files>
git commit -m "type(scope): subject" -m "body"
```

- Use multiple `-m` flags for subject + body (clear separation).
- Don't use `git commit -am` blindly — it skips the deliberate staging step.
- **Never** amend pushed commits. If you need to amend an unpushed commit, that's fine.

## After

- Report the commit hash and subject in your summary.
- If the task tracked a todo, close it (see the `todo` tool: `todo(action: "update", id: ..., status: "closed")`).