#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
PLANS_SKILL="$ROOT_DIR/skills/writing-plans/SKILL.md"

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

assert_contains 'Graph Development' 'plans expose Graph Development'
assert_contains 'Graph format: both | markdown | json' 'plans declare graph format choices'
assert_contains 'Graph review mode: bypass | gated' 'plans declare graph review choices'
assert_contains 'one graph node per task package' 'plans map nodes to task packages'
assert_contains 'task-graph.json' 'plans name JSON graph artifact'
assert_contains 'task-graph.md' 'plans name Markdown graph artifact'
assert_contains 'cross-branch write ownership must be disjoint' 'plans require disjoint branch ownership'

assert_excludes 'Mermaid[^\n]*authoritative|authoritative[^\n]*Mermaid' 'Mermaid is never authoritative'
assert_excludes '(require|requiring|must)[^\n]*YAML|YAML[^\n]*(require|requiring|must)' 'plans do not require YAML'

if [[ "$failures" -ne 0 ]]; then
    echo "FAIL: $failures Graph Development planning assertion(s) failed"
    exit 1
fi

echo 'PASS: Graph Development planning contract is present'
