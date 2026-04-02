# Vue 3 Standards

## References

- Vue.js Documentation: https://vuejs.org/
- Vue Composition API FAQ: https://composition-api.vuejs.org/
- Vue 3 Composition API Guide: https://cursorrules.org/article/vue3-composition-api-cursorrules-prompt-file
- Vue ESLint Plugin: https://eslint.vuejs.org/
- @vue/eslint-config-typescript: https://www.npmjs.com/package/@vue/eslint-config-typescript

## ESLint

Use with `@vue/eslint-config-typescript` and `eslint-plugin-vue`:

```bash
npm install --save-dev @vue/eslint-config-typescript eslint-plugin-vue vue-eslint-parser @typescript-eslint/parser @eslint/js eslint-config-prettier
```

```js
// eslint.config.js
import js from "@eslint/js";
import vuePlugin from "eslint-plugin-vue";
import vueParser from "vue-eslint-parser";
import tsParser from "@typescript-eslint/parser";
import typescript from "@vue/eslint-config-typescript";
import prettier from "eslint-config-prettier";

export default [
  js.configs.recommended,
  ...typescript,
  {
    files: ["**/*.vue"],
    plugins: { vue: vuePlugin },
    languageOptions: {
      parser: vueParser,
      parserOptions: { parser: tsParser },
    },
    rules: {
      ...vuePlugin.configs["vue3-recommended"].rules,
      ...prettier.rules,
    },
  },
];
```

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

## Reactivity

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

## Template Best Practices

### Keys in v-for

- Always use `:key` with unique, stable identifiers
- Don't use array index as key

### v-if vs v-show

- Use `v-if` for conditionals that rarely change
- Use `v-show` for frequent toggles

### No Mutating Props

- Never mutate props directly - emit changes instead

```vue
<!-- BAD -->
<script setup>
const props = defineProps(["initial"]);
props.initial = "new value"; // Error!
</script>

<!-- GOOD -->
<script setup>
const props = defineProps(["initial"]);
const localValue = ref(props.initial);
</script>
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

### Cleanup

- Always clean up side effects in `onUnmounted`
- Remove event listeners, clear timers, cancel subscriptions

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
```

## Accessibility

### Semantic HTML

- Use semantic elements: button, nav, header, footer, main, section

### ARIA

- Add aria-label to interactive elements without text
- Use ARIA only when no native HTML solution exists

```vue
<!-- GOOD -->
<button @click="open" aria-label="Open settings">
  <IconSettings />
</button>
```

### Focus Management

- Ensure focus indicators are visible
- Manage focus for modals/dialogs

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

## Security

- No sensitive data exposed in templates
- No hardcoded secrets/keys
- XSS prevention (v-html only with sanitized content)

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
