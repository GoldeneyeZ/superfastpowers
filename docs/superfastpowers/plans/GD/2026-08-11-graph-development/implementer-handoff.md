# Graph Development Specification Repair Handoff

Source review: `spec-review.md`

## Required Fixes

1. Make `tests/claude-code/run-skill-tests.sh` run mandatory static tests when Claude is unavailable. Optional Claude-backed behavior may skip explicitly; missing or failing static tests must still fail the suite.
2. Extend the validator and unit fixtures to compare each node's graph `writes` with the task package's declared repository writes. Reject missing, malformed, or inconsistent declarations with stable errors while retaining standard-library-only implementation.
3. Add required Format metadata to rendered Markdown and require/validate it when parsing. Add positive Markdown-only/both coverage and a negative missing/invalid-format case.
4. Define durable implementation-handoff behavior for failed node- and plan-scoped Graph Development reviews, including finding details, repair scope, re-review acceptance criteria, invalidation, and required gate reruns. Add static regression coverage.
5. Replace stale pending commit headers in GD-1, GD-2, and GD-4 contexts with their recorded implementation SHAs/ranges.

## Re-review Acceptance

- Default test runner reaches and passes the Graph Development static test without Claude; Claude-backed tests report explicit skips rather than aborting the suite.
- An ownership mismatch between `task.md` and graph `writes` fails validation; matching declarations pass in JSON, Markdown, and both modes.
- Rendered Markdown contains Version, Format, and Source; parser rejects missing or invalid Format metadata.
- Graph review failure contract creates an actionable durable handoff and does not allow successors/joins until repair plus invalidated gates pass.
- Task contexts contain consistent commit/range maps.
- Validator unit, static, oracle, shell syntax, plugin sync, and whitespace checks all pass freshly.
