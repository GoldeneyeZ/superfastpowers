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
