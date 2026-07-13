### Task 2: Make Goal-Driven Execution Policy-Driven

<TASK-ID>GDBP-2</TASK-ID>

**Files:**
- Modify: `skills/goal-driven-development/SKILL.md`
- Create: `skills/goal-driven-development/phase-worker-prompt.md`
- Delete: `skills/goal-driven-development/task-worker-prompt.md`
- Modify: `skills/goal-driven-development/implementer-prompt.md`
- Modify: `skills/goal-driven-development/spec-reviewer-prompt.md`
- Modify: `skills/goal-driven-development/code-quality-reviewer-prompt.md`
- Create: `skills/goal-driven-development/integration-reviewer-prompt.md`

- [ ] **Step 1: Replace hard-coded core principle and execution mechanism**

In `skills/goal-driven-development/SKILL.md`, preserve frontmatter description, then define:

```markdown
## Overview

Execute packaged plans by interpreting the explicit execution policy in `plan-progression.md`.

**Core principle:** Policy controls phase ordering and scope; invariants protect correctness.

**Default recommendation:** `goal-driven-bypass` minimizes elapsed time by implementing every task before two plan-wide review gates.
```

State that controller selects the next runnable policy phase, dispatches exactly one isolated phase worker, verifies artifacts/state, and repeats continuously.

- [ ] **Step 2: Add explicit policy schema and presets**

Add this contract to `skills/goal-driven-development/SKILL.md`:

```markdown
## Execution Policy

Each phase line uses:

`N. <name> | scope: task|plan | requires: <state> | artifact: <path pattern> | worker: <template>`

Supported phases: `implementation`, `spec-review`, `code-quality`, `integration-review`.

Validate before work:
- known phase and scope
- prerequisite references exist
- dependency graph is acyclic
- completion gate is reachable
- artifact and worker declarations exist
- `spec-review` precedes `code-quality`
- `integration-review` is final
```

Include fully expanded `goal-driven-bypass` and `goal-driven-gated` examples from the approved design. Bypass task-local gate is `implementation`; gated task-local gate is `code-quality`. Task-local gate means the last phase run per task before control advances; overall completion still requires integration review.

- [ ] **Step 3: Generalize progression state and controller loop**

Replace per-task `Implementer`, `Spec review`, and `Code quality` assumptions with:

```markdown
## Task GDBP-1: Name

- Path: `tasks/GDBP-1/`
- Status: pending
- Next action: Start implementation.

## Goal Phases

- Implementation: pending
- Spec review: unchecked
- Code quality: unchecked
- Integration review: unchecked
- Next action: Implement next pending task.
```

Document task states `pending`, `implementing`, `implemented`, `complete`, `blocked`; implementation states `pending`, `active`, `checked`, `failed`; review states `unchecked`, `checking`, `checked`, `failed`.

Controller algorithm:

```markdown
1. Validate policy before implementation.
2. Find first phase whose prerequisite is satisfied and result is incomplete.
3. For task scope, select first eligible task in plan order; for plan scope, select whole goal.
4. Dispatch phase worker with exact plan, progression, context, artifact, and diff/range paths.
5. Verify returned artifacts against progression; artifact evidence wins on disagreement.
6. Apply invalidation rules after repairs.
7. Repeat until configured completion gate passes or work is blocked.
```

- [ ] **Step 4: Preserve non-configurable invariants and invalidation**

Add explicit invariant list:

```markdown
- TDD and watched failing tests
- task verification before `implemented`
- one implementation worker at a time
- commit/range recorded in `context.md`
- required findings fixed and re-reviewed
- spec checked before quality starts
- integration review last
- unresolved blocker stops execution
```

Add invalidation table:

| Repair type | Invalidate |
|---|---|
| Behavioral/spec | Spec, quality, integration |
| Quality-only | Quality, integration |
| Uncertain scope | Spec, quality, integration |

- [ ] **Step 5: Replace full-lifecycle worker with phase worker**

Delete `skills/goal-driven-development/task-worker-prompt.md`. Create `skills/goal-driven-development/phase-worker-prompt.md`:

````markdown
# Goal-Driven Phase Worker Prompt Template

Use for one configured task- or plan-scoped phase.

```
Phase: [PHASE]
Scope: [task|plan]
Target: [TASK-ID|whole goal]

Read:
- Policy: [plan-progression.md]
- Plan: [plan.md]
- Context: [task context path(s)]
- Reviewed range: [commit or diff range]

Use phase checklist: [template path]
Write artifact: [artifact path]

Execute only this phase and target. Verify actual code and evidence. Update only fields owned by this phase. Return COMPLETE, BLOCKED, NEEDS_CONTEXT, or FAILED.
```
````

- [ ] **Step 6: Make phase templates scope-aware**

Update `implementer-prompt.md` so successful implementation sets task `Status: implemented` under bypass or advances to configured next task-scoped phase under gated policy. It must never run a review itself.

Update both reviewer prompts to accept:

```markdown
Scope: [task|plan]
Target context: [one task context.md | every task context.md]
Review artifact: [task-local path | goal-level path]
```

Spec reviewer: compare actual code/diff against task requirements for task scope or original spec + full plan for plan scope. Quality reviewer: inspect reviewed scope only after matching spec gate is checked. Both write actionable handoff and invalidate downstream phases on failure/fix.

- [ ] **Step 7: Add integration reviewer**

Create `integration-reviewer-prompt.md` requiring original spec, plan, policy, progression, all task contexts, prior review artifacts, and combined diff. It checks task integration, regressions, verification evidence, unreviewed changes, and unresolved findings; writes `final-review.md`; marks goal complete only on pass.

- [ ] **Step 8: Run behavioral test toward GREEN**

Run:

```bash
tests/claude-code/run-skill-tests.sh --test test-goal-driven-development.sh --timeout 240
```

Expected: PASS for policy, ordering, validation, and invalidation assertions. If model finds a new loophole, record wording under RED rationalizations, add minimal explicit counter, rerun.

- [ ] **Step 9: Commit controller and worker changes**

```bash
git add skills/goal-driven-development tests/claude-code/test-goal-driven-development.sh docs/superfastpowers/evals/goal-driven-bypass-policy.md
git commit -m "feat: make goal-driven execution policy-driven"
```
