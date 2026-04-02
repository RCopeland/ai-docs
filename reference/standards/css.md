# CSS Standards

## References

- MDN CSS Reference: https://developer.mozilla.org/en-US/docs/Web/CSS
- Modern CSS 2025: https://dev.to/dimeloper/css-techniques-every-developer-should-know-in-2025-30p9
- CSS Best Practices 2025: https://javascript.plainenglish.io/css-best-practices-in-2025-whats-in-what-s-out-and-what-s-timeless-3c29dce93cc0
- eslint-plugin-css: https://ota-meshi.github.io/eslint-plugin-css/

## ESLint

Use `eslint-plugin-css` for CSS files:

```bash
npm install --save-dev eslint-plugin-css
```

```js
// eslint.config.js
import cssPlugin from "eslint-plugin-css";

export default [
  {
    files: ["**/*.css"],
    plugins: { css: cssPlugin },
    rules: cssPlugin.configs.recommended.rules,
  },
];
```

## Modern CSS Features

### Container Queries

```css
.container {
  container-type: inline-size;
}

@container (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: auto 1fr;
  }
}
```

### CSS Nesting

```css
.card {
  & h2 { margin: 0; }
  & p { color: gray; }
  &:hover { shadow: ... }
}
```

### Custom Properties

```css
:root {
  --color-primary: oklch(70% 0.15 250);
  --spacing-md: 1rem;
}

.element {
  color: var(--color-primary);
  padding: var(--spacing-md);
}
```

## Layout

### Grid

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}
```

### Flexbox

```css
.flex-center {
  display: flex;
  justify-content: center;
  align-items: center;
}
```

### Container Queries vs Media Queries

Use container queries for component-based responsive design:

```css
/* Instead of */
@media (min-width: 768px) { ... }

/* Use */
@container (min-width: 500px) { ... }
```

## Typography

### Clamp for Responsive Font Size

```css
h1 {
  font-size: clamp(1.5rem, 5vw, 3rem);
}
```

### Fluid Typography

```css
body {
  font-size: clamp(1rem, 0.5rem + 1vw, 1.25rem);
}
```

## Colors

### Modern Color Functions

```css
/* OKLCH - modern, perceptually uniform */
:root {
  --color: oklch(70% 0.15 250 / 0.5);
}

/* Relative color */
.button {
  background: oklch(from var(--primary) calc(l + 10%) calc(c) calc(h));
}
```

## Performance

### Content Visibility

```css
.lazy-section {
  content-visibility: auto;
  contain-intrinsic-size: 1px 500px;
}
```

### Will Change

```css
.animated {
  will-change: transform;
  /* Use sparingly, only when needed */
}
```

## Anti-Patterns

### Avoid

- Excessive nesting (keep specificity low)
- Magic numbers
- Unused styles
- Inline styles

### Prefer

- Utility classes (Tailwind)
- Custom properties for repeated values
- Logical properties (margin-inline-start vs margin-left)
- Relative units (rem, em, ch, lh)

## Logical Properties

```css
/* Instead of */
margin-left: 1rem;
padding-right: 2rem;
border-top: 1px solid;

/* Use */
margin-inline-start: 1rem;
padding-inline-end: 2rem;
border-block-start: 1px solid;
```

## What to Check

- [ ] Modern CSS features used (container queries, nesting)
- [ ] No excessive specificity/nesting
- [ ] Custom properties for repeated values
- [ ] Logical properties for internationalization
- [ ] Responsive without media queries where possible
- [ ] Performance optimizations (content-visibility, will-change)
- [ ] Colors use modern color functions (oklch, lch)