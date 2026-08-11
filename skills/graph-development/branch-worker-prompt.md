# Graph Branch Worker Prompt

```text
Branch: [node IDs through matching join]
Graph: [path]
Tasks: [task paths]
Owned writes: [paths]
Repository: [path]
Coordination budget: [minutes remaining]

Check status and diffs for owned paths. Stop on conflicting edits. Implement current node with focused tests. Continue through linear successors; dispatch nested independent branches when capacity allows. Stop before matching join. Never stage or commit unless explicitly authorized.

Return: status, completed nodes, changed paths, verification, blockers, matching join ID, Timing (implementation minutes and coordination minutes).
```
