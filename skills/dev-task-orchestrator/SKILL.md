---
name: dev-task-orchestrator
description: Turn a repository-backed development task into a reviewed pull request through environment checks, an isolated Git worktree, and an explicit scout, developer, reviewer, and publisher workflow. Use only when explicitly invoked for a task that should follow this personal workflow.
---

# Dev Task Orchestrator

Turn the development task supplied with the invocation into a reviewed pull request. Apply this workflow only to that task; it does not expand scope or authorize unrelated changes.

## Environment Preflight

Complete the preflight before creating a branch, worktree, or subagent:

1. Resolve the repository root, current branch, `origin` URL, and intended pull-request base branch without changing them. Determine the base in this order:
   - use explicit task, user, or repository guidance when present;
   - otherwise, inspect remote branches and use `origin/develop` when it exists;
   - otherwise, use a clearly designated integration branch only when repository evidence such as control documents, CI configuration, branch policies, or established conventions identifies it as the integration target;
   - if neither a develop branch nor an evidenced integration branch can be found, ask the user which branch to use before assuming `main`, `master`, the remote default branch, or any other fallback.
2. Verify that Git and the pull-request CLI required by the remote are installed.
3. Verify remote Git access with a read-only operation such as `git ls-remote origin HEAD`.
4. When `origin` is Azure DevOps, verify all of the following without printing access tokens:
   - the `az` CLI is available;
   - the `azure-devops` CLI extension is available;
   - Azure authentication is live with `az account get-access-token --output none`;
   - Azure DevOps access works with a read-only command against the remote's explicit organization and project, such as `az devops project show`.
5. Avoid changing global Azure DevOps defaults during the preflight. Derive the organization and project from the remote or repository configuration and pass them explicitly.

If an Azure authentication check fails, stop before any repository mutation. Report the failed check, ask the user to reauthenticate with their normal `az login` flow, and rerun the preflight after they finish. Do not start an interactive login on the user's behalf. If a required CLI or extension is missing, report it and ask before installing anything.

## Start-Up Gate

Before implementation:

1. Check `git status`.
2. Require a fully clean working tree: no unstaged, staged-but-uncommitted, or untracked changes.
3. If the tree is not clean, stop and ask the user how to handle it. Do not alter or discard existing changes without direction.
4. Verify that the current branch is the appropriate pull-request base branch.
5. If it is not the appropriate base, stop and ask before switching branches.
6. Once the tree is clean and the base branch is appropriate, update it from `origin` with a fast-forward-only pull.
7. Begin implementation only after that clean, updated state is established.

If the task is not operating in a Git repository, explain that this workflow does not apply and ask whether to proceed without it.

## Isolated Worktree Gate

After the start-up gate and before invoking a subagent, create a fresh worktree and task branch for this invocation:

1. Choose a branch name consistent with repository conventions. When no convention is discoverable, use `codex/<task-slug>-<unique-suffix>`.
2. Create the worktree as a uniquely named sibling of the primary checkout so it does not make the primary working tree dirty.
3. Create the task branch from the updated pull-request base branch. Never attach the worktree to a branch already checked out elsewhere.
4. Confirm with `git worktree list --porcelain` and `git -C <worktree> rev-parse --show-toplevel` that the path and branch are unique and correctly attached.
5. Record the absolute worktree path, task branch, base branch, remote, Azure DevOps organization, and Azure DevOps project as shared workflow context.

If a path or branch collides with another invocation, generate a new suffix. Never reuse, delete, unlock, or overwrite another invocation's worktree or branch.

All implementation, review, tests, staging, commits, pushes, and PR preparation must run inside this invocation's worktree. Every subagent must receive its absolute path and confirm it is operating there before doing work. Do not fall back to the primary checkout.

## Subagent Workflow

The root agent coordinates the workflow and preserves the user's scope. Use the globally configured `dev` and `review` agents for their respective roles; their shared guidance conditionally handles frontend work. Do not spawn `frontend-dev`, `frontend-review`, or other surface-specific variants. Give each agent the resolved task, the worktree path and branch context, the minimum relevant repository context, its permitted actions, and the exact output expected from it.

