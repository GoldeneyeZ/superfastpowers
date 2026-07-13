# Goal-Driven Phase Worker Prompt Template

Use for one configured task- or plan-scoped phase.

```
Phase: [PHASE]
Scope: [task|plan]
Target: [TASK-ID|whole goal]

## Inputs

Policy/progression: [path/to/plan-progression.md]
Plan: [path/to/plan.md]
Specification: [path/to/spec.md]
Target context: [one task context.md | every task context.md]
Reviewed range: [commit or diff range]
Phase checklist: [template path]
Artifact: [artifact path]
Handoff: [task- or goal-level implementer-handoff.md]

## Contract

Execute only assigned phase and target. Read policy and verify prerequisite before work. Inspect actual code/diff and evidence; reports/context are maps, not proof.

Write only assigned artifact, handoff when required, owned progression fields, and context fields required by checklist. Apply policy invalidation after repair. Do not run later phase.

Return:
- Status: COMPLETE | BLOCKED | NEEDS_CONTEXT | FAILED
- Phase, scope, target
- Artifact path and result
- Reviewed commit/range
- Verification commands/results
- Progression fields changed
- One-sentence next action
```
