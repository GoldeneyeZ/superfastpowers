# Goal-Driven Spec Reviewer Prompt Template

Use for configured `spec-review` phase after its prerequisite passes.

```
Phase: spec-review
Scope: [task|plan]
Target: [TASK-ID|whole goal]

Specification: [path/to/spec.md]
Plan/task requirements: [path(s)]
Target context: [one task context.md | every task context.md]
Reviewed range: [task commit/range | combined goal range]
Artifact: [task-local spec-review.md | goal-level spec-review.md]
Handoff: [task- or goal-level implementer-handoff.md]
Policy/progression: [path/to/plan-progression.md]

Verify independently. Read actual code and diff. Context/reports are maps, not proof.

Check missing, extra, misunderstood, or regressed requirements; stale context/range/file lists; and missing verification evidence. Task scope compares one task. Plan scope compares original specification, complete plan, every task context, and combined implementation.

Pass:
- Write Result: checked with evidence and concise coverage notes.
- Mark owned spec phase checked.
- Advance only to policy-declared next phase.

Fail:
- Write Result: failed with specific findings and file:line refs where possible.
- Write actionable handoff with fixes and re-review acceptance criteria.
- Mark owned spec phase failed; reset quality and integration to unchecked.
- Dispatch no later review.

Return result, artifact/handoff paths, reviewed range, progression fields changed, and next action.
```
