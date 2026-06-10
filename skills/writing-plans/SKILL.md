---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code
---

# Writing Plans

## Overview

Write complete implementation plans for engineer with zero codebase context + weak taste. Include files per task, code, tests, docs to check, test method. Deliver bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume skilled developer, but new to toolset/domain and weak test design.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Context:** If in isolated worktree, it should come from `superfastpowers:using-git-worktrees` skill at execution time.

**Save plans to:** `docs/superfastpowers/plans/<PLAN-ACRONYM>/<YYYY-MM-DD-kebab-feature-name>.md`
- `<PLAN-ACRONYM>` is the uppercase acronym from the plan header, matching task IDs.
- Filename is dated + kebab-case so multiple plans under the same acronym do not collide.
- User preferences for plan location override this default.

## Scope Check

If spec covers multiple independent subsystems, it should have been split into sub-project specs during brainstorming. If not, suggest separate plans — one per subsystem. Each plan should produce working, testable software alone.

## File Structure

Before tasks, map files created/modified and each responsibility. Decomposition decisions lock here.

- Design units with clear boundaries + well-defined interfaces. One file, one clear responsibility.
- You reason best about code held in context; edits safer in focused files. Prefer small focused files over large mixed files.
- Files changing together live together. Split by responsibility, not technical layer.
- In existing codebases, follow patterns. If codebase uses large files, don't unilaterally restructure - but if modified file is unwieldy, plan split is reasonable.

Structure drives task decomposition. Each task should produce self-contained changes that stand alone.

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superfastpowers:subagent-driven-development (recommended), superfastpowers:goal-driven-development, or superfastpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]
**Plan Acronym:** [UPPERCASE acronym for the feature, used in task IDs]


**Tech Stack:** [Key technologies/libraries]

---
```

## Task Structure
Every task MUST include a stable task ID immediately under its heading:
- Format: `<TASK-ID>[PLAN-ACRONYM]-[TASK-NUMBER]</TASK-ID>`
- Use the plan acronym from the document header.
- Example: plan acronym `UA`, task 3 => `<TASK-ID>UA-3</TASK-ID>`


````markdown
### Task N: [Component Name]

<TASK-ID>[ACRONYM]-N</TASK-ID>

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

- [ ] **Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

- [ ] **Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

## No Placeholders

Every step needs actual content engineer needs. These are **plan failures** — never write:
- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above" (without actual test code)
- "Similar to Task N" (repeat the code — engineer may read tasks out of order)
- Steps saying what without how (code blocks required for code steps)
- References to types, functions, or methods not defined in any task

## Remember
- Exact file paths always
- Complete code in every step — if step changes code, show code
- Exact commands with expected output
- DRY, YAGNI, TDD, frequent commits

## Self-Review

After complete plan, review spec fresh and check plan against it. Checklist for yourself — not subagent dispatch.

**1. Spec coverage:** Skim each spec section/requirement. Can you point to task implementing it? List gaps.

**2. Placeholder scan:** Search plan for red flags — patterns from "No Placeholders" above. Fix them.

**3. Type consistency:** Do later-task types, method signatures, property names match earlier definitions? Function `clearLayers()` in Task 3 but `clearFullLayers()` in Task 7 is bug.

If issues found, fix inline. No re-review — fix and move on. If spec requirement has no task, add task.

## User Validation and Task Packages

After saving the plan, get explicit user validation before creating task packages. Do not assume validation from silence.

Once validated, create one task directory per task under a directory named after the plan filename stem:

`docs/superfastpowers/plans/<PLAN-ACRONYM>/<YYYY-MM-DD-kebab-feature-name>/tasks/<TASK-ID>/`

Each task directory MUST contain:

- `task.md` — the complete task copied from the plan, including task ID, files, steps, code blocks, commands, and expected results.
- `context.md` — starting context for the agent taking the task.

`context.md` MUST make clear that listed files are starting points, not constraints. The task agent may inspect any file needed to complete the task.

Use this `context.md` structure:

```markdown
# Context for <TASK-ID>

**Plan:** `docs/superfastpowers/plans/<PLAN-ACRONYM>/<YYYY-MM-DD-kebab-feature-name>.md`
**Task:** `<TASK-ID>`
**Commit SHA:** Pending until task completion. If review fixes add commits, update to the latest task commit and note the reviewed range below.

## Starting Context

- `path/to/file`: why this file is relevant

## Open Context Rule

The files above are starting points only. Inspect any additional files needed to complete the task correctly.

## Completion Updates

The implementer updates this section before review with the final task commit
SHA, reviewed commit range if relevant, files created, files modified,
additional relevant files, and verification commands/results.
```

The final `context.md` is the reviewer's map for finding the task commit and understanding the files that changed or mattered.

## Goal-Driven Progression File

Only create `plan-progression.md` if the user chooses Goal-Driven execution.

Create it in the task package root:

`docs/superfastpowers/plans/<PLAN-ACRONYM>/<YYYY-MM-DD-kebab-feature-name>/plan-progression.md`

Generate one section per task, in plan order:

```markdown
# Plan Progression

Last updated: YYYY-MM-DD HH:MM

## Task N: [Task Name]

- Path: `docs/superfastpowers/plans/<PLAN-ACRONYM>/<YYYY-MM-DD-kebab-feature-name>/tasks/<TASK-ID>/`
- Task status: pending
- Implementer: unchecked
- Spec review: unchecked
- Code quality: unchecked
- Next action: Start implementation.
```

Do not include review findings, implementation notes, or detailed handoffs in
`plan-progression.md`. Those belong in each task directory.

## Execution Handoff

After saving the plan and creating validated task packages, offer execution choice:

**"Plan complete and saved to `docs/superfastpowers/plans/<PLAN-ACRONYM>/<YYYY-MM-DD-kebab-feature-name>.md`. Three execution options:**

**1. Subagent-Driven (recommended)** - Dispatch fresh subagent per task, review between tasks, fast iteration

**2. Goal-Driven** - Use the Codex/OMP goal mechanism for the overall objective, with task packages and `plan-progression.md` to orchestrate implementer/spec/quality phases

**3. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?"**

**If Subagent-Driven chosen:**
- **REQUIRED SUB-SKILL:** Use superfastpowers:subagent-driven-development
- Fresh subagent per task + two-stage review

**If Goal-Driven chosen:**
- Create `plan-progression.md` using the structure above
- **REQUIRED SUB-SKILL:** Use superfastpowers:goal-driven-development
- Same-session phase loop with implementer, strict spec review, and code quality completion gate

**If Inline Execution chosen:**
- **REQUIRED SUB-SKILL:** Use superfastpowers:executing-plans
- Batch execution with checkpoints for review
