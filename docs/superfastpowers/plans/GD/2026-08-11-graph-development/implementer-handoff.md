# Graph Development Code Quality Repair Handoff

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
