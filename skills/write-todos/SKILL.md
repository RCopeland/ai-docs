---
name: write-todos
description: Break a plan into bite-sized, independently implementable todos using the todo tool. Each todo must include code examples or file references, explicit constraints, anti-patterns, and verifiable acceptance criteria. Load before creating todos (planner phase 9).
---

# Write-Todos Skill

Load this before creating any todos with the `todo` tool. The todo structure below is a contract: **workers refuse todos that lack examples/references/constraints**, so a todo that violates this structure stalls the pipeline.

## Todo Size

- **2-5 minutes of worker effort each.** If a step takes longer, split it. 5-12 todos per feature is normal; 25 means you're over-splitting.
- **Each todo is independently implementable.** A worker picks it up *without reading the other todos or the plan prose*. Repeat decisions in the todos that depend on them — never assume workers read the plan.

## Required Fields (every todo)

Every todo's `body` MUST contain all of:

### 1. Code example OR file reference — non-negotiable
Either:
- **Inline code sketch** showing expected shape (imports, types, structure, naming), or
- **Existing-code reference**: file path + line range + what to look at ("follow the pattern in `src/services/AuthService.ts:15-40`")

New patterns get a *more* detailed example, not less.

### 2. Explicit constraints
- Libraries/packages to use
- Architectural decisions to repeat (don't reference the plan prose)
- Integration points

### 3. Named anti-patterns
- Explicit "do NOT use X / do NOT do Y" where relevant

### 4. Verifiable acceptance criteria
- Binary, checkable statements tied to ISC items where the plan has them (reference `ISC-1`, `ISC-2`, ...)
- What evidence "done" requires (test output, file paths, behavior)

## Using the Tool

```text
todo(action: "create", title: "Add UserService.updateProfile", body: "...", tags: ["<plan-name>"])
```

- `tags` = the plan name so todos group by feature
- Sequence todos so each builds on the last; creation order = recommended execution order

## Anti-Patterns

- ❌ "Implement X" with no example, no reference, no criteria — workers will reject it
- ❌ "Refactor Y" without naming the target structure
- ❌ Todos that require reading the plan to understand ("see plan section 3.2")
- ❌ Splitting one logical change into several todos that can't stand alone
- ❌ Conflating with UI/UX judgment — put visual acceptance into criteria, not prose

## Checklist — run before creating each todo

- [ ] Title is a concrete action ("Add X", "Migrate Y to Z"), not a vibe
- [ ] Body has a code example or file:line reference
- [ ] Body names libraries/patterns to use and what to avoid
- [ ] Acceptance criteria are binary and verify in seconds
- [ ] ISC items referenced where the plan defines them
- [ ] Implementable without reading any other todo or the plan