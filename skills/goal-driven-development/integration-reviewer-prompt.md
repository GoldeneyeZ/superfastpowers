# Goal-Driven Integration Reviewer Prompt Template

Use for final plan-scoped `integration-review` after code quality is `checked`.

```
Phase: integration-review
Scope: plan
Target: whole goal

Specification: [path/to/spec.md]
Plan: [path/to/plan.md]
Policy/progression: [path/to/plan-progression.md]
Task contexts: [all context.md paths]
Spec artifact(s): [paths]
Quality artifact(s): [paths]
Combined range: [base..HEAD or exact range]
Artifact: [path/to/final-review.md]

Verify actual combined diff and repository state. Check every configured prerequisite, task integration, later-task regressions, combined verification evidence, unresolved findings, uncommitted/unreviewed changes, and policy completion.

Pass:
- Write Result: checked with evidence and commands/results.
- Mark Integration review: checked.
- Mark all eligible implemented tasks complete and goal complete.

Fail:
- Write Result: failed with specific findings and affected tasks.
- Write goal-level handoff.
- Apply invalidation: behavioral/uncertain resets spec, quality, integration; quality-only resets quality and integration.
- Goal remains incomplete.

Return result, artifact/handoff paths, reviewed range, progression fields changed, and next action.
```
