# ESLint Configuration

## Agent Instructions

When setting up ESLint for a project:

1. **Identify technologies**: Determine which technologies are used (Vue, TypeScript, JavaScript, HTML, CSS)
2. **Load relevant reference files**: Read the ESLint sections from each technology's standards file:
   - `vue.md` → Vue 3 + TypeScript ESLint config
   - `typescript.md` → TypeScript ESLint config
   - `javascript.md` → Vanilla JavaScript ESLint config
   - `html.md` → HTML ESLint config
   - `css.md` → CSS ESLint config
3. **Combine configs**: Merge the configs for all technologies in the project
4. **Verify no conflicts**: Ensure rules don't conflict with each other or with Prettier
5. **Ask if unsure**: If unclear on how to combine configs or if conflicts exist, ask the user

## Conflict Prevention

### Prettier Compatibility

Always include `eslint-config-prettier` last to disable conflicting ESLint rules:

```js
import prettier from "eslint-config-prettier";

// At the end of the config array
...prettier.rules
```

### Multi-Tech Projects

For projects with multiple technologies (e.g., Vue + TS + HTML):

1. Start with base JavaScript config
2. Add TypeScript-specific rules
3. Add Vue-specific rules (with Vue parser)
4. Add other file type configs
5. Always end with Prettier rules

### Verification Steps

- Run `npx eslint .` to check for errors
- Verify no rules conflict: `npx eslint --print-config .` | grep -i conflict
- Ensure Prettier is last in config array
- Test with `eslint-config-prettier` by running `npx eslint .` - should have no "conflicting" warnings

## Quick Reference

| Technology | Package | Config Key |
|------------|---------|------------|
| JavaScript | `@eslint/js` | `js.configs.recommended` |
| TypeScript | `@typescript-eslint/*` | `plugin:@typescript-eslint/recommended` |
| Vue 3 | `eslint-plugin-vue` | `plugin:vue/vue3-recommended` |
| HTML | `@html-eslint/*` | `plugin:html-eslint/recommended` |
| CSS | `eslint-plugin-css` | `plugin:css/recommended` |
| Prettier | `eslint-config-prettier` | `prettier.rules` |

## When to Ask

- Unclear how to combine multiple tech configs
- Rules appear to conflict
- Custom rules needed for specific project requirements
- Not sure which parser to use for a file type
- Need to configure specific rules beyond defaults