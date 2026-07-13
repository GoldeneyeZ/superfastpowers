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
