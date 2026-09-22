---
name: frontend-ui-engineering-global
description: Build or modify production-quality frontend UI with strong accessibility, responsive behavior, Vue/Nuxt alignment, maintainable styling, and validation discipline.
---

# Unified Frontend UI Engineering

## Purpose

Use this skill when building or modifying user-facing UI.

Goals:

- produce production-quality UI, not generic AI-looking UI
- preserve project conventions before inventing new patterns
- keep changes accessible, responsive, maintainable, and reviewable
- follow the workspace development loop: `plan -> implement -> validate -> review -> fix -> validate -> publish`

## When To Use

Use for:

- new pages, routes, and components
- UI refactors with preserved behavior
- responsive layouts
- styling and visual polish
- accessibility improvements
- Vue and Nuxt interface work
- loading, error, and empty states
- frontend interaction and state handling

## Workspace Workflow Defaults

Source of truth and planning:

- start from the task source of truth: user request, issue, ticket, PR comment, or failing test
- if the source of truth is unclear, stop in planning and ask
- define bounded scope, acceptance criteria, risks, dependencies, and validation approach before editing
- begin by exploring the codebase before making implementation decisions
- identify main source directories, tests, scripts, build config, lint config, and setup docs early
- prefer work in human-reviewable chunks
- make implementation-affecting assumptions explicit

Implementation defaults:

- confirm scope before editing
- inspect relevant files before changing them
- prefer the smallest coherent change
- preserve established project patterns unless the task intentionally changes them
- optimize for maintainability and human-parseable code over cleverness
- avoid speculative refactors and broad cleanup outside scope
- ask before architecture-affecting changes, new dependencies, broad restyling, or global token changes
- update docs when behavior, usage, setup, or developer expectations change

Validation and review defaults:

- validate before considering the task ready for review
- run the strongest practical checks for the scope: targeted tests, lint, typecheck, build, static analysis, and targeted runtime/manual checks
- if a relevant check cannot be run, say so explicitly and note the risk
- if validation fails, fix or ask rather than guessing broadly
- review for correctness, regressions, security/data handling, edge cases, test sufficiency, and maintainability where it affects reliability
- list findings before summaries and distinguish confirmed issues from open questions
- do not publish until validation and review are complete

## Documentation-Derived Frontend Rules

These rules are intentionally inlined from the workspace documentation so they remain active guidance inside the skill.

### HTML and Accessibility

Follow semantic-first markup.

- use the native HTML element that matches the meaning and behavior of the content
- prefer semantic elements over generic containers when structure is meaningful
- preserve a logical document outline with clear heading hierarchy
- keep source order aligned with intended reading and interaction order
- prefer native semantics before adding ARIA
- do not add ARIA when native HTML already provides the correct semantics
- if ARIA is used, ensure the element also fulfills the behavior that role implies
- ensure interactive content is keyboard reachable and operable
- use descriptive link and button text that communicates purpose out of context
- every form control should have an associated label
- prefer explicit labels with `label[for]` and matching control `id` values
- provide instructions for required fields, expected formats, and constraints
- do not rely on placeholder text as the only label or instruction
- group related controls with semantic structure such as `fieldset` and `legend` when needed
- provide meaningful `alt` text for informative images
- use empty `alt` text only for decorative images
- use tables for tabular data, not layout
- use actual buttons for actions and actual links for navigation
- ask before replacing native semantics with ARIA-heavy custom structures or custom widgets

Target WCAG 2.1 AA by default.

### CSS and Visual Implementation

- prefer clear, readable styling over clever selector tricks
- keep styles scoped and predictable
- preserve existing project conventions unless the task intentionally changes them
- avoid unnecessary specificity and selector complexity
- rely on the normal cascade before reaching for stronger selectors
- keep specificity low enough that styles remain easy to override intentionally
- avoid `!important` unless the project already uses it for a well-defined reason
- be cautious when changing global styles, resets, or shared utility layers
- prefer reusable design tokens or CSS custom properties for repeated values
- name tokens by purpose rather than raw visual value when practical
- avoid duplicating the same spacing, color, or sizing values across many rules
- choose layout techniques that match the problem directly, typically flexbox or grid
- design for responsive behavior rather than assuming a single viewport
- avoid brittle layouts that depend on fixed dimensions unless content truly requires them
- treat motion as meaningful, not decorative
- respect `prefers-reduced-motion` for non-essential animation
- preserve readable contrast and legible sizing
- do not rely on color alone to communicate meaning
- ensure focus states remain visible
- ask before changing global tokens, resets, foundational layout rules, or introducing animation-heavy behavior

### Vue Guidance

- preserve the established project style before introducing new component patterns
- prefer maintainable, readable components over clever abstractions
- keep component responsibilities narrow and easy to reason about
- prefer small, focused components over large multi-purpose ones
- keep presentational concerns separated from heavy business logic when practical
- prefer explicit props and events over hidden coupling
- prefer the Composition API when it matches the existing codebase
- keep component-local logic in the component unless it is clearly reusable
- extract composables only when there is real reuse, complexity reduction, or clearer separation of concerns
- respect the existing state management approach in the project
- keep reactive state as local as practical
- avoid unnecessary shared state
- be careful with watchers, derived state, and side effects that become difficult to trace
- keep template logic light; move non-trivial logic into script code when it improves readability
- ask before introducing a new abstraction layer just to make the code look cleaner

