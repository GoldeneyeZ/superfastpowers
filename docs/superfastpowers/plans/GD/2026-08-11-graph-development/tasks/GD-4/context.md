# Context for GD-4

**Plan:** `docs/superfastpowers/plans/GD/2026-08-11-graph-development.md`
**Task:** `GD-4`
**Commit SHA:** Pending until task completion. If review fixes add commits, update to latest task commit and note reviewed range below.

## Starting Context

- `tests/claude-code/test-helpers.sh`: behavioral runner and assertion helpers.
- `tests/claude-code/test-worktree-native-preference.sh`: pressure-test and oracle self-test pattern.
- `tests/claude-code/test-goal-driven-development.sh`: policy-order matcher pattern.
- `docs/superfastpowers/specs/2026-08-11-graph-development-design.md`: expected graph execution behavior.

## Open Context Rule

Files above are starting points only. Inspect any additional files needed to complete task correctly.

## Completion Updates

Implementer updates this section before review with final task commit SHA, reviewed commit range if relevant, files created, files modified, additional relevant files, and verification commands/results.

**Implementation commit:** `3484c137532d5a19c3bedb3da48a5b94793fb1d5` (`[GD-4] test: capture graph execution baseline`).

**Files created:** `tests/claude-code/test-graph-development.sh` — five-scenario behavioral pressure runner with deterministic matcher oracle self-test.

**Files modified:** `tests/claude-code/test-graph-development-static.sh` — future Graph Development skill/prompt existence and contract assertions.

**RED evidence:** `bash tests/claude-code/test-graph-development-static.sh` exited 1 with 13 expected assertions because the Graph Development skill and prompts do not exist yet.

**Verification:** `ORACLE_SELF_TEST=1 bash tests/claude-code/test-graph-development.sh` passed; `git diff --check` passed. Claude CLI is unavailable, so the runner skips live behavioral calls until a supported harness is available.
