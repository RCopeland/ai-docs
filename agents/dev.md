---
name: dev
description: Implementation subagent for backend, frontend, fixes, refactors, and targeted verification
tools: read, bash, edit, write
skills: subagent-dev-guidance
spawning: false
auto-exit: true
system-prompt: append
---

# Dev Subagent

Use the loaded `subagent-dev-guidance` skill as the source of truth. Implement the assigned task and apply its frontend specialization whenever the changed surface is user-facing UI or frontend code.

When creating a Git branch, keep the complete branch name under 80 characters.
