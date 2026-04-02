# Component Decomposition Standards

## References

- Vue.js Style Guide: https://vuejs.org/style-guide/
- Component Design Patterns: https://cursorrules.org/article/vue3-composition-api-cursorrules-prompt-file

## When to Break Down a Component

Break down a component when it exhibits any of these signals:

### Size Signals

- **Template exceeds 50-75 lines** - Likely handling too many concerns
- **Script exceeds 100-150 lines** - Logic is too complex for a single component
- **More than 3-4 distinct visual sections** - Each section is a candidate for extraction
- **Multiple v-if/v-else-if chains with complex conditions** - Split into separate components or use dynamic components

### Responsibility Signals

- **Multiple unrelated state variables** - Component is managing too many concerns
- **Mixing data fetching with presentation** - Extract data logic into composables
- **Handling both list rendering and item details** - Split into ListComponent + ItemComponent
- **Managing multiple forms or complex form logic** - Each form should be its own component
- **Combining layout concerns with content** - Extract layout into wrapper components

### Reusability Signals

- **Duplicated UI patterns** - If you copy-paste JSX/template, extract it
- **Similar logic across multiple components** - Extract into composables
- **Complex conditional rendering** - Consider dynamic components or separate branches

## How to Decompose

### Extract Composables for Logic

When a component has complex stateful logic, extract it:

```typescript
// Before: All logic in component
const products = ref([]);
const isLoading = ref(false);
const error = ref(null);
// ... 50 lines of fetch, filter, sort logic

// After: Extract to composable
const { products, isLoading, error, filteredProducts } =
  useProductList(filters);
```

Good candidates for composables:

- Data fetching and caching
- Form validation
- Complex state transformations
- Subscription/event handling
- Shared behavioral patterns

### Extract Child Components for UI

When a visual section has its own concerns:

```vue
<!-- Before: Everything in one component -->
<template>
  <div>
    <!-- 30 lines of header -->
    <!-- 40 lines of filters -->
    <!-- 50 lines of list items -->
    <!-- 20 lines of pagination -->
  </div>
</template>

<!-- After: Extract sections -->
<template>
  <div>
    <ProductHeader :title="title" :count="count" />
    <ProductFilters v-model="filters" />
    <ProductList :products="filteredProducts" />
    <ProductPagination v-model:page="page" :total="total" />
  </div>
</template>
```

### Use Slots for Flexibility

When a component needs to render different content:

```vue
<!-- Generic card that accepts any content -->
<template>
  <div class="card">
    <header v-if="$slots.header">
      <slot name="header" />
    </header>
    <main>
      <slot />
    </main>
    <footer v-if="$slots.footer">
      <slot name="footer" />
    </footer>
  </div>
</template>
```

## Component Size Guidelines

| Component Type | Template Lines | Script Lines | Total Props |
| -------------- | -------------- | ------------ | ----------- |
| Presentational | 20-50          | 20-40        | 2-5         |
| Container      | 30-60          | 50-100       | 3-7         |
| Page/View      | 50-100         | 80-150       | 0-3         |
| Form           | 40-80          | 60-120       | 2-6         |

## Anti-Patterns to Flag

### God Component

A component that does everything - fetches data, manages state, handles routing, renders complex UI. **Solution**: Split into container + presentational components + composables.

### Prop Drilling

Passing props through 3+ levels of nesting. **Solution**: Use provide/inject or Pinia store.

### Render-Heavy Components

Components with deeply nested conditionals and loops. **Solution**: Extract list items, extract conditional branches into separate components.

### Mixed Concerns

Component handles both user input AND data fetching AND complex rendering. **Solution**: Separate into data layer (composables), business logic (stores), and UI layer (components).

## Naming Conventions

- **Composables**: `use` prefix (e.g., `useProductData`, `useFormValidation`)
- **Presentational Components**: Descriptive noun (e.g., `ProductCard`, `UserAvatar`)
- **Container Components**: Feature + `View` or `Section` (e.g., `ProductListView`, `UserProfileSection`)
- **Utility Components**: Action or purpose (e.g., `ConfirmDialog`, `LoadingSpinner`)

## File Organization

```
src/
  components/
    common/           # Shared across features
      Button.vue
      Card.vue
      Modal.vue
    product/          # Feature-specific
      ProductCard.vue
      ProductList.vue
      ProductFilters.vue
  composables/        # Reusable logic
    useProductData.ts
    useFormValidation.ts
  views/              # Page-level components
    ProductPage.vue
```
