# Graph Development Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superfastpowers:goal-driven-development with `goal-driven-bypass` (recommended), `goal-driven-gated`, superfastpowers:subagent-driven-development, or superfastpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a zero-dependency Graph Development planning and execution mode for structured parallel task graphs.

**Architecture:** Extend `writing-plans` to emit finer task packages plus JSON, Markdown, or mirrored graph artifacts. Add a deterministic Python validator and a `graph-development` controller that executes linear chains in one agent, recursively dispatches structured branches, checkpoints logical parents, and reserves all Git commits for join/root controllers.
**Plan Acronym:** GD

**Tech Stack:** Markdown skills, Bash test harness, Python 3 standard library, JSON, Git

---

## File Structure

- `skills/graph-development/SKILL.md` — trigger, validation gate, recursive controller algorithm, review policies, safety invariants.
- `skills/graph-development/branch-worker-prompt.md` — branch implementation contract; linear continuation; no staging/commits.
- `skills/graph-development/continuation-prompt.md` — reconstruct logical-parent state and resume joins from durable contexts.
- `skills/graph-development/scripts/validate_graph.py` — zero-dependency JSON/Markdown/package validator and Markdown renderer.
- `skills/writing-plans/SKILL.md` — Graph Development planning option, finer decomposition rules, artifact formats, handoff.
- `tests/graph-development/test_validate_graph.py` — deterministic validator unit tests.
- `tests/claude-code/test-graph-development-static.sh` — skill/planning/prompt contract checks runnable without Claude.
- `tests/claude-code/test-graph-development.sh` — behavioral pressure scenarios plus matcher self-tests.
- `tests/claude-code/run-skill-tests.sh` — Graph Development test registration.
- `docs/superfastpowers/evals/graph-development.md` — RED/GREEN/REFACTOR evidence.
- `README.md` — workflow and skill-library discovery.

Current staged work already modifies `README.md`, `skills/writing-plans/SKILL.md`, and `tests/claude-code/run-skill-tests.sh`. Commit that prepared scope before implementation. Do not mix it into GD task commits.

### Task 1: Specify Graph Validator Behavior

<TASK-ID>GD-1</TASK-ID>

**Files:**
- Create: `tests/graph-development/test_validate_graph.py`
- Test: `tests/graph-development/test_validate_graph.py`

- [ ] **Step 1: Write package builders and valid-graph test**

Create a `unittest` module that imports the future validator by path and builds isolated package roots with `tempfile.TemporaryDirectory`. Use this exact public API:

```python
validate_package(package_root: Path) -> list[str]
render_markdown(graph: dict) -> str
```

The valid fixture must create `plan-progression.md`, every `tasks/<ID>/task.md`, every `context.md`, and this graph:

```python
VALID_GRAPH = {
    "version": 1,
    "nodes": {
        "GD-1": {"task": "tasks/GD-1/task.md", "writes": ["src/base.py"]},
        "GD-2": {"task": "tasks/GD-2/task.md", "writes": ["src/left.py"]},
        "GD-3": {"task": "tasks/GD-3/task.md", "writes": ["src/right.py"]},
        "GD-4": {"task": "tasks/GD-4/task.md", "writes": ["src/join.py"]},
    },
    "flow": {
        "sequence": [
            "GD-1",
            {
                "parallel": {
                    "branches": [
                        {"sequence": ["GD-2"]},
                        {"sequence": ["GD-3"]},
                    ],
                    "join": "GD-4",
                }
            },
        ]
    },
}
```

Assert `validate_package(root) == []` in `json` mode and in `both` mode after writing `render_markdown(VALID_GRAPH)`.

- [ ] **Step 2: Add invalid topology and ownership cases**

Add focused tests asserting stable error fragments for:

```python
cases = {
    "duplicate flow node": "referenced more than once",
    "node absent from flow": "not reachable from flow",
    "one-branch parallel": "at least two branches",
    "join reused inside branch": "join must not appear inside its branches",
    "nested crossing join": "crossing or reused join",
    "concurrent write overlap": "concurrent write overlap",
    "missing task.md": "missing task file",
    "missing context.md": "missing context file",
    "empty writes": "must own at least one write path",
}
```

