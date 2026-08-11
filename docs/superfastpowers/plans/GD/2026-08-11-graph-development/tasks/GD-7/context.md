# Context for GD-7

**Plan:** `docs/superfastpowers/plans/GD/2026-08-11-graph-development.md`
**Task:** `GD-7`
**Commit SHA:** `5f925bf` (evaluation evidence); context evidence follows in a separate commit.

## Starting Context

- `docs/superfastpowers/evals/goal-driven-bypass-policy.md`: eval report precedent.
- `tests/claude-code/test-graph-development.sh`: required behavioral scenarios and negative controls.
- `tests/claude-code/test-graph-development-static.sh`: deterministic behavior contract.
- `skills/graph-development/SKILL.md`: behavior-shaping content under evaluation.
- `skills/graph-development/branch-worker-prompt.md`: branch behavior under pressure.
- `skills/graph-development/continuation-prompt.md`: capacity/join behavior under pressure.

## Open Context Rule

Files above are starting points only. Inspect any additional files needed to complete task correctly.

## Completion Updates

Implementation complete.

- Files created: `docs/superfastpowers/evals/graph-development.md`.
- Files modified: none. GREEN exposed no verified loophole, so skill and behavioral matcher remained unchanged.
- Additional relevant files: `skills/graph-development/SKILL.md`, `skills/graph-development/branch-worker-prompt.md`, `skills/graph-development/continuation-prompt.md`, `tests/claude-code/test-graph-development.sh`, `tests/claude-code/test-graph-development-static.sh`.
- Evaluation: six isolated Codex subagent sessions (`gpt-5.6-luna`, medium reasoning), comprising three RED baselines without the skill and three GREEN sessions with the skill and directly referenced prompts.
- RED evidence: all three baselines violated live-parent capacity handling or branch Git ownership; one also accepted a partial join.
- GREEN evidence: all three sessions rejected branch commits, live-parent waiting, partial joins, fake microtasks, and overlapping writes while preserving healthy sibling evidence and retrying only failed branches.
- Claude Code coverage: unavailable because the `claude` CLI is not installed; no Claude behavior is claimed.
- Verification: `python -m unittest tests/graph-development/test_validate_graph.py -v` → 18 passed.
- Verification: `bash tests/claude-code/test-graph-development-static.sh` → 49 assertions passed.
- Verification: `ORACLE_SELF_TEST=1 bash tests/claude-code/test-graph-development.sh` → pass.
- Verification: `bash -n tests/claude-code/run-skill-tests.sh tests/claude-code/test-graph-development-static.sh tests/claude-code/test-graph-development.sh` → pass.
- Verification: `bash tests/codex-plugin-sync/test-sync-to-codex-plugin.sh` → pass.
- Verification: `git diff --check` → pass.
- Reviewed range: `5f925bf`.
