# AI Developer Workflow Bootstrap

This is a personal bootstrap for AI-assisted development. Copy to new projects as starting point.

## Workflow

The development workflow is a loop: **Plan → Implement → Validate → Review → Fix → Publish**

### Core Principles

1. **More frequent, smaller reviews** - Review at natural boundaries, not just "done"
2. **Validate before presenting** - Run tests/lint before showing for review
3. **Diff views by default** - Show what changed, not full files
4. **User decides** - Always up to user what changes to make during review

### Startup

- Run `start-up` skill at the beginning of tasks
- Use during planning, before implementing

### Loop (Plan through Fix)

1. **Plan** - Understand requirements, break into steps
   - **Research first**: Before writing tests or code, search the codebase for similar patterns
2. **Implement** - Write code
   - Load relevant reference files for the technology/context
   - Follow standards as you code
3. **Validate** - Run typecheck, lint, tests
4. **Automated Review** - Run lint/typecheck, check for issues
5. **Fix** - Address automated review findings
6. **Manual Review** - Review at natural boundaries, not all at once
7. **Fix** - Address review findings
8. **Publish** - Exit loop, everything verified and reviewed

### Implementation Standards

**Important:** Before you process a prompt, check if you need to load a reference file based on the technology/context of the request.

Load these reference files when writing code. Tell the user which files are being loaded:

| Context              | Files to Load                                                                |
| -------------------- | ---------------------------------------------------------------------------- |
| Vue 3 + TypeScript   | `vue.md`, `typescript.md`, `component-design.md`, `eslint.md`, `prettier.md` |
| Frontend (any)       | `html.md`, `css.md`, `javascript.md`, `accessibility.md`                     |
| Performance-critical | `performance.md`                                                             |
| Plain JavaScript     | `javascript.md`, `typescript.md`, `eslint.md`, `prettier.md`                 |
| Node.js/CLI          | `javascript.md`, `typescript.md`, `eslint.md`, `prettier.md`                 |
| Testing (general)    | `testing.md`, `typescript.md`                                                |
| Testing (Vitest)     | `vitest.md`, `testing.md`, `typescript.md`                                   |

Follow the standards in these files while coding to prevent issues before validation.

## Ready for Review Checklist

Before presenting any work for manual review, agent must verify:

1. ✅ All tests pass (`npm run test`)
2. ✅ Lint passes (`npm run lint`)
3. ✅ Typecheck passes (`npm run typecheck`)
4. ✅ Coverage is acceptable (>80% or maintained)
5. ✅ Agent has self-reviewed the changes
6. ✅ Agent can summarize what changed and why

**Only present for review when ALL items pass.**

## Code Conventions

- Use existing code patterns in the project
- **Use existing components when available** - Check for existing components before creating new ones
- Prefer existing libraries/frameworks over adding new ones
- Avoid unnecessary comments
- Be concise - answer directly without preamble

## Git Workflow

- **NEVER commit without explicit instruction** - Wait for user to say "commit"
- **NEVER push without explicit instruction** - Wait for user to say "push"
- **ALWAYS ask before committing** - Present what will be committed and ask for confirmation
- **ALWAYS ask before pushing** - Confirm with user before pushing
- **Check for untracked files before commit** - Run `git status` and ensure no untracked files exist unless the user is aware

## Preferences

- ESLint for linting
- TypeScript when available
- Vue 3 + Composition API for frontend

## Development Practices

### Validation Commands

Run these in order:

1. `npm run lint` or `npx eslint ...`
2. `npm run typecheck` or `npx vue-tsc --noEmit` / `tsc --noEmit`
3. `npm run test` or test suite

All must pass with **no errors or warnings** (within reason) before proceeding to manual review.

### Browser Console Validation

For frontend projects, verify no JavaScript errors in browser:
- Use Chrome DevTools to check console for errors
- Clear console, reload page, check for new errors
- Report any errors found before review

## Manual Component Review

### When to Review

- Review at natural boundaries (after each feature/component, not just at "done")
- More frequent, smaller reviews preferred
- Don't wait for a large scope - review as you go

### Ready for Review Protocol

Before presenting work:
1. Run all validation (tests, lint, typecheck)
2. Show diff of changes, not full file contents
3. Provide summary: what changed, why, any concerns
4. Include test results/coverage
5. Ask: "Ready for your review?"

### Status Tracking

Use a table to track review progress:

```markdown
## Review Status

### New Files

| File          | Status     | Notes       |
| ------------- | ---------- | ----------- |
| Component.vue | ✅ Done    | Reviewed    |
| Another.vue   | 🔄 Ready   | In progress |
| Third.vue     | ⬜ Pending |             |

### Modified Files

| File     | Status     | Notes        |
| -------- | ---------- | ------------ |
| File.vue | ⬜ Pending | Minor change |
```

**Status Legend:**
- ✅ Done - Reviewed and approved
- 🔄 Ready - Reviewed, has items to address
- ⬜ Pending - Not yet reviewed

### Output Format

For **existing components**, show diff view:
```diff
- removed line
+ added line
```

For **new components**, show full code in blocks:
```typescript
// script
```

```html
// template
```

```css
// styles (if applicable)
```

Always include brief explanation of changes, not just the code.

### Review Item Categories

- **[Bug]** - Something is broken or incorrect
- **[UX]** - User experience concern
- **[Perf]** - Performance issue
- **[A11y]** - Accessibility concern
- **[TypeScript]** - Type safety issue
- **[Style]** - Code style/consistency
- **[Security]** - Security concern
- **[Suggestion]** - Optional improvement idea

### Workflow

1. Check git status for changed files
2. Verify validation passes before presenting
3. Create/update review status table
4. Present diff view + summary (not full files)
5. User decides what changes to make
6. Update table as reviews complete

## Deferred Items

When fixing issues during implementation, if you notice things that aren't critical:
- Note them as "deferred" for later
- Don't derail current task for non-critical fixes
- Can be addressed in cleanup phase at end

## Skills

This directory contains reusable skills:
- `skills/start-up/` - Startup workflow skill
- `skills/wrap-up/` - Wrap-up/commit preparation skill

---

## Notes

<!-- Add project-specific notes here -->