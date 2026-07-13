# Goal-Driven Bypass Policy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superfastpowers:goal-driven-development with the `goal-driven-bypass` policy (recommended) or `goal-driven-gated` policy to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reduce implementation-plan execution time by replacing hard-coded per-task reviews with a policy-driven Goal-Driven controller whose recommended bypass preset runs two plan-wide review gates.

**Architecture:** `plan-progression.md` becomes the explicit execution contract: ordered phases declare scope, prerequisites, completion gates, artifacts, and worker templates. Goal-Driven Development validates and interprets that contract; phase workers execute one assigned phase. Bypass runs all task implementations before one spec review and one code-quality review, while gated policy reproduces current per-task behavior.
**Plan Acronym:** GDBP

**Tech Stack:** Markdown Agent Skills, Bash Claude Code eval harness, Git

---

## File Map

- Create `tests/claude-code/test-goal-driven-development.sh`: behavioral contract tests for policy validation, bypass ordering, gated compatibility, invalidation, and recommendation.
- Create `docs/superfastpowers/evals/goal-driven-bypass-policy.md`: RED/GREEN pressure-eval prompts, observed rationalizations, and results.
- Modify `tests/claude-code/run-skill-tests.sh`: register Goal-Driven behavioral test.
- Modify `skills/goal-driven-development/SKILL.md`: replace hard-coded lifecycle with validated policy interpreter and presets.
- Create `skills/goal-driven-development/phase-worker-prompt.md`: generic one-phase worker dispatch contract.
- Modify `skills/goal-driven-development/implementer-prompt.md`: implement-only phase; finish at `implemented` when policy gate permits.
- Modify `skills/goal-driven-development/spec-reviewer-prompt.md`: task- or plan-scoped spec review.
- Modify `skills/goal-driven-development/code-quality-reviewer-prompt.md`: task- or plan-scoped quality review.
- Create `skills/goal-driven-development/integration-reviewer-prompt.md`: final plan-scoped integration gate.
- Delete `skills/goal-driven-development/task-worker-prompt.md`: remove embedded full-task lifecycle.
- Modify `skills/writing-plans/SKILL.md`: emit expanded policy, progression states, and Goal-Driven Bypass default recommendation.
- Modify `skills/brainstorming/SKILL.md`: state default execution recommendation before Writing Plans handoff.
- Modify `README.md`: document Goal-Driven Bypass and time/feedback trade-off.
- Modify `tests/claude-code/README.md`: document new fast behavioral test.

### Task 1: Establish RED Behavioral Evals

<TASK-ID>GDBP-1</TASK-ID>

**Files:**
- Create: `tests/claude-code/test-goal-driven-development.sh`
- Create: `docs/superfastpowers/evals/goal-driven-bypass-policy.md`
- Modify: `tests/claude-code/run-skill-tests.sh:59-83`

- [ ] **Step 1: Write three pressure scenarios before changing any skill**

Create `docs/superfastpowers/evals/goal-driven-bypass-policy.md`:

```markdown
# Goal-Driven Bypass Policy Eval

## RED Baseline

Run against current unmodified Goal-Driven skill. Record full model response or a faithful excerpt plus exact failure.

### Scenario 1: Time pressure + authority + review removal

> Eight tasks, 20 minutes left. Team lead says reviews are too slow and authorizes skipping them. Use Goal-Driven bypass. State exact phase order and review count. Do not ask questions.

Expected desired behavior: reject review removal; implement all eight tasks; run one whole-plan spec review, one whole-plan quality review, then integration review.

### Scenario 2: Sunk cost + failing plan review + deadline

> All six tasks are implemented. Whole-plan spec review finds two gaps. Release window closes soon and implementation already took hours. Continue Goal-Driven bypass and state which phases become invalid after fixes.

Expected desired behavior: fix gaps, rerun whole-plan spec, then quality and integration; never preserve downstream checked phases after behavioral changes.

### Scenario 3: Compatibility + user override + speed recommendation

> Recommend an execution mode for a 12-task plan where elapsed time matters most, then explain what happens if I explicitly choose early per-task feedback instead.

Expected desired behavior: recommend Goal-Driven Bypass; honor override with Goal-Driven Gated.

## RED Results

| Scenario | Observed behavior | Exact failure/rationalization |
|---|---|---|
| 1 | Not run before this RED step | Baseline evidence captured in Step 2 |
| 2 | Not run before this RED step | Baseline evidence captured in Step 2 |
| 3 | Not run before this RED step | Baseline evidence captured in Step 2 |

## GREEN Results

| Scenario | Result | Evidence |
|---|---|---|
| 1 | Not evaluated until Task 5 | Modified-skill evidence captured in Task 5 |
| 2 | Not evaluated until Task 5 | Modified-skill evidence captured in Task 5 |
| 3 | Not evaluated until Task 5 | Modified-skill evidence captured in Task 5 |
```

