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

Default path: implement all → verify all → clean code → optional tests → commit once.

- Default `coordination_budget_minutes`: 5. Exceeding it triggers simplification: merge bookkeeping, reuse agents, or continue linearly. It does not trigger more planning.
- Schedule ready work on the critical path first; then fill remaining capacity with other ready branches.
- Reuse same agent for linear successors.
- Do not add new tests during implementation. Existing tests affected by code changes are the exception: update them with the code so the existing suite remains compatible.
- Do not run per-node verification. After implementation, parent verifies complete integrated behavior and runs existing affected tests once.
- Verify scope is locked to plan, specs, changed behavior, and blocking in-scope defects. Record unrelated findings as notes; do not expand execution.
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

## Phase 1: Full Development

1. Read canonical graph and task ownership.
2. Keep a linear one-successor chain with same agent.
3. At fork, dispatch independent branches concurrently.
   - Select each branch model from Model Routing using whole-branch complexity.
4. Branch worker may continue through its linear chain and nested forks.
5. Branch worker stops before matching join.
6. Parent waits for all predecessors, integrates their changed paths, executes join without inserting a review/test gate.
7. Failed branch blocks join; healthy siblings may finish; retry failed branch only.
8. Parent owns aggregate commit unless explicitly delegated.
9. Finish every implementation node before starting full verification.

Do not add per-node review agents, progression phases, review artifacts, multi-session evals, or full-workflow restarts by default.

During development:

- Implement plan behavior completely.
- Do not add new tests.
- Existing tests affected by code changes are the exception: update them during the owning implementation branch when old expectations/API usage would fail.
- Record changed paths and implementation notes; spec verification happens after full implementation.

## Phase 2: Full Verification

After every implementation node and join completes:

1. Read plan and specs fresh.
2. Compare every delivered behavior with the plan and specs.
3. Inspect combined diff and actual runtime/code paths; never rely only on worker reports.
4. Run existing affected tests, build/type/lint commands, and targeted runtime checks that already exist. Do not create new tests in this phase.
5. Fix missing, incorrect, or extra behavior in one focused repair pass.
6. Recheck only affected requirements and commands.

Verification answers: Was everything developed? Does it follow the plan? Does it fulfill the specs?

## Phase 3: Clean-Code Quality

After spec verification passes, inspect available clean-code skills and select only those relevant to changed languages, architecture, risks, and files. Apply them to the combined diff in one quality pass.

- Prefer project conventions plus relevant clean-code convention/auditor skills.
- Improve naming, structure, duplication, error handling, boundaries, and readability without changing approved behavior.
- Keep scope locked. No unrelated refactors or speculative architecture.
- Recheck affected verified behavior and rerun existing affected tests after quality edits.
- One quality repair pass. More requires concrete failing evidence or explicit human approval.

## Phase 4: Optional New Tests

Ask the human whether to add new tests after development, verification, and clean-code quality finish.

- If yes: add tests for delivered behavior, run them plus existing affected tests, fix failures.
- If no: do not create new tests. Report verification evidence and existing-test results.
- Never imply lack of new tests means lack of verification; specification verification remains mandatory.

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
Verification: pending until full verification | command → result
Blocker: none | ...
Timing: implementation minutes | coordination minutes
```

No separate review or handoff files required.

## Repair

Focused defect → repair affected implementation, rerun only relevant phase checks, continue. Never restart completed independent branches without evidence.

## Prompts

- `./branch-worker-prompt.md`
- `./continuation-prompt.md`

## Completion

Require valid graph, every implementation node complete, full plan/spec verification passed, clean-code pass complete, existing affected tests green, optional-test choice recorded, actual combined diff reviewed once.
