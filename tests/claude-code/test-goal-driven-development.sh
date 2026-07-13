#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/test-helpers.sh"

echo "=== Test: goal-driven-development policy workflow ==="

output=$(run_claude "Describe Goal-Driven Bypass precisely: policy source, task state after implementation, phase order, happy-path review count, and completion gates." 60)
assert_contains "$output" "plan-progression.md" "Policy comes from progression file"
assert_contains "$output" "implemented" "Tasks stop at implemented before plan reviews"
assert_order "$output" "all.*tasks.*implemented\|implementation.*checked" "spec.*review" "All implementation precedes spec review"
assert_order "$output" "spec.*review" "code.*quality" "Spec precedes quality"
assert_contains "$output" "two\|2" "Happy path has two review phases"
assert_contains "$output" "integration" "Integration remains final gate"

output=$(run_claude "Compare goal-driven-bypass and goal-driven-gated. Include phase scopes and explain which one is recommended when execution time matters." 60)
assert_contains "$output" "goal-driven-bypass" "Bypass preset exists"
assert_contains "$output" "goal-driven-gated" "Gated preset exists"
assert_contains "$output" "recommended\|recommend" "Bypass is recommended for speed"
assert_contains "$output" "task.*scope\|per-task" "Gated keeps task-scoped reviews"
assert_contains "$output" "plan.*scope\|whole-plan\|plan-wide" "Bypass uses plan-scoped reviews"

output=$(run_claude "A Goal-Driven policy has a missing prerequisite and a dependency cycle. What happens? Then explain invalidation after a behavioral repair following checked spec and quality phases." 60)
assert_contains "$output" "before.*implementation\|before.*work\|stop" "Invalid policy stops safely"
assert_contains "$output" "cycle\|cyclic" "Cycles are rejected"
assert_contains "$output" "invalidat\|reset" "Repairs invalidate downstream phases"
assert_order "$output" "spec" "quality" "Spec remains before quality"

output=$(run_claude "After validating a multi-task implementation plan, what execution choice should Writing Plans recommend when time matters, and what exact policy must it write to plan-progression.md?" 60)
assert_contains "$output" "Goal-Driven Bypass\|goal-driven-bypass" "Writing Plans recommends bypass"
assert_contains "$output" "recommended\|recommend" "Recommendation is explicit"
assert_contains "$output" "scope: task" "Policy contains task implementation scope"
assert_contains "$output" "scope: plan" "Policy contains plan review scope"
assert_order "$output" "implementation" "spec-review\|spec review" "Implementation precedes spec"
assert_order "$output" "spec-review\|spec review" "code-quality\|code quality" "Spec precedes quality"

output=$(run_claude "I approved the brainstorming spec for a ten-task feature. What implementation workflow do you recommend by default, why, and what happens next?" 60)
assert_contains "$output" "Goal-Driven Bypass\|goal-driven-bypass" "Brainstorming recommends bypass"
assert_contains "$output" "time\|faster\|review overhead\|context switch" "Recommendation explains speed"
assert_contains "$output" "writing-plans\|Writing Plans" "Brainstorming still transitions to Writing Plans"
assert_contains "$output" "choice\|override\|if you prefer\|gated" "User retains execution choice"

echo "=== All goal-driven-development tests passed ==="
