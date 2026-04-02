# HTML Standards

## References

- MDN HTML Reference: https://developer.mozilla.org/en-US/docs/Web/HTML
- Semantic HTML 2025: https://dev.to/gerryleonugroho/semantic-html-in-2025-the-bedrock-of-accessible-seo-ready-and-future-proof-web-experiences-2k01

## ESLint

Use `@html-eslint` for HTML files:

```bash
npm install --save-dev @html-eslint/parser @html-eslint/eslint-plugin
```

```js
// eslint.config.js
import htmlParser from "@html-eslint/parser";
import htmlPlugin from "@html-eslint/eslint-plugin";

export default [
  {
    files: ["**/*.html"],
    languageOptions: { parser: htmlParser },
    plugins: { "html-eslint": htmlPlugin },
    rules: htmlPlugin.configs.recommended.rules,
  },
];
```

## Semantic HTML

### Use Semantic Elements

Prefer semantic elements over generic divs:

```html
<!-- BAD -->
<div class="header"></div>
<div class="nav"></div>
<div class="main"></div>
<div class="footer"></div>

<!-- GOOD -->
<header></header>
<nav></nav>
<main></main>
<footer></footer>
```

### Semantic Elements List

| Element | Use For |
|---------|---------|
| `<header>` | Page or section header |
| `<nav>` | Navigation links |
| `<main>` | Primary content area |
| `<article>` | Self-contained content |
| `<section>` | Thematic grouping |
| `<aside>` | Sidebar, related content |
| `<footer>` | Page or section footer |
| `<figure>` | Self-contained media |
| `<time>` | Date/time content |

## Document Structure

### Required Elements

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Page Title</title>
    <meta name="description" content="..." />
  </head>
  <body>
    <!-- content -->
  </body>
</html>
```

### Headings

- Use h1-h6 in sequential order
- Never skip heading levels
- One h1 per page

```html
<!-- BAD -->
<h1>Title</h1>
<h3>Section</h3>

<!-- GOOD -->
<h1>Title</h1>
<h2>Section</h2>
<h3>Subsection</h3>
```

## Forms

### Labels

Always associate labels with inputs:

```html
<!-- BAD -->
<input type="email" placeholder="Email" />

<!-- GOOD -->
<label for="email">Email</label>
<input type="email" id="email" placeholder="Email" />

<!-- GOOD - wrapped -->
<label>
  Email
  <input type="email" />
</label>
```

### Input Types

Use appropriate input types:

```html
<input type="email" />
<input type="tel" />
<input type="url" />
<input type="search" />
<input type="date" />
<input type="number" />
```

## Accessibility

### Alt Text

```html
<!-- Decorative -->
<img src="decorative.png" alt="" />

<!-- Meaningful -->
<img src="chart.png" alt="Sales increased by 25% in Q4" />
```

### ARIA (Minimal)

- Prefer native HTML over ARIA
- Don't override native semantics

```html
<!-- BAD -->
<span role="button">Click</span>

<!-- GOOD -->
<button>Click</button>
```

## SEO

### Meta Tags

```html
<meta name="description" content="..." />
<meta name="keywords" content="..." />
<meta property="og:title" content="..." />
<meta property="og:image" content="..." />
```

## What to Check

- [ ] Semantic elements used appropriately
- [ ] Heading hierarchy is logical (no skipped levels)
- [ ] Form inputs have associated labels
- [ ] Images have appropriate alt text
- [ ] Document has proper lang attribute
- [ ] Viewport meta tag present
- [ ] ARIA used only when necessary