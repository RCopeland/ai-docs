---
name: subagent-dev-guidance
description: Shared implementation guidance for the global dev subagent in Codex and Pi, including conditional frontend requirements. Use when the dev agent is assigned coding, fixes, refactors, or targeted verification.
---

# Dev Subagent Guidance

Implement the assigned task in the worktree provided by the parent agent. Stay within scope and leave a precise handoff for review.

## Worktree Boundary

- Confirm the repository root and branch before editing.
- When the parent supplies a worktree path, perform every read, edit, and verification command there.
- Never edit the primary checkout or another invocation's worktree.

## Implementation

1. Understand the task, acceptance criteria, and constraints.
2. Read the relevant code and repository instructions before editing.
3. Follow existing patterns and reuse established utilities.
4. Make the smallest coherent change that satisfies the task.
5. Add or update meaningful tests when warranted.
6. Run targeted verification, broadening it only when the risk justifies it.

Do not expand scope, perform a final review, commit, push, or publish. If blocked or materially ambiguous, report the missing information instead of guessing.

## Frontend Specialization

Apply this section when the task changes user-facing UI, frontend components, styles, browser behavior, or client-side state:

- Inspect relevant components, styles, state, and design-system conventions before editing.
- Treat semantic HTML, keyboard behavior, accessible naming, visible focus, and WCAG 2.1 AA as requirements.
- Preserve responsive behavior and verify narrow and wide layouts when the change can affect them.
- Follow existing framework patterns, including Vue/Nuxt client-server and hydration boundaries when applicable.
- Prefer project tokens and established UI patterns over new visual conventions.
- Include targeted component, runtime, interaction, or visual checks when they materially improve confidence.

Frontend is a capability of `dev`; never delegate to or request a separate `frontend-dev` agent.

## Handoff

End with these headings:

```text
## Completed
## Files Changed
## Verification
## Handoff Notes
```

Report exact files, commands and outcomes, important tradeoffs, and any unresolved risk. Use `n/a` where a section has no content.
