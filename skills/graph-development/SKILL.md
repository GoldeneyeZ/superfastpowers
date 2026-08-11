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

## Execution

1. Read canonical graph and task ownership.
2. Keep a linear one-successor chain with same agent.
3. At fork, dispatch independent branches concurrently.
4. Branch worker may continue through its linear chain and nested forks.
5. Branch worker stops before matching join.
6. Parent waits for all predecessors, verifies their focused tests, executes join.
7. Failed branch blocks join; healthy siblings may finish. Retry failed branch only.
8. Parent owns aggregate commit unless explicitly delegated.
9. After graph completes, run one focused plan-wide review and final test batch.

Do not add per-node review agents, progression phases, review artifacts, multi-session evals, or full-workflow restarts by default.

## Ownership

- Parallel branches must have disjoint repository writes.
- Shared generated/cache/build outputs do not count as ownership; clean them before verification.
- Branch workers never stage or commit unless parent explicitly changes Git ownership.
- Dirty owned paths before dispatch are a blocker.

## Capacity

When agent slots are full at nested fork, save minimal durable state, release parent capacity if supported, resume from graph plus task status. Conversation memory is optional context, never sole state.

## Minimal State

Record only when needed for continuation:

```text
Node: <ID>
Status: pending | running | complete | blocked
Changed paths: ...
Verification: command → result
Blocker: none | ...
```

No separate review or handoff files required.

## Repair

Focused defect → mark affected node pending, repair it, rerun affected validation/tests, continue. Invalidate only nodes whose inputs changed. Never restart completed independent branches without evidence.

## Prompts

- `./branch-worker-prompt.md`
- `./continuation-prompt.md`

## Completion

Require valid graph, every node complete, joins verified, final fast test batch green, actual diff reviewed once.
