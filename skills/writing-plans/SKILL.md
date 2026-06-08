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

**Save plans to:** `docs/superfastpowers/plans/YYYY-MM-DD-<feature-name>.md`
- (User preferences for plan location override this default)

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

> **For agentic workers:** REQUIRED SUB-SKILL: Use superfastpowers:subagent-driven-development (recommended) or superfastpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

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

## Execution Handoff

After saving plan, offer execution choice:

**"Plan complete and saved to `docs/superfastpowers/plans/<filename>.md`. Two execution options:**

**1. Subagent-Driven (recommended)** - Dispatch fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?"**

**If Subagent-Driven chosen:**
- **REQUIRED SUB-SKILL:** Use superfastpowers:subagent-driven-development
- Fresh subagent per task + two-stage review

**If Inline Execution chosen:**
- **REQUIRED SUB-SKILL:** Use superfastpowers:executing-plans
- Batch execution with checkpoints for review
