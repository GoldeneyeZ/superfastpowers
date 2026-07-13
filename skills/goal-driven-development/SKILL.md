---
name: goal-driven-development
description: Use when executing implementation plans with task package directories, context.md files, or plan-progression.md; also use when the user chooses Goal-Driven execution
---

# Goal-Driven Development

## Overview

Execute packaged plans by interpreting the explicit execution policy in `plan-progression.md`.

**Core principle:** Policy controls phase order and scope; invariants protect correctness.

**Default recommendation:** `goal-driven-bypass` minimizes elapsed time. Implement every task first, then run two plan-wide review phases. For `N` tasks, happy-path spec and quality reviews fall from `2N` to `2`.

Main agent stays lightweight: validate policy, select next runnable target, dispatch one isolated phase worker, verify durable artifacts/state, repeat. Detailed implementation and review evidence stays in task or goal files.

**Continuous execution:** Do not pause between phases or tasks. Stop only for unresolved `BLOCKED`, ambiguity preventing progress, invalid policy, or completed goal.

## When to Use

Use when:

- Implementation plan has task package directories.
- Each task has `task.md` and `context.md`.
- `plan-progression.md` declares execution policy.
- User chooses Goal-Driven execution.

If progression or task packages are absent, use `writing-plans` first. Ordinary un-packaged plans use `subagent-driven-development` or `executing-plans`.

## Entry Point

1. Confirm one active goal for whole plan. Never create separate goals per task or phase.
2. Locate plan, task-package root, and `plan-progression.md`.
3. Read and validate complete execution policy before implementation.
4. Select first incomplete phase whose prerequisites are satisfied.
5. Dispatch exactly one phase worker using `./phase-worker-prompt.md`.

If policy is invalid, stop before implementation and report exact invalid field, reference, or dependency.

## Execution Policy

`plan-progression.md` contains preset label plus fully expanded phases. Preset alone is insufficient; expanded lines are durable contract.

Each phase line uses:

```text
N. <name> | scope: task|plan | requires: <state> | artifact: <path pattern> | worker: <template>
```

Supported phases:

- `implementation`
- `spec-review`
- `code-quality`
- `integration-review`

### Validate Before Work

- Phase name known.
- Scope is `task` or `plan`.
- Every prerequisite references existing phase/state.
- Dependency graph acyclic.
- Task-local and goal completion gates reachable.
- Artifact and worker declarations present.
- `spec-review` precedes matching `code-quality`.
- `integration-review` is final.
- Task-scoped phase has eligible task target.
- Plan-scoped phase has goal-level artifact.

Unknown phases are not executable extensions. Stop and ask for policy correction.

## Shipped Presets

### Goal-Driven Bypass — Recommended

Use when elapsed time matters more than earliest task-local review feedback.

```markdown
## Execution Policy

- Preset: goal-driven-bypass
- Task-local gate: implementation
- Phases:
  1. implementation | scope: task | requires: none | artifact: `tasks/<TASK-ID>/context.md` | worker: `skills/goal-driven-development/implementer-prompt.md`
  2. spec-review | scope: plan | requires: all tasks implemented | artifact: `spec-review.md` | worker: `skills/goal-driven-development/spec-reviewer-prompt.md`
  3. code-quality | scope: plan | requires: spec-review checked | artifact: `code-quality.md` | worker: `skills/goal-driven-development/code-quality-reviewer-prompt.md`
  4. integration-review | scope: plan | requires: code-quality checked | artifact: `final-review.md` | worker: `skills/goal-driven-development/integration-reviewer-prompt.md`
```

Happy path: implement all tasks → one whole-plan spec review → one whole-plan code-quality review → final integration review. Required fix re-reviews remain uncapped.

### Goal-Driven Gated

Use when early task-local feedback matters more than elapsed time.

```markdown
## Execution Policy

- Preset: goal-driven-gated
- Task-local gate: code-quality
- Phases:
  1. implementation | scope: task | requires: none | artifact: `tasks/<TASK-ID>/context.md` | worker: `skills/goal-driven-development/implementer-prompt.md`
  2. spec-review | scope: task | requires: task implementation checked | artifact: `tasks/<TASK-ID>/spec-review.md` | worker: `skills/goal-driven-development/spec-reviewer-prompt.md`
  3. code-quality | scope: task | requires: task spec-review checked | artifact: `tasks/<TASK-ID>/code-quality.md` | worker: `skills/goal-driven-development/code-quality-reviewer-prompt.md`
  4. integration-review | scope: plan | requires: all tasks complete | artifact: `final-review.md` | worker: `skills/goal-driven-development/integration-reviewer-prompt.md`
```

This reproduces per-task implementation → spec → quality behavior without embedding that sequence in controller logic.

Explicit user choice always overrides default recommendation.

## Required Package Shape

```text
<package-root>/
  plan-progression.md
  tasks/<TASK-ID>/
    task.md
    context.md
```

Create as policy needs:

