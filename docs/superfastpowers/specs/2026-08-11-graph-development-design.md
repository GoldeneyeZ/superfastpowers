# Graph Development Design

## Goal

Add a graph-based execution mode that refines an approved implementation plan into smaller task packages, exposes safe parallel work, and preserves the existing `tasks/<TASK-ID>/` organization.

`writing-plans` creates the task graph. A new `graph-development` skill validates and executes it.

## Non-goals

- Arbitrary DAG scheduling
- Cross-branch file ownership
- Concurrent Git staging or commits by branch workers
- Automatic Git worktree creation
- Replacing existing Goal-Driven, Subagent-Driven, or Inline execution modes
- Adding third-party dependencies

## Terms

- **Node:** One task package at `tasks/<TASK-ID>/`.
- **Linear chain:** Consecutive nodes where each node has one successor and that successor has one predecessor.
- **Fork:** A `parallel` flow element containing two or more branches.
- **Join:** The node that depends on every branch in one fork.
- **Logical parent:** The controller role that creates a fork, waits for its branches, executes its join, and resumes the graph. A replacement agent may resume this role from durable context.
- **Branch worker:** An agent that implements one branch until its matching join.
- **Write ownership:** Exact repository paths a node may modify.

## Package Layout

```text
<package-root>/
  plan.md
  plan-progression.md
  task-graph.json
  task-graph.md
  tasks/<TASK-ID>/
    task.md
    context.md
```

Graph artifact mode is declared in `plan-progression.md`:

```text
Graph format: both
Graph review mode: bypass
```

Accepted graph formats:

- `both` — default; JSON is canonical and Markdown is a generated readable mirror.
- `json` — only `task-graph.json` is required and canonical.
- `markdown` — only `task-graph.md` is required and canonical.

## Planning Responsibilities

`writing-plans` gains a Graph Development output path. When selected, it must:

1. Break work into smaller independently implementable tasks when that creates useful parallel branches.
2. Create one task folder per graph node.
3. Give every node exact write ownership.
4. Keep files that must change together in the same branch or after a join.
5. Produce a structured fork/join flow rather than an arbitrary DAG.
6. Emit graph artifacts using the configured format.
7. Validate graph artifacts before offering Graph Development as an execution choice.

Extra tasks are justified only when they expose real parallelism, improve ownership, or isolate verification. Tiny sequential steps remain one node.

## Canonical JSON Contract

```json
{
  "version": 1,
  "nodes": {
    "AUTH-1": {
      "task": "tasks/AUTH-1/task.md",
      "writes": ["src/auth/model.ts"]
    },
    "AUTH-2": {
      "task": "tasks/AUTH-2/task.md",
      "writes": ["src/auth/service.ts"]
    },
    "AUTH-3": {
      "task": "tasks/AUTH-3/task.md",
      "writes": ["src/auth/view.ts"]
    },
    "AUTH-4": {
      "task": "tasks/AUTH-4/task.md",
      "writes": ["src/auth/index.ts"]
    }
  },
  "flow": {
    "sequence": [
      "AUTH-1",
      {
        "parallel": {
          "branches": [
            { "sequence": ["AUTH-2"] },
            { "sequence": ["AUTH-3"] }
          ],
          "join": "AUTH-4"
        }
      }
    ]
  }
}
```

Nested `parallel` elements are allowed inside branch sequences. Each fork owns exactly one join. Cross-branch edges and crossing joins are invalid.

## Markdown Contract

`task-graph.md` contains:

1. Graph metadata: version, format, source.
2. Node table: node ID, task path, owned write paths.
3. Fork table: fork location, ordered branch flows, join node.
4. Mermaid graph for human inspection.

The node and fork tables are authoritative in Markdown-only mode. Mermaid is always derived and never authoritative.

In `both` mode, Markdown must match canonical JSON. Any mismatch blocks execution.

## Task Context Contract

Topology is immutable during execution. Runtime state stays distributed across task contexts to avoid concurrent writes to one shared state file.

Each `context.md` contains a Graph State section:

```text
Graph status: pending | running | implemented | blocked | reviewed | complete
Logical parent: <node ID or root>
Changed paths: <paths or none>
Verification: <commands and results or none>
Checkpoint: <continuation summary or none>
Failure: <exact blocker or none>
Commit/range: <SHA/range or pending>
```

Fork parents write continuation data into the matching join node's context before dispatch. A replacement continuation agent reconstructs parent state from graph topology and task contexts, not conversation history.

## Validation

`skills/graph-development/scripts/validate_graph.py` uses Python's standard library only.

Validation rejects:

- malformed or unsupported graph versions
- missing or duplicate nodes
- missing task folders, `task.md`, or `context.md`
- empty write ownership
- nodes omitted from flow or referenced more than once
- forks with fewer than two branches
- missing, reused, crossing, or incorrectly placed joins
- cycles or unreachable nodes
- pairwise write overlap between concurrent branches
- graph ownership inconsistent with task package declarations
- JSON/Markdown mismatch in `both` mode
- task-owned repository paths already dirty before dispatch
- topology changes after execution starts without invalidating affected downstream state

