---
name: github-issues
description: Work with GitHub issues via the gh CLI - pull, break up, create, and close issues. Use when a workflow is driven by GitHub issues (planning breaks work into issues, workers pull tasks and close them when done).
---

# GitHub Issues (gh CLI)

The task store is GitHub issues. This skill covers pulling them down, breaking work up into new ones, and updating them through the lifecycle.

---

## Setup — DETECT, THEN STOP

**Step 1: Check gh is installed.**
```bash
command -v gh || echo "GH_MISSING"
```

- If `GH_MISSING`: do **not** improvise an install. Print exactly this and stop:

  > **gh CLI is required.** Install it, then re-run:
  > ```bash
  > brew install gh        # macOS (or: winget install --id GitHub.cli / apt install gh / your distro's package)
  > gh auth login          # choose GitHub.com → HTTPS → "Login with a web browser" → authenticate
  > ```
  > After `gh auth login`, verify with `gh auth status` before continuing.

**Step 2: Check authentication.**
```bash
gh auth status 2>&1 | head -5
```
- If not authenticated: tell the user to run `gh auth login` (browser flow, scopes: `repo` for private repos, `workflow` if workflow files are edited), then stop and wait for confirmation.

**Never** attempt workarounds (token-in-env hacks, curling the REST API by hand) unless explicit setup instructions fail and the user agrees. Auth is a human-in-the-loop event — it happens once in the main session, not inside an agent mid-task.

---

## Resolving the repo

Always prefer the explicit form — never assume:

```bash
# From inside the repo (reliable): parse origin
git remote get-url origin

# Or just view the current repo
gh repo view --json nameWithOwner -q .nameWithOwner

# Or look up by name
gh repo view <owner>/<repo> --json nameWithOwner -q .nameWithOwner
```

Pass `--repo <owner>/<repo>` on every command below. If `gh repo set-default` is configured, `--repo` can be omitted — but explicit is safer for autonomous use.

---

## Pulling issues

```bash
# List open issues
gh issue list --repo OWNER/REPO --state open --limit 50

# Filtered lists (combine freely)
gh issue list --repo OWNER/REPO --state open --label "bug" --assignee @me --limit 100
gh issue list --repo OWNER/REPO --state open --search 'label:"p1" sort:created-asc'

# Full context of one issue (body + comments)
gh issue view 123 --repo OWNER/REPO --comments

# Machine-readable (for parsing, combine with jq)
gh issue list --repo OWNER/REPO --state open --json number,title,labels,assignees,updatedAt
```

**Parsing discipline:** when you need numbers/titles for downstream work, use `--json` + `jq`, not `--format` strings you have to regex. Never invent issue numbers — every number you act on must come from an actual list/view result.

---

## Breaking work up (process)

Before creating issues, apply the same contract the `write-todos` skill uses:

- **Each issue is independently implementable.** A worker picks it up without reading the other issues. Repeat constraints inside the issue body — don't rely on "see issue #1".
- **Every issue needs:**
  1. A concrete title — imperative action ("Add UserService.updateProfile"), not a vibe ("Improve profile stuff")
  2. **Acceptance criteria** — binary, checkable items; reference plan ISC numbers when a plan exists
  3. A **code example or file reference** (file path + line range, or a sketch) — the shape of what's expected
  4. **Explicit constraints** — libraries, architecture decisions, integration points
  5. **Named anti-patterns** — "do NOT use X" where it matters
