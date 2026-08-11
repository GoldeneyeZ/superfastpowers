---
name: goal-driven-development
description: Use when executing a written implementation plan with several related tasks.
---

# Goal-Driven Development

## Goal

Finish a plan with minimal coordination overhead.

## Workflow

1. Read plan once; identify dependencies and owned files.
2. Implement ready independent tasks in parallel when safe.
3. Keep linear dependent work with same agent.
4. Each worker runs focused tests and returns changed paths plus blockers.
5. Controller integrates results.
6. Run one plan-wide review against requirements and code quality.
7. Fix actionable findings; rerun affected tests plus one final verification batch.

Task folders and `context.md` files are optional. Use them only when already present, user requests them, or plan is too large for one document.

Do not create `plan-progression.md`, phase artifacts, implementer handoffs, separate spec/quality/integration reviewers, or repeated gate invalidation by default.

## Worker Rules

- One bounded task per worker.
- Parallel workers own disjoint writes.
- No worker commits unless controller explicitly assigns commit ownership.
- Verify actual files and tests; do not trust status claims alone.
- Stop only on real blockers, unsafe overlap, or missing authority.

## Review

One focused final review covers:

- plan requirements met;
- tests proportional to changed behavior;
- no obvious correctness, security, or integration defects;
- no unrelated changes.

Focused defect found → repair defect → rerun affected checks. Do not restart entire workflow.

## Prompt

Use `./implementer-prompt.md` for delegated tasks.
