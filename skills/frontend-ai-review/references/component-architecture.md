# Component-Based Architecture Review Guide

Use this guide when reviewing component-oriented frontend changes.

## Core Standard

A component should have one clear reason to exist and a readable ownership boundary.

Prefer a structure where another engineer can quickly answer:

- what this component is responsible for
- what data it needs
- what it renders
- what events it emits
- what state it owns
- what it delegates elsewhere

## Review Checks

### 1. Responsibility and Size

- is the component focused on one UI concern or one coherent slice of behavior?
- has the diff turned a simple component into a multi-purpose controller?
- is the file becoming large enough that subcomponents or helpers would improve clarity?
- does the component mix orchestration, data shaping, rendering, and styling in a way that is hard to reason about?

### 2. Props, Emits, and Slots

- are props explicit, minimal, and named for meaning?
- are emitted events clear and intention-revealing?
- are slots used to simplify composition rather than create hidden behavior?
- did the change introduce a prop API that is too configurable for the actual use case?

### 3. State Ownership

- is state kept as local as practical?
- does shared state exist for a real coordination reason?
- has the change introduced prop drilling that suggests the structure should change?
- are derived values computed clearly instead of duplicated across components?

### 4. Composables and Reuse

- was logic extracted because it is actually reused, or because the file looked long?
- does the composable reduce complexity, or just move it?
- are composables hiding side effects that should remain visible at the call site?
- does the naming make ownership and purpose obvious?

### 5. Coupling and Boundaries

- are child components tightly coupled to parent internals?
- did the change add knowledge of store structure, route shape, or API shape in too many places?
- is feature-specific behavior leaking into a shared component?
- are boundaries becoming harder to change independently?

### 6. Rendering Clarity

- is the template easy to scan?
- are conditional branches understandable without tracing many reactive dependencies?
- is display logic separated from business logic when complexity warrants it?
- are loading, empty, error, and disabled states explicit where relevant?

### 7. Framework-Aware Risks

For Vue/Nuxt specifically, check for:

- watcher side effects that are hard to trace
- hydration-sensitive branching
- client-only assumptions in shared code
- hidden coupling between page, store, composable, and component layers
- overuse of global state where local state would suffice

## Structural Remedies

When you find a problem, suggest the structural move:

- split a large component into focused subcomponents
- move orchestration into a parent and keep children presentational
- keep a component presentational and move data loading upward
- replace an over-configured prop API with composition or slots
- inline a composable that is not earning its abstraction
- extract a truly shared helper when duplication is real
- move feature logic out of a shared component
- localize state that does not need to be shared

## Anti-Patterns

- god components
- wrapper components that only forward props and add indirection
- composables with hidden side effects
- presentational components that reach into global state directly without justification
- deeply nested render conditionals used instead of clearer structure
- adding a new abstraction only because the current one feels messy

## Approval Standard

Approve the architecture when the change keeps ownership clear, complexity proportionate, and future edits easier rather than harder.
