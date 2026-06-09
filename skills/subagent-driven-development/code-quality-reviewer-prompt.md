# Code Quality Reviewer Prompt Template

Use when dispatching code quality reviewer subagent.

**Purpose:** Verify implementation clean, tested, maintainable.

**Only dispatch after spec compliance review passes.**

```
Task tool (general-purpose):
  Use template at requesting-code-review/code-reviewer.md

  DESCRIPTION: [task summary, from implementer's report]
  PLAN_OR_REQUIREMENTS: Task N from [plan-file]
  TASK_PACKAGE_DIR: [path/to/tasks/<TASK-ID>/, if present]
  TASK_CONTEXT: [task package context.md if present]
  BASE_SHA: [commit before task]
  HEAD_SHA: [current commit]
```

**Beyond standard code quality, reviewer checks:**
- Each file one clear responsibility + well-defined interface?
- Units decomposed for independent understanding + testing?
- Implementation follows plan file structure?
- New files already large, or existing files significantly grown? (Don't flag pre-existing file sizes — focus on this change.)
- `context.md` commit SHA matches the reviewed task commit/range?
- `context.md` lists files created/modified by the task and relevant files used for implementation?
- `context.md` verification commands/results are specific enough for a reviewer to reproduce?

**Code reviewer returns:** Strengths, Issues (Critical/Important/Minor), Assessment.
