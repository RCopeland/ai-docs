---
name: frontend-ai-review
description: Runs an AI-first frontend code review for Vue/Nuxt and related UI changes. Use when reviewing frontend diffs, PRs, or local changes for correctness, architecture, accessibility, system impact, and user-ready change summaries.
---

# Frontend AI Review

This skill is the AI-review counterpart to `manual-review`.

Use it when Pi should do the review itself instead of launching a human review workflow.

This skill is fully inline. Do not depend on external reference files for normal use. Apply the guidance in this document directly.

## Purpose

Use this skill when reviewing frontend code changes, especially in Vue/Nuxt applications.

Goals:

- perform a strong AI-first frontend code review
- include the quality standards from general code review guidance
- include the frontend quality standards from frontend UI engineering guidance
- include workspace workflow and review expectations inline
- evaluate component-based architecture explicitly
- summarize system-level impact, not just line-level issues
- produce a plain-language summary a user can review and ask questions about

## What This Skill Covers

Use for:

- PR review of Vue, Nuxt, HTML, CSS, or frontend TypeScript changes
- review of local git diffs before commit or before PR submission
- AI review of component refactors
- review of accessibility, responsive behavior, and UI state handling
- review of pages, routes, components, composables, stores, and frontend config
- summarizing frontend changes for teammates or non-authors

## Core Workflow

Follow this workspace loop during review-aware work:

`plan -> implement -> validate -> review -> fix -> validate -> publish`

For review tasks, operate mainly in:

- understand the source of truth
- inspect the change
- evaluate validation
- review the implementation
- classify findings
- summarize risks and next steps

Control rules:

- if the review target is unclear, stop and ask
- if validation is missing, call that out clearly
- if findings reveal scope confusion, move back to plan
- do not treat publish as complete unless validation and review are complete

## Default Operating Assumptions

- start by identifying the source of truth for the task
- inspect the codebase and diff before making architectural judgments
- prefer existing project conventions over invented patterns
- optimize for changes that are easy to reason about
- keep recommendations scoped and reviewable
- ask before endorsing architecture-affecting changes unless the user explicitly requested them
- make assumptions explicit when they affect review quality
- prioritize maintainability where it affects reliability
- avoid destructive or high-risk actions without explicit confirmation

## Review Standard

Review every change across these five axes:

### 1. Correctness

- does the change do what it claims to do?
- does it match the task or expected behavior?
- are edge cases handled?
- are error paths handled?
- do tests cover the actual behavior?
- are there state inconsistencies, null issues, or regression risks?

### 2. Readability and Simplicity

- are names clear and consistent?
- is control flow understandable?
- is the code organized logically?
- is there unnecessary cleverness?
- could the same result be achieved with less complexity?
- are abstractions earning their cost?
- were new branches bolted onto unrelated flows?
- do repeated conditionals suggest a missing model or helper?

### 3. Architecture

- does the change fit existing patterns?
- does it preserve clean boundaries?
- is there duplication that should be shared?
- is feature logic leaking into shared modules?
- does the refactor reduce complexity or just relocate it?
- are type and ownership boundaries explicit?
- did the change materially grow an already-large file instead of decomposing it?

### 4. Security

- is external or user data treated as untrusted?
- is unsafe rendering or injection risk introduced?
- are secrets or sensitive config exposed?
- are boundaries validated before data is used in logic or rendering?

### 5. Performance

- are unnecessary re-renders introduced?
- is data fetched or recomputed more than necessary?
- are loops, lists, or rendering paths unbounded?
- are large objects or heavy transforms created in hot paths?

## Frontend Review Priorities

Prioritize findings in this order:

1. broken behavior or likely regressions
2. accessibility or semantic HTML issues
3. incorrect Vue/Nuxt execution-context behavior
4. weak component boundaries or hidden coupling
5. missing or weak tests
6. responsive/layout risks
7. maintainability issues that materially affect future work
8. style nits

## Frontend UI Quality Standard

Review UI against production-quality standards.

Prefer UI that is intentional and project-native.

Watch for common low-quality AI patterns:

- default purple or indigo-heavy palettes without project basis
- gratuitous gradients
- excessive rounding
- oversized padding everywhere
- generic hero/banner sections
- stock card-grid layouts without information hierarchy
- placeholder copy hiding layout issues
- shadow-heavy surfaces without design-system reason

Prefer:

- the project's spacing, color, typography, radius, and shadow tokens
- realistic content and states
- content-first layouts
- clear hierarchy and scanability
- subtle, purposeful visual treatment

## Component-Based Architecture Review

Always evaluate component architecture explicitly, even for a small diff.

