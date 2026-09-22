---
name: legacy-ui-migrator
description: Use when migrating a specific UI component, section, or route from a read-only legacy ASP.NET 4.6 app (.cshtml, .js, .scss/.css) into a Nuxt/Vue app using source analysis plus browser inspection for parity.
---

# Legacy UI Migrator

## Purpose

Use this skill to isolate a specific UI component, section, or route from a legacy ASP.NET 4.6 application and recreate it in a modern Nuxt/Vue application.

The legacy application is always read-only reference material. The new Nuxt/Vue application is the only codebase that may be modified.

This skill should combine:
- legacy source analysis
- rendered browser inspection of the legacy QA app
- local execution and inspection of the new app
- dependency tracing across views, partials, scripts, and styles

## Required user inputs

Before doing migration work, ask the user for all missing required inputs:

1. Legacy app source root
   - absolute or workspace-relative path
   - read-only reference only
2. New app source root
   - absolute or workspace-relative path
   - the only codebase to modify
3. Legacy QA URL
   - URL for the old app route or environment to inspect
4. New app local URL
   - local dev URL for the new app
5. Target route, page, or component to migrate
   - exact route, page name, selector, screenshot region, or file path if known
6. AI documentation root
   - path to the user's AI-facing coding standards or reference docs folder if one exists
   - user-supplied because its location differs by environment
   - optional unless the user expects the skill to follow that documentation
7. Project standards
   - Nuxt version
   - Vue version
   - TypeScript or JavaScript
   - styling conventions
   - state and data patterns
   - accessibility requirements
   - SSR constraints
   - forbidden patterns
8. Expected deliverable
   - migration report first
   - implementation only
   - implementation plus parity checklist
   - open questions and blockers list

If any required input is missing, stop and ask for it.

## Hard rules

- Never modify the legacy app
- Treat the legacy source as read-only
- Treat the legacy QA site as inspection-only
- Make changes only in the new app
- Do not assume source markup equals runtime markup
- Use browser inspection to verify actual rendered DOM, classes, states, and behavior
- When available, use Chrome DevTools MCP for browser inspection of both the legacy QA app and the new local app
- Preserve behavior and visual intent unless the user explicitly approves changes
- Preserve intended user-facing behavior, but do not blindly preserve accidental legacy implementation quirks unless the user asks for strict bug-compatible parity
- If behavior is ambiguous, document it and ask when needed instead of guessing
- Ask before adding a dependency
- Ask before making architecture-affecting changes

## Code-writing references

If the user provides an AI documentation root, read the relevant coding standards and workflow documents from that location before implementing.

Suggested documents to look for under the user-supplied documentation root:
- general operating guidelines
- Vue guidance
- Nuxt guidance
- CSS guidance
- HTML guidance
- workflow guidance
- linting and testing guidance

If the user does not provide an AI documentation root, fall back to repo-local conventions and any explicit project documentation.

Default expectations when no stronger repo-specific rule overrides them:
- ask for missing requirements before coding
- inspect the codebase before making architectural assumptions
- preserve existing app patterns
- keep changes minimal and reviewable
- prefer semantic accessible HTML
- keep styles scoped and maintainable
- prefer CSS custom properties for tunable visual values such as spacing, color, borders, and sizing, with reasonable component defaults and the ability for parent contexts to override them
- be explicit about SSR and client behavior in Nuxt
- prefer Composition API when it matches the codebase
- prefer standard Vue single-file component section order: `<script setup>` first for logic, `<template>` second for layout, `<style>` last for styling
- extract composables only when there is real reuse or complexity reduction
- validate with relevant checks before declaring work done

Standard recommended Vue file structure:

```vue
<script setup>
// 1. LOGIC (JavaScript / TypeScript)
import { ref } from 'vue'

const message = ref('Hello Vue!')
</script>

<template>
  <!-- 2. LAYOUT (HTML) -->
  <div class="container">
    <h1>{{ message }}</h1>
  </div>
</template>

<style scoped>
/* 3. STYLING (CSS / SCSS) */
.container {
  text-align: center;
}
</style>
```

Recommended styling pattern for migrated Vue components:

```vue
<script setup>
const cssVars = {
  '--example-text-color': 'var(--color-gray-900, #2d2d2d)',
  '--example-top-spacing': '25px',
}
</script>

<template>
  <div
    class="example"
    :style="cssVars"
  >
    Example
  </div>
</template>

<style scoped>
.example {
  color: var(--example-text-color);
  margin-top: var(--example-top-spacing);
}
</style>
```

Use this pattern when the component needs sensible defaults but should still allow parent or page-level overrides without rewriting the component styles.

## Authoring model for new components

