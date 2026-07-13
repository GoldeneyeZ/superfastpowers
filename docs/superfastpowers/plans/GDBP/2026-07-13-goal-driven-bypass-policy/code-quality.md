# Goal-Driven Bypass Policy Code Quality Review

Result: failed

Reviewed range: `ed9dc5d..HEAD`

## Important Findings

### Core `2N` to `2` regression assertion permits false positives

`tests/claude-code/test-goal-driven-development.sh:55` accepts the unanchored pattern `two\|2`. It passes whenever the response contains any digit `2`, including the baseline term `2N`, even if the response says Bypass performs the wrong number of reviews. A direct probe using `Bypass performs three review phases. Gated performs 2N review phases.` returned `grep_exit=0` for the exact assertion pattern. The central elapsed-time contract can therefore regress while the behavioral test remains green.

Fix: assert that the Bypass result explicitly binds `two` or `2` to the plan-scoped spec-and-quality review count, and add a negative/contrast assertion that rejects a Bypass per-task or `2N` review count. Keep integration identified separately as the final gate. Add similarly explicit gated ordering coverage rather than relying only on the presence of `task`/`per-task` at lines 62-63.

## Strengths

- The policy schema, controller algorithm, state transitions, and invalidation rules are cohesive and use consistent domain names.
- The repaired implementer contract now clearly distinguishes behavioral/spec, quality-only, and uncertain repairs without permitting unrelated progression edits.
- Phase templates have focused responsibilities and consistently require actual diff inspection rather than trusting reports.
- Deleted full-lifecycle worker references are absent from active skills; the compatibility preset remains policy-driven.
- Documentation and handoffs describe the time-versus-feedback trade-off consistently without changing unrelated execution semantics.
- Shell scripts are syntactically portable within the existing Git Bash harness and focused static checks are registered in the fast suite.

## Verification Evidence

- `STATIC_ONLY=1 tests/claude-code/test-goal-driven-development.sh` — all 10 static assertions passed.
- `bash -n tests/claude-code/*.sh` — all Claude Code shell scripts parsed successfully.
- `git diff --check ed9dc5d..HEAD` — passed with no output.
- False-positive probe against the exact `two\|2` pattern — `grep_exit=0` for an intentionally wrong Bypass count.
- Full `run_claude` behavioral execution remains unavailable because the `claude` CLI is not installed.

## Re-review after repair commit `ea71f4e`

Result: failed

### Important — correct one-plus-one review wording is rejected

The original false positive is fixed, but `tests/claude-code/test-goal-driven-development.sh:57` now requires the literal aggregate `two` or `2`. A correct response such as “Bypass performs one plan-wide spec review and one plan-wide code-quality review after all tasks, then final integration” does not match (`correct_one_plus_one_exit=1`). This is common wording taken directly from the skill contract and violates the prior handoff acceptance criterion that one spec plus one quality review must pass.

The deterministic self-test at lines 81-94 does not cover that required form; its only positive fixture at line 83 uses `2 spec/quality reviews`, so it masks the false-negative risk.

Fix: make the positive assertion accept both supported correct forms—an explicit aggregate two/2 tied to spec and quality, or one plan-scoped spec review plus one plan-scoped quality review—while preserving the negative rejection of Bypass `2N`/per-task counts. Add both correct forms and the wrong-count form to `REGEX_SELF_TEST`.

### Fresh evidence

- `REGEX_SELF_TEST=1 tests/claude-code/test-goal-driven-development.sh` — existing wrong/aggregate-correct/Gated fixtures passed.
- Direct correct one-plus-one probe — rejected with `correct_one_plus_one_exit=1`.
- `STATIC_ONLY=1 tests/claude-code/test-goal-driven-development.sh` — all 10 static assertions passed.
- `bash -n tests/claude-code/*.sh` — all shell scripts parsed.
- `git diff --check ed9dc5d..HEAD` also reports the prior review artifact's extra blank line at EOF; preserve clean diff formatting when updating this artifact.
