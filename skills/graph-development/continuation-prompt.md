# Graph Development Continuation Prompt

Use to resume a checkpointed logical parent at a matching join.

```text
Repository: [absolute repository path]
Package root: [absolute package root]
Canonical graph: [task-graph.json | task-graph.md]
Policy/progression: [plan-progression.md]
Join: [JOIN-ID and context.md]
Predecessor contexts: [ordered context.md paths]
Graph review mode: [bypass | gated]
Aggregate commit message: [[TASK-ID] subject]

## Reconstruction gate

Reconstruct state from the canonical graph, plan-progression.md, join context, predecessor contexts, repository status, unstaged diff, and staged diff. Retained conversation memory is never authoritative and cannot replace any durable input. Stop with NEEDS_CONTEXT when an input is missing or contradictory.

Verify before join work:

1. Join is the matching join for this fork and has not been reused.
2. Every predecessor has verified required gates for Graph review mode.
3. Reported changed paths match actual diff and declared graph ownership.
4. No predecessor is blocked, running, or missing verification.
5. Unrelated changes and staging are identified and excluded.

If any predecessor failed, keep the join blocked and retry only failed branches. Preserve healthy sibling evidence. Do not rerun verified siblings unless their state was invalidated by the repair.

## Join execution

When every predecessor has verified required gates:

1. Mark Join Graph State running.
2. Implement the join node with `superfastpowers:test-driven-development` using only declared join-owned integration paths.
3. Run focused integration verification and the configured join/review gates.
4. Inspect status, unstaged diff, and staged diff again.
5. Stage only branch and join graph-owned paths. Create a path-limited aggregate commit; preserve unrelated staged changes.
6. Record commit/range, changed paths, verification, and cleared checkpoint/failure in join and predecessor contexts.
7. Update owned progression fields.
8. Resume linear flow after Join in the same logical parent. At another fork, checkpoint and dispatch using the branch prompt.

Use `superfastpowers:verification-before-completion` before the aggregate commit or any completion claim.

## Return exactly

Status: COMPLETE | CHECKPOINTED | BLOCKED | NEEDS_CONTEXT | FAILED
Join ID: [ID]
Verified predecessors: [ordered IDs or none]
Completed nodes: [ordered IDs or none]
Changed paths: [exact paths or none]
Verification: [commands and results]
Commit/range: [SHA/range or none]
Blockers: [exact blockers or none]
Context paths: [updated paths]
Next action: [one sentence]
```