```text
<package-root>/
  implementer-handoff.md       # goal-scoped repair brief
  spec-review.md               # plan-scoped spec evidence
  code-quality.md              # plan-scoped quality evidence
  final-review.md              # final integration evidence
  tasks/<TASK-ID>/
    implementer-handoff.md     # task-scoped repair brief
    spec-review.md              # task-scoped spec evidence
    code-quality.md             # task-scoped quality evidence
```

`context.md` is reviewer map, never proof: commit/range, files changed, relevant files inspected, verification commands/results, notes.

## Progression State

Task section:

```markdown
## Task 1: Name

- Path: `tasks/PLAN-1/`
- Status: pending
- Next action: Start implementation.
```

Task status values:

- `pending`
- `implementing`
- `implemented`
- `complete`
- `blocked`

Goal section:

```markdown
## Goal Phases

- Implementation: pending
- Spec review: unchecked
- Code quality: unchecked
- Integration review: unchecked
- Next action: Implement next pending task.
```

Implementation values: `pending`, `active`, `checked`, `failed`.

Review values: `unchecked`, `checking`, `checked`, `failed`.

Under bypass, successful task implementation sets `Status: implemented`; task becomes `complete` only after every plan-scoped gate passes. Under gated, successful task quality phase sets `Status: complete`.

`Next action` stays one sentence. Detailed findings belong in artifacts/handoffs.

## Controller Algorithm

1. Validate policy before implementation.
2. Find first phase whose prerequisite is satisfied and result incomplete.
3. For task scope, select first eligible task in plan order. For plan scope, select whole goal.
4. Mark selected phase/target active.
5. Dispatch `./phase-worker-prompt.md` with exact plan, policy, context, artifact, worker-template, and reviewed-range paths.
6. Verify returned artifact against actual files/diff and progression.
7. If progression disagrees with artifact, artifact evidence wins; correct progression.
8. Apply invalidation rules after repair.
9. Repeat until configured completion gate passes or work is blocked.

Never dispatch multiple implementation workers concurrently. Never carry unrelated prior-task details into worker prompt.

## Phase Results

Workers return:

- `COMPLETE`: artifact/state valid; advance policy.
- `BLOCKED`: unresolved external or plan blocker; stop.
- `NEEDS_CONTEXT`: provide exact missing context and redispatch.
- `FAILED`: inspect failure; change context, model capability, task split, or plan before retry.

Review failure is not worker failure. Reviewer writes findings/handoff, marks review `failed`, and controller dispatches implementation repair before re-running same review.

## Invalidation

Repairs invalidate checked evidence:

| Repair type | Invalidate |
|---|---|
| Behavioral/spec | Spec, quality, integration |
| Quality-only | Quality, integration |
| Uncertain scope | Spec, quality, integration |

Reset invalidated phase to `unchecked`; remove no evidence. Review artifact keeps prior result plus fresh result/history. Any uncertainty about behavior counts as behavioral/spec repair.

## Non-Configurable Invariants

Policy can change order/scope only. It cannot disable:

- TDD and watched failing tests.
- Task verification before `implemented`.
- One implementation worker at a time.
- Prefer one commit per task; record reviewed range in `context.md`.
- Continuous execution without unnecessary user pauses.
- Stop for unresolved blockers or ambiguity.
- Fix every blocking review finding and re-run its review.
- Spec review checked before code-quality review starts.
- Integration review as final gate.
- Independent inspection of actual code/diff; never trust reports as proof.

Bypass means defer reviews, never skip reviews.

## Commit Policy

Prefer one implementation commit per task. Repair may amend if repository policy permits. Otherwise record full reviewed range. Metadata-only context updates may follow implementation commit; distinguish them explicitly.

Reviewers inspect actual task commit/range for task scope or combined goal range for plan scope. Uncommitted changes require staged and unstaged diff inspection.

## Phase Templates

- `./phase-worker-prompt.md` — generic one-phase dispatch envelope.
- `./implementer-prompt.md` — implementation or active repair only.
- `./spec-reviewer-prompt.md` — task- or plan-scoped spec review.
- `./code-quality-reviewer-prompt.md` — task- or plan-scoped quality review.
- `./integration-reviewer-prompt.md` — final plan-scoped integration review.

## Red Flags

Never:

- Execute preset label without expanded phase lines.
- Embed implementation → spec → quality lifecycle in controller/worker.
- Start phase before declared prerequisite.
- Start quality before spec is `checked`.
- Mark bypass task complete when only implementation finished.
- Begin plan-scoped bypass review before every task is `implemented`.
- Treat bypass as permission to skip TDD, verification, review, fixes, or integration.
- Preserve downstream checked phase after invalidating repair.
- Put detailed findings in `plan-progression.md`.
- Trust `context.md` or implementer report as correctness proof.
- Run multiple implementation workers in parallel.
- Create separate goal per task or phase.
- Finish branch while configured gate remains unchecked/failed.

## Integration

**Required workflow skills:**

- `using-git-worktrees` — isolated execution unless human explicitly approves current branch.
- `writing-plans` — creates task packages and expanded policy.
- `test-driven-development` — implementation phases.
- `verification-before-completion` — final verification evidence.
- `finishing-a-development-branch` — completion handoff.
