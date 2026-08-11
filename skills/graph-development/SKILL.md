---
name: graph-development
description: Use when executing a validated task graph containing independent parallel branches.
---

# Graph Development

## Goal

Exploit real parallelism without turning every node into coordination ceremony.

## Entry

Use only when plan contains Graph Development artifacts. Validate once before execution:

```bash
python3 skills/graph-development/scripts/validate_graph.py <package-root>
```

Invalid graph → stop and repair plan. Valid graph → execute.

Before choosing Graph Development, confirm expected parallel savings exceed coordination cost. Otherwise execute the plan linearly.

## Speed Contract

Graph Development must never create more coordination steps than implementation nodes.

Default path: validate once → execute graph → review once → verify once → commit once.

- Default `coordination_budget_minutes`: 5. Exceeding it triggers simplification: merge bookkeeping, reuse agents, or continue linearly. It does not trigger more planning.
- Schedule ready work on the critical path first; then fill remaining capacity with other ready branches.
- Reuse same agent for linear successors.
- Node workers run focused tests. Parent runs the full fast suite once after integration.
- Review scope is locked to requested work and blocking in-scope defects. Record unrelated findings as notes; do not expand execution.
- One repair pass is default. Another pass requires a failing test or explicit human approval.
- Commit at joins only when a durable checkpoint is useful; otherwise commit once after final verification.
- Track implementation time and coordination time. Warn and simplify when coordination time dominates.

## Model Routing

Every spawned branch worker uses `reasoning_effort: medium`. Select cheapest model that reliably fits whole branch:

| Model | Use for |
|---|---|
| `gpt-5.6-sol` | Ambiguous architecture, security/high-risk work, hard debugging, complex integration or synthesis |
| `gpt-5.6-terra` | Default normal implementation, cross-file work, exploration, review, moderate edge cases |
| `gpt-5.6-luna` | Narrow deterministic, read-heavy, repetitive, documentation, or mechanical work |
| `gpt-5.3-codex-spark` | Well-defined small/medium coding with clear acceptance criteria and bounded files |

Explicit human model choice wins. Select once per branch, not once per node; preserve model across linear successors and continuation. If selected model is unavailable, use `gpt-5.6-terra` at medium and report fallback. Escalate only after evidence current model cannot finish reliably: Luna/Spark → Terra → Sol.

## Execution

1. Read canonical graph and task ownership.
2. Keep a linear one-successor chain with same agent.
3. At fork, dispatch independent branches concurrently.
   - Select each branch model from Model Routing using whole-branch complexity.
4. Branch worker may continue through its linear chain and nested forks.
5. Branch worker stops before matching join.
6. Parent waits for all predecessors, verifies their focused tests, executes join.
7. Failed branch blocks join; healthy siblings may finish; retry failed branch only.
8. Parent owns aggregate commit unless explicitly delegated.
9. After graph completes, run one focused plan-wide review and final test batch.

Do not add per-node review agents, progression phases, review artifacts, multi-session evals, or full-workflow restarts by default.

## Ownership

- Parallel branches must have disjoint repository writes.
- Shared generated/cache/build outputs do not count as ownership; clean them before verification.
- Branch workers never stage or commit unless parent explicitly changes Git ownership.
- Dirty owned paths before dispatch are a blocker.

## Capacity

When agent slots are full at nested fork, save minimal durable state, release parent capacity if supported, resume from graph plus task status. Never keep an idle parent consuming the slot needed by its branch. Conversation memory is optional context, never sole state.

## Minimal State

Record only when needed for continuation:

```text
Node: <ID>
Status: pending | running | complete | blocked
Changed paths: ...
Verification: command → result
Blocker: none | ...
Timing: implementation minutes | coordination minutes
```

No separate review or handoff files required.

## Repair

Focused defect → mark affected node pending, repair it, rerun affected validation/tests, continue. Invalidate only nodes whose inputs changed. Never restart completed independent branches without evidence.

## Prompts

- `./branch-worker-prompt.md`
- `./continuation-prompt.md`

## Completion

Require valid graph, every node complete, joins verified, final fast test batch green, actual diff reviewed once.