### Core Standard

A component should have one clear reason to exist and a readable ownership boundary.

A reviewer should be able to quickly answer:

- what this component is responsible for
- what data it needs
- what it renders
- what events it emits
- what state it owns
- what it delegates elsewhere

### Responsibility and Size

- is the component focused on one UI concern or coherent behavior slice?
- has the diff turned a simple component into a controller for too many concerns?
- is the file large enough that subcomponents or helpers would improve clarity?
- does it mix orchestration, data shaping, rendering, and styling in a way that is hard to reason about?

### Props, Emits, and Slots

- are props explicit, minimal, and named for meaning?
- are emitted events clear and intention-revealing?
- are slots simplifying composition rather than hiding behavior?
- did the change introduce an over-configured prop API?

### State Ownership

- is state kept as local as practical?
- does shared state exist for a real coordination reason?
- has the change introduced prop drilling that suggests restructuring?
- are derived values computed clearly instead of duplicated?

### Composables and Reuse

- was logic extracted because it is truly reused, or only because a file looked long?
- does the composable reduce complexity or just move it?
- are composables hiding side effects that should stay visible?
- is naming clear about ownership and purpose?

### Coupling and Boundaries

- are child components tightly coupled to parent internals?
- did the change add store, route, or API knowledge in too many places?
- is feature-specific behavior leaking into a shared component?
- are boundaries harder to change independently now?

### Rendering Clarity

- is the template easy to scan?
- are conditional branches understandable without tracing many reactive dependencies?
- is display logic separated from business logic when complexity warrants it?
- are loading, empty, error, and disabled states explicit where relevant?

### Framework-Aware Risks

For Vue/Nuxt specifically, check for:

- watcher side effects that are hard to trace
- hydration-sensitive branching
- client-only assumptions in shared code
- hidden coupling between page, store, composable, and component layers
- overuse of global state where local state would suffice

### Structural Remedies

When flagging an architecture problem, propose the move:

- split a large component into focused subcomponents
- move orchestration into a parent and keep children presentational
- move data loading upward if a component should stay presentational
- replace an over-configured prop API with composition or slots
- inline a composable that is not earning its abstraction
- extract a truly shared helper when duplication is real
- move feature logic out of a shared component
- localize state that does not need to be shared

## HTML and Accessibility Review

Follow semantic-first review.

- use native HTML elements before ARIA
- use buttons for actions and links for navigation
- preserve heading hierarchy
- keep DOM order aligned with reading and interaction order
- every control needs an accessible label
- do not rely on placeholder text as the only instruction
- ensure keyboard reachability and operability
- ensure focus states are visible
- do not rely on color alone to communicate meaning
- provide meaningful empty, loading, and error states
- manage focus for dialogs and significant state changes
- prefer native semantics over ARIA-heavy custom structures
- avoid clickable non-interactive elements unless truly required
- if custom controls exist, verify keyboard and accessibility behavior

Target WCAG 2.1 AA by default.

## CSS and Visual Review

- prefer reusable tokens or custom properties over repeated raw values
- use spacing and sizing from the existing scale
- avoid arbitrary values unless clearly justified
- keep specificity low and styles easy to override intentionally
- avoid `!important` unless the codebase clearly depends on it
- use flexbox or grid intentionally based on layout needs
- design mobile-first and verify narrow and wide viewport behavior
- respect `prefers-reduced-motion` for non-essential motion
- treat motion as meaningful, not decorative
- preserve readable contrast and visible focus states
- be cautious with global styles, resets, and shared utility layers

## Vue Review Guidance

- keep component responsibilities narrow
- prefer explicit props and events over hidden coupling
- be careful with watchers and side effects
- avoid prop mutation
- keep single-file components readable and not oversized
- keep component-local logic local unless there is real reuse
- extract composables only for reuse, complexity reduction, or clearer ownership
- keep template logic light and move non-trivial logic into script when it improves readability
- test user-visible behavior and component contracts

Common Vue risks:

- hidden reactivity bugs
- watchers with unclear side effects
- prop mutation or unclear ownership
- oversized single-file components
- duplicated logic with unclear extraction decisions

## Nuxt Review Guidance

- respect file-based routing and directory conventions
- identify whether the change belongs in pages, components, composables, server routes, plugins, or middleware
- be explicit about client, server, or shared execution context
- be careful with SSR and hydration-sensitive logic
- avoid runtime-config leaks to the client
- use established data-fetching patterns before endorsing a new one
- pay attention to route behavior, async data, middleware behavior, and plugin side effects

Common Nuxt risks:

