# Goal-Driven Bypass Policy Design

## Problem

Goal-Driven Development currently embeds one lifecycle: implement each task, review its spec compliance, review its code quality, then mark it complete. This catches issues early but forces review context switches after every task. Users need a bypass mode that implements and verifies every task first, then runs one whole-plan spec review and one whole-plan code-quality review.

Bypass changes review timing only. It never bypasses TDD, task verification, commits, blocker handling, required fixes, or re-review.

## Decision

Make Goal-Driven Development policy-driven. `plan-progression.md` contains an explicit ordered execution policy. The controller validates and executes that policy instead of hard-coding implementer, spec-review, and code-quality phases.

Ship two presets:

- `goal-driven-bypass` — recommended default: task-scoped implementation followed by plan-scoped spec review, code-quality review, and integration review.
- `goal-driven-gated` — current behavior: task-scoped implementation, spec review, and code-quality review followed by plan-scoped integration review.

Brainstorming and plan handoff recommend `goal-driven-bypass`. Explicit user choice always overrides the recommendation.

## Execution Policy Contract

When task packages are created, the selected preset expands into a complete policy in `plan-progression.md`. The expanded policy is the durable execution contract; workers do not need hidden knowledge of preset definitions.

Example bypass policy:

```markdown
## Execution Policy

- Preset: goal-driven-bypass
- Task completion gate: implementation
- Phases:
  1. implementation | scope: task | requires: none
  2. spec-review | scope: plan | requires: all tasks implemented
  3. code-quality | scope: plan | requires: spec-review checked
  4. integration-review | scope: plan | requires: code-quality checked
```

Each phase declares:

- Stable phase name.
- Scope: `task` or `plan`.
- Prerequisite state.
- Completion gate.
- Artifact path and worker template where applicable.

The controller rejects unknown phase names, invalid scopes, missing prerequisites, cyclic dependencies, unreachable completion gates, or missing artifact/template declarations before implementation starts.

## State Model

Task state tracks implementation independently from goal-level reviews:

```markdown
## Task GD-1

- Status: pending
- Next action: Start implementation.
```

Allowed task status values:

- `pending`
- `implementing`
- `implemented`
- `complete`
- `blocked`

Goal phase state records plan-scoped gates:

```markdown
## Goal Phases

- Implementation: pending
- Spec review: unchecked
- Code quality: unchecked
- Integration review: unchecked
- Next action: Implement next pending task.
```

Allowed implementation values: `pending`, `active`, `checked`, `failed`.

Allowed review values: `unchecked`, `checking`, `checked`, `failed`.

With bypass policy, a task becomes `implemented` after its implementation, tests, task verification, context update, and commit succeed. It becomes `complete` only when all required plan-scoped gates pass. With gated policy, phase progression preserves current per-task review semantics.

## Controller and Worker Responsibilities

The Goal-Driven controller:

1. Reads and validates the expanded policy.
2. Finds the next phase whose prerequisites are satisfied.
3. Selects the next task for task-scoped phases or the full goal for plan-scoped phases.
4. Dispatches the matching phase worker.
5. Verifies artifacts and progression state after return.
6. Repeats continuously until completion or an unresolved blocker.

Workers execute only the assigned phase. The current task worker no longer embeds the full implementation → spec → quality lifecycle. Implementation workers may inspect any required code, follow TDD, run task verification, commit, and update `context.md`. Review workers independently inspect actual diffs and evidence.

Policy never makes these invariants configurable:

- TDD and watched failing tests.
- Task-level verification before `implemented`.
- One task implementation worker at a time.
- Prefer one commit per task and record reviewed ranges.
- Continuous execution without unnecessary user pauses.
- Stop for unresolved blockers or ambiguity.
- Fix every blocking review finding and re-run its review.
- Spec review must pass before code-quality review.
- Integration review remains the final gate.

## Bypass Review Flow

After every task reaches `implemented`:

1. Run one whole-plan spec review against the original specification, implementation plan, every task context, and combined diff.
2. Write findings to goal-level `spec-review.md` beside `plan-progression.md`.
3. On failure, write goal-level `implementer-handoff.md`, repair affected tasks, update their context and commit ranges, then rerun the whole-plan spec review.
4. After spec review is `checked`, run one whole-plan code-quality review.
5. Write findings to goal-level `code-quality.md`.
6. On failure, repair affected tasks and rerun the whole-plan code-quality review.
7. Run final integration review and write `final-review.md`.
8. Mark all implemented tasks and the goal complete only after every configured gate passes.

A repair that changes behavior invalidates all checked downstream phases. A quality-only repair invalidates code-quality and integration results, but retains checked spec status unless the change affects specified behavior. Any uncertainty invalidates spec status too.

## Gated Compatibility

`goal-driven-gated` reproduces existing behavior through policy rather than controller-specific branching:

```markdown
## Execution Policy

- Preset: goal-driven-gated
- Task completion gate: code-quality
- Phases:
  1. implementation | scope: task | requires: none
  2. spec-review | scope: task | requires: task implementation checked
  3. code-quality | scope: task | requires: task spec-review checked
  4. integration-review | scope: plan | requires: all tasks complete
```

Existing task-local artifacts remain valid for this preset: `spec-review.md`, `code-quality.md`, and `implementer-handoff.md` under each task directory.

## Brainstorming and Plan Handoff

Brainstorming recommends Goal-Driven Bypass when transitioning from approved design to implementation planning. It explains the trade-off: fewer review context switches and better whole-feature visibility, with later discovery of task-local mistakes.

Writing Plans offers these execution choices after user validation and task-package creation:

1. Goal-Driven Bypass — recommended.
2. Goal-Driven Gated.
3. Subagent-Driven.
4. Inline Execution.

Choosing either Goal-Driven option creates `plan-progression.md` with the fully expanded policy. Bypass is a recommendation, never an implicit override of explicit user preference.

## Failure Handling

- Invalid policy: stop before implementation and report exact invalid field or dependency.
- Task implementation failure: keep owning task active or blocked; do not advance implementation phase.
- Plan spec failure: record concrete findings, repair affected tasks, rerun whole-plan spec review.
- Plan code-quality failure: record severity-ranked findings, repair affected tasks, rerun whole-plan quality review.
- Repair after checked review: invalidate affected phase and every downstream phase.
- Progression/artifact disagreement: artifact evidence wins; correct progression before continuing.

## Evaluation Strategy

Skill changes follow `writing-skills` RED-GREEN-REFACTOR:

1. Baseline pressure eval proves current Goal-Driven instructions perform per-task spec and quality reviews even when asked to defer them.
2. Bypass eval proves all tasks reach `implemented` before either review begins.
3. Whole-plan eval proves exactly one spec gate precedes exactly one quality gate, excluding required re-review after findings.
4. Compatibility eval proves gated preset preserves current per-task lifecycle.
5. Validation eval proves malformed, incomplete, and cyclic policies stop safely before implementation.
6. Invalidation eval proves behavioral repair resets spec, quality, and integration; quality-only repair resets quality and integration.
7. Recommendation eval proves brainstorming and Writing Plans recommend Goal-Driven Bypass while honoring explicit user choice.

## Scope

In scope:

- Policy-driven Goal-Driven controller and phase workers.
- Bypass and gated presets.
- Progression schema and goal-level review artifacts.
- Brainstorming and Writing Plans recommendation/handoff updates.
- Documentation and adversarial skill evals.

Out of scope:

- Arbitrary user-authored executable worker code.
- Parallel implementation workers.
- Disabling TDD, verification, commits, review fixes, or integration review.
- Changing Subagent-Driven or Inline execution semantics beyond option descriptions.
