# Architecture Escalation Protocol

Applies when the architecture review returns `DEVIATION_SIGNIFICANT` or `NO_BASELINE`: the task is paused, and a human decides before code review or publishing continues.

## The Reviewer Emits A Token

The reviewer is read-only. It never writes a label, comment, or status. It emits a structured escalation:

```text
Decision: DEVIATION_SIGNIFICANT | NO_BASELINE
Recommended label: needs-arch-review
Reason: architecture-deviation
Human question: <the single decision required>
```

## The Integration Layer Acts

The orchestrator, supervisor, or human applies the label. This mirrors the factory-supervisor read-contract design: the review defines the vocabulary, and the layer that owns state applies it.

| Layer | Action on the token |
|---|---|
| `AGENTS.md` standard flow | Pause the task, apply `needs-arch-review`, and stop for human direction before `review`. |
| `dev-task-orchestrator` | Pause between the Architecture Gate and the Reviewer, apply `needs-arch-review`, record reason `architecture-deviation`, and stop before review or publish. |
| `factory-supervisor` | Apply `needs-arch-review` to the source item and record a `task.escalated` with reason `architecture-deviation`. The supervisor classifies and reports; it does not apply labels without authorization. |

The agent itself never writes the label.

## Unblocking

The task resumes only when a human resolves the escalation:

- `DEVIATION_SIGNIFICANT` — accept the deviation, revise the change, or update the stated architecture, then re-run the architecture gate.
- `NO_BASELINE` — establish an architecture baseline in a separate task, then re-run the gate. The gate cannot pass without a stated baseline.
