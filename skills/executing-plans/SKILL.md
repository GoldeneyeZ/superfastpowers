---
name: executing-plans
description: Use when you have a written implementation plan to execute in a separate session with review checkpoints
---

# Executing Plans

## Overview

Load plan, review critically, execute all tasks, report complete.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

**Note:** Tell human partner Superfastpowers works much better with subagent access. Work quality much higher on platforms with subagent support (Claude Code or Codex). If subagents available, use superfastpowers:subagent-driven-development instead of this skill.

## The Process

### Step 1: Load and Review Plan
1. Read plan file
2. Review critically - find questions or concerns
3. If concerns: Raise with human partner before starting
4. If no concerns: Create TodoWrite and proceed

### Step 2: Execute Tasks

For each task:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run specified verifications
4. Mark as completed

### Step 3: Complete Development

After all tasks complete and verified:
- Announce: "I'm using the finishing-a-development-branch skill to complete this work."
- **REQUIRED SUB-SKILL:** Use superfastpowers:finishing-a-development-branch
- Follow that skill to verify tests, present options, execute choice

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit blocker (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing start
- You don't understand instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates plan based on feedback
- Fundamental approach needs rethinking

**Don't force through blockers** - stop and ask.

## Remember
- Review plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- Stop when blocked, don't guess
- Use the current checkout unless the human explicitly requests another workspace.
- Preserve unrelated user changes; do not switch branches or relocate work to avoid them.
- Do not propose or ask about another workspace unless the human explicitly requests one; a dirty checkout or general isolation request does not count.
- Before editing or committing in a Git checkout, inspect `git status --short`, `git diff`, and `git diff --cached`.
- Stage only task-owned paths; never include pre-existing staged or unrelated changes in task commits.
- If any task-owned path already has changes not created by the task, stop and ask before editing.

## Integration

**Required workflow skills:**
- **superfastpowers:writing-plans** - Creates plan this skill executes
- **superfastpowers:finishing-a-development-branch** - Complete development after all tasks