### Nuxt Guidance

- preserve established Nuxt conventions before introducing custom structure
- understand whether the task affects client, server, or both before implementing
- treat framework conventions as the default unless the project clearly chose a different pattern
- respect file-based routing and established directory conventions
- identify whether the change belongs in pages, components, composables, server routes, plugins, or middleware before editing
- ask before making structural changes that alter routing or application boundaries
- be explicit about whether logic runs on the server, the client, or both
- use the project's established data-fetching patterns before introducing a new one
- be careful with hydration-sensitive logic and anything that can diverge between server and client
- treat runtime config, environment variables, and server-only values carefully
- avoid exposing server-only configuration to the client
- ask before changing config shape, plugin behavior, or deployment-sensitive settings

### Testing, Linting, and Formatting

Unit testing:

- default to writing unit tests before implementation when practical
- keep unit tests fast, focused, and easy to reason about
- verify outcomes and observable behavior rather than internal implementation details where practical
- cover success paths, failure paths, and edge cases relevant to the changed behavior
- prefer fewer meaningful tests over many shallow tests
- ask before introducing a new test runner, assertion library, or mocking strategy

Integration testing:

- use integration tests to verify behavior at meaningful system boundaries
- keep the integration scope intentional and explicit
- prefer narrow integration tests over broad, slow, hard-to-diagnose tests
- verify serialization, deserialization, persistence, request/response behavior, and boundary contracts where relevant
- avoid relying on production systems for automated integration tests
- ask before introducing new infrastructure or broadening integration scope materially

Linting and formatting:

- preserve the existing repo linting and formatting setup by default
- follow project-specific linting rules first, then existing repo config, then personal standards
- identify the current lint/format setup during exploration
- do not migrate, replace, or normalize toolchains unless explicitly asked
- if a linting change is made, validate with the repo's actual configured commands
- use Prettier for formatting concerns, not semantic correctness
- avoid broad reformatting unless the task explicitly includes it

## Design Quality Standard

Build UI that looks intentional and project-native.

Avoid the common AI aesthetic:

- default purple or indigo-heavy palettes
- gratuitous gradients
- excessive rounding
- oversized padding everywhere
- generic hero/banner sections
- stock card-grid layouts without information hierarchy
- placeholder copy that hides real layout issues
- shadow-heavy surfaces without a design-system reason

Prefer:

- the project's real spacing, color, typography, radius, and shadow tokens
- realistic content and states
- content-first layouts
- clear hierarchy and scanability
- subtle, purposeful visual treatment

## Component Architecture

- prefer small, focused components
- prefer composition over over-configured component APIs
- separate data fetching from presentation when complexity warrants it
- keep template logic light and readable
- extract composables only for real reuse, complexity reduction, or clearer ownership
- avoid prop drilling more than a few levels; restructure or use context/store only when justified
- keep state as local as practical
- respect the project's existing state management approach

### Prefer composition over configuration

```tsx
// Good: composable
<Card>
  <CardHeader>
    <CardTitle>Tasks</CardTitle>
  </CardHeader>
  <CardBody>
    <TaskList tasks={tasks} />
  </CardBody>
</Card>

// Avoid: over-configured
<Card
  title="Tasks"
  headerVariant="large"
  bodyPadding="md"
  content={<TaskList tasks={tasks} />}
/>
```

### Keep components focused

```tsx
export function TaskItem({ task, onToggle, onDelete }: TaskItemProps) {
  return (
    <li className="flex items-center gap-3 p-3">
      <Checkbox checked={task.done} onChange={() => onToggle(task.id)} />
      <span className={task.done ? 'line-through text-muted' : ''}>{task.title}</span>
      <Button variant="ghost" size="sm" onClick={() => onDelete(task.id)}>
        <TrashIcon />
      </Button>
    </li>
  )
}
```

### Separate data fetching from presentation

```tsx
// Container: handles data
export function TaskListContainer() {
  const { tasks, isLoading, error } = useTasks()

  if (isLoading) return <TaskListSkeleton />
  if (error) return <ErrorState message="Failed to load tasks" retry={refetch} />
  if (tasks.length === 0) return <EmptyState message="No tasks yet" />

  return <TaskList tasks={tasks} />
}

// Presentation: handles rendering
export function TaskList({ tasks }: { tasks: Task[] }) {
  return (
    <ul role="list" className="divide-y">
      {tasks.map(task => <TaskItem key={task.id} task={task} />)}
    </ul>
  )
}
```

## State Management

Choose the simplest approach that works:

- local state for component-specific UI state
- lifted state for state shared across a few siblings
- context for read-heavy cross-cutting concerns like theme, auth, or locale
- URL state for shareable filters, pagination, and routing-aware UI state
- server-state tools for remote data caching and mutations
- global store only for truly app-wide complex client state

