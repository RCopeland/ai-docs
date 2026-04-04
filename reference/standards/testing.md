# Unit Testing Best Practices

> **Note**: When tests are written in TypeScript, also load `typescript.md` for TypeScript-specific testing patterns and typing guidance.

## General Principles

### Test Structure

- **Arrange, Act, Assert (AAA)** - Organize tests into clear sections
- **One assertion per test** - Prefer focused tests over monolithic ones
- **Descriptive names** - Test names should describe what/why, not just what

### Test Focus

- **Verify output/behavior, not implementation** - Tests should verify the expected result of an input or action
- **Combine existence checks** - Multiple "element exists" checks can be combined into 1-2 tests

```typescript
// GOOD - tests behavior/output
it('submits form when button clicked', async () => {
  await wrapper.find('form').trigger('submit')
  expect(emit).toHaveBeenCalledWith('submit', expectedData)
})

it('shows error message for invalid input', async () => {
  await wrapper.find('input').setValue('')
  await wrapper.find('input').trigger('blur')
  expect(wrapper.text()).toContain('Required')
})

// GOOD - combined existence checks (rarely needed)
it('renders required UI elements', () => {
  expect(wrapper.find('form').exists()).toBe(true)
  expect(wrapper.find('button[type="submit"]').exists()).toBe(true)
})

// BAD - too granular, tests implementation details
it('renders submit button with return icon', () => { ... })
it('renders formatting toolbar buttons', () => { ... })
it('renders heading dropdown button', () => { ... })
```

### Test Coverage

- **Priority**: Critical paths, edge cases, error handling
- **Avoid**: Testing trivial code (getters, simple formatters)
- **Meaningful coverage**: Focus on logic, not line count

### Mocking

- **Check for global mocks first**: Before mocking something in a test file, check if there is a globally defined version in `src/__tests__/mocks/`. If one exists, explore its usage in another test file before writing test code.
- **Mock external dependencies**: APIs, databases, timers
- **Don't mock internals**: Test the unit, not implementation details
- **Spies for partial mocking**: Track calls without replacing behavior

```typescript
// Mock external module
vi.mock('@/api/client', () => ({
  fetchUser: vi.fn().mockResolvedValue({ id: 1 })
}));

// Spy on existing method
const alertSpy = vi.spyOn(window, 'alert');
```

### Async Testing

```typescript
// Promises
it('should resolve with data', async () => {
  const result = await fetchData();
  expect(result).toEqual({ id: 1 });
});

// Async/Await with error
it('should reject on failure', async () => {
  await expect(fetchData()).rejects.toThrow('Network error');
});
```

### Test Isolation

- **Each test independent** - No shared state between tests
- **Cleanup after test**: Reset mocks, clear storage, restore globals
- **Deterministic**: No reliance on timing, randomness, or external state

### Common Pitfalls

| Issue | Fix |
|-------|-----|
| Flaky tests | Remove timing dependencies |
| Slow tests | Mock heavy operations |
| Brittle tests | Test behavior, not implementation |
| Unclear failures | Add descriptive expect messages |

## References

- [Testing Library Guiding Principles](https://testing-library.com/docs/guiding-principles/)
- [Common Testing Mistakes](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)