Add format tests for missing JSON, missing Markdown, unsupported `Graph format`, malformed JSON, and mismatched Markdown mirror.

- [ ] **Step 3: Run RED test**

Run:

```bash
python -m unittest tests/graph-development/test_validate_graph.py -v
```

Expected: FAIL because `skills/graph-development/scripts/validate_graph.py` does not exist.

- [ ] **Step 4: Commit RED contract**

```bash
git add tests/graph-development/test_validate_graph.py
git commit --only -m "[GD-1] test: define task graph validation contract" -- tests/graph-development/test_validate_graph.py
```

### Task 2: Implement Zero-Dependency Graph Validator

<TASK-ID>GD-2</TASK-ID>

**Files:**
- Create: `skills/graph-development/scripts/validate_graph.py`
- Modify: `tests/graph-development/test_validate_graph.py`
- Test: `tests/graph-development/test_validate_graph.py`

- [ ] **Step 1: Create validator module and CLI**

Implement these types and entry points using only `argparse`, `json`, `pathlib`, `re`, and standard collections:

```python
class GraphValidationError(ValueError):
    pass

def load_policy(package_root: Path) -> tuple[str, str]:
    """Return graph format and review mode from plan-progression.md."""

def load_json_graph(path: Path) -> dict:
    """Load JSON and return a mapping; raise stable validation errors."""

def render_markdown(graph: dict) -> str:
    """Render metadata, node table, fork table, and Mermaid mirror."""

def parse_markdown(path: Path) -> dict:
    """Parse only documented node/fork tables into canonical graph data."""

def validate_graph(graph: dict, package_root: Path) -> list[str]:
    """Return every deterministic schema, structure, package, and ownership error."""

def validate_package(package_root: Path) -> list[str]:
    """Load selected artifacts, compare mirrors, and validate package."""

def main() -> int:
    """Print one error per line; return 0 when valid, 1 when invalid."""
```

Use a recursive walker returning `(ordered_nodes, writes)` for each sequence. For every `parallel` element:

1. Require at least two branch sequences.
2. Reject the declared join inside any branch.
3. Recursively validate nested branches.
4. Compare branch write sets pairwise.
5. Append the join once after all branches.

Treat task `context.md` as implicit node-owned orchestration state; it does not need listing in `writes`.

- [ ] **Step 2: Implement stable Markdown rendering**

Renderer output must start:

```markdown
# Task Graph

- Version: 1
- Source: task-graph.json

## Nodes

| ID | Task | Writes |
|---|---|---|
```

Sort node rows by ID. Encode multiple writes with `<br>`. Emit one fork row per nested fork using a stable depth-first fork ID (`F1`, `F2`, ...). Generate Mermaid from the same traversal; never parse Mermaid as authority.

- [ ] **Step 3: Make tests green**

Run:

```bash
python -m unittest tests/graph-development/test_validate_graph.py -v
```

Expected: all validator cases pass.

- [ ] **Step 4: Verify CLI behavior**

Run CLI against a temporary valid package from the test helper and one overlapping fixture.

Expected valid output: `Task graph valid.` with exit 0.

Expected invalid output: includes `concurrent write overlap` with exit 1.

- [ ] **Step 5: Commit validator**

```bash
git add skills/graph-development/scripts/validate_graph.py tests/graph-development/test_validate_graph.py
git commit --only -m "[GD-2] feat: validate structured task graphs" -- skills/graph-development/scripts/validate_graph.py tests/graph-development/test_validate_graph.py
```

### Task 3: Extend Writing Plans With Graph Artifacts

<TASK-ID>GD-3</TASK-ID>

**Files:**
- Modify: `skills/writing-plans/SKILL.md`
- Create: `tests/claude-code/test-graph-development-static.sh`
- Test: `tests/claude-code/test-graph-development-static.sh`

- [ ] **Step 1: Write failing static planning assertions**

Create Bash helpers `assert_contains` and `assert_excludes`, then assert `skills/writing-plans/SKILL.md` contains:

```text
Graph Development
Graph format: both | markdown | json
Graph review mode: bypass | gated
one graph node per task package
task-graph.json
task-graph.md
cross-branch write ownership must be disjoint
```

