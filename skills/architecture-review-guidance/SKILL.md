---
name: architecture-review-guidance
description: Read-only architecture conformance method for the architecture-reviewer subagent - evaluates a change against stated architecture patterns and returns a conformance decision, escalating significant deviations or a missing baseline for human review.
---

# Architecture Review Guidance

Decide whether an assigned change conforms to the repository's **stated** architecture. This is a gate in the workflow, not a general code review.

## Position in the Workflow

- Runs **between `dev` and `review`**: after implementation, before code review.
- A passing decision admits the change to `review`. A blocking decision pauses the task and hands the decision to a human.
- It is **not** the release gate. Do not judge code quality, correctness, tests, naming, or style — those belong to `review`.
- Judge only conformance to the declared architecture. If the architecture is undocumented, that is a blocking result, not a license to invent rules.

## Read-Only Boundary

- Confirm the repository root and branch before review.
- When the parent supplies a worktree path, perform every inspection there.
- Never edit, stage, commit, push, or publish.
- Never create, scaffold, or modify an architecture baseline or its documentation.

## Step 1: Resolve The Stated Architecture

Load and follow the `architecture-baseline` skill. It returns either a cited baseline or `NO_BASELINE`. Record the exact source files you relied on. Only documented statements count as "stated architecture".

## Hard Stop On A Missing Baseline

If the baseline is `NO_BASELINE`, return `NO_BASELINE` and stop. Do not infer stated architecture from existing code, folder names, or habit. Do not create a baseline. Establishing one is a separate human task, started deliberately outside this review.

## Step 2: Inspect The Change

Inspect the actual diff and enough surrounding structure to judge boundaries — module edges, dependency direction, contracts, and integration points. Prefer reading the real call and data flow over assuming intent.

## Step 3: Evaluate Conformance

Apply each dimension the change touches; skip the rest:

- **Module/service boundaries** — new or crossed ownership lines.
- **Layering and dependency direction** — for example, a UI layer reaching directly into data access.
- **Integration and communication patterns** — sync vs async, direct call vs broker, REST vs events.
- **Data ownership and contracts** — who owns a store, schema, or shared type.
- **Cross-cutting concerns** — auth, caching, logging, configuration, error handling.
- **Public contracts** — APIs, schemas, events, published types.
- **Deployment and topology** — services, environments, configuration surface.
- **Consistency** — whether the change competes with an established pattern.

## What Counts As Significant

A deviation is significant, and therefore blocking, when it would change the architecture a future reader must assume. Concrete triggers:

- A new module, service, or ownership boundary, or a boundary the change crosses.
- A new external integration, message broker, queue, or datastore.
- A changed communication pattern (sync to async, direct call to broker, or the reverse).
- A cross-cutting concern implemented differently from the established approach.
- A change to a public API, schema, event contract, or shared type.
- A layering or dependency-direction violation.
- A competing pattern introduced alongside an established one.
- A deployment, topology, or configuration-surface change.

A change that stays inside an existing boundary and follows the established pattern is not significant. Use `CONFORMS_WITH_NOTES` for small drift a human should know about but that does not change the architecture.

## Decision Taxonomy

Return exactly one decision:

| Decision | Meaning | Next action |
|---|---|---|
| `CONFORMS` | Matches the stated architecture. | Proceed to `review`. |
| `CONFORMS_WITH_NOTES` | Minor, non-blocking drift; the architecture is unchanged. | Proceed to `review`, carrying the notes as context. |
| `DEVIATION_SIGNIFICANT` | A significant change to the intended architecture. | Pause the task and escalate for a human decision. |
| `NO_BASELINE` | No stated architecture is documented. | Pause and escalate; a human establishes the baseline separately. |

## Output

Return this block, then a short rationale. Link escalated cases to `references/escalation.md`.

```text
Architecture Decision: CONFORMS | CONFORMS_WITH_NOTES | DEVIATION_SIGNIFICANT | NO_BASELINE

Baseline sources:
- path/to/source

Evidence:
- path/to/file.ext:line - <the change> vs <the stated pattern>

Significant: yes | no

Human question: <the single decision a person must make>   # escalation cases only
```

End with a one-paragraph summary. A short report with few, high-confidence findings is the right answer; do not manufacture deviations to look thorough.
