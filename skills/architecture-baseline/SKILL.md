---
name: architecture-baseline
description: Locate the stated architecture for a repository - discovery order for ADRs, arc42/C4 docs, control documents, and structural conventions - and return a cited baseline or an explicit NO_BASELINE result. Use before an architecture conformance review or when a task needs the declared patterns.
---

# Architecture Baseline

Find the repository's **stated** architecture: the documented patterns a change is expected to follow. Load this before an architecture conformance review, and use it whenever planning or scouting depends on the declared design.

## What Counts As Architecture

- System and module boundaries and ownership.
- Layering and dependency direction.
- Integration and communication patterns.
- Data ownership and contracts.
- Cross-cutting concerns (auth, caching, logging, configuration).
- Public contracts (APIs, schemas, events).
- Deployment and topology.

## Discovery Order

Stop at the first source that states the architecture authoritatively, then cite it:

1. A dedicated baseline artifact such as `.pi/architecture.md` — canonical when present.
2. Repository control documents: `AGENTS.md`, `CLAUDE.md`, or a project-local skill.
3. Architecture docs: `docs/architecture/` and similarly named directories.
4. Architecture Decision Records: an `adr/`, `decisions/`, or `docs/adr/` directory.
5. arc42 or C4 documents and diagrams.
6. The repository `README`.
7. Only as **supporting evidence**, never as the sole source: module/package structure and configuration files.

## Output

Return one of:

- A **cited baseline** — the stated rules, each with the exact file path it came from.
- `NO_BASELINE` — no authoritative source documents the architecture.

## Hard Rule

Never create, scaffold, or modify a baseline. A missing baseline is escalated so a human can establish one deliberately in a separate task. Guessing architecture from existing code defeats the purpose of the review.
