---
name: graph-development
description: Use when executing packaged implementation plans containing validated structured task graphs with independent parallel branches.
---

# Graph Development

## Overview

Execute validated fork/join task graphs while preserving task-package context, agent continuity on linear chains, isolated branch writes, and parent-owned joins.

**Core principle:** topology determines concurrency; durable files determine truth.

## Entry Gate

Before implementation:

1. Read the plan, `plan-progression.md`, every node's `task.md` and `context.md`, and the canonical graph.
2. Confirm `Graph format: both | markdown | json` and `Graph review mode: bypass | gated` resolve to one value each.
3. Run:

   ```bash
   python3 skills/graph-development/scripts/validate_graph.py <package-root>
   ```

4. Inspect `git status --short`, `git diff`, and `git diff --cached`.
5. Stop if validation fails, graph-owned paths are dirty, topology changed after execution began without downstream invalidation, or available agent capacity cannot be determined.

Never infer or repair invalid graph topology during execution. Return to `writing-plans` for graph changes, revalidate, and explicitly invalidate affected downstream state.

## Graph/Context Contracts

- One node maps to one `tasks/<TASK-ID>/` package.
- JSON is canonical in `both` and `json` modes. Markdown node/fork tables are canonical only in `markdown` mode. Mermaid is never authoritative.
- Flow is structured, nested `sequence`/`parallel` with one matching join per fork; it is not an arbitrary DAG.
- Concurrent branch write sets are exact, non-empty, and disjoint.
- Topology is immutable during a run.

Before first dispatch, root writes package-level `graph-state.json` with exactly
`version: 1`, `started: true`, the validator's current `topology` snapshot, and
an empty `invalidated` node-ID list. Root alone updates this preflight file. If
topology changes, list every affected node in `invalidated`, then reset every affected downstream context to `pending` before validation. After the
changed graph is accepted, replace the snapshot and clear `invalidated` before
dispatch. Node runtime evidence remains distributed across contexts.

Each node context carries durable Graph State:

```text
Graph status: pending | running | implemented | blocked | reviewed | complete
Logical parent: <node ID or root>
Changed paths: <paths or none>
Verification: <commands and results or none>
Checkpoint: <continuation summary or none>
Failure: <exact blocker or none>
Commit/range: <SHA/range or pending>
```

Update the node context after each implementation, review, failure, or completion transition. Context is a map to evidence; inspect actual files and diffs before trusting it.

## Recursive Algorithm

1. Execute the entry node using TDD and focused verification.
2. If the current node has exactly one successor and that successor has exactly one predecessor, keep the same agent through that linear chain.
3. At a fork, recheck branch write disjointness and owned-path cleanliness.
4. Write branch IDs, matching join, completed predecessors, blockers, and next action into the join context checkpoint.
5. Dispatch one branch worker per branch as capacity permits; queue excess branches. Use [branch-worker-prompt.md](branch-worker-prompt.md).
6. Each worker follows its branch, recursively handles nested forks, and stops before its matching join.
7. Let healthy sibling branches finish after another branch fails. Keep the join blocked.
8. Retry or repair only failed branches. Preserve verified sibling evidence.
9. Run a join only after every predecessor has verified all gates required by the selected review mode.
10. Resume the logical parent with [continuation-prompt.md](continuation-prompt.md), execute and verify the join, then create a path-limited aggregate commit.
11. Resume linear execution after the join. At graph completion, root verifies and commits trailing graph-owned work.

Never execute a partial or early join.

## Capacity/Continuation

A waiting live parent can consume the slot needed by a nested fork. Parent identity is logical, not tied to one process.

Before waiting when capacity is constrained, the parent must checkpoint durable state in the matching join context, return a checkpointed status, and release its slot. Start a continuation agent after branch state changes. The continuation reconstructs from canonical graph and contexts; retained conversation is optional, never required.

Prefer same-agent continuation only when it cannot starve runnable branches.

## Review Modes

Read mode from `plan-progression.md`.

| Mode | Node gate | After graph implementation |
|---|---|---|
| `bypass` | TDD, focused verification, self-review | plan-wide spec review, plan-wide code-quality review, final integration review |
| `gated` | TDD, node spec review, node code-quality review | final plan integration review |

**REQUIRED SUB-SKILL:** Use `superfastpowers:requesting-code-review` for configured reviews. A failed review reopens implementation, invalidates dependent state, and reruns the required gates before successors or joins continue.

Bypass defers reviews; it never removes them.

### Review Failure Handoff

Review failure must leave a durable repair brief before implementation resumes:

- Node-scoped failure: `tasks/<TASK-ID>/implementer-handoff.md`.
- Plan-scoped failure: `<package-root>/implementer-handoff.md`.