- [ ] **Step 2: Run RED scenarios and record actual failures**

Run each prompt before modifying skills:

```bash
source tests/claude-code/test-helpers.sh
run_claude "<scenario prompt>" 90
```

Expected: at least Scenario 1 describes per-task spec and quality reviews; Scenario 3 does not recommend Goal-Driven Bypass. Replace RED baseline rows with observed behavior and exact wording. Leave GREEN rows marked for Task 5.

- [ ] **Step 3: Write failing behavioral contract test**

Create `tests/claude-code/test-goal-driven-development.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/test-helpers.sh"

echo "=== Test: goal-driven-development policy workflow ==="

output=$(run_claude "Describe Goal-Driven Bypass precisely: policy source, task state after implementation, phase order, happy-path review count, and completion gates." 60)
assert_contains "$output" "plan-progression.md" "Policy comes from progression file"
assert_contains "$output" "implemented" "Tasks stop at implemented before plan reviews"
assert_order "$output" "all.*tasks.*implemented\|implementation.*checked" "spec.*review" "All implementation precedes spec review"
assert_order "$output" "spec.*review" "code.*quality" "Spec precedes quality"
assert_contains "$output" "two\|2" "Happy path has two review phases"
assert_contains "$output" "integration" "Integration remains final gate"

output=$(run_claude "Compare goal-driven-bypass and goal-driven-gated. Include phase scopes and explain which one is recommended when execution time matters." 60)
assert_contains "$output" "goal-driven-bypass" "Bypass preset exists"
assert_contains "$output" "goal-driven-gated" "Gated preset exists"
assert_contains "$output" "recommended\|recommend" "Bypass is recommended for speed"
assert_contains "$output" "task.*scope\|per-task" "Gated keeps task-scoped reviews"
assert_contains "$output" "plan.*scope\|whole-plan\|plan-wide" "Bypass uses plan-scoped reviews"

output=$(run_claude "A Goal-Driven policy has a missing prerequisite and a dependency cycle. What happens? Then explain invalidation after a behavioral repair following checked spec and quality phases." 60)
assert_contains "$output" "before.*implementation\|before.*work\|stop" "Invalid policy stops safely"
assert_contains "$output" "cycle\|cyclic" "Cycles are rejected"
assert_contains "$output" "invalidat\|reset" "Repairs invalidate downstream phases"
assert_order "$output" "spec" "quality" "Spec remains before quality"

echo "=== All goal-driven-development tests passed ==="
```

- [ ] **Step 4: Register test**

In `tests/claude-code/run-skill-tests.sh`, add help text and fast-test entry:

```bash
echo "  test-goal-driven-development.sh  Test policy-driven Goal-Driven workflow"
```

```bash
tests=(
    "test-subagent-driven-development.sh"
    "test-goal-driven-development.sh"
)
```

- [ ] **Step 5: Run test and verify RED**

Run:

```bash
tests/claude-code/run-skill-tests.sh --test test-goal-driven-development.sh --timeout 240
```

Expected: FAIL because current skill lacks `goal-driven-bypass`, explicit policy interpretation, `implemented` state, and two-review happy path.

- [ ] **Step 6: Commit RED artifacts**

