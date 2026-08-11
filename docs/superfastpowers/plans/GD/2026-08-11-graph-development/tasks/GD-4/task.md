### Task 4: Establish Behavioral RED Baseline

<TASK-ID>GD-4</TASK-ID>

**Files:**
- Create: `tests/claude-code/test-graph-development.sh`
- Modify: `tests/claude-code/test-graph-development-static.sh`
- Test: `tests/claude-code/test-graph-development.sh`

- [ ] **Step 1: Add skill and prompt static assertions**

Assert future files exist:

```text
skills/graph-development/SKILL.md
skills/graph-development/branch-worker-prompt.md
skills/graph-development/continuation-prompt.md
```

Require behavior strings covering linear continuation, stop-before-join, no branch staging/commits, parent checkpoint/release, durable continuation reconstruction, strict predecessor verification, failed-branch join blocking, sibling completion, and explicit-request-only worktrees.

- [ ] **Step 2: Create behavioral pressure runner**

Use `test-helpers.sh`. Add five prompts and assertions:

1. Linear chain: same agent continues; reject spawning per node.
2. Two-way fork: both branches dispatched; parent does not execute join early.
3. Nested fork with all slots occupied: checkpoint/release/continuation; reject waiting-process dependency.
4. One failed branch: healthy sibling completion, strict join block, targeted retry.
5. Deadline pressure: branch workers refuse Git staging/commit; parent retains commit ownership.

Add `ORACLE_SELF_TEST=1` with one positive and one adversarial negative string for every matcher.

- [ ] **Step 3: Capture RED evidence**

Run static test. Expected: FAIL because skill and prompt files do not exist.

If Claude CLI exists, run behavioral prompts without new skill. Otherwise dispatch three isolated Codex agents with only scenario and current skill tree. Expected baseline failures: node-per-agent dispatch, central-root scheduling, live-parent waiting, or worker commits.

- [ ] **Step 4: Commit RED harness**

```bash
git add tests/claude-code/test-graph-development.sh tests/claude-code/test-graph-development-static.sh
git commit --only -m "[GD-4] test: capture graph execution baseline" -- tests/claude-code/test-graph-development.sh tests/claude-code/test-graph-development-static.sh
```
