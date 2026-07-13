#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/test-helpers.sh"

echo "=== Test: goal-driven-development policy workflow ==="

ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

assert_file_contains() {
    local file="$1"
    local pattern="$2"
    local name="$3"
    if grep -Fq -- "$pattern" "$file"; then
        echo "PASS: $name"
    else
        echo "FAIL: $name"
        echo "  Missing: $pattern"
        echo "  File: $file"
        exit 1
    fi
}

assert_ere() {
    local output="$1"
    local pattern="$2"
    local name="$3"
    local normalized
    normalized=$(printf '%s' "$output" | tr '\n' ' ')
    if printf '%s' "$normalized" | grep -Eiq -- "$pattern"; then
        echo "  [PASS] $name"
    else
        echo "  [FAIL] $name"
        echo "  Expected ERE: $pattern"
        echo "  In output: $normalized"
        return 1
    fi
}

assert_not_ere() {
    local output="$1"
    local pattern="$2"
    local name="$3"
    local normalized
    normalized=$(printf '%s' "$output" | tr '\n' ' ')
    if printf '%s' "$normalized" | grep -Eiq -- "$pattern"; then
        echo "  [FAIL] $name"
        echo "  Rejected ERE matched: $pattern"
        echo "  In output: $normalized"
        return 1
    else
        echo "  [PASS] $name"
    fi
}

bypass_count_pattern='bypass.{0,320}((two|2)[[:space:]]+(plan-wide[[:space:]]+)?(spec[/ -]?(and|&)?[[:space:]]*quality|spec[^.]{0,80}quality|review phases)|one[[:space:]]+(plan-wide[[:space:]]+)?spec[^.]{0,100}review.{0,160}one[[:space:]]+(plan-wide[[:space:]]+)?(code[ -]?)?quality[^.]{0,100}review)'
bypass_wrong_count_pattern='bypass.{0,160}(2N|per-task|per task|two[[:space:]]+per[[:space:]]+task)'
gated_order_pattern='gated.{0,300}(task|per-task).{0,120}implementation.{0,120}spec.{0,120}(code[ -]?quality|quality).{0,160}(plan|integration)'

goal_skill="$ROOT_DIR/skills/goal-driven-development/SKILL.md"
writing_skill="$ROOT_DIR/skills/writing-plans/SKILL.md"
brainstorm_skill="$ROOT_DIR/skills/brainstorming/SKILL.md"

assert_file_contains "$goal_skill" 'Preset: goal-driven-bypass' "Bypass preset contract"
assert_file_contains "$goal_skill" 'Preset: goal-driven-gated' "Gated preset contract"
assert_file_contains "$goal_skill" 'implementation | scope: task' "Task-scoped implementation"
assert_file_contains "$goal_skill" 'spec-review | scope: plan | requires: all tasks implemented' "Plan spec waits for all tasks"
assert_file_contains "$goal_skill" 'code-quality | scope: plan | requires: spec-review checked' "Plan quality waits for spec"
assert_file_contains "$goal_skill" 'Bypass means defer reviews, never skip reviews.' "Bypass safety boundary"
assert_file_contains "$ROOT_DIR/skills/goal-driven-development/implementer-prompt.md" 'policy-required plan-scoped review fields' "Repair worker may invalidate plan review fields"
assert_file_contains "$writing_skill" 'Goal-Driven Bypass (recommended)' "Writing Plans default recommendation"
assert_file_contains "$writing_skill" 'Explicit user choice overrides recommendation.' "Execution override"
assert_file_contains "$brainstorm_skill" 'reduce happy-path spec/quality reviews from `2N` to `2`' "Brainstorming time rationale"

if [[ -e "$ROOT_DIR/skills/goal-driven-development/task-worker-prompt.md" ]]; then
    echo "FAIL: hard-coded task worker still exists"
    exit 1
fi

if [[ "${REGEX_SELF_TEST:-0}" == "1" ]]; then
    wrong='Bypass performs three review phases. Gated performs 2N review phases.'
    correct_aggregate='Goal-Driven Bypass performs 2 spec/quality reviews after all tasks, then final integration.'
    correct_decomposed='Goal-Driven Bypass performs one plan-wide spec review and one plan-wide code-quality review after all tasks, then final integration.'
    gated='Goal-Driven Gated uses per-task implementation, task spec review, task code-quality review, then plan integration.'

    if printf '%s' "$wrong" | grep -Eiq -- "$bypass_count_pattern"; then
        echo "FAIL: wrong Bypass count produced false positive"
        exit 1
    fi
    printf '%s' "$correct_aggregate" | grep -Eiq -- "$bypass_count_pattern"
    printf '%s' "$correct_decomposed" | grep -Eiq -- "$bypass_count_pattern"
    ! printf '%s' "$correct_aggregate" | grep -Eiq -- "$bypass_wrong_count_pattern"
    ! printf '%s' "$correct_decomposed" | grep -Eiq -- "$bypass_wrong_count_pattern"
    printf '%s' "$gated" | grep -Eiq -- "$gated_order_pattern"
    echo "=== Review-count regex self-test passed ==="
    exit 0
fi

if [[ "${STATIC_ONLY:-0}" == "1" ]]; then
    echo "=== Static goal-driven-development contract passed ==="
    exit 0
fi

output=$(run_claude "Describe Goal-Driven Bypass precisely: policy source, task state after implementation, phase order, happy-path review count, and completion gates." 60)
assert_contains "$output" "plan-progression.md" "Policy comes from progression file"
assert_contains "$output" "implemented" "Tasks stop at implemented before plan reviews"
assert_order "$output" "all.*tasks.*implemented\|implementation.*checked" "spec.*review" "All implementation precedes spec review"
assert_order "$output" "spec.*review" "code.*quality" "Spec precedes quality"
assert_ere "$output" "$bypass_count_pattern" "Bypass binds count to two spec/quality reviews"
assert_not_ere "$output" "$bypass_wrong_count_pattern" "Bypass never uses per-task or 2N review count"
assert_contains "$output" "integration" "Integration remains final gate"

output=$(run_claude "Compare goal-driven-bypass and goal-driven-gated. Include phase scopes and explain which one is recommended when execution time matters." 60)
assert_contains "$output" "goal-driven-bypass" "Bypass preset exists"
assert_contains "$output" "goal-driven-gated" "Gated preset exists"
assert_contains "$output" "recommended\|recommend" "Bypass is recommended for speed"
assert_contains "$output" "task.*scope\|per-task" "Gated keeps task-scoped reviews"
assert_contains "$output" "plan.*scope\|whole-plan\|plan-wide" "Bypass uses plan-scoped reviews"
assert_ere "$output" "$gated_order_pattern" "Gated lifecycle order is explicit"

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
