---
name: start-up
description: Prepare for a new task by checking git state, fetching latest, validating branch name, checking related issues, and running tests.
license: MIT
compatibility: opencode
---

# Start-Up Skill

Prepare the workspace for a new task by ensuring everything is clean and ready.

## What I Do

When the user wants to start working on something new, I perform these steps:

### 1. Determine What We're Working On

Ask the user what they want to work on if not explicitly stated.

### 2. Check Git Status

Run these git commands to verify the working directory is clean:
- `git status` - Check for pending changes
- `git diff --stat` - See what files would be changed

**If there are uncommitted changes (tracked or untracked), STOP and ask the user how to proceed:**
- Stash them
- Commit them
- Discard them

Do not proceed until the working directory is clean.

### 3. Validate Branch Name

Check the current git branch name. If it doesn't match the task (e.g., on "main", "master", or an unrelated feature branch):

1. Derive an appropriate branch name from the issue/task:
   - Use kebab-case (e.g., `add-combat-log`, `fix-npc-health-bar`)
   - Prefix with type: `feature/`, `fix/`, `refactor/`, `docs/`
   - Example: Issue "encounter management" → `feature/encounter-management`
2. Create and checkout the new branch: `git checkout -b <branch-name>`

Only ask the user for a branch name if the derived name is ambiguous.

### 4. Fetch Latest from Origin

Run `git fetch origin` to get the latest remote changes.

### 5. Check for Related GitHub Issues

Search for related issues using `gh issue list` if the user has a GitHub repo configured. Ask the user if they want me to search for issues related to the task.

### 6. Run Unit Tests

Run the project's unit tests to ensure the codebase is in a good state before starting:
- Look for test scripts in package.json: `npm run test`, `npm run test:unit`, `npm run test:watch`
- If using vitest: `npm run test:unit -- --run` for non-watch mode
- If using jest: `npm test` or `npm run test -- --passWithNoTests`

Report test results to the user.

## When to Use

Use this skill at the beginning of a new task or work session to ensure the workspace is clean and ready.

Example invocations:
- "Let's start working on X"
- "I'm ready to begin a new feature"
- "Prepare the workspace for adding X"
