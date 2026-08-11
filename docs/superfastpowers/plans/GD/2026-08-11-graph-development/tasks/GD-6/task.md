### Task 6: Integrate Discovery and Test Runner

<TASK-ID>GD-6</TASK-ID>

**Files:**
- Modify: `README.md`
- Modify: `tests/claude-code/run-skill-tests.sh`
- Test: `tests/claude-code/run-skill-tests.sh`
- Test: `tests/codex-plugin-sync/test-sync-to-codex-plugin.sh`

- [ ] **Step 1: Register tests**

Add `test-graph-development-static.sh` to fast tests. Add `test-graph-development.sh` to behavioral tests. Preserve skip behavior only for missing optional behavioral harness; static test must never silently skip.

- [ ] **Step 2: Update README workflow**

Add:

```text
graph-development — Executes validated structured task graphs: linear agent continuity, parallel branches, durable parent continuations, parent-owned joins and commits.
```

Document `writing-plans` output modes `json`, `markdown`, `both`; default `both`. Do not present Graph Development as default over Goal-Driven Bypass.

- [ ] **Step 3: Run integration checks**

```bash
bash tests/claude-code/test-graph-development-static.sh
ORACLE_SELF_TEST=1 bash tests/claude-code/test-graph-development.sh
bash tests/codex-plugin-sync/test-sync-to-codex-plugin.sh
git diff --check
```

Expected: all commands exit 0.

- [ ] **Step 4: Commit discovery integration**

```bash
git add README.md tests/claude-code/run-skill-tests.sh tests/claude-code/test-graph-development.sh
git commit --only -m "[GD-6] docs: expose graph development workflow" -- README.md tests/claude-code/run-skill-tests.sh tests/claude-code/test-graph-development.sh
```
