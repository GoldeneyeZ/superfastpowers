# Goal-Driven Implementer Prompt Template

Use for `implementation` phase or active repair handoff.

```
Phase: implementation
Scope: task
Target: [TASK-ID]: [task name]

Task: [path/to/task.md]
Context: [path/to/context.md]
Handoff: [path/to/implementer-handoff.md or none]
Policy/progression: [path/to/plan-progression.md]

Implement only target task or active handoff. Use test-driven-development: write test, watch correct failure, implement minimally, watch pass, refactor while green. Inspect any needed file; starting context is not constraint.

Inspect `git status --short`, `git diff`, and `git diff --cached` before editing. If any task-owned path already has changes not created by this task, stop and ask. Commit only task-owned paths. Use a path-limited commit (`git commit --only ... -- <task-owned paths>`) so pre-existing staged changes stay out.

For repair, reopen affected target before editing: task `implementing`, goal incomplete. Reset repair-triggering and downstream phases per policy:

- Behavioral/spec repair: reset spec, quality, and integration.
- Quality-only repair: preserve checked spec; reset quality and integration.
- Uncertain repair: treat as behavioral/spec.

After successful bypass repair, return task to `implemented`, never `complete`.

Before COMPLETE:
- task requirements or handoff satisfied
- focused and relevant regression verification passed
- self-review actual diff
- commit created; commit/range recorded
- `context.md` updated with files, inspected dependencies, commands/results, notes
- resolved handoff replaced by short resolved record

Update only affected task, implementation fields, and policy-required plan-scoped review fields needed for invalidation. Do not edit unrelated task fields or unrelated goal state.

On successful bypass implementation:
- Task Status: implemented
- Next action: Await plan-scoped reviews after all tasks are implemented.

On successful gated implementation:
- Advance target to configured next task-scoped phase.
- Do not run review yourself.

On blocker:
- Task Status: blocked
- Next action: one exact controller action.

Return Status, target, commit/range, verification, files/context updated, and one-sentence next action.
```