### 1. Scout When Needed

Skip the scout when the task is sufficiently clear to implement and verify.

Invoke a scout only when ambiguity can be reduced through repository inspection. The scout is read-only and must:

- locate relevant code, tests, conventions, and existing behavior;
- identify evidence that resolves the ambiguity;
- report any remaining question whose answer would materially change the result.

The scout must not create an implementation plan or edit files. If material ambiguity remains after scouting, the root asks the user a focused question before invoking the developer.

### 2. Developer

Invoke the global `dev` agent with the resolved task and acceptance criteria. The developer owns implementation and should:

- confirm its repository root is the assigned worktree before editing;
- make only in-scope changes;
- add or update meaningful tests when warranted;
- run checks appropriate to the change;
- report changed files, verification performed, and any unresolved risk.

Use additional instances of the global `dev` agent only when the task has independent workstreams with non-overlapping file ownership inside the invocation worktree, or give each instance another explicitly managed worktree. The root is responsible for preventing conflicting edits and integrating their work into the task branch.

### 3. Reviewer

After development is complete, invoke the global `review` agent as a distinct subagent in the same invocation worktree. The reviewer independently inspects the task, final diff, and test evidence. It may run read-only diagnostics and tests but must not edit implementation files.

The reviewer must end with exactly one decision:

- `APPROVED` when the task and acceptance criteria are satisfied with no blocking findings.
- `CHANGES_REQUESTED` with concrete, prioritized findings when further work is required.

### 4. Developer/Reviewer Loop

If the reviewer requests changes, send all findings back to the developer. After the developer addresses or explicitly resolves them, return the updated result to the same reviewer. Every material implementation change must be reviewed again.

Continue until the reviewer returns `APPROVED`. If the same material blocker survives three review cycles, stop the loop, summarize the disagreement or impediment, and ask the user for direction. Do not invoke the publisher without reviewer approval.

### 5. Publisher

Once review is approved, invoke a publisher with the task, approved diff, verification results, and reviewer decision. The publisher must:

1. Confirm it is operating in the invocation worktree on the approved task branch.
2. Recheck the relevant Git and pull-request CLI authentication before publishing; if Azure authentication expired, pause for user reauthentication and retry after confirmation.
3. Verify that the worktree contains only the approved task changes, stage exactly those files, and confirm the staged diff matches the reviewed diff.
4. Stop and report any staged or unstaged change that does not belong to the task.
5. Fetch the latest pull-request base from `origin`. If incorporating it changes the reviewed result or causes a conflict, return the task to the developer and reviewer loop; publishing remains locked until the reviewer approves the integrated result.
6. Re-verify that the task and base branches are appropriate; ask before renaming or replacing either branch.
7. Summarize the changes and propose a commit message with a short subject and brief body.
8. Ask the user to approve the commit before creating it.
9. After approval, create the commit and push the task branch to `origin`.
10. Open a pull request with a concise title and a body that covers the change, verification, and relevant risks or follow-ups. For Azure DevOps, use explicit organization, project, repository, source branch, and target branch arguments rather than mutable global defaults.
11. Return the pull request URL, task branch, and retained worktree path as the workflow output.

Do not commit, push, or open the pull request before the required commit approval. If any gate cannot be satisfied safely, report the exact blocker and wait for user direction.

## Coordination Rules

- Follow repository-specific control documents and instructions throughout the workflow.
- Preserve unrelated changes and existing authorization boundaries.
- Prefer reusing the developer and reviewer agents across feedback cycles so they retain context.
- Treat frontend as conditional guidance within `dev` and `review`, never as separate agent identities.
- Keep the invocation worktree after publishing so an open pull request can be amended safely. Remove it only when the user explicitly requests cleanup and it is clean.
- Keep human-facing and inter-agent messages concise and legible.
