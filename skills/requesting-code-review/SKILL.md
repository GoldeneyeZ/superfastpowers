---
name: requesting-code-review
description: Use when completing tasks, implementing major features, or before merging to verify work meets requirements
---

# Requesting Code Review

Dispatch code reviewer subagent before issues cascade. Reviewer gets exact context for evaluation — never session history. Keeps reviewer focused on work product, not thought process; preserves own context.

**Core principle:** Review early, often.

## When to Request Review

**Mandatory:**
- After each subagent-driven development task
- After major feature
- Before merge to main

**Optional but valuable:**
- When stuck (fresh view)
- Before refactor (baseline)
- After complex bug fix

## How to Request

**1. Get git SHAs:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Dispatch code reviewer subagent:**

Use Task tool with `general-purpose` type; fill template at `code-reviewer.md`

**Placeholders:**
- `{DESCRIPTION}` - Short summary of what built
- `{PLAN_OR_REQUIREMENTS}` - Expected behavior
- `{BASE_SHA}` - Start commit
- `{HEAD_SHA}` - End commit

**3. Act on feedback:**
- Fix Critical now
- Fix Important before proceeding
- Note Minor for later
- Push back if reviewer wrong (with reasoning)

## Example

```
[Just completed Task 2: Add verification function]

You: Let me request code review before proceeding.

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[Dispatch code reviewer subagent]
  DESCRIPTION: Added verifyIndex() and repairIndex() with 4 issue types
  PLAN_OR_REQUIREMENTS: Task 2 from docs/superfastpowers/plans/deployment-plan.md
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661

[Subagent returns]:
  Strengths: Clean architecture, real tests
  Issues:
    Important: Missing progress indicators
    Minor: Magic number (100) for reporting interval
  Assessment: Ready to proceed

You: [Fix progress indicators]
[Continue to Task 3]
```

## Integration with Workflows

**Subagent-Driven Development:**
- Review after EACH task
- Catch issues before compound
- Fix before next task

**Executing Plans:**
- Review after each task or natural checkpoint
- Get feedback, apply, continue

**Ad-Hoc Development:**
- Review before merge
- Review when stuck

## Red Flags

**Never:**
- Skip review because "simple"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Argue with valid technical feedback

**If reviewer wrong:**
- Push back with technical reasoning
- Show code/tests proving it works
- Request clarification

See template at: requesting-code-review/code-reviewer.md
