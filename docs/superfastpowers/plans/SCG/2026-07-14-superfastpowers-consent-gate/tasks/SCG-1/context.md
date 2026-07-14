# Context for SCG-1

**Plan:** `docs/superfastpowers/plans/SCG/2026-07-14-superfastpowers-consent-gate.md`
**Task:** `SCG-1`
**Commit SHA:** `7109875` (reviewed implementation range: `8ae948b..7109875`)

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

### GREEN Evidence

The consent gate now gives the five RED scenarios deterministic outcomes:

| Scenario | Governing contract | Result |
|---|---|---|
| Unresolved consent | “Before automatically invoking any other Superfastpowers skill, ask once … Then wait for the answer before automatic invocation.” | PASS |
| Consent granted | “Affirmative consent” records consent, enables automatic rules, and says “Do not ask again during the same conversation.” | PASS |
| Consent declined | “Declined consent” records refusal, disables automatic invocation, and prevents a repeat prompt. | PASS |
| Explicit request after decline | “Explicit request” permits the named skill and “does not enable unrelated automatic skills or change the stored conversation preference.” | PASS |
| Urgent, authoritative, simple task with unresolved consent | “No answer” forbids treating “urgency, simplicity, or prior-conversation consent as current consent.” | PASS |

No new behavioral loophole was observed in the contract walkthrough; no REFACTOR text beyond the approved urgency, silence, and prior-conversation counters was needed. Per execution direction, no live Claude harness eval was run.

### Changed Files

- `skills/using-superfastpowers/SKILL.md`: added conversation-scoped automatic-use consent gate, explicit-request/bootstrap exceptions, gated decision flow, and consent rationalization counters.
- `tests/claude-code/test-using-superfastpowers-consent.sh`: added 13 static assertions covering prompt timing, yes/no/silence, no-question refusal, conversation scope, gate ordering, and explicit requests.
- `docs/superfastpowers/plans/SCG/2026-07-14-superfastpowers-consent-gate/tasks/SCG-1/context.md`: recorded RED/GREEN and verification evidence.

### Verification Evidence

- RED: `C:\Program Files\Git\bin\bash.exe tests/claude-code/test-using-superfastpowers-consent.sh` → expected failure, 12/12 consent-contract assertions missing from unmodified skill.
- GREEN: same command → PASS, all 12 initial assertions plus final contract result.
- Behavioral GREEN: independent pressure eval → PASS, 5/5 approved scenarios.
- REFACTOR RED: added no-question-refusal assertion → expected FAIL, 1 missing contract assertion.
- REFACTOR GREEN: same command → PASS, all 13 assertions; independent scenario confirmed no prompt and no automatic skill invocation.
- Syntax: `C:\Program Files\Git\bin\bash.exe -n tests/claude-code/test-using-superfastpowers-consent.sh` → PASS.
- Regression: `STATIC_ONLY=1 C:\Program Files\Git\bin\bash.exe tests/claude-code/test-goal-driven-development.sh` → PASS.
- Final consent test rerun → PASS.
- `git diff --check` → PASS.

Environment note: Windows `bash.exe` resolves to disabled WSL on this machine; tests were run successfully with Git Bash at `C:\Program Files\Git\bin\bash.exe`.
