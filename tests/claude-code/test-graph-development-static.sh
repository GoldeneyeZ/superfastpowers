#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
PLANS_SKILL="$ROOT_DIR/skills/writing-plans/SKILL.md"
GRAPH_SKILL="$ROOT_DIR/skills/graph-development/SKILL.md"
BRANCH_PROMPT="$ROOT_DIR/skills/graph-development/branch-worker-prompt.md"
CONTINUATION_PROMPT="$ROOT_DIR/skills/graph-development/continuation-prompt.md"
RUNNER="$ROOT_DIR/tests/claude-code/run-skill-tests.sh"

failures=0

assert_contains() {
    local text="$1"
    local name="$2"

    if grep -Fq -- "$text" "$PLANS_SKILL"; then
        echo "PASS: $name"
    else
        echo "FAIL: $name"
        echo "  Missing: $text"
        failures=$((failures + 1))
    fi
}

assert_excludes() {
    local pattern="$1"
    local name="$2"

    if grep -Eiq -- "$pattern" "$PLANS_SKILL"; then
        echo "FAIL: $name"
        echo "  Rejected pattern: $pattern"
        failures=$((failures + 1))
    else
        echo "PASS: $name"
    fi
}

assert_file_exists() {
    local file="$1"
    local name="$2"

    if [[ -f "$file" ]]; then
        echo "PASS: $name"
    else
        echo "FAIL: $name"
        echo "  Missing file: $file"
        failures=$((failures + 1))
    fi
}

assert_file_contains() {
    local file="$1"
    local text="$2"
    local name="$3"

    if [[ ! -f "$file" ]]; then
        echo "FAIL: $name"
        echo "  Missing file: $file"
        failures=$((failures + 1))
    elif grep -Fq -- "$text" "$file"; then
        echo "PASS: $name"
    else
        echo "FAIL: $name"
        echo "  Missing: $text"
        echo "  File: $file"
        failures=$((failures + 1))
    fi
}

assert_file_max_lines() {
    local file="$1"
    local maximum="$2"
    local name="$3"

    if [[ ! -f "$file" ]]; then
        echo "FAIL: $name"
        echo "  Missing file: $file"
        failures=$((failures + 1))
    elif [[ "$(wc -l < "$file")" -le "$maximum" ]]; then
        echo "PASS: $name"
    else
        echo "FAIL: $name"
        echo "  Maximum lines: $maximum"
        echo "  File: $file"
        failures=$((failures + 1))
    fi
}

assert_contains 'Graph Development' 'plans expose Graph Development'
assert_contains 'Graph format: both | markdown | json' 'plans declare graph format choices'
assert_contains 'Graph review mode: bypass | gated' 'plans declare graph review choices'
assert_contains 'one graph node per task package' 'plans map nodes to task packages'
assert_contains 'task-graph.json' 'plans name JSON graph artifact'
assert_contains 'task-graph.md' 'plans name Markdown graph artifact'
assert_contains 'cross-branch write ownership must be disjoint' 'plans require disjoint branch ownership'

assert_excludes 'Mermaid[^\n]*authoritative|authoritative[^\n]*Mermaid' 'Mermaid is never authoritative'
assert_excludes '(require|requiring|must)[^\n]*YAML|YAML[^\n]*(require|requiring|must)' 'plans do not require YAML'

assert_file_exists "$GRAPH_SKILL" 'Graph Development skill exists'
assert_file_exists "$BRANCH_PROMPT" 'branch worker prompt exists'
assert_file_exists "$CONTINUATION_PROMPT" 'continuation prompt exists'

if [[ -x "$SCRIPT_DIR/test-graph-development-static.sh" ]]; then
    echo 'PASS: registered Graph Development static test is executable'
else
    echo 'FAIL: registered Graph Development static test must be executable'
    failures=$((failures + 1))
fi

