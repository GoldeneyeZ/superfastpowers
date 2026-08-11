# Graph Development Spec Review

Result: failed

Reviewed range: `e8194a9..539f11a`

## Findings

### Important — the registered static test cannot run without Claude

GD-6 requires the static Graph Development test to remain mandatory while only the optional behavioral harness may skip. `tests/claude-code/run-skill-tests.sh:18-23` exits before test selection whenever `claude` is absent, so the registered static test at lines 81-82 never runs. Fresh execution returned exit 1 with `ERROR: Claude Code CLI not found`. This contradicts `tasks/GD-6/task.md` Step 1 and makes the no-harness contract unreachable through the repository runner.

### Important — graph ownership is not checked against task declarations

The approved design requires validation to reject graph ownership inconsistent with task-package declarations (`docs/superfastpowers/specs/2026-08-11-graph-development-design.md:156`). `validate_graph.py:370-396` verifies the task path exists and validates the graph's own `writes` list, but never reads the task's `**Files:**` declarations. A package whose task declared `src/task.py` while its graph owned `src/graph.py` returned `[]`. The unit fixture reinforces the gap by writing only `# Task` (`tests/graph-development/test_validate_graph.py:72-76`) and accepting it as valid.

### Important — Markdown graph metadata omits the required format

The approved Markdown contract requires version, format, and source metadata (`docs/superfastpowers/specs/2026-08-11-graph-development-design.md:112-117`). `render_markdown()` emits only Version and Source (`validate_graph.py:154-159`), and `parse_markdown()` requires only those two fields (`validate_graph.py:233-242`). Consequently an artifact missing required Format metadata is generated and accepted.

### Important — failed reviews do not create the specified implementation handoff

The approved review policy says a failed review creates an implementation handoff before invalidation and gate reruns (`docs/superfastpowers/specs/2026-08-11-graph-development-design.md:230`). The graph skill mentions reopening and invalidation, and the branch prompt says to resolve findings, but no Graph Development skill or prompt defines or writes an implementer handoff. This loses the durable repair brief and re-review acceptance criteria needed when the reviewing agent is replaced.

### Minor — three task contexts retain stale pending commit headers

`tasks/GD-1/context.md`, `tasks/GD-2/context.md`, and `tasks/GD-4/context.md` still say `Commit SHA: Pending until task completion` even though their completion sections record implementation commits. The detailed evidence is present, but the reviewer map is internally stale.

## Coverage Evidence

- Structured nested sequence/parallel flow, node/package mapping, duplicate/unreachable references, join placement/reuse, and concurrent write overlap are implemented and unit-tested.
- JSON, Markdown-only, and mirrored modes validate in an independent probe; mirror mismatch blocks.
- Planning exposes Graph Development, all three artifact modes, both review modes, finer decomposition guidance, exact write ownership, Graph State fields, and validator handoff.
- Branch and continuation contracts preserve linear-agent continuity, stop workers before joins, checkpoint/release parents under capacity pressure, reconstruct from durable state, block partial joins, preserve healthy siblings, retry failed branches only, and reserve commits for logical parents.
- Eval evidence contains three isolated RED and three GREEN sessions with raw behavior and honest harness metadata. No Claude behavior is claimed.
- README and plugin synchronization expose the skill without making it the default execution workflow.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests/graph-development/test_validate_graph.py -v` — 18 passed.
- `bash tests/claude-code/test-graph-development-static.sh` — 49 assertions passed.
- `ORACLE_SELF_TEST=1 bash tests/claude-code/test-graph-development.sh` — passed.
- `python3 /home/goldeneye/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/graph-development` — `Skill is valid!`.
- `bash tests/codex-plugin-sync/test-sync-to-codex-plugin.sh` — passed.
- `bash -n tests/claude-code/run-skill-tests.sh tests/claude-code/test-graph-development-static.sh tests/claude-code/test-graph-development.sh` — passed.
- `git diff --check` — passed before review artifacts.
- `bash tests/claude-code/run-skill-tests.sh` — failed before running tests because Claude CLI is unavailable; this is Finding 1, not an unavailable behavioral-runner skip.
- Independent mode probe — `json`, `markdown`, and `both` each returned no validation errors.
- Independent ownership-mismatch probe — returned no validation errors; this is Finding 2.

## Next Action

Apply `implementer-handoff.md`, then rerun plan-scoped specification review before code-quality review.
