#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
SKILL="$ROOT_DIR/skills/using-superfastpowers/SKILL.md"

assert_contains() {
    local pattern="$1"
    local name="$2"
    if grep -Fq -- "$pattern" "$SKILL"; then
        echo "PASS: $name"
    else
        echo "FAIL: $name"
        echo "  Missing: $pattern"
        failures=$((failures + 1))
    fi
}

assert_before() {
    local first="$1"
    local second="$2"
    local name="$3"
    local first_line second_line
    first_line=$(grep -nF -- "$first" "$SKILL" | head -1 | cut -d: -f1 || true)
    second_line=$(grep -nF -- "$second" "$SKILL" | head -1 | cut -d: -f1 || true)
    if [[ -n "$first_line" && -n "$second_line" && "$first_line" -lt "$second_line" ]]; then
        echo "PASS: $name"
    else
        echo "FAIL: $name"
        echo "  Expected '$first' before '$second'"
        failures=$((failures + 1))
    fi
}

failures=0

assert_contains '## Conversation Consent Gate' 'consent gate exists'
assert_contains '`using-superfastpowers` is the bootstrap exception' 'bootstrap may load before consent'
assert_contains 'Use Superfastpowers skills automatically for this conversation?' 'exact conversation prompt'
assert_contains 'ask once' 'prompt occurs once per conversation'
assert_contains 'wait for the answer' 'automatic invocation waits for answer'
assert_contains 'Affirmative consent' 'yes enables automatic skill use'
assert_contains 'Declined consent' 'no disables automatic skill use'
assert_contains 'Silence is unresolved consent' 'silence never enables automatic skill use'
assert_contains 'treat that instruction as declined automatic-use consent' 'no-question instruction declines automatic use'
assert_contains 'Do not ask again during the same conversation' 'answered preference is conversation-scoped'
assert_contains 'explicitly requests a named Superfastpowers skill' 'explicit named-skill exception'
assert_contains 'does not enable unrelated automatic skills' 'explicit request does not change preference'
assert_before '## Conversation Consent Gate' '# Using Skills' 'gate precedes automatic skill rules'

if [[ "$failures" -ne 0 ]]; then
    echo "FAIL: $failures consent contract assertion(s) failed"
    exit 1
fi

echo 'PASS: using-superfastpowers consent contract'
