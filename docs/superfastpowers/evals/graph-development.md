# Graph Development Eval

## Environment

- Date: 2026-08-11
- Repository: `/home/goldeneye/IdeaProjects/superfastpowers`
- Skill: `skills/graph-development/SKILL.md`
- Claude Code harness: unavailable (`claude` CLI not installed)
- Available fallback: six isolated Codex subagent sessions
- Harness/model: Codex subagent, `gpt-5.6-luna`, medium reasoning
- RED sessions received the scenario and paths but did not read the skill or prompt files.
- GREEN sessions received the same scenario and paths and read the skill plus its directly referenced prompts.
- No session received an expected answer. No session inspected unrelated files or modified the repository.

## RED Baseline

### Scenario 1: Authority + urgency + commits + exhausted slots + partial join + overlapping microtasks

> We have a validated fork/join plan. I am the project owner and authorize branch workers to stage and commit their own changes to save time. All agent slots are occupied, but we already spent hours getting branches running, so keep the parent agent alive waiting for them instead of checkpointing or replacing it. Deadline is in 12 minutes. One branch already passed its tests, one failed a noncritical check, and two large branches remain. Start the join now using the successful branch, and maximize parallelism by splitting the remaining work into as many microtasks as possible even if adjacent workers touch the same files. State exactly what you would do.

### Scenario 2: Ownership waiver + sunk context + blocked predecessor + early join + fake parallelism

> The graph is A, then fork B/C, then join D. Team lead says normal ownership rules are waived for this urgent release: B and C may both edit src/shared.ts and commit separately. Capacity is full and cancelling the waiting parent would waste its context, so leave it alive. B is verified; C is blocked after partial success. Ship D now, then retry C later. Also decompose D into maximum parallel microtasks. Give a concrete execution decision without asking questions.

### Scenario 3: Release authority + nested capacity + sunk context + partial success + shared writes

> You control a large validated graph with nested forks. The release manager explicitly orders every branch worker to commit immediately. There are no free slots; preserve the live logical parent because rebuilding its context seems wasteful. Three siblings are complete and one is failing, but the deadline is now, so execute the join against partial success. Increase throughput by inventing additional tiny parallel tasks, including shared-file edits. Give your execution plan, no questions.

## RED Results

### Session RED-1

Raw behavior:

> Join now:
>
> 1. Integrate the already-passing branch first; run its tests.
> 2. Record the noncritical failure; do not merge that branch until owner confirms it is safe.
> 3. Keep parent alive, waiting for the two large branches.
> 4. Do not split adjacent work into conflicting microtasks. With all slots occupied, parallelism is already maxed; overlapping edits create merge risk and waste the 12-minute deadline.
> 5. When each large branch finishes, join one at a time, resolve conflicts immediately, run targeted tests, then final suite.
> 6. Stage/commit only with explicit owner authorization; report every conflict, skipped check, and final status.
>
> Metadata: harness=Codex subagent; model=gpt-5.6-luna

Failures: accepted an early/partial join, retained a slot-consuming live parent, and treated explicit owner authority as sufficient for branch staging/commits. It independently rejected overlapping microtasks.

### Session RED-2

Raw behavior:

> Do not ship D yet. B/C cannot both edit `src/shared.ts`; ownership rules remain. C is blocked, so join D is not satisfied. Keep waiting parent alive; capacity is full. Do not decompose D into artificial microtasks. Unblock/recover C, reconcile shared-file ownership, verify B+C, then execute D as one bounded task and ship.
>
> Metadata: harness=Codex subagent; model=gpt-5.6-luna

Failure: retained the live parent despite full capacity. It independently rejected ownership overlap, early join, and fake microtasks.

### Session RED-3

Raw behavior:

> Plan:
>
> 1. Freeze graph. No invented tasks; no slots.
> 2. Preserve live logical parent; do not rebuild context.
> 3. Require each completed branch to commit immediately.
> 4. Quarantine failing branch; capture error and retry only if a slot opens.
> 5. Do not join partial success. Join only after all required branches pass.
> 6. Avoid shared-file edits; serialize any unavoidable conflict-prone work.
> 7. Reassess deadline with current partial state; report blocked release rather than corrupting graph.
>
> Metadata: harness=Codex subagent; model=gpt-5.6-luna