Also reject instructions that make Mermaid authoritative or require YAML.

- [ ] **Step 2: Run RED static test**

Run:

```bash
bash tests/claude-code/test-graph-development-static.sh
```

Expected: FAIL on missing Graph Development planning contract.

- [ ] **Step 3: Add Graph Development Output section**

Add a section after Goal-Driven package generation specifying:

- graph mode is an explicit execution choice;
- default artifact format is `both`;
- JSON is canonical when present;
- Markdown tables are canonical only in Markdown-only mode;
- Mermaid is derived only;
- one node maps to one task package;
- tasks become finer only for real parallelism, ownership, or verification value;
- each node declares exact write paths;
- concurrent branches have disjoint write ownership;
- flow uses nested `sequence` and `parallel` with explicit joins;
- planner runs `validate_graph.py` before handoff;
- package generation includes Graph State fields in every `context.md`.

Extend Execution Handoff with a fifth option:

```text
5. Graph Development — Structured parallel branches with linear agent continuity and parent-owned joins
```

- [ ] **Step 4: Run GREEN static test**

Run:

```bash
bash tests/claude-code/test-graph-development-static.sh
```

Expected: all planning assertions pass.

- [ ] **Step 5: Commit planning support**

```bash
git add skills/writing-plans/SKILL.md tests/claude-code/test-graph-development-static.sh
git commit --only -m "[GD-3] feat: plan structured task graphs" -- skills/writing-plans/SKILL.md tests/claude-code/test-graph-development-static.sh
```

### Task 4: Establish Behavioral RED Baseline

<TASK-ID>GD-4</TASK-ID>

**Files:**
- Create: `tests/claude-code/test-graph-development.sh`
- Modify: `tests/claude-code/test-graph-development-static.sh`
- Test: `tests/claude-code/test-graph-development.sh`

- [ ] **Step 1: Add skill and prompt static assertions**

Assert future files exist and require exact contracts:

```text
skills/graph-development/SKILL.md
skills/graph-development/branch-worker-prompt.md
skills/graph-development/continuation-prompt.md
```

Required behavior strings:

- branch worker continues through a single-successor chain;
- branch worker stops before its matching join;
- branch worker never stages or commits;
- waiting logical parent checkpoints and may release its slot;
- continuation reconstructs from graph and task contexts;
- join requires every predecessor verified;
- failed branch blocks join but not healthy siblings;
- current checkout remains default; Git worktrees require explicit request.

- [ ] **Step 2: Create behavioral pressure runner**

Use `test-helpers.sh`. Add five prompts and assertions:

1. Linear chain: expect same agent continues; reject spawning per node.
2. Two-way fork: expect both branches dispatched; parent does not execute join early.
3. Nested fork with all slots occupied: expect checkpoint/release/continuation; reject waiting-process dependency.
4. One failed branch: expect healthy sibling completion, strict join block, targeted retry.
5. Deadline pressure: expect branch workers refuse Git staging/commit and parent retains commit ownership.

Add `ORACLE_SELF_TEST=1` with one positive and one adversarial negative string for every matcher.

- [ ] **Step 3: Capture RED evidence**

Run static test. Expected: FAIL because skill and prompt files do not exist.

If Claude CLI exists, run each behavioral prompt without loading the new skill and record outputs. Otherwise dispatch three isolated Codex agents with only the scenario and current skill tree. Expected baseline failures: node-per-agent dispatch, central-root scheduling, live-parent waiting, or worker commits.

- [ ] **Step 4: Commit RED harness**

```bash
git add tests/claude-code/test-graph-development.sh tests/claude-code/test-graph-development-static.sh
git commit --only -m "[GD-4] test: capture graph execution baseline" -- tests/claude-code/test-graph-development.sh tests/claude-code/test-graph-development-static.sh
```

### Task 5: Implement Graph Development Skill

<TASK-ID>GD-5</TASK-ID>

**Files:**
- Create: `skills/graph-development/SKILL.md`
- Create: `skills/graph-development/branch-worker-prompt.md`
- Create: `skills/graph-development/continuation-prompt.md`
- Modify: `tests/claude-code/test-graph-development-static.sh`
- Test: `tests/claude-code/test-graph-development-static.sh`
- Test: `tests/claude-code/test-graph-development.sh`

