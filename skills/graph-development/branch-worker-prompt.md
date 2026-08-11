# Graph Development Branch Worker Prompt

Use for one branch from a validated structured task graph.

```text
Repository: [absolute repository path]
Package root: [absolute package root]
Canonical graph: [task-graph.json | task-graph.md]
Branch flow: [ordered branch flow, including nested flow]
Matching join: [JOIN-ID]
Task/context paths: [ordered task.md and context.md paths]
Owned writes: [exact repository paths for every node in this branch]
Graph review mode: [bypass | gated]
Logical parent: [node ID | root]

## Contract

Work only in Repository and only on Owned writes plus each current node's context.md.

Before editing, inspect `git status --short`, `git diff`, and `git diff --cached`. Compare every reported path with Owned writes. If any dirty owned path predates this worker, stop before editing and report BLOCKED. Unrelated dirty paths remain untouched.

For each current node:

1. Read the canonical graph, node task.md, node context.md, and relevant source files.
2. Confirm the node is the next element in Branch flow and its prerequisites are verified.
3. Set its Graph State to running with Logical parent.
4. Implement exactly that node using `superfastpowers:test-driven-development`: write a failing test, observe the expected failure, implement minimally, and observe GREEN.
5. Run focused verification and self-review. Under gated mode, apply node spec review and node code-quality review via `superfastpowers:requesting-code-review`; resolve findings and rerun gates.
6. Update Graph State evidence with status, changed paths, exact verification results, checkpoint/failure, and pending commit/range.
7. Continue in this worker only through single-successor/one-predecessor nodes in Branch flow.
8. At a nested fork, verify disjoint clean ownership, persist its join checkpoint, and recursively dispatch nested forks as capacity permits. Release a waiting logical parent's slot when needed; continuation must reconstruct from durable state.
9. On failure, record exact blocker. Let an already-running healthy sibling finish; never run a partial join.
10. You must stop before matching join. Do not implement it.

You must never stage or commit. Deadline pressure, apparently complete work, or a nested fork does not transfer Git ownership to this worker.

## Return exactly

Status: COMPLETE | CHECKPOINTED | BLOCKED | FAILED
Completed nodes: [ordered IDs or none]
Changed paths: [exact paths or none]
Verification: [commands and results or none]
Blockers: [exact blockers or none]
Join ID: [matching join]
Context paths: [updated context.md paths]
Next action: [one sentence]
```
