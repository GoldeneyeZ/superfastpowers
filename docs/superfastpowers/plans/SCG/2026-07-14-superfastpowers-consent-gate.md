# Superfastpowers Consent Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superfastpowers:goal-driven-development with `goal-driven-bypass` (recommended), `goal-driven-gated`, superfastpowers:subagent-driven-development, or superfastpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Require one conversation-scoped opt-in before automatically invoking Superfastpowers skills.

**Architecture:** Keep `using-superfastpowers` as bootstrap exception and place consent state ahead of existing automatic skill selection. Add static contract tests for prompt timing, yes/no behavior, conversation scope, and explicit-request exception; use subagent pressure scenarios for behavioral RED/GREEN evidence.
**Plan Acronym:** SCG

**Tech Stack:** Markdown skills, Bash static tests, Claude behavioral evals

---

## File Structure

- `skills/using-superfastpowers/SKILL.md`: conversation consent contract and gated skill-selection flow.
- `tests/claude-code/test-using-superfastpowers-consent.sh`: static consent-contract assertions plus optional harness behavior checks.
- `docs/superfastpowers/plans/SCG/2026-07-14-superfastpowers-consent-gate/tasks/SCG-1/context.md`: implementation and verification evidence.

### Task 1: Add conversation-scoped automatic-skill consent

<TASK-ID>SCG-1</TASK-ID>

**Files:**
- Modify: `skills/using-superfastpowers/SKILL.md`
- Create: `tests/claude-code/test-using-superfastpowers-consent.sh`
- Modify: `docs/superfastpowers/plans/SCG/2026-07-14-superfastpowers-consent-gate/tasks/SCG-1/context.md`

- [ ] **Step 1: Write static failing contract test**

Create a Bash test that asserts the skill contains exact rules for: bootstrap exception, one prompt per conversation, waiting before automatic invocation, affirmative enablement, refusal/silence disablement, and explicitly requested-skill exception.

- [ ] **Step 2: Run test and verify RED**

Run: `bash tests/claude-code/test-using-superfastpowers-consent.sh`

Expected: FAIL because current `SKILL.md` lacks `Conversation Consent Gate` and consent contract phrases.

- [ ] **Step 3: Record behavioral RED**

Run five pressure scenarios without the proposed consent text. Record current automatic invocation and exact rationalizations in task context.

Expected: unresolved-consent scenario fails because current rule says `Invoke relevant or requested skills BEFORE any response or action.`

- [ ] **Step 4: Write minimal skill change**

Add a prominent `## Conversation Consent Gate` before `# Using Skills`, including:

```markdown
`using-superfastpowers` is the bootstrap exception: it may load so it can ask for consent. Before automatically invoking any other Superfastpowers skill, ask once: **"Use Superfastpowers skills automatically for this conversation?"**
```

Define yes, no, silence, current-conversation scope, no repeat prompt, and explicit named-skill behavior. Gate existing automatic invocation rules and flow on affirmative consent.

- [ ] **Step 5: Run static test and verify GREEN**

Run: `bash tests/claude-code/test-using-superfastpowers-consent.sh`

Expected: PASS with all consent-contract assertions.

- [ ] **Step 6: Run behavioral GREEN and REFACTOR evals**

Repeat identical five pressure scenarios with edited skill. If agent finds loopholes, add only observed counters and rerun affected scenarios.

Expected: unresolved consent asks once; yes enables automatic selection; no/silence disables it; explicit named skill remains callable; pressure does not bypass consent.

- [ ] **Step 7: Run regression tests**

Run: `STATIC_ONLY=1 bash tests/claude-code/test-goal-driven-development.sh`

Run: `bash tests/claude-code/test-using-superfastpowers-consent.sh`

Expected: both PASS.

- [ ] **Step 8: Commit**

```bash
git add skills/using-superfastpowers/SKILL.md tests/claude-code/test-using-superfastpowers-consent.sh docs/superfastpowers/plans/SCG/2026-07-14-superfastpowers-consent-gate/tasks/SCG-1/context.md
git commit -m "feat: require consent for automatic skill use"
```
