#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
PLANS_SKILL="$ROOT_DIR/skills/writing-plans/SKILL.md"
GRAPH_SKILL="$ROOT_DIR/skills/graph-development/SKILL.md"
BRANCH_PROMPT="$ROOT_DIR/skills/graph-development/branch-worker-prompt.md"
CONTINUATION_PROMPT="$ROOT_DIR/skills/graph-development/continuation-prompt.md"

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

if [[ "$failures" -ne 0 ]]; then
    echo "FAIL: $failures Graph Development planning assertion(s) failed"
    exit 1
fi

echo 'PASS: Graph Development planning contract is present'
