# Performance Review Standards

## References

- Google Core Web Vitals: https://web.dev/explore/performance
- Core Web Vitals 2025 Guide: https://www.digitalapplied.com/blog/core-web-vitals-optimization-guide-2025

## Core Web Vitals

### Key Metrics

| Metric | Good    | Needs Improvement | Poor    |
| ------ | ------- | ----------------- | ------- |
| LCP    | < 2.5s  | 2.5s - 4.0s       | > 4.0s  |
| CLS    | < 0.1   | 0.1 - 0.25        | > 0.25  |
| INP    | < 200ms | 200ms - 500ms     | > 500ms |

### LCP (Largest Contentful Paint)

- Optimize initial load time
- Preload critical resources
- Optimize images and fonts
- Reduce render-blocking resources

### CLS (Cumulative Layout Shift)

- Reserve space for images with width/height
- Reserve space for dynamic content
- Don't inject content above existing content
- Use font-display: swap or optional

### INP (Interaction to Next Paint)

- Break up long tasks
- Yield to main thread periodically
- Optimize event handlers
- Debounce expensive operations

## Performance Investigation

### What to Check

- Large bundle sizes (check import statements)
- Unoptimized images (missing lazy loading, wrong formats)
- Blocking resources (inline critical CSS, defer non-critical)
- Cache effectiveness
- API response times

### Common Issues

- Loading all components eagerly instead of async
- Large dependencies imported entirely
- Missing code splitting
- Synchronous operations blocking main thread

```typescript
// BAD - eager import
import { heavyLibrary } from "heavy-library";

// GOOD - dynamic import when needed
const heavyLibrary = await import("heavy-library");
```

## Vue-Specific Performance

### Reactivity

- Use `shallowRef` for large arrays/objects
- Use `computed` for derived state
- Avoid reactive on large complex objects

### Rendering

- Use `v-memo` for expensive list updates
- Use `v-once` for static content
- Avoid unnecessary re-renders

### Lifecycle

- Clean up in `onUnmounted`
- Remove event listeners
- Clear timers and intervals
- Cancel subscriptions

## Investigation Tools

When investigating performance:

- Use Chrome DevTools Performance tab
- Check network waterfall
- Analyze bundle size
- Profile runtime performance

## What to Check

When reviewing for performance, look for:

- [ ] Images optimized (lazy loading, proper formats)
- [ ] Large lists use virtualization or v-memo
- [ ] Async components for code splitting
- [ ] No unnecessary re-renders
- [ ] Cleanup in onUnmounted
- [ ] Computed used for derived state
- [ ] ShallowRef for large data
- [ ] Event handlers debounced when needed
