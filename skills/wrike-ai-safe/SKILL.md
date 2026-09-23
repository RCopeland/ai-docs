---
name: wrike
description: Safely use ~/Dev/wrike-ai for Wrike task, custom item type, approval, assignee, and comment work. Use when listing, creating, updating, assigning, approving, commenting on, or bulk-cleaning Wrike items through the wrike CLI, especially when target scope, item type selection, duplicate avoidance, HTML conversion, confirmation, and secret-handling guardrails matter.
---

# Wrike AI Safe

Use `~/Dev/wrike-ai` as the source of truth for CLI behavior and safety expectations.

Primary README:
- `~/Dev/wrike-ai/README.md`

This skill is for safe, agentic use of the `wrike` CLI across read and write workflows.

---

## Core operating mode

- Default to **read-only discovery and planning**.
- Treat **create**, **update**, **comment**, and **bulk cleanup** as **write actions**.
- **Do not perform any write action until the user confirms.**
- If the correct target space or folder is not known, **do not guess**. Ask.
- Only operate in **explicitly allowed spaces/folders when appropriate**.
- If scope is ambiguous, stop and ask before proceeding.

---

## Safety rules

### 1) Targeting rules

- Prefer targeting a **specific folder** for task creation and bulk operations.
- If the task can be done at either space or folder scope, prefer the **narrower** scope.
- If the user has not identified an allowed space/folder and it matters for the action, ask for it.
- Never silently fall back to a broader target just because a narrower one was not supplied.
- Never assume that a default `.env` target is safe for autonomous writes.

### 2) Confirmation rules

Before any write action, present a short confirmation summary and wait.

The confirmation must include:
- action type
- profile name if known
- target space and/or folder
- item type for creates (for example, standard Task or `Dev`)
- item count
- titles and/or task IDs being changed

Use wording like:

```text
Confirm Wrike write:
- Action: create tasks
- Profile: default
- Target folder: IEABCD123
- Item count: 3
- Items:
  1. Build parity inventory for the new app
  2. Migrate account overview widgets
  3. Audit legacy route coverage
```

Do not execute the write until the user clearly confirms.

### 3) Duplicate prevention

Before creating tasks in bulk, and preferably before any create action:
- inspect the target folder with `wrike listTasks`
- look for likely duplicates by title or obviously overlapping work
- if duplicates are likely, stop and ask instead of creating

### 4) Item type selection

Before creating work, determine whether it should use the standard Wrike task type or a custom item type.

- Use `wrike listCustomItemTypes --type Task` to discover applicable task-like custom item types and their space IDs.
- Match the custom item type to the target space and the nature of the work. For example, software implementation work in an engineering sprint may belong to a `Dev` item type.
- Do not assume that the user's generic words “task,” “item,” or “work” mean the standard Task type.
- If both a standard Task and a plausible custom item type are reasonable, ask which type to use before confirmation.
- Include the resolved item type and custom item type ID in the confirmation summary.
- When a custom item type is selected, pass `--custom-item-type-id <ID>` to `wrike createTask`.
- After creation, verify the response contains the expected `customItemTypeId` when Wrike returns that field.

### 5) Secret and auth handling

- Never print tokens or secrets.
- Never edit `.env` unless the user explicitly asks.
- Never invent credentials or auth workarounds.
- Do not run auth commands unless the user explicitly asks.
- If auth is missing or broken, report the exact issue and stop.

### 6) Ambiguity rules

Ask instead of guessing when any of these are unclear:
- which profile to use
- which space or folder is allowed
- whether the user wants read-only discovery vs applying changes
- how to map a source document into Wrike tasks
- whether an existing item should be updated vs a new one created
- whether new work should be a standard Task or a custom item type such as `Dev`

---

## Setup and environment checks

Before using the CLI, verify the basics.

### Check the repo and CLI

```bash
cd ~/Dev/wrike-ai
command -v wrike || echo "WRIKE_CLI_MISSING"
```

If the CLI is missing, direct the user to the project README install flow:

```bash
cd ~/Dev/wrike-ai
npm install
npm run build
npm link
```

### Check auth state safely

Use read-only auth inspection when needed:

```bash
wrike auth profiles
```

If the user explicitly wants auth setup or repair, follow the README guidance. Otherwise stop and ask.

---

## Read workflows

Prefer these for discovery before proposing writes.

### Get current user

```bash
wrike getMe
```

### List spaces

```bash
wrike listSpaces --limit 25
```

### List folders

```bash
wrike listFolders --space-id <SPACE_ID>
```

If a safe, user-approved `WRIKE_SPACE_ID` exists, this may be omitted per README behavior. If not, be explicit.