Markdown parsing supports only the documented tables. Unsupported free-form graph descriptions fail validation.

## Execution Algorithm

1. Load `plan-progression.md`, graph artifacts, task packages, and repository status.
2. Run deterministic graph validation.
3. Confirm review mode and available agent capacity.
4. Execute the entry node.
5. Update node context after every implementation or review transition.
6. Continue in the same agent while the next flow element is one linear successor.
7. At a fork:
   - verify branch write sets are disjoint;
   - verify owned paths are clean;
   - checkpoint logical-parent state in the join context;
   - dispatch one child per branch as capacity allows;
   - queue excess branches.
8. Each child executes its linear chain, recursively applying the same algorithm to nested forks.
9. A child reaching its matching join stops and returns status, changed paths, verification, and context paths. It never stages or commits.
10. Healthy siblings may finish after another branch fails. The join remains blocked.
11. The logical parent retries or repairs failed branches. It never executes a partial join.
12. After every predecessor is verified, resume the logical parent, execute the join node, run integration checks, and create a path-limited aggregate commit.
13. Continue from the join. At graph completion, root verifies and commits any trailing linear work.

## Capacity and Continuations

Live waiting parents consume limited agent slots and can deadlock nested forks. Therefore parent identity is logical, not tied to one live process.

When capacity is needed, a waiting parent:

1. persists branch IDs, join ID, completed predecessors, blockers, and next action in join context;
2. returns a checkpointed status;
3. releases its agent slot;
4. resumes later through a continuation agent after branch state changes.

Same-agent continuation is preferred when capacity permits. Correctness must never depend on retained conversation context.

## Git and Workspace Safety

- Use current checkout unless human explicitly requests another workspace.
- Never auto-create or suggest Git worktrees.
- Before dispatch, inspect status, unstaged diff, and staged diff.
- Existing changes on any task-owned path block execution.
- Concurrent branches must have disjoint write ownership.
- Branch workers never stage or commit.
- Logical parent stages only graph-owned paths at a join.
- Parent uses path-limited commits so unrelated staged changes remain excluded.
- Join integration owns explicitly declared integration paths not owned by child branches.

## Review Policies

`Graph review mode` accepts:

### Bypass — default

1. Every node uses TDD, focused verification, and self-review.
2. Parent performs integration verification at each join.
3. After implementation graph completes, run one plan-wide spec review.
4. Run one plan-wide code-quality review after spec approval.
5. Run final integration review.

### Gated

1. Every node uses TDD and focused verification.
2. Run node-scoped spec review.
3. Run node-scoped code-quality review after spec approval.
4. Mark node reviewed; only then may successors run.
5. Parent performs integration verification at each join.
6. Run final plan integration review.

Review failure creates an implementation handoff, invalidates dependent state, and reruns required gates before successors or joins continue.

## Skill Contents

```text
skills/graph-development/
  SKILL.md
  branch-worker-prompt.md
  continuation-prompt.md
  scripts/validate_graph.py
```

The main skill remains concise. Prompt templates carry branch and continuation contracts. The validator owns deterministic format and topology checks.

The skill reuses existing `test-driven-development`, `requesting-code-review`, and `verification-before-completion` behavior rather than duplicating their instructions.

## Testing Strategy

Skill development follows RED-GREEN-REFACTOR.

Baseline pressure scenarios run without `graph-development` and record failures before skill authoring. Forward tests then repeat the same scenarios with the skill:

1. Linear chain stays with one agent.
2. Independent branches dispatch concurrently and stop at join.
3. Parent resumes and executes join only after all predecessors verify.
4. Nested fork checkpoints a waiting parent under slot pressure and later resumes it.
5. Failed branch blocks join while healthy siblings finish.
6. Branch retry preserves sibling evidence.
7. Write-overlapping branches fail validation before dispatch.
8. Dirty task-owned paths fail preflight.
9. Branch workers refuse staging and commits under time pressure.
10. `json`, `markdown`, and `both` formats validate.
11. Mismatched JSON and Markdown fail.
12. Bypass and gated review orders match policy.

Automated coverage includes validator unit fixtures, shell/static contract tests, and multi-session behavioral pressure tests on supported harnesses.

## Success Criteria

- Approved plans expose more useful parallel work without inventing artificial tasks.
- Every node maps to one existing-style task folder.
- Linear branches retain agent continuity.
- Forks execute in parallel within capacity.
- Nested forks cannot deadlock solely from waiting parents consuming slots.
- Joins never run early or partially.
- Parallel workers cannot race Git staging or commits.
- Graph state survives agent replacement and session compaction.
- Human can select `both`, `markdown`, or `json`; default remains `both`.
- Human can select bypass or gated review; default remains bypass.
- No third-party dependency is introduced.
