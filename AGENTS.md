# AI Developer Workflow Bootstrap

This is a personal bootstrap for AI-assisted development. Copy `AGENTS.md` to new projects as a starting point.

## Workflow

The development workflow is a loop: **Plan → Implement → Validate → Automated Review → Fix → Manual Review → Fix → Publish**

### Startup
- Run `start-up` skill at the beginning of tasks
- Use during planning, before implementing

### Loop (Plan through Fix)
1. **Plan** - Understand requirements, break into steps
2. **Implement** - Write code
   - Load relevant reference files for the technology/context
   - Follow standards as you code
3. **Validate** - Run typecheck, lint, tests
4. **Automated Review** - Run lint/typecheck, check for issues
5. **Fix** - Address automated review findings
6. **Manual Review** - Use Review mode for chunk-based review
7. **Fix** - Address manual review findings
8. **Publish** - Exit loop, everything verified and reviewed

### Implementation Standards

**Important:** Before you process a prompt, check if you need to load a reference file based on the technology/context of the request.

Load these reference files when writing code. Tell the user which files are being loaded:

| Context | Files to Load |
|---------|---------------|
| Vue 3 + TypeScript | `vue.md`, `typescript.md`, `component-design.md`, `eslint.md`, `prettier.md` |
| Frontend (any) | `html.md`, `css.md`, `javascript.md`, `accessibility.md` |
| Performance-critical | `performance.md` |
| Plain JavaScript | `javascript.md`, `typescript.md`, `eslint.md`, `prettier.md` |
| Node.js/CLI | `javascript.md`, `typescript.md`, `eslint.md`, `prettier.md` |
| Testing (general) | `testing.md`, `typescript.md` |
| Testing (Vitest) | `vitest.md`, `testing.md`, `typescript.md` |

Follow the standards in these files while coding to prevent issues before validation.

### ESLint Setup

For new projects, construct ESLint config by:
1. Loading the ESLint section from relevant technology reference files
2. Combining configs as described in `eslint.md`
3. Verifying no conflicts with Prettier (ask if unsure)

### Publish (Exit)
- Run `wrap-up` skill
- Ensure all lint/typecheck pass
- Ensure all tests pass
- Ensure manual review is complete
- Commit and PR ready

## Code Conventions

- Use existing code patterns in the project
- Prefer existing libraries/frameworks over adding new ones
- Avoid unnecessary comments
- Be concise - answer directly without preamble

## Git Workflow

- **NEVER commit without explicit instruction** - Wait for user to say "commit" or "ready to commit"
- **NEVER push without explicit instruction** - Wait for user to say "push" or "ready to push"
- **ALWAYS ask before committing** - Present what will be committed and ask for confirmation
- **ALWAYS ask before pushing** - Confirm with user before pushing to remote
- **Summarize all changes** - When asked to summarize changes, always report staged, unstaged, and untracked changes separately. Make the user explicitly aware of any unstaged or untracked files that are not included in the summary.

## Preferences

- ESLint for linting
- TypeScript when available
- Vue 3 + Composition API for frontend

## Development Practices

### Validation with ESLint

ESLint is the primary tool for automated code validation. Run linting as part of every automated review step:

- **Frontend (Vue/React)**: `eslint --ext .vue,.js,.ts src/`
- **Backend (Node)**: `eslint --ext .js,.ts src/`
- **CLI tools**: `eslint --ext .js,.ts src/`
- **Configuration**: Use `eslint.config.js` (flat config) when possible

### Project Setup

For new projects, ensure:

- ESLint configured with appropriate parser and plugins
- Prettier configured (see `prettier.md`)
- TypeScript strict mode enabled
- Git hooks (husky) for pre-commit lint checks

### Stack Conventions

| Context | Linter | Type Check |
|---------|--------|------------|
| Vue 3 + TypeScript | ESLint + vue-eslint-parser | vue-tsc |
| React + TypeScript | ESLint + @typescript-eslint/parser | tsc --noEmit |
| Node.js + TypeScript | ESLint + @typescript-eslint/parser | tsc --noEmit |
| Vanilla JS/TS | ESLint | tsc (if using TS) |

### Validation Commands

Run these in order:
1. `npm run lint` or `npx eslint ...`
2. `npm run typecheck` or `npx vue-tsc --noEmit` / `tsc --noEmit`
3. `npm run test` or test suite

All must pass with **no errors or warnings** (within reason) before proceeding to manual review.

### Fix Guidelines

When ESLint reports issues:
- **DEFAULT to fixing the issue** - Don't disable rules or comment out code
- **If no clear fix exists** - Ask user for guidance
- **Prop mutations**: Refactor to use emits or local state instead of mutating props

### Browser Console Validation

For frontend projects, verify no JavaScript errors in the browser console:
- Open browser DevTools and check Console tab for errors
- Clear console, reload page, check for new errors
- Report any errors found

## Manual Component Review

When user asks to review component + tests together:

### Output Format

For **new components**, show full code in triple-backtick blocks with language specifier:
- Script: ```typescript
- Template: ```html
- Style: ```css

For **existing components**, show a diff view of changes.

Use this exact format:

```markdown
## [N]. [ComponentName].vue

[Full new component code OR diff for existing component]

### Suggestions
- [Category] Line X: Brief issue/fix

---

## Tests: [ComponentName].spec.ts

[Full test code - no truncation]

### Suggestions
- [Category] Line X: Brief issue/fix

---

**Remaining ([N]):**
1. ~~[ComponentName].vue~~ ✅
2. [Next Component].vue
```

### Syntax Highlighting for Component Code

Use triple backticks with language specifier to get syntax highlighting:
- **Script section**: ```typescript
- **Template section**: ```html
- **Style section**: ```css

Example:

```typescript
<script setup lang="ts">
import { ref } from 'vue'
</script>
```

```html
<template>
  <div>Component</div>
</template>
```

```css
<style scoped>
.class { color: red; }
</style>
```

### Test File Review

For manual component review, show the FULL test code even if long - do not truncate. Use ```typescript for test files.

### Workflow

1. Update todo list in todowrite tool
2. Show component code (full file, no truncation, ```typescript for script, ```html for template, ```css for styles)
3. Show test code (full file, no truncation)
4. Provide review notes with line references
5. Show remaining items list
6. Ask user if ready for next

## Modes

### Review Mode

When user invokes Review mode or asks to review code:

1. **Load Standards Dynamically** - Based on file types being reviewed:
   - Vue/TypeScript files → `vue-review.md`, `typescript.md`, `vue.md`
   - Vue components → `component-design.md`
   - Any frontend → `accessibility.md`, `performance.md`, `html.md`, `css.md`
   - Plain JavaScript → `javascript.md`, `typescript.md`
   - Always load `vue-review.md` as base

2. **Show Whole Files** - Present the FULL file code without truncating:
   - Use ```typescript for script blocks, ```html for templates, ```css for styles
   - Include all lines with line numbers
   - Do not truncate even for large files

3. **Output Format** - Use:
   ```
   ## [ComponentName].vue

   ```typescript
   [full script code]
   ```

   ```html
   [full template code]
   ```

   ```css
   [style block if present]
   ```

   ### Suggestions
   - **[Category]** Line X: Brief issue
   ```

4. **Summary** - End with review summary:
   - Files reviewed
   - Key issues (top 3-5)
   - Praise (good patterns)

## Notes

<!-- Add project-specific notes here -->