Use the current `BottomCta` and `BaseImage` or `CmsImage` direction as the architectural baseline, but apply it with clearer separation of responsibilities.

### Core principle

The CMS schema must stay separate from the reusable UI component API.

Do not make the reusable UI component accept raw CMS-shaped props when that shape is app-specific, unstable, or unlikely to belong in the shared UI library.

Instead, author in layers:
1. pure UI component
2. app-specific adapter component
3. transform or normalization file
4. optional shared app-level types file

### Layer responsibilities

#### 1. Pure UI component

This is the reusable component that could be moved into a UI library later.

Rules:
- place only presentation-focused props on this component
- props should describe rendered UI, not CMS field names
- do not import CMS types into this component
- do not read raw CMS entries here
- do not embed app-specific token replacement, analytics wiring, or CMS parsing here unless those concerns are part of the reusable contract
- keep styling with the UI component so the visual implementation is easy to find

Examples of good UI props:
- `titleHtml`
- `image`
- `primaryAction`
- `align`
- `hasBackground`

Examples of bad UI props:
- `bottom_cta_entry`
- `image_desktop`
- `spacing_variants`
- `data_attributes_pairs`

#### 2. App-specific adapter component

This component bridges app or CMS data into the reusable UI component.

Rules:
- adapter components may accept CMS-shaped props
- adapters may call app composables such as token replacement, route helpers, analytics helpers, or CMS link resolvers
- adapters should be thin orchestration layers
- adapters should prefer calling transform functions instead of embedding large normalization logic inline
- adapters should render the pure UI component, not duplicate its markup

#### 3. Transform or normalization file

Use a dedicated file for transforming CMS data into the UI-facing model.

Rules:
- keep parsing, fallback rules, normalization, and missing-content handling here
- return a UI-oriented model, not raw CMS structures, whenever practical
- keep the transform file framework-light when possible so it is easy to test
- this file is the right place for field aliasing, fallback image selection, spacing or variant mapping, and defensive handling of incomplete CMS content

#### 4. Types

Keep CMS input types distinct from reusable UI types.

Rules:
- UI types should describe the reusable component contract
- CMS types should describe the source data shape
- do not collapse those into one type just because the current component is local to the app
- colocate single-use types with the file that uses them
- extract types into separate files only when they are reused or meaningfully improve clarity
- do not create a global dumping ground for all CMS types

### Type placement policy

Use the smallest reasonable scope for each type.

#### UI component types

For pure UI components:
- keep `Props` types in the `.vue` file by default when they are only used there
- keep small local emit payload types in the `.vue` file when they are only used there
- extract to `component.types.ts` only when a UI-facing type is reused by the component, adapter, transform, tests, or multiple related components

Examples:
- keep `interface Props` inside `BottomCta.vue` if only `BottomCta.vue` uses it
- move `BottomCtaAction` to `bottomCta.types.ts` if it is shared by the UI component and adapter

#### CMS and adapter types

For CMS-facing or adapter-facing code:
- keep small single-use CMS prop or entry types in the adapter `.vue` file when they are only used there
- extract to `component.cms.types.ts` when the CMS types are reused by the adapter, transform, tests, or multiple related files
- keep transform return types close to the transform unless they are part of the reusable UI contract

Examples:
- a small adapter-only `Props` interface can stay in `BottomCtaCmsAdapter.vue`
- `BottomCtaCmsEntry` should move to `bottomCta.cms.types.ts` if both adapter and transform use it heavily

#### Shared app-level types

Only promote types to an app-level shared location when they are truly reused across multiple features.

Good candidates:
- common CMS asset shapes
- common CMS link field shapes
- common metadata shapes
- cross-feature shared app models

Bad candidates:
- every component-specific CMS entry type
- one-off adapter props
- UI props that belong only to one component

If the app uses Nuxt shared code intentionally, framework-agnostic shared types may live in a shared location such as `shared/types/`, but only when they are broadly reused and not tied to one component.

### Recommended directory plan

The current app mixes pure UI, adapter, and transform concerns near each other. That works, but it makes it harder to immediately see what is reusable UI versus app integration.

For future work, prefer a structure that separates these concerns more clearly.

Recommended shape:

```text
app/
  components/
    ui/
      bottom-cta/
        BottomCta.vue
        bottomCta.types.ts
      image/
        BaseImage.vue
        BasePicture.vue
        image.types.ts

    cms/
      bottom-cta/
        BottomCtaCmsAdapter.vue
      image/
        CmsImage.vue
        CmsPicture.vue

  transforms/
    cms/
      bottom-cta/
        bottomCta.transform.ts
        bottomCta.cms.types.ts
      image/
        cmsImage.transform.ts
        cmsImage.types.ts
```

