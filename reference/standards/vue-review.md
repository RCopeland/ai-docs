# Vue 3 Review Standards

## References

- Vue.js Documentation: https://vuejs.org/
- Vue Composition API FAQ: https://composition-api.vuejs.org/
- Vue 3 Composition API Guide: https://cursorrules.org/article/vue3-composition-api-cursorrules-prompt-file

## Composition API

### Script Setup

- Use `<script setup>` syntax for Vue 3 components
- Prefer composition API over options API

### Props

- Define props with proper TypeScript types
- Use `defineProps` with type inference
- Provide defaults for optional props

```typescript
// GOOD
interface Props {
  title: string;
  count?: number;
  items: Item[];
}

const props = withDefaults(defineProps<Props>(), {
  count: 0,
});
```

### Emits

- Use `defineEmits` with type inference
- Prefer object syntax for emit definitions

```typescript
// GOOD
const emit = defineEmits<{
  (e: "update", value: string): void;
  (e: "delete", id: number): void;
}>();
```

## Vue Component Patterns

### What to Check

- Single-responsibility (components should do one thing well)
- `<script setup>` syntax for Vue 3
- Props defined with proper TypeScript types (not `any`)
- Emits defined using `defineEmits` with type inference
- `v-for` always has `:key` (unique, stable keys)
- `v-if` vs `v-show` - use `v-if` for conditionals that rarely change, `v-show` for frequent toggles
- No mutating props directly (anti-pattern)
- Proper prop validation (type, required, default)

### Anti-patterns

```vue
<!-- BAD: Mutating props -->
<script setup>
const props = defineProps(["initial"]);
props.initial = "new value"; // Error!
</script>

<!-- GOOD: Emit changes -->
<script setup>
const props = defineProps(["initial"]);
const localValue = ref(props.initial);
</script>
```

## Reactivity & Performance

### Computed vs Methods

- Use `computed` for derived state (caches value, updates on dependencies)
- Use methods for actions or when you need fresh values each call

```typescript
// GOOD - computed for derived state
const filteredItems = computed(() => items.value.filter((item) => item.active));
```

### Ref vs Reactive

- Use `ref` for primitives and when you need to reassign
- Use `reactive` for objects where you won't reassign
- Avoid mixing ref and reactive

### Shallow Ref

- Use `shallowRef` for large arrays/objects to avoid deep reactivity overhead

### Cleanup

- Always clean up side effects in `onUnmounted`
- Remove event listeners, clear timers, cancel subscriptions

```vue
<!-- BAD - method called in template (re-runs every render) -->
<template>{{ formatDate(date) }}</template>

<!-- GOOD - computed (only re-runs when dependencies change) -->
<template>{{ formattedDate }}</template>
```

## State Management

### Pinia Stores

Use Pinia when:

- State is shared across multiple components
- State needs persistence
- State affects app-wide behavior (combat state, party data, settings)

```typescript
// GOOD - Pinia store
export const useCombatStore = defineStore("combat", () => {
  const combatants = ref<Combatant[]>([]);
  const currentRound = ref(1);

  function addCombatant(combatant: Combatant) {
    combatants.value.push(combatant);
  }

  return { combatants, currentRound, addCombatant };
});
```

### Local State

Use local state (`ref`, `computed`) when:

- State is only used by one component
- State is transient (modal open/closed, form input, UI toggle)

```typescript
// GOOD - local state
const isModalOpen = ref(false);
const searchQuery = ref("");
```

### Anti-patterns

- Don't use Pinia for modal state or other transient UI state
- Don't use a store when a simple ref will do

```typescript
// BAD - Pinia for modal state (should be local)
const useModalStore = () =>
  defineStore("modal", () => ({
    isOpen: ref(false),
  }));

// GOOD - local state for UI concerns
const isOpen = ref(false);
```

## Composables

### Structure

- Use named exports (not default)
- Return type interface for type safety
- Use `readonly()` for exposed reactive state

```typescript
// GOOD composable
export function useFeature() {
  const data = ref<FeatureData | null>(null);

  onMounted(() => {
    window.addEventListener("resize", handler);
  });

  onUnmounted(() => {
    window.removeEventListener("resize", handler);
  });

  return { data: readonly(data) };
}
```

## Styling

### Tailwind Only

- Use Tailwind utility classes in templates
- No `<style>` blocks
- No inline styles
- Use responsive utilities (md:, lg:, etc.)

```vue
<!-- GOOD -->
<template>
  <div class="p-4 bg-red-500 md:p-6"></div>
</template>

<!-- BAD -->
<template>
  <div style="padding: 16px; background-color: red;"></div>
</template>

<!-- BAD -->
<style>
.container {
  padding: 16px;
}
</style>
```

## Security

- No sensitive data exposed in templates
- No hardcoded secrets/keys
- XSS prevention (v-html only with sanitized content)

## Error Handling

- Use try/catch around async operations
- Show error states in UI
- Provide user-friendly error messages

```typescript
// GOOD
try {
  await saveData();
} catch (error) {
  errorMessage.value = "Failed to save. Please try again.";
}
```

## Investigation

When reviewing, search for anti-patterns:

- `any` - untyped code
- `TODO\|FIXME` - incomplete work
- `console\.log` - debug code
- `<style` - custom CSS blocks
- `style=` - inline styles

## What to Check

When reviewing Vue code, look for:

- [ ] `<script setup>` syntax
- [ ] Props properly typed with defineProps
- [ ] Emits properly typed with defineEmits
- [ ] v-for has unique :key
- [ ] computed used for derived state
- [ ] No prop mutation
- [ ] Pinia for shared state, ref for local
- [ ] Tailwind only, no <style> blocks
- [ ] Semantic HTML and ARIA where needed
- [ ] onUnmounted cleanup for side effects
- [ ] Error handling for async operations