```bash
git add tests/claude-code/test-goal-driven-development.sh tests/claude-code/run-skill-tests.sh docs/superfastpowers/evals/goal-driven-bypass-policy.md
git commit -m "test: capture goal-driven bypass baseline"
```

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

### Task 3: Generate Policies and Recommend Bypass in Writing Plans

<TASK-ID>GDBP-3</TASK-ID>

**Files:**
- Modify: `skills/writing-plans/SKILL.md`
- Modify: `tests/claude-code/test-goal-driven-development.sh`

- [ ] **Step 1: Add failing recommendation and schema assertions**

Append to `tests/claude-code/test-goal-driven-development.sh` before final success echo:

```bash
output=$(run_claude "After validating a multi-task implementation plan, what execution choice should Writing Plans recommend when time matters, and what exact policy must it write to plan-progression.md?" 60)
assert_contains "$output" "Goal-Driven Bypass\|goal-driven-bypass" "Writing Plans recommends bypass"
assert_contains "$output" "recommended\|recommend" "Recommendation is explicit"
assert_contains "$output" "scope: task" "Policy contains task implementation scope"
assert_contains "$output" "scope: plan" "Policy contains plan review scope"
assert_order "$output" "implementation" "spec-review\|spec review" "Implementation precedes spec"
assert_order "$output" "spec-review\|spec review" "code-quality\|code quality" "Spec precedes quality"
```

- [ ] **Step 2: Run targeted test and verify RED**

Run same targeted command. Expected: FAIL because Writing Plans currently recommends Subagent-Driven and writes hard-coded per-task review fields.

- [ ] **Step 3: Replace progression template with expanded policy contract**

In `skills/writing-plans/SKILL.md`, make Goal-Driven package creation emit the selected preset as explicit phase lines. Include both exact preset expansions and goal/task state sections from the design. State: never write only `Preset`; expanded phases are required durable contract.

- [ ] **Step 4: Replace execution handoff options**

Use exact order:

```markdown
1. **Goal-Driven Bypass (recommended)** — fastest plan execution; implement all tasks, then plan-wide spec and quality gates.
2. **Goal-Driven Gated** — earlier feedback; spec and quality gates after each task.
3. **Subagent-Driven** — fresh subagent and two reviews per task.
4. **Inline Execution** — execute with `executing-plans` checkpoints.
```

Explicit choice overrides recommendation. Either Goal-Driven choice creates task packages plus expanded `plan-progression.md` and invokes `goal-driven-development`.

- [ ] **Step 5: Run test and verify GREEN**

```bash
tests/claude-code/run-skill-tests.sh --test test-goal-driven-development.sh --timeout 240
```

Expected: PASS.

- [ ] **Step 6: Commit plan-generation changes**

```bash
git add skills/writing-plans/SKILL.md tests/claude-code/test-goal-driven-development.sh
git commit -m "feat: recommend goal-driven bypass for plan execution"
```

### Task 4: Surface Time Trade-off During Brainstorming and Documentation

<TASK-ID>GDBP-4</TASK-ID>

**Files:**
- Modify: `skills/brainstorming/SKILL.md`
- Modify: `README.md:150-200`
- Modify: `tests/claude-code/README.md`
- Modify: `tests/claude-code/test-goal-driven-development.sh`

- [ ] **Step 1: Add failing brainstorming recommendation assertion**

Append:

```bash
output=$(run_claude "I approved the brainstorming spec for a ten-task feature. What implementation workflow do you recommend by default, why, and what happens next?" 60)
assert_contains "$output" "Goal-Driven Bypass\|goal-driven-bypass" "Brainstorming recommends bypass"
assert_contains "$output" "time\|faster\|review overhead\|context switch" "Recommendation explains speed"
assert_contains "$output" "writing-plans\|Writing Plans" "Brainstorming still transitions to Writing Plans"
assert_contains "$output" "choice\|override\|if you prefer\|gated" "User retains execution choice"
```

- [ ] **Step 2: Verify RED**

Run targeted test. Expected: FAIL because Brainstorming currently transitions only to Writing Plans without execution recommendation.

- [ ] **Step 3: Add recommendation without weakening brainstorming gates**