If the repo prefers fewer top-level directories, an acceptable alternative is:

```text
app/
  components/
    ui/
      bottom-cta/
        BottomCta.vue
        bottomCta.types.ts
    adapters/
      cms/
        bottom-cta/
          BottomCtaCmsAdapter.vue
    transforms/
      cms/
        bottom-cta/
          bottomCta.transform.ts
```

The important part is not the exact folder names. The important part is that a reader can quickly distinguish:
- reusable UI
- CMS adapters
- transform logic
- source-shape types

### Naming guidance

Prefer names that reveal the layer:
- `BottomCta.vue` for pure UI
- `BottomCtaCmsAdapter.vue` for CMS-to-UI wiring
- `bottomCta.transform.ts` for normalization and mapping
- `bottomCta.cms.types.ts` for CMS entry shapes
- `bottomCta.types.ts` for reusable UI contract types

Avoid ambiguous names when possible, especially names that make an adapter look like the canonical UI component.

### How to use the current examples

Use the current `BottomCta` pattern as a positive example of separating UI props from CMS input.
Use the current `CmsImage` pattern as a positive example of separating normalized image handling from the low-level image renderer.

But when authoring new work, prefer clearer physical separation than the current file layout if the user approves that structure.

### Default recommendation for migrated components

Unless the user asks otherwise, implement migrated components using this plan:
- create a pure UI component for the migrated visual unit
- create a CMS or app adapter only if the component is fed by CMS-shaped or route-specific data
- place normalization and fallback mapping in a transform file
- keep pure UI components free of CMS field names and app-specific source schemas
- keep reusable UI visually and structurally easy to find
- favor future extraction to a shared UI library

## When to use this skill

Use this skill when the user wants to:
- migrate a legacy route or UI section to Nuxt/Vue
- isolate a component from old Razor, JS, and CSS code
- trace dependencies for a piece of UI in an ASP.NET app
- reproduce old UI behavior in a modern frontend
- compare rendered output between old and new apps

## Workflow

For nontrivial migrations, maintain a migration state or handoff document so work can be resumed if the model must be switched mid-process.

### 1. Clarify the migration target

Ask the user to identify the target as clearly as possible:
- route
- page section
- component name
- selector
- screenshot
- surrounding text or content
- known file path

If the target boundary is unclear, say so and define a working boundary before implementing.
If the migration is nontrivial or ambiguous, prefer producing a migration report or dependency plan before coding.

### 2. Inspect the new app first

Before implementing, inspect the new app source root to understand:
- project structure
- pages, components, composables, and style organization
- existing component patterns
- standard npm commands for dev, test, lint, typecheck, and build
- any established route or page patterns relevant to the target
- local linting and testing rules

Prefer existing conventions over inventing new structure.
Do not guess commands if the project already defines them. Prefer the repo's npm scripts and documented local workflow.
### 2.5 Create or update a migration state file

For nontrivial work, create or update a structured migration state file before major implementation work begins.

Recommended location:
- `docs/migrations/<component-or-route>.md`
- or another repo-appropriate notes location if the project already has one

Recommended contents:
- target route or component
- legacy source root
- new app root
- AI documentation root if provided
- legacy QA URL
- new local URL
- legacy dependency map
- proposed new structure
- implementation status checklist
- decisions made
- assumptions
- blockers
- parity findings
- validation status
- exact next steps

Update this file after each major phase so another model can resume with minimal context loss.

### 3. Inspect legacy source code

Use the provided legacy app source root to locate:
- `.cshtml` views
- partial views
- layouts
- `.js` files
- `.scss` and `.css` files
- server-side helpers or models if needed to understand rendering

Trace:
- component markup origins
- conditional rendering
- partial composition
- JS-driven states and interactions
- style dependencies
- shared or global CSS dependencies
- backend-provided values affecting the UI
- controller, viewmodel, helper, or endpoint dependencies
- hidden inputs, data attributes, token replacement, personalization, and analytics hooks that affect behavior

Produce a short dependency map before coding if the scope is nontrivial.
If backend or data dependencies are required for parity, document what must be reimplemented, mocked, deferred, or clarified.

### 4. Inspect rendered legacy behavior in browser

Open the legacy QA URL and inspect the real rendered output.

When available, use Chrome DevTools MCP.

Check:
- actual DOM structure
- runtime classes and attributes
- visible and hidden states
- interactions
- responsive behavior
- desktop and mobile breakpoints
- form states
- modals, dropdowns, tabs, and accordions
- client-side DOM mutations
- computed styles when needed
- any content or structure not obvious from source

Do not rely solely on static Razor files if runtime behavior differs.

