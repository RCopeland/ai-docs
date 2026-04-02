# Prettier Configuration

## References

- Prettier Documentation: https://prettier.io/docs/
- Prettier Options: https://prettier.io/docs/options

## Installation

```bash
npm install --save-dev prettier eslint-config-prettier
```

## Standard Configuration

Create `prettier.config.js` in project root:

```js
/** @type {import('prettier').Config} */
export default {
  // Print width
  printWidth: 100,

  // Tab width
  tabWidth: 2,

  // Use spaces instead of tabs
  useTabs: false,

  // Semicolons at end of statements
  semi: true,

  // Use single quotes
  singleQuote: true,

  // Quote props only when needed
  quoteProps: "as-needed",

  // Trailing commas
  trailingComma: "es5",

  // Spaces inside object literals
  bracketSpacing: true,

  // Arrow fn single param doesn't need parens
  arrowParens: "always",

  // Format JSX
  jsxSingleQuote: false,

  // Vue files
  vueIndentScriptAndStyle: false,

  // End of line
  endOfLine: "lf",

  // Embedded languages
  embeddedLanguageFormatting: "auto",
};
```

## Alternative: JSON Format

Create `.prettierrc`:

```json
{
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "semi": true,
  "singleQuote": true,
  "quoteProps": "as-needed",
  "trailingComma": "es5",
  "bracketSpacing": true,
  "arrowParens": "always",
  "endOfLine": "lf"
}
```

## Key Options Explained

| Option | Value | Rationale |
|--------|-------|-----------|
| `printWidth` | 100 | Good balance for modern screens |
| `tabWidth` | 2 | Standard, readable |
| `semi` | true | Prevents bugs with ASI |
| `singleQuote` | true | Less keystrokes, consistent |
| `trailingComma` | "es5" | ES5 compatible, cleaner diffs |
| `bracketSpacing` | true | Better readability |

## Integration with ESLint

Use `eslint-config-prettier` to disable ESLint formatting rules that conflict with Prettier:

```bash
npm install --save-dev eslint-config-prettier
```

Then in `eslint.config.js`:

```js
import prettier from "eslint-config-prettier";

// Add to end of config array
{ rules: prettier.rules }
// or use spread: ...prettier.rules
```

## Verify Compatibility

After setup, run:

```bash
npx eslint . --format stylish
```

If configured correctly, you should see no "conflicting" warnings from Prettier rules.

## Editor Integration

### VS Code

```json
// .vscode/settings.json
{
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  }
}
```

## When to Customize

- **Legacy project**: Match existing style (80 chars, single quotes)
- **Team conventions**: Follow team guidelines
- **Framework requirements**: Some frameworks need specific settings