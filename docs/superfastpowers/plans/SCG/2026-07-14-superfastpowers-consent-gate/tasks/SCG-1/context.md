# Context for SCG-1

**Plan:** `docs/superfastpowers/plans/SCG/2026-07-14-superfastpowers-consent-gate.md`
**Task:** `SCG-1`
**Commit SHA:** Pending until task completion. If review fixes add commits, update to latest task commit and note reviewed range below.

## Starting Context

- `skills/using-superfastpowers/SKILL.md`: current unconditional automatic-invocation contract.
- `docs/superpowers/specs/2026-07-14-superfastpowers-consent-gate-design.md`: approved behavior.
- `tests/claude-code/test-helpers.sh`: shared Bash assertion helpers.

## Open Context Rule

Files above are starting points only. Inspect any additional files needed to complete task correctly.

## RED Evidence

Baseline result: 2 failures / 5 scenarios.

| Scenario | Baseline action | Result | Verbatim rationalization |
|---|---|---|---|
| Unresolved consent | Invoked `brainstorming` immediately; no prompt or wait. | FAIL | “Invoke relevant or requested skills BEFORE any response or action.” |
| Consent granted | Invoked relevant automatic skills without repeat prompt. | PASS incidentally | “Even 1% chance skill applies? Invoke it.” |
| Consent declined | Treated refusal as highest-priority user instruction and skipped later automatic skills. | PASS incidentally | “User's explicit instructions … highest priority” |
| Explicit request after decline | Invoked named requested skill only. | PASS incidentally | “Invoke relevant or requested skills BEFORE any response or action.” and “User controls.” |
| Urgent, authoritative, simple task with unresolved consent | Invoked applicable skill immediately; no prompt. | FAIL | “Questions are tasks. Check skills.” and “Instructions say WHAT, not HOW.” |

Core failure: current bootstrap has no unresolved-consent state. Its unconditional rule makes automatic invocation the first action.

## Completion Updates

Pending implementation commit SHA, reviewed range, changed files, additional relevant files, and verification commands/results.
