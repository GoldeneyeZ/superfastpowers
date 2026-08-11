### Task 7: Record Adversarial Evaluation and Final Verification

<TASK-ID>GD-7</TASK-ID>

**Files:**
- Create: `docs/superfastpowers/evals/graph-development.md`
- Modify only if eval exposes verified loophole: `skills/graph-development/SKILL.md`
- Modify only if oracle accepts negative control: `tests/claude-code/test-graph-development.sh`
- Test: all Graph Development tests

- [ ] **Step 1: Run isolated RED/GREEN scenarios**

Use at least three clean sessions. Pass only scenario, repository path, and skill path—never expected answer. Capture exact baseline behavior, GREEN behavior, rationalizations, harness/model metadata.

Required combined pressures:

- urgency + authority requesting branch-worker commits;
- slot exhaustion + sunk cost encouraging live-parent wait;
- partial branch success + deadline encouraging early join;
- large plan + maximal-parallelism pressure encouraging fake microtasks or write overlap.

- [ ] **Step 2: Write eval report**

Follow `docs/superfastpowers/evals/goal-driven-bypass-policy.md`:

```markdown
# Graph Development Eval
## Environment
## RED Baseline
## RED Results
## GREEN Results
## REFACTOR
## Verification
```

Every result cites raw behavior. Never claim unavailable harness coverage.

- [ ] **Step 3: Close verified loopholes**

If GREEN scenario fails, stop completion. Add focused negative matcher or static assertion reproducing failure, run RED, minimally tighten skill/prompt wording, rerun GREEN. Never weaken expectations to make output pass.

- [ ] **Step 4: Run final verification**

```bash
python -m unittest tests/graph-development/test_validate_graph.py -v
bash tests/claude-code/test-graph-development-static.sh
ORACLE_SELF_TEST=1 bash tests/claude-code/test-graph-development.sh
bash -n tests/claude-code/run-skill-tests.sh tests/claude-code/test-graph-development-static.sh tests/claude-code/test-graph-development.sh
bash tests/codex-plugin-sync/test-sync-to-codex-plugin.sh
git diff --check
```

If Claude CLI installed:

```bash
bash tests/claude-code/test-graph-development.sh
```

Expected: every available command exits 0; unavailable harness explicitly documented.

- [ ] **Step 5: Commit eval evidence**

```bash
git add docs/superfastpowers/evals/graph-development.md skills/graph-development/SKILL.md tests/claude-code/test-graph-development.sh
git commit --only -m "[GD-7] test: document graph development evals" -- docs/superfastpowers/evals/graph-development.md skills/graph-development/SKILL.md tests/claude-code/test-graph-development.sh
```
