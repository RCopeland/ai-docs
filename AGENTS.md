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

Load these reference files when writing code:

| Context | Files to Load |
|---------|---------------|
| Vue 3 + TypeScript | `vue.md`, `typescript.md`, `component-design.md`, `eslint.md`, `prettier.md` |
| Frontend (any) | `html.md`, `css.md`, `javascript.md`, `accessibility.md` |
| Performance-critical | `performance.md` |
| Plain JavaScript | `javascript.md`, `typescript.md`, `eslint.md`, `prettier.md` |
| Node.js/CLI | `javascript.md`, `typescript.md`, `eslint.md`, `prettier.md` |

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

### Browser Console Validation

For frontend projects, verify no JavaScript errors in the browser console:
- Open browser DevTools and check Console tab for errors
- Clear console, reload page, check for new errors
- Report any errors found

## Modes

### Review Mode

When user invokes Review mode or asks to review code:

1. **Load Standards Dynamically** - Based on file types being reviewed:
   - Vue/TypeScript files → `vue-review.md`, `typescript.md`, `vue.md`
   - Vue components → `component-design.md`
   - Any frontend → `accessibility.md`, `performance.md`, `html.md`, `css.md`
   - Plain JavaScript → `javascript.md`, `typescript.md`
   - Always load `vue-review.md` as base

2. **Chunk-Based Review** - Present code in 50-100 line chunks with:
   - Title describing the chunk
   - Code with line numbers
   - Structure/organization notes
   - Suggestions as concise bullets with category and line reference

3. **Iteration** - End each chunk with "Ready for next chunk?" or "Review complete"

4. **Apply Changes** - When user asks to fix:
   - Apply changes with edit/write tools
   - Re-verify the modified code
   - Present changes back for review

5. **Output Format** - Use:
   ```
   ## Chunk [N]: [Title]
   
   ### Code
   [50-100 lines with line numbers]
   
   ### Structure
   [Organization notes]
   
   ### Suggestions
   - **[Category]** Line X: Brief issue
   ```

6. **Summary** - End with review summary:
   - Files reviewed
   - Key issues (top 3-5)
   - Praise (good patterns)

## Notes

<!-- Add project-specific notes here -->