- **Size:** aim for work that fits a single focused session (roughly todo-scale to a few hours). If a piece is bigger, split it.
- **Sequence dependencies:** create issues in dependency order; note blocking with issue references ("requires #123").
- **Labels tell the pipeline what to do:** e.g. `research`, `architecture`, `dev`, `test`, `release` — use a consistent label set per repo so the orchestrator can filter.
- **Size as you create** — see [Triage & sizing](#triage--sizing): every new issue gets a `size:N` label and passes the oversize check before it's created.
- **Don't mass-create blindly.** Creating 20 issues is a decision that deserves a human glance. Create the set, then present the summary (numbers + titles + labels) back.

---

## Creating issues

```bash
# Body from a file (always the reliable way for multi-line bodies)
cat > /tmp/issue-body.md <<'EOF'
## Context
Why this matters (2-3 sentences).

## Acceptance Criteria
- [ ] ISC-1: <atomic checkable statement>
- [ ] ISC-2: ...

## Constraints
- Use <library/pattern>, follow <file>:<line> as the reference shape
- Do NOT use <anti-pattern>

## References
- Plan: .pi/plans/<date>-<name>/plan.md
- Related issue: #123
EOF

gh issue create --repo OWNER/REPO --title "TITLE" --body-file /tmp/issue-body.md --label dev --assignee @me
```

Flags that matter:
- `--label` repeatable; `--assignee @me` or a username
- `--milestone "v1.0"` when the repo uses milestones
- `--body-file` over `--body` for anything longer than a line

**Always verify after creating:**

```bash
gh issue view <number> --repo OWNER/REPO --json number,title,labels -q '{n:.number,t:.title,l:[.labels[].name]}'
```

---

## Updating and closing

```bash
# Close when done
gh issue close 123 --repo OWNER/REPO

# Close with a reason
gh issue close 123 --repo OWNER/REPO --comment "Integrated in <sha> via PR #456."

# Edit title/body/labels
gh issue edit 123 --repo OWNER/REPO --add-label done --remove-label dev

# Add context without closing
gh issue comment 123 --repo OWNER/REPO --body "..."
```

**Lifecycle conventions:** developer claims → `in_progress` comment → closes with evidence (test output, PR link) in the close comment. Never close without evidence. If blocked, comment `blocked: <reason>` *before* closing anything.

---

## Triage & sizing (effort pointing)

Issues get a relative effort rating stored as a `size:N` label. This lets the pipeline do real work: filter "open `size:1`+`size:2`" for a quick session, "ready, unsized" for a triage pass, "needs-split" for the planner.

### The scale — relative effort, NOT time

| Size | Meaning | Signals |
|------|---------|---------|
| `size:1` | Trivial — one rename, one flag, a doc line | Single atomic change, existing pattern, no new decisions |
| `size:2` | Small — one focused change in one file/module | One behavior, example or file reference present, no open design questions |
| `size:3` | Medium — a few files, one subsystem | Coherent feature, clear acceptance criteria, maybe one design decision |
| `size:5` | Large — multiple subsystems, new patterns or flows | Cross-cutting, needs several files + tests, decisions with tradeoffs |
| `size:8` | Very large — **needs splitting before it can be worked** | See oversize checklist below |

Points are **relative scope, not hours**. Assign by comparing against other issues in the repo ("about the same size as #42"), not by estimating time. When in doubt, round up — a misfit `size:3` costs less than an undersized `size:1` that gets started and stalls.

### Detecting oversized issues

An issue is **too large** (`size:8` / needs-split) if any of these hold — always quote the evidence from the body, never assert "feels big":

- **Bundles 2+ distinct behaviors** — multiple top-level goals, "and also", "plus": *"Add login, and also implement account recovery and SSO"*
- **No acceptance criteria** — nothing checkable means the worker can't finish it
- **No example or file reference** — the shape of "done" is undefined (apply the write-todos contract)
- **Touches 2+ subsystems** — auth + billing + UI in one issue is a plan, not a task
- **Requires a design decision first** — the issue proposes options, so it's architecture work, not implementation
- **Vague verbs / no scope boundary** — "Improve", "Refactor the module", "Make it production-grade"

### Triage procedure

When asked to run a triage pass (new pipeline start, backlog review, or "which issues can I grab"):

1. **Pull candidates** — unsized or `needs-split` issues:
   ```bash
   gh issue list --repo OWNER/REPO --state open --search 'no:label "size:"' --limit 30
   gh issue list --repo OWNER/REPO --state open --label "needs-split"
   ```
2. **Read each** — `gh issue view N --repo OWNER/REPO --comments` (comments often hold scope that the body omits)
3. **Score** against the scale, with the oversize checklist as the gate
4. **Label it:**
   ```bash
   gh issue edit 123 --repo OWNER/REPO --add-label size:3
   ```
5. **Split oversized ones:** for each `size:8` candidate, apply the breaking-work-up process — create the child issues, size them, mark the parent:
   ```bash
   gh issue edit 456 --repo OWNER/REPO --add-label needs-split --comment "Split into #457, #458, #459"
   ```
   - Remove `needs-split` only after the children exist and the pipeline has a plan or the parent is closed as a tracking issue.
6. **Write the triage report** (artifact, same `write` discipline as the other outputs):
   ```markdown
   # Issue Triage
   **Date:** ...
   ## Sized
   | Issue | Size | Evidence |
   |---|---:|---|
   | #42 | 2 | single-file change, example present |
   ## Split
   | #456 → children | sizes |
   ## Unsized by design
   - #91 unassigned — waiting on product decision
   ```
   Report the path in your summary.

7. **Present the outcome** — a short table (issue → size → action) back to whoever asked, and flag anything `size:5`+ for a human glance.

### Sizing filters the pipeline uses

```bash
# Quick session candidates (small only)
gh issue list --repo OWNER/REPO --state open --label size:1 --label size:2

# Ready but unsized (needs a triage pass)
gh issue list --repo OWNER/REPO --state open --search 'no:label "size:"'

# Blocked on planning
gh issue list --repo OWNER/REPO --state open --label needs-split
```

**Honesty rule:** sizing is an **estimate from signals, not a measurement**. Mark anything you're unsure about with a `?` in the report ("size:3? — depends on existing rate-limit behavior") instead of pretending precision. The point of pointing is to drive filtering and flag splits — not to make exact promises.

---

## Quick reference

| Task | Command |
|---|---|
| List open | `gh issue list --repo O/R --state open --limit 50` |
| Full issue | `gh issue view N --repo O/R --comments` |
| Create | `gh issue create --repo O/R --title "..." --body-file /tmp/body.md --label dev --assignee @me` |
| Close | `gh issue close N --repo O/R --comment "..."` |
| Edit labels | `gh issue edit N --repo O/R --add-label X --remove-label Y` |
| Size an issue | `gh issue edit N --repo O/R --add-label size:3` |
| Find unsized | `gh issue list --repo O/R --state open --search 'no:label "size:"'` |
| Comment | `gh issue comment N --repo O/R --body "..."` |
| Check setup | `command -v gh && gh auth status` |

## Error rules

- Any `gh` command failing with auth/permission errors → report the exact error, do not retry variations silently
- Never fabricate issue numbers, labels, or repo names
- A created issue is not "done" until `gh issue view` confirms it