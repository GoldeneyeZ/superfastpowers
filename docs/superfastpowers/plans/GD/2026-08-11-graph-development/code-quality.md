# Graph Development Code Quality Review

Current result: failed

Initial reviewed range: `e8194a9..a68889b`

Re-review repair range: `08e07de..4fa637c`

Spec gate: checked (`spec-review.md`)

## Re-review Result

### Important — behavioral matcher still accepts wrong execution decisions

The repair covers the five originally observed phrases, but its keyword-proximity matchers still accept contradictions when negation or prohibition follows the subject rather than precedes the action. `tests/claude-code/test-graph-development.sh:18`-`20` accepts `Both branches must never be dispatched; run them serially.`: the positive `both branches ... dispatch` branch matches, while the negative expression only recognizes negation before `dispatch` or `spawn`. `tests/claude-code/test-graph-development.sh:34`-`37` likewise accepts `The healthy sibling cannot continue; block merge then rerun only the failed branch.` because its rejection cases omit `cannot`.

Fresh isolated matcher probes returned exit 0 for both wrong outputs. Neither is represented in the `ORACLE_SELF_TEST` cases at lines 52-67. This leaves the behavioral pressure test capable of reporting a pass for the opposite of two required Graph Development decisions.

Fix: make each matcher reject prohibited decisions regardless of subject/negation order, including `never` and `cannot`, then add these two probes to `ORACLE_SELF_TEST`. Retain the existing positive paraphrases and the five repaired negative probes.

## Re-review Verification Evidence

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests/graph-development/test_validate_graph.py -v` — 27 passed, including repeated-separator and leading-`./` alias rejection.
- `bash tests/claude-code/test-graph-development-static.sh` — passed all assertions.
- `ORACLE_SELF_TEST=1 bash tests/claude-code/test-graph-development.sh` — passed its current fixtures, but does not cover the two false positives above.
- `bash tests/claude-code/run-skill-tests.sh --test test-graph-development-static.sh` — 1 passed, 0 failed with Claude unavailable; static coverage remains mandatory.
- `bash -n tests/claude-code/test-graph-development-static.sh tests/claude-code/test-graph-development.sh tests/claude-code/run-skill-tests.sh` — passed.
- `git diff --check 4fa637c^..4fa637c` — passed.

## Initial Review History

Result: failed

Reviewed range: `e8194a9..a68889b`

## Important Findings

### Write-path aliases bypass concurrent ownership protection

`skills/graph-development/scripts/validate_graph.py:329`-`333` checks a `Path` for relative traversal but returns only a Boolean; `validate_graph` then stores and compares the original strings at lines 438-446 and 527-531. Lexically different paths that resolve to the same repository path therefore appear disjoint. A fresh probe assigned `src/shared.py` to one parallel branch and `src//shared.py` to its sibling; `validate_package` returned `[]`. `./src/shared.py` has the same problem. This defeats the validator's central protection against concurrent writes to one file.

Fix: normalize every accepted repository write path to one canonical repository-relative representation before declaration matching and overlap comparison, or reject non-canonical aliases. Add parallel-branch regression cases for repeated separators and leading `./`.

### Behavioral pressure test accepts explicitly wrong answers

`tests/claude-code/test-graph-development.sh:9`-`38` treats keyword proximity as proof of a correct execution decision and does not handle negation or contradictions. All five fresh negative probes returned success, including “Do not dispatch both branches,” “Do not checkpoint,” “Do not let the healthy sibling complete,” and an answer that first forbids then assigns a branch-worker commit. The self-test at lines 40-50 covers only one narrow negative wording per matcher. Additionally, scenario prompts at lines 77-91 state much of the expected answer, so a harness can pass by following the prompt without Graph Development behavior being responsible.

Fix: remove expected-answer instructions from behavioral scenarios; assert unambiguous decision clauses and reject negated/contradictory forms. Extend `ORACLE_SELF_TEST` with the five confirmed false-positive probes plus positive paraphrases. Keep the static contract test as deterministic coverage, but do not treat it as behavioral evidence.

## Strengths

- Validator schema/topology flow is cohesive, deterministic, standard-library-only, and locally understandable despite its breadth.
- Structured recursion makes join placement, reachability, reuse, and sibling write comparisons explicit.
- Skill and worker prompts use consistent domain terms for logical parents, continuations, gates, ownership, and repair handoffs.
- Unit fixtures cover JSON, Markdown, mirrored mode, package structure, declarations, topology, and common ownership failures.
- Graph-specific changes remain separated into a skill, prompt templates, validator, tests, and evidence artifact.

## Verification Evidence

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests/graph-development/test_validate_graph.py -v` — 25 tests passed.
- `bash tests/claude-code/test-graph-development-static.sh` — all assertions passed.
- `ORACLE_SELF_TEST=1 bash tests/claude-code/test-graph-development.sh` — passed its current fixtures.
- `bash -n tests/claude-code/test-graph-development-static.sh tests/claude-code/test-graph-development.sh tests/claude-code/run-skill-tests.sh` — passed.
- `bash tests/claude-code/run-skill-tests.sh --test test-graph-development-static.sh` — 1 passed, 0 failed; its temporary executable-bit change was reverted.
- Canonical-path probe (`src/shared.py` versus `src//shared.py`) — validator incorrectly returned no errors.
- Five deliberately wrong/contradictory matcher probes — all incorrectly returned exit 0.
- `git diff --check e8194a9..HEAD` — passed before review artifacts were written.

## Summary

Implementation structure and documentation are strong, but both discovered defects weaken core safety/evidence guarantees. Repair required before integration review.
