---
name: writing-plans
description: Use when approved requirements need a multi-step implementation plan before coding.
---

# Writing Plans

## Goal

Produce an executable plan quickly. Include enough detail to remove ambiguity; avoid process artifacts.

## Standard Plan

Write one Markdown file under `docs/plans/` or project-native location:

```markdown
# <Feature> Implementation Plan

## Goal
## Constraints
## Tasks

### 1. <Task>
- Depends on: none | task IDs
- Files: exact paths
- Change: concise behavior
- Verify: exact command or observable result
```

Prefer tasks sized for coherent ownership, usually 15–60 minutes. Do not split work into artificial microtasks merely to increase task count.

## Planning Workflow

1. Read approved requirements and relevant existing code.
2. Identify minimal coherent tasks and dependencies.
3. Assign exact paths; parallel tasks must have disjoint writes.
4. Add focused verification per task.
5. Review plan once against requirements; fix gaps inline.
6. Offer execution.

No mandatory user checkpoint between writing plan and creating optional artifacts unless a real design choice remains.

## Optional Task Packages

Use `tasks/<TASK-ID>/task.md` only when user requests separate folders, graph execution needs them, or plan size makes folders materially clearer. `context.md`, progression files, evidence files, and review artifacts are not required.

## Optional Graph

Use Graph Development when plan has useful parallel branches. Ask or infer artifact mode:

- `json`
- `markdown`
- `both` (default)

Create one graph node per coherent task package. Model only structured sequence, fork, and join. Declare exact repository writes per node. Reject parallel overlap.

Minimal package config may use `plan-progression.md` solely for validator compatibility:

```text
Graph format: both
Graph review mode: bypass
coordination_budget_minutes: 5
```

Use Graph Development only when expected parallel savings exceed coordination cost. Order ready branches by critical path. Keep graph nodes coherent; never create microtasks merely to expose more parallelism.

Create `task-graph.json` and/or `task-graph.md`, then run:

```bash
python3 skills/graph-development/scripts/validate_graph.py <package-root>
```

Do not create phase progression, review gates, handoffs, or eval plans.

## Execution Choice

- Graph Development: validated independent branches.
- Goal-Driven Development: several related plan tasks.
- Subagent-Driven Development: user explicitly wants task-isolated workers.
- Executing Plans: inline/sequential execution.

Recommend simplest option matching actual dependencies.

## Completion

Return plan path, task count, parallel branches if any, validation result, recommended execution mode.
