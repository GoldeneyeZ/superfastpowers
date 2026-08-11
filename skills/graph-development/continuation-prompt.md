# Graph Continuation Prompt

```text
Graph: [path]
Task package: [path]
Join: [ID]
Repository: [path]
Coordination budget: [minutes remaining]
Selected model: [preserve branch model]
Reasoning effort: medium

Reconstruct state from graph plus recorded node status. Schedule critical-path ready work first. Verify every predecessor completed and its focused tests passed. If one failed, retry only that branch. Execute join, run focused integration tests, create aggregate commit only if authorized and useful as a checkpoint, then continue linear flow. Simplify or continue linearly when coordination budget is exhausted.

Return: completed nodes, join result, changed paths, verification, blockers, next node, Timing (implementation minutes and coordination minutes).
```