### List tasks

Folder scope:

```bash
wrike listTasks --folder-id <FOLDER_ID> --limit 25 --descendants true
```

Space scope:

```bash
wrike listTasks --space-id <SPACE_ID> --limit 25
```

Use filters like `--title`, `--status`, and `--next-page-token` when helpful.

### List custom item types

```bash
wrike listCustomItemTypes --type Task --limit 100
```

Use the returned `spaceId` to select a type that belongs to the target space.

---

## Write workflows

All write workflows require confirmation first.

### Create task

Prefer `--description-html` over plain `--description` when content has structure.

Example:

```bash
wrike createTask \
  --folder-id IEABCD123 \
  --title "Build parity inventory for the new app" \
  --custom-item-type-id IECUSTOM123456789 \
  --description-html "<h3>Why</h3><p>Create a reliable view of what the new app already supports.</p><h3>Scope</h3><ul><li>Review routing</li><li>Review modular blocks</li></ul><h3>Acceptance</h3><ul><li>Status exists for each comparison bucket</li></ul>"
```

### Update task

```bash
wrike updateTask \
  --task-id IEACDEF456 \
  --title "Updated title" \
  --add-responsible-ids KUAAAAAA
```

Use `--description-html` for structured body updates.

Task status writes are intentionally unsupported by this CLI. `--status` remains available only as a read filter on `listTasks`.

### Create approval

```bash
wrike createApproval \
  --task-id IEACDEF456 \
  --approver-ids KUAAAAAA \
  --description "Please review"
```

Use `--folder-id` instead of `--task-id` for a folder or project. Creating an approval and updating approvers are write actions and require confirmation.

### Create comment

```bash
wrike createTaskComment --task-id IEACDEF456 --text-html "<p><strong>Comment</strong> from CLI</p>"
```

### Bulk cleanup

Bulk cleanup includes things like:
- removing numbering from titles
- replacing markdown-like/plain descriptions with HTML descriptions
- normalizing existing tasks from planning documents

Always preview the exact intended scope and item count before applying.

---

## Formatting rules from the README

Apply these consistently.

### Titles

- Use a meaningful title only.
- Strip numbering and labels such as:
  - `Card 01 — ...`
  - `Task 7 - ...`
  - `WR-CM-03 - ...`
- Create the title from the actual work item, not the source document prefix.

Good:

```text
Build parity inventory for the new app
```

Bad:

```text
Card 01 — Build parity inventory for the new app
```

### Descriptions

- Prefer `--description-html` over plain text when the source has structure.
- Convert markdown-like content into simple Wrike-safe HTML.
- Use a small HTML set:
  - `<h3>`
  - `<p>`
  - `<ul>` / `<li>`
  - `<strong>` when useful
- Do not paste raw markdown and expect Wrike to render it.

Recommended structure:
- `Why`
- `Scope`
- `Acceptance`

### Bulk conversion behavior

When cleaning up existing tasks created from numbered planning docs:
- remove leading numbering from titles
- replace markdown-like or plain-text bodies with `--description-html`
- preserve the original meaning while improving readability

---

## Mapping source material into tasks

If the user asks to turn a document into Wrike tasks and the mapping is ambiguous, ask whether they want:
- one task per section
- one task per checklist/story
- one task per component/feature

Do not choose a mapping silently when the source can reasonably support multiple interpretations.

---

## Recommended execution pattern

For non-trivial Wrike work, follow this sequence:

1. Confirm the allowed profile and target space/folder.
2. Run read-only discovery (`listSpaces`, `listFolders`, `listTasks`) as needed.
3. For creates, resolve the standard/custom item type with `listCustomItemTypes`; ask if ambiguous.
4. Check for likely duplicates before creates.
5. Draft cleaned titles and HTML descriptions.
6. Present the confirmation summary with folder, item type, and item count.
7. Wait for approval.
8. Execute the write.
9. Verify results with a read command when possible.

---

## Output discipline

- Prefer JSON command outputs for parsing and verification.
- Summarize proposed writes in plain language before asking for confirmation.
- After applying confirmed writes, report:
  - what changed
  - target folder/space
  - item count
  - any duplicates skipped
  - any items that were ambiguous and left untouched

---

## Failure handling

- If the CLI is unavailable, stop and point to the README install steps.
- If auth is missing, stop and ask the user to set it up explicitly.
- If the target folder/space is unclear, stop and ask.
- If likely duplicates are found, stop and ask.
- If the input content is too ambiguous to map safely, stop and ask.

Never guess on scope, target, or destructive intent.
