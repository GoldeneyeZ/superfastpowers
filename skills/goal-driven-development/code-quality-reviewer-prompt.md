# Goal-Driven Code Quality Reviewer Prompt Template

Use for configured `code-quality` phase only after matching spec phase is `checked`.

```
Phase: code-quality
Scope: [task|plan]
Target: [TASK-ID|whole goal]

Spec artifact: [checked spec-review.md]
Target context: [one task context.md | every task context.md]
Reviewed range: [task commit/range | combined goal range]
Artifact: [task-local code-quality.md | goal-level code-quality.md]
Handoff: [task- or goal-level implementer-handoff.md]
Policy/progression: [path/to/plan-progression.md]

Stop if matching spec result is not checked. Review actual code/diff for correctness risks, test quality, maintainability, names, focused files, project fit, unrelated changes, and accurate context/range/evidence. Do not relitigate spec unless quality finding exposes spec miss.

Pass:
- Write Result: checked, or checked-with-minor-notes when policy permits, with evidence.
- Mark owned quality phase checked.
- Under gated policy, mark task complete.
- Under bypass, advance to integration; tasks remain implemented until every plan gate passes.

Fail:
- Write Result: failed with Critical, Important, Minor findings and file:line refs.
- Write actionable handoff with fixes and acceptance criteria.
- Mark quality failed; reset integration to unchecked.
- If finding changes specified behavior or scope is uncertain, reset spec to unchecked too.

Return result, artifact/handoff paths, reviewed range, progression fields changed, and next action.
```