Avoid prop drilling deeper than a few levels; restructure or introduce context/store only when justified.

## Accessibility and Interaction Examples

### Keyboard-accessible controls

```tsx
<button onClick={handleClick}>Click me</button> // Good
<div onClick={handleClick}>Click me</div> // Avoid
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={e => {
    if (e.key === 'Enter') handleClick()
    if (e.key === ' ') e.preventDefault()
  }}
  onKeyUp={e => {
    if (e.key === ' ') handleClick()
  }}
>
  Click me
</div>
```

### Labels and focus management

```tsx
<button aria-label="Close dialog"><XIcon /></button>

<label htmlFor="email">Email</label>
<input id="email" type="email" />
```

```tsx
function Dialog({ isOpen, onClose }: DialogProps) {
  const closeRef = useRef<HTMLButtonElement>(null)

  useEffect(() => {
    if (isOpen) closeRef.current?.focus()
  }, [isOpen])

  return (
    <dialog open={isOpen}>
      <button ref={closeRef} onClick={onClose}>Close</button>
    </dialog>
  )
}
```

### Empty states

```tsx
function TaskList({ tasks }: { tasks: Task[] }) {
  if (tasks.length === 0) {
    return (
      <div role="status" className="text-center py-12">
        <TasksEmptyIcon className="mx-auto h-12 w-12 text-muted" />
        <h3 className="mt-2 text-sm font-medium">No tasks</h3>
        <p className="mt-1 text-sm text-muted">Get started by creating a new task.</p>
        <Button className="mt-4" onClick={onCreateTask}>Create Task</Button>
      </div>
    )
  }

  return <ul role="list">...</ul>
}
```

## Responsive and State Guidance

Always account for:

- mobile-first layout behavior
- narrow, tablet, desktop, and wide viewport checks
- loading states
- empty states
- error states
- disabled states
- optimistic or async interaction states when relevant
- long content, overflow, and wrapping behavior

Recommended breakpoint checks:

- 320px
- 768px
- 1024px
- 1440px

### Mobile-first responsive example

```tsx
<div className="
  grid grid-cols-1
  sm:grid-cols-2
  lg:grid-cols-3
  gap-4
">
```

## Loading and Async UX

Prefer skeletons for content loading and explicit async-state handling.

```tsx
function TaskListSkeleton() {
  return (
    <div className="space-y-3" aria-busy="true" aria-label="Loading tasks">
      {Array.from({ length: 3 }).map((_, i) => (
        <div key={i} className="h-12 bg-muted animate-pulse rounded" />
      ))}
    </div>
  )
}
```

```tsx
function useToggleTask() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: toggleTask,
    onMutate: async (taskId) => {
      await queryClient.cancelQueries({ queryKey: ['tasks'] })
      const previous = queryClient.getQueryData(['tasks'])

      queryClient.setQueryData(['tasks'], (old: Task[]) =>
        old.map(t => t.id === taskId ? { ...t, done: !t.done } : t)
      )

      return { previous }
    },
    onError: (_err, _taskId, context) => {
      queryClient.setQueryData(['tasks'], context?.previous)
    },
  })
}
```

## Validation Checklist

Before considering the work done, verify:

- the change matches the scoped task
- accessibility was not regressed
- responsive behavior was checked
- existing project patterns were preserved
- tests are sufficient for the changed behavior
- the diff is no larger than necessary
- relevant checks were run: targeted tests, lint, typecheck, build, and manual verification where practical
- any skipped checks or residual risks are stated clearly

## Red Flags

- components that are too large to reason about
- deeply nested template conditionals
- hidden reactivity side effects
- clickable non-semantic elements
- missing loading, error, or empty states
- arbitrary styling values outside the design system
- hydration-sensitive logic added without verification
- broad UI cleanup beyond the requested scope
- new abstractions added only to look cleaner
- tests coupled tightly to implementation details
- integration tests that mock away the real boundary

## Reference Paths

For deeper detail, the workspace references remain useful:

- `../../../WP-PCLAIDocumentation/workflow.md`
- `../../../WP-PCLAIDocumentation/references/general-operating-guidelines.md`
- `../../../WP-PCLAIDocumentation/references/build.md`
- `../../../WP-PCLAIDocumentation/references/review.md`
- `../../../WP-PCLAIDocumentation/references/html.md`
- `../../../WP-PCLAIDocumentation/references/css.md`
- `../../../WP-PCLAIDocumentation/references/vue.md`
- `../../../WP-PCLAIDocumentation/references/nuxt.md`
- `../../../WP-PCLAIDocumentation/references/unit-testing.md`
- `../../../WP-PCLAIDocumentation/references/integration-testing.md`
- `../../../WP-PCLAIDocumentation/references/linting.md`
- `../../../WP-PCLAIDocumentation/references/eslint.md`
- `../../../WP-PCLAIDocumentation/references/prettier.md`

## Default Output Shape

When using this skill, return:

- implementation summary
- validation performed
- review findings or residual risks
- any follow-up questions if scope or architecture is unclear