- server-client boundary mistakes
- hydration mismatches
- route behavior changes
- runtime config leaks
- plugin side effects
- data-fetching behavior that differs between development and production

## Responsive and State Review

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

## Validation Review

Review the verification story before trusting the implementation.

Typical frontend validation to look for:

- targeted unit tests for changed behavior
- integration tests when meaningful boundaries were touched
- lint
- typecheck
- build
- manual UI verification for interaction, responsiveness, and accessibility

Validation rules:

- test user-visible behavior and component contracts
- cover success, failure, and edge paths relevant to the change
- avoid shallow coverage inflation
- prefer meaningful assertions over implementation-detail tests
- if a relevant check cannot be run, say so explicitly and note the risk
- if validation is unusually expensive or disruptive, ask before recommending it as mandatory

Review output should explicitly note:

- what checks ran or appear to have run
- what checks are missing
- whether the test coverage matches the risk level
- whether manual verification is needed

## System-Level Change Summary

Always include a system-level summary, even if there are no blocking findings.

Summarize:

- what capabilities or flows changed
- what user-visible behavior changed
- which layers were touched
- whether the change is isolated, cross-cutting, or architectural
- any new coupling or cross-module impact
- the highest-risk files or flows
- where manual review attention should go

Do not reduce the review to file-by-file nitpicks. Explain the shape of the change.

## Change Sizing and Scope

Small, focused changes are easier to review and safer to merge.

Guideposts:

- around 100 changed lines: good
- around 300 changed lines: acceptable if one logical change
- around 1000 changed lines: usually too large, ask for splitting unless mostly deletions or mechanical refactor

Also watch total file size, not just diff size. A small diff can still push a file past a healthy boundary.

Separate refactoring from feature work when possible.

## Severity Rules

Label findings clearly:

- `Critical:` blocks merge
- no prefix = required fix
- `Optional:` or `Consider:` = worthwhile but non-blocking
- `Nit:` = minor polish only
- `FYI:` = informational

Order findings by impact, not by file order.

Lead with what matters. A few high-conviction comments are better than many low-value nits.

## Required Questions for Every Review

A good review should answer these explicitly or implicitly:

- what changed at the system level?
- what user-visible behavior changed?
- what are the highest-risk files or flows?
- does the component structure still make sense?
- are state ownership and reactivity boundaries clear?
- are SSR, hydration, or client/server boundaries safe?
- were accessibility and responsive behavior protected?
- is the validation story strong enough for the risk level?
- what should the user review manually?
- what open questions remain?

## Output Rules

- list findings before summaries
- include file references whenever possible
- separate confirmed issues from open questions
- be direct and non-sycophantic
- do not invent issues to fill space
- if no significant problems are found, still provide system impact, validation notes, and review focus areas for the user

## Default Response Pattern

Use this structure by default:

```markdown
## Findings
- [severity] `path:line` issue and why it matters

## Validation review
- checks run or missing
- test coverage assessment
- notable verification gaps

## System-level summary
- behavior or flow changes
- layers touched
- coupling or architectural impact
- highest-risk areas

## User review summary
- what changed in plain language
- what areas the user should review manually
- anything that looks risky or deserves questions

## Open questions / manual review focus
- question 1
- question 2
```

If there are no findings, say so explicitly:

```markdown
## Findings
- No blocking or required issues found in the reviewed scope.
```

## User Review Summary Standard

The user-facing summary should:

- use plain language
- explain what changed without assuming the reader authored it
- highlight where the user should click, test, or compare behavior
- call out accessibility, responsive, and state-transition behaviors worth checking
- help the user know what questions to ask

## Common Red Flags

- oversized single-file components
- business logic embedded deeply in templates
- watchers with non-obvious side effects
- prop mutation or unclear ownership
- broad state shared without a clear reason
- composables that only hide complexity instead of reducing it
- route or hydration behavior that is not validated
- clickable non-semantic elements
- inaccessible forms, dialogs, or dynamic states
- arbitrary styling values outside established tokens
- visual changes with no responsive verification
- tests that only snapshot markup without asserting behavior
- feature logic in shared modules
- refactors that relocate complexity instead of reducing it

## Optional Follow-Ups

After reviewing, Pi may also:

- suggest a fix plan
- identify likely low-risk cleanup items
- draft a PR summary
- draft a QA checklist
- write the review summary to a file if the user asks

## Approval Standard

Approve a change when it clearly improves the codebase, follows project conventions, and does not introduce unresolved correctness, accessibility, architectural, or validation concerns that should block merge.

Do not block a change just because it is not exactly how you would have written it. Do block when the implementation introduces real risk or makes the structure meaningfully worse.
