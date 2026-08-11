### Task 3: Extend Writing Plans With Graph Artifacts

<TASK-ID>GD-3</TASK-ID>

**Files:**
- Modify: `skills/writing-plans/SKILL.md`
- Create: `tests/claude-code/test-graph-development-static.sh`
- Test: `tests/claude-code/test-graph-development-static.sh`

- [ ] **Step 1: Write failing static planning assertions**

Create Bash helpers `assert_contains` and `assert_excludes`, then assert `skills/writing-plans/SKILL.md` contains:

```text
Graph Development
Graph format: both | markdown | json
Graph review mode: bypass | gated
one graph node per task package
task-graph.json
task-graph.md
cross-branch write ownership must be disjoint
```

Reject instructions making Mermaid authoritative or requiring YAML.

- [ ] **Step 2: Run RED static test**

```bash
bash tests/claude-code/test-graph-development-static.sh
```

Expected: FAIL on missing Graph Development planning contract.

- [ ] **Step 3: Add Graph Development Output section**

Add after Goal-Driven package generation:

- graph mode is explicit execution choice;
- default artifact format is `both`;
- JSON is canonical when present;
- Markdown tables are canonical only in Markdown-only mode;
- Mermaid is derived only;
- one node maps to one task package;
- tasks become finer only for real parallelism, ownership, or verification value;
- each node declares exact write paths;
- concurrent branches have disjoint write ownership;
- flow uses nested `sequence` and `parallel` with explicit joins;
- planner runs `validate_graph.py` before handoff;
- package generation includes Graph State fields in every `context.md`.

Extend Execution Handoff with:

```text
5. Graph Development — Structured parallel branches with linear agent continuity and parent-owned joins
```

- [ ] **Step 4: Run GREEN static test**

```bash
bash tests/claude-code/test-graph-development-static.sh
```

Expected: all planning assertions pass.

- [ ] **Step 5: Commit planning support**

```bash
git add skills/writing-plans/SKILL.md tests/claude-code/test-graph-development-static.sh
git commit --only -m "[GD-3] feat: plan structured task graphs" -- skills/writing-plans/SKILL.md tests/claude-code/test-graph-development-static.sh
```
