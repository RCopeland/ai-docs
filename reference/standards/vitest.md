# Vitest Standards

## References

- Vitest Documentation: https://vitest.dev/
- Vitest API: https://vitest.dev/api/
- Vitest Guide: https://vitest.dev/guide/
- @vitest/eslint-plugin: https://github.com/vitest-dev/eslint-plugin-vitest

## Installation

```bash
npm install --save-dev vitest @vitest/coverage-v8 @vitest/eslint-plugin jsdom
```

## ESLint Configuration

```typescript
// eslint.config.ts
import pluginVitest from '@vitest/eslint-plugin';

export default [
  {
    ...pluginVitest.configs.recommended,
    files: ['src/**/__tests__/*'],
  },
];
```

## Test File Patterns

- Files in `src/__tests__/`
- Naming: `*.spec.ts` or `*.test.ts`

## Configuration (vite.config.ts)

```typescript
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  test: {
    environment: 'jsdom',
    globals: true,
    include: ['src/**/__tests__/*.spec.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
    },
  },
});
```

## Common Patterns

### Component Testing

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import MyComponent from './MyComponent.vue';

describe('MyComponent', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders properly', () => {
    const wrapper = mount(MyComponent, {
      props: { title: 'Test' }
    });
    expect(wrapper.text()).toContain('Test');
  });
});
```

### Store Testing

```typescript
import { describe, it, expect, beforeEach } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useMyStore } from './myStore';

beforeEach(() => {
  setActivePinia(createPinia());
});

it('updates state', () => {
  const store = useMyStore();
  store.increment();
  expect(store.count).toBe(1);
});
```

### Mocking Components

```typescript
vi.mock('@/components/ChildComponent.vue', () => ({
  default: {
    template: '<div>Mocked</div>'
  }
}));
```

### Mocking Modules

```typescript
vi.mock('@/api/client', () => ({
  fetchUser: vi.fn().mockResolvedValue({ id: 1 })
}));
```

### Timers

```typescript
// Fake timers for setTimeout, intervals
vi.useFakeTimers();
vi.advanceTimersByTime(1000);
vi.useRealTimers();
```

### Router

```typescript
import { createRouter, createWebHistory } from 'vue-router';
import { setActiveRouter } from 'vue-router';

const router = createRouter({
  history: createWebHistory(),
  routes: [{ path: '/', component: Home }]
});

setActiveRouter(router);
```

## Common Rules

### Avoid

- Testing implementation details
- Over-mocking (mocking everything)
- Tight coupling to component internals

### Prefer

- Testing user-visible behavior
- Composition API with shallowRef/reactive for stores
- Screen/dom-testing-library patterns for components

## Shared Mocks

### Creating Global Mocks

Create reusable mocks in `src/__tests__/mocks/` for dependencies used across multiple test files:

```typescript
// src/__tests__/mocks/tiptap.ts
import { vi } from 'vitest';
import { ref } from 'vue';

export function createMockEditor(overrides = {}) {
  const mockEditor = {
    chain: vi.fn(() => ({
      focus: vi.fn(() => ({
        toggleBold: vi.fn().mockReturnThis(),
        toggleItalic: vi.fn().mockReturnThis(),
        run: vi.fn(),
      })),
    })),
    destroy: vi.fn(),
    getHTML: vi.fn(() => '<p>Test</p>'),
    isEmpty: true,
    isActive: vi.fn(() => false),
    commands: {
      setContent: vi.fn(),
      clearContent: vi.fn(),
      ...overrides,
    },
  };

  return mockEditor;
}

export const mockUseEditor = (overrides = {}) => {
  return ref(createMockEditor(overrides));
};

export const EditorContent = {
  template: '<div><textarea /></div>',
};
```

### Using Shared Mocks

Import and configure in test files:

```typescript
// In your test file
import { mockUseEditor, EditorContent } from '@/__tests__/mocks/tiptap';

vi.mock('@tiptap/vue-3', () => ({
  useEditor: vi.fn(() => mockUseEditor()),
  EditorContent,
}));

// Now test and verify
it('emits on change', async () => {
  const wrapper = mount(MyComponent);
  // ... trigger change
  expect(editor.commands.setContent).toHaveBeenCalled();
});
```

### Auto-loading Mocks

For mocks needed in many tests, add to vitest setupFiles in `vite.config.ts`:

```typescript
export default defineConfig({
  test: {
    globals: true,
    setupFiles: ['./src/__tests__/setup.ts'],
  },
});
```

## Tiptap Mocking

Tiptap requires mocking `@tiptap/vue-3` because:
- It has DOM dependencies not available in jsdom
- Editor internals are not relevant to component unit tests

Key points:
- Mock `useEditor` to return a reactive ref containing the editor object
- Mock `EditorContent` as a simple stub component
- Track method calls on editor commands to verify component behavior
- Use `createMockEditor()` for reusable, configurable mocks