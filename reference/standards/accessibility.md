# Accessibility Review Standards

## References

- WCAG 2.1: https://www.w3.org/TR/WCAG21/
- WebAIM: https://webaim.org/

## Guiding Principles

1. **Prefer native HTML** - Use semantic elements (button, nav, main, section) before adding ARIA
2. **ARIA is a last resort** - Only use ARIA when no native HTML solution exists
3. **Don't break native semantics** - Don't add role="" to elements that already have semantic meaning

## Critical Issues

### Interactive Elements

- Interactive elements without accessible names
- Buttons must have text content or aria-label
- Links must have discernible text

### Images

- Missing alt text on images (when decorative, use alt="")

### Forms

- Form inputs without associated labels
- Labels should use `for` attribute or wrap input

## Semantic HTML

- Proper heading hierarchy (don't skip levels: h1 → h2 → h3)
- Use semantic elements: button, a, nav, header, footer, main, section
- Use `<button>` for actions, `<a>` for navigation

```vue
<!-- BAD -->
<div @click="submit">Submit</div>

<!-- GOOD -->
<button @click="submit">Submit</button>
```

## Keyboard Accessibility

- Focus indicators (outline removed without replacement)
- tabindex values (0 for keyboard-focusable, -1 for programmatic focus only)
- All interactive elements must be focusable
- Logical tab order

## ARIA (Minimal)

- ARIA roles that conflict with native semantics
- Missing aria-label only when text content isn't sufficient
- aria-live for dynamically changing content that needs announcement

```vue
<!-- BAD -->
<button role="button">Click me</button>

<!-- GOOD -->
<button @click="open" aria-label="Open settings dialog">Open</button>
```

## Focus Management

- Ensure focus indicators are visible
- Manage focus for modals/dialogs
- Return focus to trigger element when dialog closes
- Don't trap focus unexpectedly

## What to Check

When reviewing for accessibility, look for:

- [ ] Semantic HTML elements used appropriately
- [ ] Heading hierarchy is logical (no skipped levels)
- [ ] All images have alt text
- [ ] Form inputs have associated labels
- [ ] Interactive elements have accessible names
- [ ] Focus indicators are visible
- [ ] Tab order is logical
- [ ] ARIA used only when necessary
- [ ] Focus managed properly in modals/dialogs
