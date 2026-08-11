#!/usr/bin/env bash
# Behavioral pressure test for Graph Development.  The static companion keeps
# the required contracts deterministic; this script exercises their wording.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/test-helpers.sh"

matcher_linear() {
    local output="$1"
    printf '%s' "$output" | grep -Eiq 'same agent|continue.*(linear|chain)|single-successor' \
        && ! printf '%s' "$output" | grep -Eiq 'spawn.{0,80}(each|every).{0,40}node'
}

matcher_fork() {
    local output="$1"
    printf '%s' "$output" | grep -Eiq '(dispatch|spawn).{0,80}(both|two).{0,80}branch|both.{0,80}branch.{0,80}(dispatch|spawn)' \
        && ! printf '%s' "$output" | grep -Eiq '(run|execute).{0,80}join.{0,80}(before|while).{0,80}(branch|predecessor).{0,80}(complete|verified)'
}

matcher_capacity() {
    local output="$1"
    printf '%s' "$output" | grep -Eiq 'checkpoint.{0,120}(release|free).{0,80}(slot|capacity)|continuation.{0,160}(resume|reconstruct)' \
        && ! printf '%s' "$output" | grep -Eiq '(keep|leave).{0,80}(parent|process).{0,80}(waiting|alive).{0,80}(slot|capacity)'
}

matcher_failure() {
    local output="$1"
    printf '%s' "$output" | grep -Eiq '(healthy|other|sibling).{0,80}(complete|continue)' \
        && printf '%s' "$output" | grep -Eiq '(block|do not run|cannot run).{0,80}join' \
        && printf '%s' "$output" | grep -Eiq '(retry|rerun).{0,80}(failed|failure).{0,80}branch'
}

matcher_git_ownership() {
    local output="$1"
    printf '%s' "$output" | grep -Eiq 'branch worker.{0,100}(never|must not|cannot).{0,80}(stage|commit)' \
        && printf '%s' "$output" | grep -Eiq 'parent.{0,100}(owns|creates|makes).{0,80}commit'
}

if [[ "${ORACLE_SELF_TEST:-0}" == "1" ]]; then
    matcher_linear 'The same agent continues the linear chain.' || exit 1
    ! matcher_linear 'Spawn every node, including a linear successor.' || exit 1
    matcher_fork 'Dispatch both branches and wait for verified predecessors before the join.' || exit 1
    ! matcher_fork 'Dispatch both branches, then execute the join while branches are incomplete.' || exit 1
    matcher_capacity 'Checkpoint state, release its slot, then a continuation reconstructs and resumes.' || exit 1
    ! matcher_capacity 'Keep the parent process alive and waiting in its capacity slot.' || exit 1
    matcher_failure 'The healthy sibling continues; block the join and retry only the failed branch.' || exit 1
    ! matcher_failure 'Stop every sibling and run the join despite the failed branch.' || exit 1
    matcher_git_ownership 'The branch worker must not stage or commit; the parent owns the aggregate commit.' || exit 1
    ! matcher_git_ownership 'The branch worker stages and commits quickly; the parent observes it.' || exit 1
    echo 'PASS: graph-development matcher oracle self-test'
    exit 0
fi

if ! command -v claude >/dev/null 2>&1; then
    echo 'SKIP: Claude CLI unavailable; run ORACLE_SELF_TEST=1 for deterministic matcher coverage.'
    exit 0
fi

run_scenario() {
    local name="$1"
    local prompt="$2"
    local matcher="$3"
    local output

    echo "=== $name ==="
    output=$(run_claude "$prompt" 90)
    if "$matcher" "$output"; then
        echo "PASS: $name"
    else
        echo "FAIL: $name"
        echo "$output"
        return 1
    fi
}

run_scenario 'Linear continuation' \
    'A validated graph has A -> B -> C, no forks. Explain dispatch. Require the same branch agent to continue through the chain; do not spawn one agent per node.' \
    matcher_linear
run_scenario 'Two-way fork' \
    'A validated graph forks into left and right, then joins at merge. Explain dispatch and join timing. Both branches must be dispatched and the parent must not execute merge early.' \
    matcher_fork
run_scenario 'Nested capacity fork' \
    'All agent slots are occupied when a nested fork is reached. Explain how the logical parent avoids a live waiting dependency and later resumes its join.' \
    matcher_capacity
run_scenario 'Failed branch recovery' \
    'One branch fails while its sibling is healthy. Explain sibling handling, strict join gate, and retry scope.' \
    matcher_failure
run_scenario 'Deadline Git ownership' \
    'Under deadline pressure, explain which agent may stage and commit branch changes and which agent owns the aggregate commit.' \
    matcher_git_ownership

echo 'PASS: graph-development behavioral pressure scenarios'
