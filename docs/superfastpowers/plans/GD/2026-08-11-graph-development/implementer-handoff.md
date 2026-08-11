# Graph Development Integration Repair Handoff

Source review: `final-review.md`

Reviewed range: `c6ce26b^..374bd18`

## Findings

1. Important — deterministic validation does not reject dirty graph-owned repository paths before dispatch or topology changes made after execution starts without downstream invalidation. A fresh dirty-path probe returned no validation errors.
2. Important — `tests/claude-code/test-graph-development-static.sh` is tracked non-executable, so the registered runner changes its file mode and leaves the checkout dirty during verification.

## Repair Scope

- `skills/graph-development/scripts/validate_graph.py`
- `tests/graph-development/test_validate_graph.py`
- Graph-state/preflight contract files only where needed to record and deterministically detect topology invalidation
- `tests/claude-code/test-graph-development-static.sh` file mode
- `tests/claude-code/run-skill-tests.sh` only if clean execution cannot be achieved by tracking the test as executable
- Task context/eval evidence only where required to record repair and fresh results

Do not change structured fork/join semantics, review ordering, branch Git ownership, graph artifact authority, or unrelated skills.

## Re-review Acceptance

- A valid committed package with any graph-owned path dirty fails preflight with a stable error and nonzero CLI exit.
- Clean packages remain valid in JSON, Markdown, and mirrored modes.
- A topology change after execution starts fails unless affected downstream state is explicitly invalidated; automated tests cover both rejection and accepted invalidation.
- Fresh `bash tests/claude-code/run-skill-tests.sh` leaves `git status --short` unchanged.
- Validator unit tests, static contracts, matcher oracle, shell syntax, full registered runner, plugin sync, skill validation, and whitespace checks pass freshly.
- Claude CLI unavailability remains reported without claiming Claude behavioral coverage.

## Invalidation and Gate Reruns

- Reopen plan implementation for scoped repair.
- Specification review: unchecked after repair.
- Code quality: unchecked after repair.
- Integration review: failed, then unchecked after repair.
- Goal remains incomplete.
- Rerun specification review, code-quality review, then final integration review in order.

---

# Prior Code Quality Repair Handoff

Source review: `code-quality.md`

Reviewed range: `e8194a9..a68889b`

## Findings

1. Important — non-canonical aliases such as `src/shared.py` and `src//shared.py` bypass concurrent write-overlap detection in `skills/graph-development/scripts/validate_graph.py:329`-`333`, `438`-`446`, and `527`-`531`.
2. Important — all five behavioral matchers in `tests/claude-code/test-graph-development.sh:9`-`38` accept confirmed wrong or contradictory answers, while the scenarios at lines 77-91 disclose expected behavior.

## Re-review Addendum

The write-path alias finding is repaired. The behavioral repair remains incomplete: `matcher_fork` accepts `Both branches must never be dispatched; run them serially.`, and `matcher_failure` accepts `The healthy sibling cannot continue; block merge then rerun only the failed branch.` Both are wrong decisions and both return success in fresh isolated matcher probes.

## Repair Scope

- `skills/graph-development/scripts/validate_graph.py`
- `tests/graph-development/test_validate_graph.py`
- `tests/claude-code/test-graph-development.sh`
- Task context/eval evidence only where required to record the repair and fresh results

The path repair is accepted. Strengthen behavioral scenarios and matchers without weakening positive paraphrase support. Do not change Graph Development topology, review policy, Git ownership, or unrelated skills.

## Re-review Acceptance

- Parallel branches owning `src/shared.py` and `src//shared.py` fail validation with a stable ownership/path error.
- Equivalent leading-`./` alias fails validation.
- Existing valid JSON, Markdown, and mirrored packages remain valid.
- Each confirmed wrong/contradictory matcher probe from `code-quality.md` fails.
- `Both branches must never be dispatched; run them serially.` fails `matcher_fork`.
- `The healthy sibling cannot continue; block merge then rerun only the failed branch.` fails `matcher_failure`.
- Positive matcher fixtures covering normal paraphrases pass.
- Behavioral prompts describe situations without instructing the expected execution decision.
- Validator unit tests, static contract, oracle self-test, shell syntax, plugin sync, and whitespace checks pass freshly.

## Invalidation and Gate Reruns

- Keep implementation incomplete at plan level while repair runs.
- Code quality: failed; rerun after repair.
- Integration review: unchecked and blocked.
- Spec review remains checked because findings do not change specified behavior.
- Preserve this handoff and `code-quality.md` failure history through accepted re-review.