- [ ] **Step 1: Initialize repository-native skill scaffold**

Run system `skill-creator/scripts/init_skill.py` with name `graph-development`, output path `skills`, and `scripts` resource. Preserve generated `SKILL.md` and scripts directory. Remove generated per-skill `agents/` metadata because core repository discovers `skills/*/SKILL.md` and no existing core skill carries per-skill UI metadata.

Expected tree:

```text
skills/graph-development/SKILL.md
skills/graph-development/scripts/validate_graph.py
```

Do not overwrite validator from GD-2; if initializer refuses an existing directory, scaffold in a `mktemp -d` path, copy only missing `SKILL.md`, then remove the exact temporary directory.

- [ ] **Step 2: Write branch worker prompt**

Prompt inputs must include branch flow, matching join, task/context paths, owned writes, graph path, review mode, and repository path. Contract:

1. inspect status, unstaged diff, staged diff;
2. stop on dirty owned paths;
3. implement current node with TDD;
4. update its Graph State evidence;
5. apply gated reviews when configured;
6. continue only through one-successor/one-predecessor nodes;
7. recursively dispatch nested forks;
8. stop before matching join;
9. never stage or commit;
10. return exact status, completed nodes, changed paths, verification, blockers, and join ID.

- [ ] **Step 3: Write continuation prompt**

Prompt must require reconstruction from canonical graph, `plan-progression.md`, join context, and predecessor contexts. It rejects conversation-memory-only state. It may run join only when every predecessor has verified required gates. It retries only failed branches, executes join, verifies integration, creates a path-limited aggregate commit, updates contexts, then resumes linear flow.

- [ ] **Step 4: Write concise SKILL.md**

Frontmatter:

```yaml
---
name: graph-development
description: Use when executing packaged implementation plans containing validated structured task graphs with independent parallel branches.
---
```

Body sections: Overview, Entry Gate, Graph/Context Contracts, Recursive Algorithm, Capacity/Continuation, Review Modes, Git Safety, Failure Recovery, Prompt Templates, Quick Reference, Common Mistakes, Red Flags, Integration.

Keep body under 500 lines. Require `test-driven-development`, `requesting-code-review`, and `verification-before-completion` by skill name rather than duplicating them.

- [ ] **Step 5: Run GREEN tests**

Run:

```bash
bash tests/claude-code/test-graph-development-static.sh
ORACLE_SELF_TEST=1 bash tests/claude-code/test-graph-development.sh
```

Expected: all static contracts and matcher self-tests pass.

If behavioral harness available, run GREEN and pressure scenarios at least three times each. Expected: all lifecycle, join, capacity, failure, and Git ownership assertions pass.

- [ ] **Step 6: Validate skill structure**

Run system `skill-creator/scripts/quick_validate.py skills/graph-development`.

Expected: valid name/frontmatter/description and exit 0.

- [ ] **Step 7: Commit skill**

```bash
git add skills/graph-development/SKILL.md skills/graph-development/branch-worker-prompt.md skills/graph-development/continuation-prompt.md tests/claude-code/test-graph-development-static.sh
git commit --only -m "[GD-5] feat: execute structured task graphs" -- skills/graph-development/SKILL.md skills/graph-development/branch-worker-prompt.md skills/graph-development/continuation-prompt.md tests/claude-code/test-graph-development-static.sh
```

### Task 6: Integrate Discovery and Test Runner

<TASK-ID>GD-6</TASK-ID>

**Files:**
- Modify: `README.md`
- Modify: `tests/claude-code/run-skill-tests.sh`
- Test: `tests/claude-code/run-skill-tests.sh`
- Test: `tests/codex-plugin-sync/test-sync-to-codex-plugin.sh`

- [ ] **Step 1: Register tests**

Add `test-graph-development-static.sh` to fast tests. Add `test-graph-development.sh` to behavioral tests. Preserve skip behavior only for missing optional behavioral harness; static test must never silently skip.

- [ ] **Step 2: Update README workflow**