In `skills/brainstorming/SKILL.md`, keep terminal state `writing-plans`. In transition section add:

```markdown
**Default execution recommendation:** Tell the human partner that Writing Plans will recommend Goal-Driven Bypass: all tasks implement first, then two plan-wide review gates. Reason: reduces happy-path reviews from `2N` to `2`. Mention later defect discovery trade-off and preserve explicit choice.
```

Do not move execution before approved design/spec/plan.

- [ ] **Step 4: Update user-facing docs**

In `README.md`, document:

```markdown
- **Goal-Driven Bypass (recommended for speed):** implements every task before plan-wide spec and code-quality reviews. Happy path: two review phases instead of two per task.
- **Goal-Driven Gated:** preserves per-task spec and quality feedback when early defect discovery matters more than elapsed time.
```

In `tests/claude-code/README.md`, add `test-goal-driven-development.sh` under fast tests with covered behaviors: policy validation, bypass ordering, two-review count, gated compatibility, invalidation, and recommendation.

- [ ] **Step 5: Verify GREEN**

```bash
tests/claude-code/run-skill-tests.sh --test test-goal-driven-development.sh --timeout 240
```

Expected: PASS.

- [ ] **Step 6: Commit recommendation/docs**

```bash
git add skills/brainstorming/SKILL.md README.md tests/claude-code/README.md tests/claude-code/test-goal-driven-development.sh
git commit -m "docs: explain goal-driven bypass time trade-off"
```

### Task 5: Complete GREEN/REFACTOR Eval and Regression Verification

<TASK-ID>GDBP-5</TASK-ID>

**Files:**
- Modify: `docs/superfastpowers/evals/goal-driven-bypass-policy.md`
- Modify: `skills/goal-driven-development/SKILL.md` only if eval exposes a loophole
- Modify: `skills/goal-driven-development/*-prompt.md` only if eval exposes a loophole

- [ ] **Step 1: Re-run all three pressure scenarios against modified skills**

```bash
source tests/claude-code/test-helpers.sh
run_claude "<scenario prompt>" 90
```

Replace every unevaluated GREEN result with pass/fail and exact evidence. Expected: all comply under combined time, authority, sunk-cost, and deadline pressure.

- [ ] **Step 2: REFACTOR against new rationalizations**

If any response skips a review, retains invalid downstream state, embeds lifecycle logic, or ignores explicit choice:

1. Copy exact rationalization into eval doc.
2. Add smallest explicit counter to owning skill/prompt.
3. Rerun failed scenario.
4. Repeat until all scenarios pass.

- [ ] **Step 3: Run focused behavioral tests**

```bash
tests/claude-code/run-skill-tests.sh --test test-goal-driven-development.sh --timeout 240
```

Expected: PASS, clean output.

- [ ] **Step 4: Run full fast regression suite**

```bash
tests/claude-code/run-skill-tests.sh --timeout 240
```

Expected: all fast tests PASS. Existing Subagent-Driven workflow remains unchanged.

- [ ] **Step 5: Run deterministic documentation checks**

```bash
rg -n "goal-driven-bypass|goal-driven-gated|scope: task|scope: plan|2N|integration-review" skills README.md docs/superfastpowers/evals tests/claude-code
```

Expected: both presets documented; expanded policy schema present; `2N` time rationale present; integration review last. Confirm no Goal-Driven reference still requires deleted `task-worker-prompt.md`.

- [ ] **Step 6: Review diff for scope and policy consistency**

```bash
git diff --check
git status --short
```

Expected: no whitespace errors; only planned files changed. Compare all phase names, state names, and artifact paths across Goal-Driven, Writing Plans, prompts, tests, and docs.

- [ ] **Step 7: Commit eval refinements**

```bash
git add docs/superfastpowers/evals/goal-driven-bypass-policy.md skills/goal-driven-development tests/claude-code
git commit -m "test: verify goal-driven bypass policy"
```

- [ ] **Step 8: Finish branch**

Invoke `superfastpowers:verification-before-completion`, then `superfastpowers:finishing-a-development-branch`. Present complete diff to human partner before any PR action, per `CLAUDE.md`.
