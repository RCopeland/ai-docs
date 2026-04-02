# TypeScript Standards

## References

- TypeScript Documentation: https://www.typescriptlang.org/docs/
- Effective TypeScript: https://blog.dennisokeeffe.io/blog/2025-03-16-effective-typescript-principles-in-2025
- TypeScript Best Practices 2025: https://dev.to/mitu_mariam/typescript-best-practices-in-2025-57hb
- typescript-eslint: https://typescript-eslint.io/

## ESLint

Use `@typescript-eslint` for TypeScript projects:

```bash
npm install --save-dev @typescript-eslint/parser @typescript-eslint/eslint-plugin @eslint/js eslint-config-prettier
```

```js
// eslint.config.js
import js from "@eslint/js";
import tsParser from "@typescript-eslint/parser";
import tsPlugin from "@typescript-eslint/eslint-plugin";
import prettier from "eslint-config-prettier";

export default [
  js.configs.recommended,
  {
    files: ["**/*.ts", "**/*.js"],
    languageOptions: { parser: tsParser },
    plugins: { "@typescript-eslint": tsPlugin },
    rules: {
      ...tsPlugin.configs.recommended.rules,
      ...prettier.rules,
    },
  },
];
```

## Type Safety

### No `any`

- Never use `any` - use `unknown` if type is truly unknown
- Prefer strict typing over implicit any

```typescript
// BAD
const data: any = fetchData();

// GOOD
interface User {
  id: number;
  name: string;
}
const data = ref<User[]>([]);
```

### Interfaces and Types

- Use interfaces for object shapes that may be extended
- Use types for unions, intersections, and primitives
- Define reusable types in a `types/` directory

### Generics

- Use generics in composables and utility functions
- Constrain generics when you need specific properties

```typescript
// GOOD - generic with constraint
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
```

## Type Inference

- Let TypeScript infer types from initial values when possible
- Add explicit types when inference isn't clear
- Use `as const` for literal types

```typescript
// GOOD - inference from initial value
const items = ref<string[]>([]);

// GOOD - explicit return type
function processData(data: string[]): Promise<Result> {
  // ...
}
```

## Common Patterns

### Optional Properties

- Use `?` for optional properties
- Check for existence before use

### Null Handling

- Use optional chaining (`?.`) and nullish coalescing (`??`)
- Avoid non-null assertions (`!`) unless certain

### Enums

- Prefer const objects or string unions over enums

## What to Check

When reviewing TypeScript code, look for:

- [ ] No `any` types
- [ ] Proper interfaces/types for reusable shapes
- [ ] Generics used appropriately
- [ ] Type inference leveraged where appropriate
- [ ] Optional chaining used for nested property access
- [ ] No hardcoded type assertions that bypass safety