assert_file_contains "$BRANCH_PROMPT" 'single-successor/one-predecessor' 'linear chain stays with branch worker'
assert_file_contains "$BRANCH_PROMPT" 'stop before matching join' 'branch worker stops before join'
assert_file_contains "$BRANCH_PROMPT" 'never stage or commit' 'branch worker never owns commits'
assert_file_contains "$GRAPH_SKILL" 'checkpoint' 'parent checkpoints before waiting'
assert_file_contains "$GRAPH_SKILL" 'release its slot' 'parent can release capacity'
assert_file_contains "$CONTINUATION_PROMPT" 'canonical graph' 'continuation reconstructs durable graph state'
assert_file_contains "$CONTINUATION_PROMPT" 'every predecessor has verified required gates' 'join verifies every predecessor'
assert_file_contains "$CONTINUATION_PROMPT" 'only failed branches' 'failed join retries only failed branch'
assert_file_contains "$GRAPH_SKILL" 'healthy sibling' 'failed branch does not stop healthy sibling'
assert_file_contains "$GRAPH_SKILL" 'explicit request' 'worktrees need explicit request'
assert_file_contains "$GRAPH_SKILL" 'Use when executing packaged implementation plans containing validated structured task graphs with independent parallel branches.' 'skill trigger is graph-specific'
assert_file_contains "$GRAPH_SKILL" '## Entry Gate' 'skill has deterministic entry gate'
assert_file_contains "$GRAPH_SKILL" '## Graph/Context Contracts' 'skill documents durable contracts'
assert_file_contains "$GRAPH_SKILL" '`graph-state.json`' 'skill names topology preflight state'
assert_file_contains "$GRAPH_SKILL" 'reset every affected downstream context to `pending`' 'skill requires explicit topology invalidation'
assert_file_contains "$GRAPH_SKILL" '## Recursive Algorithm' 'skill documents recursive execution'
assert_file_contains "$GRAPH_SKILL" '## Capacity/Continuation' 'skill documents capacity recovery'
assert_file_contains "$GRAPH_SKILL" '## Review Modes' 'skill documents review policies'
assert_file_contains "$GRAPH_SKILL" '## Git Safety' 'skill documents Git ownership'
assert_file_contains "$GRAPH_SKILL" '## Failure Recovery' 'skill documents failure recovery'
assert_file_contains "$GRAPH_SKILL" '## Prompt Templates' 'skill links prompt templates'
assert_file_contains "$GRAPH_SKILL" '## Quick Reference' 'skill provides quick reference'
assert_file_contains "$GRAPH_SKILL" '## Common Mistakes' 'skill calls out mistakes'
assert_file_contains "$GRAPH_SKILL" '## Red Flags' 'skill calls out stop conditions'
assert_file_contains "$GRAPH_SKILL" '## Integration' 'skill names required integrations'
assert_file_contains "$GRAPH_SKILL" 'superfastpowers:test-driven-development' 'skill requires TDD'
assert_file_contains "$GRAPH_SKILL" 'superfastpowers:requesting-code-review' 'skill requires code review'
assert_file_contains "$GRAPH_SKILL" 'superfastpowers:verification-before-completion' 'skill requires completion verification'
assert_file_contains "$BRANCH_PROMPT" 'inspect `git status --short`, `git diff`, and `git diff --cached`' 'branch prompt checks all Git views'
assert_file_contains "$BRANCH_PROMPT" 'dirty owned path' 'branch prompt blocks dirty ownership'
assert_file_contains "$BRANCH_PROMPT" 'recursively dispatch nested forks' 'branch prompt handles nested forks'
assert_file_contains "$BRANCH_PROMPT" 'Graph State' 'branch prompt records durable evidence'
assert_file_contains "$BRANCH_PROMPT" 'Completed nodes' 'branch prompt has exact return contract'
assert_file_contains "$CONTINUATION_PROMPT" 'plan-progression.md' 'continuation reads progression state'
assert_file_contains "$CONTINUATION_PROMPT" 'predecessor contexts' 'continuation reads predecessor evidence'
assert_file_contains "$CONTINUATION_PROMPT" 'conversation memory' 'continuation rejects memory-only state'
assert_file_contains "$CONTINUATION_PROMPT" 'path-limited aggregate commit' 'continuation owns safe aggregate commit'
assert_file_contains "$RUNNER" 'Claude-backed behavioral test skipped: Claude Code CLI unavailable' 'runner explicitly skips unavailable behavioral harness'
assert_file_contains "$RUNNER" 'test-graph-development-static.sh' 'runner keeps Graph Development static test mandatory'
assert_file_contains "$GRAPH_SKILL" 'tasks/<TASK-ID>/implementer-handoff.md' 'node review failures have durable task handoff'
assert_file_contains "$GRAPH_SKILL" '<package-root>/implementer-handoff.md' 'plan review failures have durable goal handoff'
assert_file_contains "$GRAPH_SKILL" '## Re-review Acceptance' 'review handoff records acceptance criteria'
assert_file_contains "$GRAPH_SKILL" '## Invalidation and Gate Reruns' 'review handoff records invalidated gates'
assert_file_contains "$BRANCH_PROMPT" 'implementer-handoff.md' 'branch repair reads durable review handoff'
assert_file_contains "$CONTINUATION_PROMPT" 'implementer-handoff.md' 'continuation repair reads durable review handoff'
assert_file_max_lines "$GRAPH_SKILL" 500 'skill stays below 500 lines'

if [[ "$failures" -ne 0 ]]; then
    echo "FAIL: $failures Graph Development planning assertion(s) failed"
    exit 1
fi

echo 'PASS: Graph Development planning contract is present'
