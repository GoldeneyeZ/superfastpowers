# Graph Continuation Prompt

```text
Graph: [path]
Task package: [path]
Join: [ID]
Repository: [path]

Reconstruct state from graph plus recorded node status. Verify every predecessor completed and its focused tests passed. If one failed, retry only that branch. Execute join, run focused integration tests, create aggregate commit only if authorized, then continue linear flow.

Return: completed nodes, join result, changed paths, verification, blockers, next node.
```
