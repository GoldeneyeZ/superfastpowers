#!/usr/bin/env bash
# Behavioral pressure test for Graph Development.  The static companion keeps
# the required contracts deterministic; this script exercises their wording.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/test-helpers.sh"

matcher_linear() {
    local output="$1"
    printf '%s' "$output" | grep -Eiq '(same|one) (agent|worker).{0,100}(continue|through|handles?| on )|continue.{0,80}(same|one) (agent|worker)|single-successor' \
        && ! printf '%s' "$output" | grep -Eiq '(do not|don.t|must not|never).{0,80}(same (agent|worker)|continue.{0,40}(linear|chain))|same (agent|worker).{0,40}(do not|don.t|must not|never).{0,40}continue' \
        && ! printf '%s' "$output" | grep -Eiq 'spawn.{0,80}(each|every).{0,40}node'
}

matcher_fork() {
    local output="$1"
    printf '%s' "$output" | grep -Eiq '(dispatch|spawn).{0,80}(both|two).{0,80}branch|both.{0,80}branch.{0,80}(dispatch|spawn)' \
        && ! printf '%s' "$output" | grep -Eiq '(do not|don.t|must not|never).{0,60}(dispatch|spawn).{0,80}(both|two).{0,40}branch|(leave|keep).{0,40}(left|right|one).{0,40}branch.{0,40}(idle|undispatched)' \
        && ! printf '%s' "$output" | grep -Eiq '(run|execute).{0,80}join.{0,80}(before|while).{0,80}(branch|predecessor).{0,80}(complete|verified)'
}

matcher_capacity() {
    local output="$1"
    printf '%s' "$output" | grep -Eiq '(checkpoint|save|saving).{0,120}(state|progress)' \
        && printf '%s' "$output" | grep -Eiq '(release|free).{0,80}(slot|capacity)|((slot|capacity).{0,80}(release|free))' \
        && printf '%s' "$output" | grep -Eiq '(continuation|another (agent|worker)).{0,160}(resume|reconstruct)|(resume|reconstruct).{0,160}(continuation|another (agent|worker))' \
        && ! printf '%s' "$output" | grep -Eiq '(do not|don.t|must not|never).{0,80}(checkpoint|save|saving|release|free)' \
        && ! printf '%s' "$output" | grep -Eiq '(keep|leave).{0,80}(parent|process).{0,80}(waiting|alive).{0,80}(slot|capacity)'
}

matcher_failure() {
    local output="$1"
    printf '%s' "$output" | grep -Eiq '(healthy|other|sibling).{0,80}(complete|continue|finish)|(let|allow).{0,40}(healthy|other|sibling).{0,80}(complete|continue|finish)' \
        && printf '%s' "$output" | grep -Eiq '(block|hold|do not run|cannot run).{0,80}(join|merge)' \
        && printf '%s' "$output" | grep -Eiq '(retry|rerun).{0,80}(failed|failing|failure).{0,80}branch' \
        && ! printf '%s' "$output" | grep -Eiq '(do not|don.t|must not|never).{0,80}(let|allow).{0,40}(healthy|other|sibling).{0,80}(complete|continue|finish)|(stop|cancel).{0,60}(healthy|other|sibling)'
}

matcher_git_ownership() {
    local output="$1"
    printf '%s' "$output" | grep -Eiq '(branch )?(worker|agent).{0,100}(never|must not|cannot|does not).{0,80}(stage|commit)|(worker|agent)s?.{0,80}leave git untouched' \
        && printf '%s' "$output" | grep -Eiq '(logical )?parent.{0,100}(owns|creates|makes).{0,80}(aggregate|combined)? ?commit' \
        && ! printf '%s' "$output" | grep -Eiq 'branch worker.{0,40}(stages|commits)|(it|worker|agent).{0,40}(stages|commits).{0,80}(anyway|itself|its branch)'
}

if [[ "${ORACLE_SELF_TEST:-0}" == "1" ]]; then
    matcher_linear 'The same agent continues the linear chain.' || exit 1
    matcher_linear 'Keep one worker on A, B, then C because each node has one successor.' || exit 1
    ! matcher_linear 'Spawn every node, including a linear successor.' || exit 1
    ! matcher_linear 'The same agent must not continue the linear chain.' || exit 1
    matcher_fork 'Dispatch both branches and wait for verified predecessors before the join.' || exit 1
    matcher_fork 'Spawn the two branch workers concurrently; merge runs only after both finish.' || exit 1
    ! matcher_fork 'Dispatch both branches, then execute the join while branches are incomplete.' || exit 1
    ! matcher_fork 'Do not dispatch both branches; leave the right branch idle.' || exit 1
    matcher_capacity 'Checkpoint state, release its slot, then a continuation reconstructs and resumes.' || exit 1
    matcher_capacity 'Free the parent capacity after saving state; another agent reconstructs the state and resumes.' || exit 1
    ! matcher_capacity 'Keep the parent process alive and waiting in its capacity slot.' || exit 1
    ! matcher_capacity 'Do not checkpoint or release the parent slot; a continuation can resume later.' || exit 1
    matcher_failure 'The healthy sibling continues; block the join and retry only the failed branch.' || exit 1
    matcher_failure 'Let the other branch finish, hold merge, then rerun the failing branch alone.' || exit 1
    ! matcher_failure 'Stop every sibling and run the join despite the failed branch.' || exit 1
    ! matcher_failure 'Do not let the healthy sibling complete; block the join and retry the failed branch.' || exit 1
    matcher_git_ownership 'The branch worker must not stage or commit; the parent owns the aggregate commit.' || exit 1
    matcher_git_ownership 'Workers leave Git untouched; their logical parent creates the combined commit.' || exit 1
    ! matcher_git_ownership 'The branch worker stages and commits quickly; the parent observes it.' || exit 1
    ! matcher_git_ownership 'The branch worker must not commit. It stages and commits its branch anyway; the parent owns the aggregate commit.' || exit 1
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
    'A validated graph has A -> B -> C with no forks. Explain how Graph Development assigns and advances this work.' \
    matcher_linear
run_scenario 'Two-way fork' \
    'A validated graph forks into left and right, then converges at merge. Explain assignment and merge timing under Graph Development.' \
    matcher_fork
run_scenario 'Nested capacity fork' \
    'All agent slots are occupied when a nested fork is reached. Explain how Graph Development handles parent state, capacity, and the eventual join.' \
    matcher_capacity
run_scenario 'Failed branch recovery' \
    'One branch fails while its sibling still has useful work. Explain what happens next and when their merge may run.' \
    matcher_failure
run_scenario 'Deadline Git ownership' \
    'Several branch agents share one checkout during a deadline. Explain how Graph Development handles Git operations.' \
    matcher_git_ownership

echo 'PASS: graph-development behavioral pressure scenarios'
