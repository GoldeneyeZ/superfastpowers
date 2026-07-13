# Goal-Driven Bypass Policy Spec Review

Result: failed

Reviewed range: `ed9dc5d..HEAD`

## Finding

### Important — repair worker cannot perform the invalidation it is required to perform

`skills/goal-driven-development/implementer-prompt.md:17` requires a repair worker to reset the repair-triggering phase and downstream phases, but line 27 then limits it to updating only the task and implementation-phase fields. Under bypass, spec, quality, and integration are plan-scoped fields, so the later restriction prevents the worker from applying the invalidation required by the design (`2026-07-13-goal-driven-bypass-policy-design.md:125`, `:132`, and `:171`). This leaves the repair contract internally contradictory and can preserve stale checked review evidence.

## Coverage Evidence

- The expanded policy is durable and policy-driven, with validation rules for known phases, scopes, prerequisites, acyclic dependencies, reachable gates, artifacts, and worker templates.
- `goal-driven-bypass` implements all tasks before one plan-scoped spec review and one plan-scoped quality review, reducing happy-path review phases from `2N` to `2`; required re-reviews and integration remain mandatory.
- `goal-driven-gated` preserves task-scoped implementation, spec, and quality phases before plan integration.
- Task and goal state values, completion timing, repair reopening, downstream invalidation, and artifact-over-progression precedence are documented.
- Generic phase dispatch and separate implementation, spec, quality, and integration worker templates replace the deleted full-lifecycle task worker.
- Brainstorming, Writing Plans, and README documentation recommend Bypass for elapsed time while preserving explicit user choice and the Gated early-feedback option.
- Behavioral/static tests, RED/GREEN eval documentation, test registration, and Claude Code test documentation are present. No unrelated execution semantics or parallel implementation behavior were added.

## Verification

- `STATIC_ONLY=1 tests/claude-code/test-goal-driven-development.sh` — passed all static policy and recommendation assertions.
- `bash -n tests/claude-code/*.sh` — all shell scripts parsed successfully.
- `git diff --check ed9dc5d..HEAD` — passed with no output.
- The Claude Code behavioral runner remains unavailable because the `claude` CLI is not installed; the recorded isolated-agent RED/GREEN eval evidence was reviewed but not treated as proof of the contradictory repair prompt.