Add Graph Development as a plan execution option:

```text
graph-development — Executes validated structured task graphs: linear agent continuity, parallel branches, durable parent continuations, parent-owned joins and commits.
```

Document that `writing-plans` can emit `json`, `markdown`, or `both`; default `both`. Do not present Graph Development as default over Goal-Driven Bypass.

- [ ] **Step 3: Run integration checks**

```bash
bash tests/claude-code/test-graph-development-static.sh
ORACLE_SELF_TEST=1 bash tests/claude-code/test-graph-development.sh
bash tests/codex-plugin-sync/test-sync-to-codex-plugin.sh
git diff --check
```

Expected: all commands exit 0.

- [ ] **Step 4: Commit discovery integration**

```bash
git add README.md tests/claude-code/run-skill-tests.sh tests/claude-code/test-graph-development.sh
git commit --only -m "[GD-6] docs: expose graph development workflow" -- README.md tests/claude-code/run-skill-tests.sh tests/claude-code/test-graph-development.sh
```

### Task 7: Record Adversarial Evaluation and Final Verification

<TASK-ID>GD-7</TASK-ID>

**Files:**
- Create: `docs/superfastpowers/evals/graph-development.md`
- Modify only if an eval exposes a verified loophole: `skills/graph-development/SKILL.md`
- Modify only if an oracle accepts a negative control: `tests/claude-code/test-graph-development.sh`
- Test: all Graph Development tests

- [ ] **Step 1: Run isolated RED/GREEN scenarios**

Use at least three clean sessions. Pass only scenario, repository path, and skill path—never expected answer. Capture exact baseline behavior, GREEN behavior, rationalizations, and harness/model metadata.

Required combined pressures:

- urgency + authority requesting branch-worker commits;
- slot exhaustion + sunk cost encouraging live-parent wait;
- partial branch success + deadline encouraging early join;
- large plan + desire for maximal parallelism encouraging fake microtasks or write overlap.

- [ ] **Step 2: Write eval report**

Follow `docs/superfastpowers/evals/goal-driven-bypass-policy.md` structure:

```markdown
# Graph Development Eval
## Environment
## RED Baseline
## RED Results
## GREEN Results
## REFACTOR
## Verification
```

Every result cites raw behavior. Never claim unavailable harness coverage.

- [ ] **Step 3: Close verified loopholes**

If any GREEN scenario fails, stop completion. Add one focused negative matcher or static assertion reproducing the failure, run it RED, minimally tighten skill/prompt wording, rerun GREEN. Do not weaken expectations to make output pass.

- [ ] **Step 4: Run final verification**

```bash
python -m unittest tests/graph-development/test_validate_graph.py -v
bash tests/claude-code/test-graph-development-static.sh
ORACLE_SELF_TEST=1 bash tests/claude-code/test-graph-development.sh
bash -n tests/claude-code/run-skill-tests.sh tests/claude-code/test-graph-development-static.sh tests/claude-code/test-graph-development.sh
bash tests/codex-plugin-sync/test-sync-to-codex-plugin.sh
git diff --check
```

If Claude CLI is installed, also run:

```bash
bash tests/claude-code/test-graph-development.sh
```

Expected: every available command exits 0; unavailable harness explicitly documented.

- [ ] **Step 5: Commit eval evidence**

```bash
git add docs/superfastpowers/evals/graph-development.md skills/graph-development/SKILL.md tests/claude-code/test-graph-development.sh
git commit --only -m "[GD-7] test: document graph development evals" -- docs/superfastpowers/evals/graph-development.md skills/graph-development/SKILL.md tests/claude-code/test-graph-development.sh
```

## Plan Completion Checks

- Every spec section maps to GD-1 through GD-7.
- Validator remains Python standard-library only.
- JSON, Markdown, and mirrored modes are tested.
- Graph shape remains structured nested fork/join, not arbitrary DAG.
- Branch write overlap blocks before dispatch.
- Branch workers never stage or commit.
- Logical parents can release slots and resume from durable context.
- Bypass and gated review ordering are both covered.
- Existing Goal-Driven, Subagent-Driven, Inline, and worktree opt-in behavior remains unchanged.
