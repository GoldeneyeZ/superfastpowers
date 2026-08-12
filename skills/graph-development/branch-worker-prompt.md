# Graph Branch Worker Prompt

```text
Branch: [node IDs through matching join]
Graph: [path]
Tasks: [task paths]
Owned writes: [paths]
Repository: [path]
Coordination budget: [minutes remaining]
Selected model: [gpt-5.6-sol | gpt-5.6-terra | gpt-5.6-luna | gpt-5.3-codex-spark]
Reasoning effort: medium

Check status and diffs for owned paths. Stop on conflicting edits. Implement current node completely. Do not add new tests and do not run per-node verification; spec verification happens after full implementation. Existing affected tests are the exception: update existing tests when code changes would make them fail. Continue through linear successors; dispatch nested independent branches when capacity allows. Stop before matching join. Never stage or commit unless explicitly authorized.

Return: status, completed nodes, changed paths, existing tests updated, implementation notes, blockers, matching join ID, Timing (implementation minutes and coordination minutes).
```
