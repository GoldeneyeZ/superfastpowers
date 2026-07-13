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
1. **Goal-Driven Bypass (recommended)** â€” fastest plan execution; implement all tasks, then plan-wide spec and quality gates.
2. **Goal-Driven Gated** â€” earlier feedback; spec and quality gates after each task.
3. **Subagent-Driven** â€” fresh subagent and two reviews per task.
4. **Inline Execution** â€” execute with `executing-plans` checkpoints.
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
