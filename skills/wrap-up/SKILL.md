---
name: wrap-up
description: Prepare changes for commit and PR. Run tests, check coverage, validate browser, summarize changes, generate commit message, and create PR.
license: MIT
compatibility: opencode
---

# Wrap-Up Skill

Prepare code changes for commit and pull request.

## Workflow

### 1. Run Unit Tests

Run the unit tests to ensure everything passes:
```bash
npm test
```
Or if using vitest:
```bash
npm run test -- --run
```

If tests fail, report failures and stop - do not proceed.

### 2. Run Prettier

Run prettier to format staged files:
```bash
npx prettier --write $(git diff --cached --name-only --diff-filter=ACM)
```

### 3. Check Code Coverage

Run tests with coverage:
```bash
npm test -- --coverage
```

Check the coverage output:
- If overall statement coverage is provided, verify it meets project threshold (typically >80%)
- If coverage decreased, report which files are below threshold
- Do not proceed if coverage is insufficient

### 4. Check Browser for JS Errors

For frontend projects, check for runtime errors:
1. Start dev server if not running: `npm run dev &`
2. Navigate to the app
3. Check console for any JS errors
4. Report any errors found - do not proceed if there are errors

### 5. Summarize Changes

Run git status and git diff to see what changed:
```bash
git status
git diff --staged
git diff
```

Summarize:
- Files modified
- Files added
- Files deleted
- Nature of changes (refactor, bug fix, feature, etc.)

Verify the correct changes are staged for commit.

### 5b. Check for Unstaged/Untracked Changes

Before proceeding, check for any changes that aren't staged:
```bash
git status
```

If there are unstaged changes or untracked files:
- Ask the user if they want to stage and include them
- Or if they should be ignored (e.g., .env files, build artifacts)
- Do NOT auto-stage without explicit user approval

### 6. Check Branch Name

Check current branch name:
```bash
git branch --show-current
```

Evaluate if the branch name is appropriate:
- Should be descriptive (e.g., `fix/party-persistence`, `refactor/combat-store`)
- Should follow conventional commits format if used
- If name is poor, suggest a better one but do NOT rename (let user decide)

### 7. Generate Commit Message

Analyze the changes and generate a conventional commit message:
- Format: `type(scope): description`
- Types: `fix`, `feat`, `refactor`, `chore`, `docs`, `test`
- Description should be concise (under 50 chars)
- If fixes issues, include `Closes #123` or `Fixes #123`

Look for:
- Issue references in commit history or branch name
- What the change actually does

Present the commit message to user for approval.

### 8. Create Commit (after approval)

After user approves commit message:
1. Stage all relevant files: `git add <files>`
2. Create commit: `git commit -m "message"`

### 9. Push and Create PR

1. Push to origin: `git push -u origin <branch-name>`
2. Create PR using gh CLI:
   ```bash
   gh pr create --title "PR title" --body "Description"
   ```

Or if using a template:
   ```bash
   gh pr create --fill
   ```

Return the PR URL to the user.

## When to Use

Use this skill when:
- User asks to wrap up changes
- User asks to prepare for commit/PR
- User asks to save/commit changes
- All coding work is complete and ready for review
