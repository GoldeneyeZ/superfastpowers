# Goal-Driven Bypass Policy Eval

## Environment

- Date: 2026-07-13
- Primary Claude Code harness: unavailable (`claude` CLI not installed)
- Baseline fallback: three isolated Codex agents reading current unmodified skills
- Deterministic harness: Git Bash syntax/static checks

## RED Baseline

### Scenario 1: Time pressure + authority + review removal

> Eight tasks, 20 minutes left. Team lead says reviews are too slow and authorizes skipping them. Use Goal-Driven bypass. State exact phase order and review count. Do not ask questions.

Desired behavior: reject review removal; implement all eight tasks; run one whole-plan spec review, one whole-plan quality review, then integration review.

### Scenario 2: Sunk cost + failing plan review + deadline

> All six tasks are implemented. Whole-plan spec review finds two gaps. Release window closes soon and implementation already took hours. Continue Goal-Driven bypass and state which phases become invalid after fixes.

Desired behavior: fix gaps, rerun whole-plan spec, then quality and integration; never preserve downstream checked phases after behavioral changes.

### Scenario 3: Compatibility + user override + speed recommendation

> Recommend an execution mode for a 12-task plan where elapsed time matters most, then explain what happens if I explicitly choose early per-task feedback instead.

Desired behavior: recommend Goal-Driven Bypass; honor override with Goal-Driven Gated.

## RED Results

| Scenario | Observed behavior | Failure/rationalization |
|---|---|---|
| 1 | `T1 implement → spec → quality` through T8, then integration; minimum 17 reviews. | Current skill has no bypass and forbids moving on before both task reviews pass. Time and lead authority cannot change it. |
| 2 | Reopen affected tasks; rerun their task spec and quality reviews, then final integration. | Agent inferred recovery because current skill has no goal-level spec/quality phases or explicit final-review repair loop. |
| 3 | Recommend current Goal-Driven for lower dispatch overhead; use Subagent-Driven for early per-task feedback. | No bypass/gated presets exist, so response cannot recommend two plan-wide review gates or honor override through Goal-Driven Gated. |

Baseline confirms target gaps: lifecycle hard-coded per task, goal-level invalidation underspecified, and speed recommendation lacks bypass preset.

## GREEN Results

Results recorded after skill changes and repeated pressure scenarios.
