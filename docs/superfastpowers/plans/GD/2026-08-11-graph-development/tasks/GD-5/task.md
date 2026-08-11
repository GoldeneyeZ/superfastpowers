### Task 5: Implement Graph Development Skill

<TASK-ID>GD-5</TASK-ID>

**Files:**
- Create: `skills/graph-development/SKILL.md`
- Create: `skills/graph-development/branch-worker-prompt.md`
- Create: `skills/graph-development/continuation-prompt.md`
- Modify: `tests/claude-code/test-graph-development-static.sh`
- Test: `tests/claude-code/test-graph-development-static.sh`
- Test: `tests/claude-code/test-graph-development.sh`

- [ ] **Step 1: Initialize repository-native skill scaffold**

Run system `skill-creator/scripts/init_skill.py` with name `graph-development`, output path `skills`, and `scripts` resource. Preserve generated `SKILL.md` and scripts directory. Remove generated per-skill `agents/` metadata because core repository discovers `skills/*/SKILL.md` and no existing core skill carries per-skill UI metadata.

Expected tree:

```text
skills/graph-development/SKILL.md
skills/graph-development/scripts/validate_graph.py
```

Do not overwrite validator from GD-2. If initializer refuses existing directory, scaffold in `mktemp -d`, copy only missing `SKILL.md`, then remove exact temporary directory.

- [ ] **Step 2: Write branch worker prompt**

Inputs: branch flow, matching join, task/context paths, owned writes, graph path, review mode, repository path.

Contract:

1. inspect status, unstaged diff, staged diff;
2. stop on dirty owned paths;
3. implement current node with TDD;
4. update Graph State evidence;
5. apply gated reviews when configured;
6. continue only through one-successor/one-predecessor nodes;
7. recursively dispatch nested forks;
8. stop before matching join;
9. never stage or commit;
10. return exact status, completed nodes, changed paths, verification, blockers, join ID.

- [ ] **Step 3: Write continuation prompt**

Require reconstruction from canonical graph, `plan-progression.md`, join context, and predecessor contexts. Reject conversation-memory-only state. Run join only when every predecessor has verified required gates. Retry only failed branches, execute join, verify integration, create path-limited aggregate commit, update contexts, resume linear flow.

- [ ] **Step 4: Write concise SKILL.md**

```yaml
---
name: graph-development
description: Use when executing packaged implementation plans containing validated structured task graphs with independent parallel branches.
---
```

Body sections: Overview, Entry Gate, Graph/Context Contracts, Recursive Algorithm, Capacity/Continuation, Review Modes, Git Safety, Failure Recovery, Prompt Templates, Quick Reference, Common Mistakes, Red Flags, Integration.

Keep body under 500 lines. Require `test-driven-development`, `requesting-code-review`, and `verification-before-completion` by skill name; do not duplicate them.

- [ ] **Step 5: Run GREEN tests**

```bash
bash tests/claude-code/test-graph-development-static.sh
ORACLE_SELF_TEST=1 bash tests/claude-code/test-graph-development.sh
```

Expected: all static contracts and matcher self-tests pass.

If behavioral harness available, run GREEN and pressure scenarios at least three times each. Expected: all lifecycle, join, capacity, failure, Git ownership assertions pass.

- [ ] **Step 6: Validate skill structure**

Run system `skill-creator/scripts/quick_validate.py skills/graph-development`.

Expected: valid name/frontmatter/description; exit 0.

- [ ] **Step 7: Commit skill**

```bash
git add skills/graph-development/SKILL.md skills/graph-development/branch-worker-prompt.md skills/graph-development/continuation-prompt.md tests/claude-code/test-graph-development-static.sh
git commit --only -m "[GD-5] feat: execute structured task graphs" -- skills/graph-development/SKILL.md skills/graph-development/branch-worker-prompt.md skills/graph-development/continuation-prompt.md tests/claude-code/test-graph-development-static.sh
```
