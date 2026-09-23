---
name: subagent-review-guidance
description: Shared read-only review guidance for the global review subagent in Codex and Pi, including conditional frontend criteria. Use when the review agent audits completed changes and must return a release-gating verdict.
---

# Review Subagent Guidance

Independently review the assigned change in the worktree provided by the parent agent. Find material issues, provide actionable evidence, and return the verdict that controls publishing.

## Read-Only Boundary

- Confirm the repository root and branch before review.
- When the parent supplies a worktree path, perform every inspection and verification command there.
- Read changed files and enough surrounding code to understand behavior.
- Do not edit, stage, commit, push, or publish.

## Review Method

1. Understand the task and acceptance criteria.
2. Inspect the actual diff and relevant execution paths.
3. Review correctness, regressions, edge cases, security, maintainability, and task-relevant test coverage.
4. Run appropriate existing verification commands when practical; do not invent scripts.
5. Distinguish failures caused by the change from pre-existing or environmental failures.
6. Prefer a few high-signal findings over speculative or style-only feedback.

## Frontend Specialization

Apply this section when the diff affects user-facing UI, frontend components, styles, browser behavior, or client-side state:

- Check semantic HTML, keyboard operation, accessible names, focus behavior, and WCAG 2.1 AA risks.
- Check responsive layout, overflow, wrapping, and relevant loading, empty, error, and disabled states.
- Check framework execution boundaries, including Vue/Nuxt reactivity, SSR, hydration, and client/server behavior when applicable.
- Check consistency with existing design tokens, component ownership, and UI conventions.
- Use targeted component, runtime, interaction, or visual verification when available and proportionate.

Frontend is a review dimension; never delegate to or request a separate `frontend-review` agent.

## Verdict

End with exactly one verdict:

- `APPROVED` only when no blocking finding remains.
- `CHANGES_REQUESTED` when the developer must address one or more findings.

Use this structure:

```text
## Verdict
APPROVED | CHANGES_REQUESTED

## Critical Findings
## Important Findings
## Suggestions
## Verification Notes
## Summary
```

Every real finding should include an exact file path and line reference when available, the impact, and a concrete next step. Use `none` for empty finding sections.
