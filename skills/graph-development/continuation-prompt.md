# Graph Continuation Prompt

```text
Graph: [path]
Task package: [path]
Join: [ID]
Repository: [path]
Coordination budget: [minutes remaining]
Selected model: [preserve branch model]
Reasoning effort: medium

Reconstruct state from graph plus recorded node status. Schedule critical-path ready work first. Confirm every predecessor implementation completed; full verification phase starts only after all implementation nodes finish. If one branch failed implementation, retry only that branch. Execute join without a per-join review/test gate, create aggregate commit only if authorized and useful as a checkpoint, then continue linear flow. Simplify or continue linearly when coordination budget is exhausted.

Return: completed nodes, join result, changed paths, existing tests updated, implementation notes, blockers, next node, Timing (implementation minutes and coordination minutes).
```