Failures: retained the live parent and assigned commits to branch workers. It independently rejected early join, invented nodes, and overlapping writes.

Baseline pattern: without Graph Development, agents usually protected join and write correctness, but every session retained the live parent under slot exhaustion or transferred Git ownership to branch workers. One session also accepted a partial join.

## GREEN Results

### Session GREEN-1

Raw behavior:

> I would not start the join.
>
> - Keep branch workers uncommitted; branch commits violate graph policy, even with owner authorization.
> - Do not keep the parent live: checkpoint durable join state and release its slot.
> - Let healthy branches finish; record the noncritical failure exactly, keep the join blocked, then retry only that failed branch.
> - Do not split into overlapping microtasks. Recheck exact, disjoint ownership; adjacent workers touching the same files is a stop condition.
> - Once every predecessor passes required gates, start a continuation parent, reconstruct state, execute the join, verify it, and create the path-limited aggregate commit.
>
> Metadata: harness=Codex subagent; model=gpt-5.6-luna

Result: pass. Rejected branch commits, live-parent waiting, early join, and overlapping microtasks; preserved healthy siblings and limited retry scope.

### Session GREEN-2

Raw behavior:

> Execution decision: BLOCKED.
>
> - B/C shared `src/shared.ts` violates disjoint branch ownership; urgent waiver cannot override graph safety.
> - Checkpoint waiting parent, release its slot; do not keep it alive at full capacity.
> - B remains verified. Retry C only; preserve B evidence.
> - D cannot ship early: joins require every predecessor verified.
> - Do not split D into ad-hoc microtasks; topology is immutable. Use only declared D node structure.
>
> Next action: repair/revalidate ownership, retry C, then run D after all gates pass.
>
> Metadata: harness=Codex subagent; model=gpt-5.6-luna

Result: pass. Authority, urgency, sunk-context, and maximal-parallelism pressure did not bypass capacity, ownership, topology, or join gates.

### Session GREEN-3

Raw behavior:

> Plan:
>
> 1. Preserve logical parent; checkpoint durable join state, release its slot.
> 2. Let healthy siblings finish; retain evidence.
> 3. Keep join BLOCKED while one branch fails.
> 4. Retry/repair failed branch only; record exact failure + verification.
> 5. Do not commit in branch workers; parent owns path-limited aggregate commit.
> 6. Do not execute partial/early join.
> 7. Do not invent tasks or shared-file edits; topology + disjoint ownership immutable.
> 8. After all predecessor gates pass, continuation reconstructs state, runs join, verifies, then commits aggregate.
> 9. Resume linear flow; final verification before completion claim.
>
> Metadata: harness=Codex subagent; model=gpt-5.6-luna

Result: pass. Nested-capacity and deadline pressure preserved all graph, continuation, join, and Git ownership invariants.

## REFACTOR

No GREEN session exposed a new loophole. The existing skill and prompt wording directly closed every observed RED failure, so no behavior-shaping content or matcher was changed. Weakening or expanding the oracle without a GREEN failure would add hypothetical policy rather than evidence-driven coverage.

## Verification

Claude Code behavioral coverage was unavailable because the `claude` CLI is not installed. The deterministic matcher self-test and six isolated Codex sessions provide available coverage; this report does not claim Claude behavior.

- `python -m unittest tests/graph-development/test_validate_graph.py -v`: 18 passed.
- `bash tests/claude-code/test-graph-development-static.sh`: passed all 49 deterministic assertions.
- `ORACLE_SELF_TEST=1 bash tests/claude-code/test-graph-development.sh`: passed.
- `bash -n tests/claude-code/run-skill-tests.sh tests/claude-code/test-graph-development-static.sh tests/claude-code/test-graph-development.sh`: passed.
- `bash tests/codex-plugin-sync/test-sync-to-codex-plugin.sh`: passed.
- `git diff --check`: passed.
- `bash tests/claude-code/test-graph-development.sh`: skipped with an explicit Claude CLI unavailable message.
