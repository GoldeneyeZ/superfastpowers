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