The reviewer writes the failed review artifact and handoff first. The handoff records the source review and reviewed range, then these sections:

```markdown
## Findings
[each finding, severity, evidence, and file:line when available]

## Repair Scope
[exact behavior and owned paths the implementer may change]

## Re-review Acceptance
[observable criteria and exact verification required]

## Invalidation and Gate Reruns
[statuses/evidence invalidated and ordered gates to rerun]
```

After writing the handoff, reopen the affected node or plan implementation and block every successor, join, and later review. Dispatch repair with the handoff path; conversation summaries never substitute for it. The repair worker changes only listed scope, uses TDD, updates context with paths plus commit/range, resets the failed review to unchecked, and reruns graph validation when ownership could change. Re-run the failed gate, then every invalidated downstream gate. Preserve the handoff and prior review history until re-review records acceptance.

Behavioral/spec findings invalidate spec, quality, integration, and dependent downstream node evidence. Quality-only findings invalidate quality and integration. Uncertain scope uses behavioral/spec invalidation. A plan-scoped failure blocks later plan gates; a node-scoped failure blocks that node's successors and matching joins.

## Git Safety

- Use the current checkout unless the human makes an explicit request for another workspace.
- Never auto-create or suggest a Git worktree.
- Inspect status plus unstaged and staged diffs before dispatch and before committing.
- Existing changes on a node-owned path block that node.
- Branch workers never stage or commit.
- Only the logical parent creates aggregate commits at joins.
- Stage only graph-owned paths and use a path-limited commit so unrelated staged changes remain excluded.
- Join integration paths must be explicitly owned by the join node, not a child branch.

## Failure Recovery

When a branch fails:

1. Record exact failure and verification evidence in that branch context.
2. Allow each healthy sibling to complete and persist evidence.
3. Keep the matching join blocked.
4. Repair or retry only failed branches.
5. Invalidate only dependent downstream state plus any review evidence affected by the repair.
6. Re-run graph validation if ownership or topology could have changed.
7. Resume the join only after all predecessor gates are verified again.

Stop for ownership overlap, dirty owned paths, malformed durable state, topology ambiguity, exhausted repair options, or an external blocker. Never guess.

## Prompt Templates

- [branch-worker-prompt.md](branch-worker-prompt.md) — execute one branch through linear successors and nested forks; stop before its matching join.
- [continuation-prompt.md](continuation-prompt.md) — reconstruct a logical parent, gate and execute a join, commit owned integration, then resume.

Fill every input. Do not dispatch a prompt with placeholders or conversation-only context.

## Quick Reference

| Situation | Action |
|---|---|
| Invalid graph | Stop; return to planning and revalidate |
| One successor/one predecessor | Same agent continues |
| Fork | Check ownership, checkpoint, dispatch branches |
| Insufficient capacity | Checkpoint parent, release its slot, continue later |
| Worker reaches matching join | Stop and report; do not execute join |
| One branch fails | Healthy siblings finish; join blocks; retry failed branch only |
| All predecessor gates verified | Continuation executes join and parent commits |
| Dirty owned path | Stop before dispatch |

## Common Mistakes

| Mistake | Correction |
|---|---|
| Spawn one agent per node | Preserve agent continuity across linear chains |
| Treat Mermaid as execution data | Read the canonical JSON or Markdown tables |
| Keep waiting parents live | Checkpoint and release capacity |
| Stop all siblings after one failure | Preserve healthy sibling progress |
| Let a worker commit its branch | Parent owns the path-limited aggregate commit |
| Trust context summaries | Inspect graph, files, diffs, and verification evidence |
| Run join when work merely exists | Require every predecessor's configured gates |

## Red Flags

Stop immediately if you are about to:

- Skip deterministic validation.
- Infer topology from task numbering or prose.
- Dispatch overlapping or dirty write ownership.
- Spawn every linear node separately.
- Execute a matching join from a branch worker.
- Run a join before every predecessor gate verifies.
- Stage or commit from a branch worker.
- Depend on conversation memory for continuation.
- Keep a parent waiting when its slot blocks runnable work.
- Create or suggest a worktree without an explicit request.

## Integration

**REQUIRED SUB-SKILL:** Use `superfastpowers:test-driven-development` for every implementation node.

**REQUIRED SUB-SKILL:** Use `superfastpowers:requesting-code-review` according to Graph review mode.

**REQUIRED SUB-SKILL:** Use `superfastpowers:verification-before-completion` before any completion claim or aggregate commit.

`writing-plans` creates and validates graph packages. `goal-driven-development` remains the policy precedent for progression, invalidation, and plan-wide gates. `finishing-a-development-branch` handles the final human handoff.
