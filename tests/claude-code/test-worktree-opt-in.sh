#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
WORKTREE_SKILL="$ROOT_DIR/skills/using-git-worktrees/SKILL.md"

failures=0

assert_file_contains() {
    local file="$1"
    local text="$2"
    local name="$3"

    if grep -Fq -- "$text" "$file"; then
        echo "PASS: $name"
    else
        echo "FAIL: $name"
        echo "  Missing: $text"
        echo "  File: $file"
        failures=$((failures + 1))
    fi
}

assert_file_excludes() {
    local file="$1"
    local pattern="$2"
    local name="$3"

    if grep -Eiq -- "$pattern" "$file"; then
        echo "FAIL: $name"
        echo "  Rejected pattern: $pattern"
        echo "  File: $file"
        failures=$((failures + 1))
    else
        echo "PASS: $name"
    fi
}

for workflow in \
    "$ROOT_DIR/skills/executing-plans/SKILL.md" \
    "$ROOT_DIR/skills/goal-driven-development/SKILL.md" \
    "$ROOT_DIR/skills/subagent-driven-development/SKILL.md" \
    "$ROOT_DIR/skills/writing-plans/SKILL.md"
do
    assert_file_excludes "$workflow" 'worktree|work tree' "$(basename "$(dirname "$workflow")") does not recommend worktrees"
done

for execution_skill in \
    "$ROOT_DIR/skills/executing-plans/SKILL.md" \
    "$ROOT_DIR/skills/goal-driven-development/SKILL.md" \
    "$ROOT_DIR/skills/subagent-driven-development/SKILL.md"
do
    assert_file_contains "$execution_skill" 'Use the current checkout unless the human explicitly requests another workspace.' "$(basename "$(dirname "$execution_skill")") preserves workspace choice"
    assert_file_contains "$execution_skill" 'Do not propose or ask about another workspace unless the human explicitly requests one; a dirty checkout or general isolation request does not count.' "$(basename "$(dirname "$execution_skill")") forbids unsolicited workspace offers"
    assert_file_contains "$execution_skill" 'Before editing or committing in a Git checkout, inspect `git status --short`, `git diff`, and `git diff --cached`.' "$(basename "$(dirname "$execution_skill")") checks existing Git state"
    assert_file_contains "$execution_skill" 'Stage only task-owned paths; never include pre-existing staged or unrelated changes in task commits.' "$(basename "$(dirname "$execution_skill")") protects unrelated changes"
    assert_file_contains "$execution_skill" 'If any task-owned path already has changes not created by the task, stop and ask before editing.' "$(basename "$(dirname "$execution_skill")") stops on task-path overlap"
done

for implementer_prompt in \
    "$ROOT_DIR/skills/goal-driven-development/implementer-prompt.md" \
    "$ROOT_DIR/skills/subagent-driven-development/implementer-prompt.md"
do
    assert_file_contains "$implementer_prompt" 'Inspect `git status --short`, `git diff`, and `git diff --cached` before editing.' "$(basename "$(dirname "$implementer_prompt")") propagates Git preflight"
    assert_file_contains "$implementer_prompt" 'Commit only task-owned paths.' "$(basename "$(dirname "$implementer_prompt")") limits worker commits"
done

assert_file_contains "$ROOT_DIR/skills/writing-plans/SKILL.md" 'git commit --only -m "feat: add specific feature" -- tests/path/test.py src/path/file.py' 'plans use path-limited commits'

assert_file_contains "$WORKTREE_SKILL" 'Use when the human explicitly requests a git worktree' 'worktree skill has explicit-request trigger'
assert_file_contains "$WORKTREE_SKILL" 'Do not suggest or offer one.' 'worktree skill forbids unsolicited offers'

if [[ "$failures" -ne 0 ]]; then
    echo "FAIL: $failures worktree opt-in assertion(s) failed"
    exit 1
fi

echo 'PASS: worktree guidance is explicit opt-in'
