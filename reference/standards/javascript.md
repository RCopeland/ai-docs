# JavaScript Standards

## References

- MDN JavaScript Guide: https://developer.mozilla.org/en-US/docs/Web/JavaScript
- Modern JS Best Practices 2025: https://javascript.plainenglish.io/javascript-best-practises-in-2025-88c7a3d5f08e
- ES6+ Features: https://playground.halfaccessible.com/blog/modern-javascript-es6-features

## ESLint

Use `@eslint/js` for vanilla JavaScript:

```bash
npm install --save-dev @eslint/js eslint-config-prettier
```

```js
// eslint.config.js
import js from "@eslint/js";
import prettier from "eslint-config-prettier";

export default [
  js.configs.recommended,
  {
    rules: prettier.rules,
  },
];
```

## Modern JavaScript (ES6+)

### Const/Let Instead of Var

```javascript
// BAD
var count = 0;

// GOOD
const count = 0;        // immutable reference
let total = 0;           // mutable reference
```

### Arrow Functions

```javascript
// BAD
function add(a, b) {
  return a + b;
}

// GOOD
const add = (a, b) => a + b;
```

### Destructuring

```javascript
// Array
const [first, second] = items;

// Object
const { name, age } = user;

// With alias
const { name: userName } = user;

// Default values
const { name = 'Anonymous' } = user;
```

### Template Literals

```javascript
// BAD
const greeting = 'Hello, ' + name + '!';

// GOOD
const greeting = `Hello, ${name}!`;
```

### Optional Chaining & Nullish Coalescing

```javascript
// BAD
const street = user && user.address && user.address.street;

// GOOD
const street = user?.address?.street;

// BAD
const value = data !== null && data !== undefined ? data : 'default';

// GOOD
const value = data ?? 'default';
```

## Async/Await

### Prefer Over Callbacks/Promises

```javascript
// BAD
fetchData()
  .then(data => process(data))
  .catch(err => handleError(err));

// GOOD
try {
  const data = await fetchData();
  const result = await process(data);
} catch (err) {
  handleError(err);
}
```

### Parallel Execution

```javascript
// Sequential (slower)
const user = await fetchUser(id);
const posts = await fetchPosts(id);

// Parallel (faster)
const [user, posts] = await Promise.all([
  fetchUser(id),
  fetchPosts(id)
]);
```

## Arrays

### Methods

```javascript
// map - transform each item
const names = users.map(user => user.name);

// filter - keep matching items
const adults = users.filter(user => user.age >= 18);

// reduce - accumulate to single value
const total = items.reduce((sum, item) => sum + item.price, 0);

// find - get first match
const user = users.find(u => u.id === id);

// some/every - boolean checks
const hasAdult = users.some(u => u.age >= 18);
const allAdults = users.every(u => u.age >= 18);
```

### Avoid for loops when possible

```javascript
// BAD
for (let i = 0; i < items.length; i++) {
  process(items[i]);
}

// GOOD
items.forEach(item => process(item));
```

## Objects

### Spread Operator

```javascript
// Clone and merge
const updated = { ...original, name: 'New Name' };

// Merge objects
const combined = { ...defaults, ...userOptions };
```

### Object.fromEntries

```javascript
// Array of pairs to object
const obj = Object.fromEntries(
  entries.map(([key, value]) => [key, value])
);
```

## Modules

### Named Exports

```javascript
// utilities.js
export function formatDate(date) { ... }
export function capitalize(str) { ... }

// Import specific
import { formatDate } from './utilities';
```

### Default Exports

```javascript
// component.js
export default function Component() { ... }

// Import default
import Component from './component';
```

## Error Handling

### Custom Errors

```javascript
class AppError extends Error {
  constructor(message, code, statusCode = 500) {
    super(message);
    this.code = code;
    this.statusCode = statusCode;
  }
}
```

### Try/Catch with Async

```javascript
async function fetchData() {
  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error('Network error');
    return await response.json();
  } catch (error) {
    // Handle error appropriately
    console.error('Fetch failed:', error);
    throw error;
  }
}
```

## Performance

### Debounce/Throttle

```javascript
// Debounce - wait for pause
function debounce(fn, delay) {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), delay);
  };
}

// Throttle - limit frequency
function throttle(fn, limit) {
  let inThrottle;
  return (...args) => {
    if (!inThrottle) {
      fn(...args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}
```

### Memoization

```javascript
const memoize = (fn) => {
  const cache = new Map();
  return (...args) => {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
};
```

## Anti-Patterns

- Avoid `var` - use const/let
- Avoid `==` - use `===`
- Avoid `any` - use proper typing
- Avoid callbacks - use async/await
- Avoid mutate parameters
- Avoid global state

## What to Check

- [ ] Modern ES6+ syntax used
- [ ] Const/let instead of var
- [ ] Arrow functions where appropriate
- [ ] Optional chaining and nullish coalescing
- [ ] Async/await over callbacks
- [ ] Array methods (map, filter, reduce)
- [ ] Proper error handling
- [ ] No console.log in production code
- [ ] Functions are pure when possible