### 5. Define the migration boundary

Decide what belongs in:
- one Vue component
- multiple child components
- composables
- page-level integration
- styles

Keep the boundary practical:
- isolate reusable UI where possible
- do not over-fragment prematurely
- preserve behavior and maintainability

State the proposed boundary briefly before implementation when it is not obvious.

### 6. Implement in the new app

Work only in the new app source root.

Follow the user's project standards and the code-writing references above.

Prefer modern Vue and Nuxt patterns over direct legacy translation.

Examples of modernization to prefer when compatible:
- Vue reactivity instead of jQuery DOM manipulation
- composables for reusable shared logic
- scoped or approved-project styling patterns
- semantic accessible markup
- clear prop and event interfaces for reusable components
- client guards around browser-only APIs such as `window`, `document`, and similar runtime-only access where needed

### 7. Run and inspect the new app locally

Use the provided local URL for the new app.

Verify:
- visual structure
- text and content placement
- interactions
- state transitions
- spacing and alignment
- responsive behavior
- desktop and mobile breakpoints
- accessibility basics
- SSR and client safety where relevant
- hydration-sensitive behavior where relevant

### 8. Compare old vs new

Compare the old QA rendering and new local rendering for parity.

Document:
- matched behavior
- intentional deviations
- unresolved gaps
- assumptions
- blockers caused by missing backend behavior or unclear requirements

### 9. Validate

Run the project's local npm-based validation commands for the scoped change whenever available.

Validation expectations:
- follow the repo's local linting rules
- use the project's npm scripts for test, lint, typecheck, and build when those scripts exist
- prefer targeted test execution when practical
- perform targeted manual verification in the browser

Typical checks:
- targeted unit tests
- lint
- typecheck
- build
- targeted manual verification

If a relevant check cannot be run, say so explicitly and note the risk.
If the correct npm command is unclear, stop and ask instead of guessing.

## Output contract

Unless the user asks otherwise, provide:

1. What was migrated
2. Legacy dependency map
3. Files created or changed in the new app
4. Parity summary
5. Validation performed
6. Known gaps, parity gaps, or risks
7. Questions for the user
8. Suggested follow-up work
9. Handoff summary when the work is incomplete or likely to continue in another session

A good handoff summary should include:
- current task status
- files read
- files changed
- important findings
- exact next step
- open questions
- commands still to run

## Quality bar

The migrated result should aim for:
- visual parity with the legacy UI
- interaction parity where applicable
- responsive parity where applicable
- accessible markup and behavior
- no edits to the legacy app
- no jQuery-style DOM manipulation in the new app unless explicitly required
- SSR-safe implementation for Nuxt where relevant
- controlled styling with minimal leakage
- clear separation between UI, behavior, and data concerns
- explicit documentation of assumptions and gaps
- compliance with local linting rules
- basic unit tests for the migrated behavior without getting blocked on maximizing coverage

## Stop conditions

Stop and ask the user when:
- the target component boundary is unclear
- the legacy route or QA page cannot be accessed
- required project conventions are unknown
- old behavior depends on backend logic that cannot be inferred safely
- multiple conflicting implementations exist and the correct one is unclear
- parity cannot be verified from source or browser inspection
- required backend or data dependencies cannot be inferred safely
- the change appears to require architecture-affecting modifications

## Session continuity expectations

If the work is large, ambiguous, or likely to exceed model limits:
- prefer report-first and plan-first execution
- keep the migration state file current
- summarize progress after each major phase
- leave behind an exact next step, not just a broad description
- record validation already run and validation still pending

Before switching models or ending an incomplete session, save:
- what component or route is being migrated
- where the legacy source was found
- what runtime behavior was observed
- what files were created or changed in the new app
- what remains to be done
- what risks, blockers, or unanswered questions exist

## Testing expectations

Add basic unit tests for the migrated behavior when the project has an established testing setup.

Testing guidance:
- cover the main rendered states and critical interactions for the migrated component
- follow the local test file placement and naming conventions
- prefer simple, maintainable unit tests over exhaustive test suites
- prefer testing the pure UI component first, and test adapters when mapping behavior is important
- do not get hung up on increasing coverage numbers beyond what is reasonable for the scoped change
- if the project has no clear unit test pattern for this area, follow the nearest established example or ask
- do not introduce a new testing library without asking

## Standard kickoff questions

Before I start, please provide:
1. Legacy app source root
2. New app source root
3. AI documentation root if you want me to follow shared AI coding references
4. Legacy QA URL
5. New app local URL
6. Target route or component to migrate
7. Nuxt and Vue coding conventions
8. Desired output format
9. Any required npm commands or local validation expectations if they differ from the repo defaults
