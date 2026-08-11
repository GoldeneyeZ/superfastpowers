---
name: subagent-driven-development
description: Use when a written plan has independent tasks suitable for isolated workers in the current session.
---

# Subagent-Driven Development

## Workflow

1. Read plan; identify independent tasks and disjoint writes.
2. Dispatch one bounded implementer per ready task, within available capacity.
3. Each worker implements, runs focused tests, self-reviews, returns changed paths and blockers.
4. Controller verifies actual diff and results.
5. After all tasks integrate, run one focused whole-plan review and one final verification batch.

Use `./implementer-prompt.md`. Separate spec and quality reviewers are optional, reserved for high-risk changes or explicit human request.

## Rules

- Never parallelize overlapping writes.
- Keep dependent linear tasks with same worker when practical.
- Do not require commits per task.
- Do not create review artifacts or restart completed stages.
- Focused finding → focused repair → affected tests.
- Controller owns final integration and completion claim.

## Completion

Requirements met, actual combined diff reviewed once, relevant tests green, no unresolved blockers.
