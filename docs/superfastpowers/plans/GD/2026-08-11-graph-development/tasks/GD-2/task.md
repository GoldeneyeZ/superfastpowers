### Task 2: Implement Zero-Dependency Graph Validator

<TASK-ID>GD-2</TASK-ID>

**Files:**
- Create: `skills/graph-development/scripts/validate_graph.py`
- Modify: `tests/graph-development/test_validate_graph.py`
- Test: `tests/graph-development/test_validate_graph.py`

- [ ] **Step 1: Create validator module and CLI**

Implement using only `argparse`, `json`, `pathlib`, `re`, and standard collections:

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
2. Reject declared join inside any branch.
3. Recursively validate nested branches.
4. Compare branch write sets pairwise.
5. Append join once after all branches.

Treat task `context.md` as implicit node-owned orchestration state; it need not appear in `writes`.

- [ ] **Step 2: Implement stable Markdown rendering**

Renderer starts:

```markdown
# Task Graph

- Version: 1
- Source: task-graph.json

## Nodes

| ID | Task | Writes |
|---|---|---|
```

Sort node rows by ID. Encode multiple writes with `<br>`. Emit one fork row per nested fork using stable depth-first fork ID (`F1`, `F2`, ...). Generate Mermaid from same traversal; never parse Mermaid as authority.

- [ ] **Step 3: Make tests green**

```bash
python -m unittest tests/graph-development/test_validate_graph.py -v
```

Expected: all validator cases pass.

- [ ] **Step 4: Verify CLI behavior**

Run CLI against temporary valid package from test helper and one overlapping fixture.

Expected valid output: `Task graph valid.` with exit 0.

Expected invalid output: includes `concurrent write overlap` with exit 1.

- [ ] **Step 5: Commit validator**

```bash
git add skills/graph-development/scripts/validate_graph.py tests/graph-development/test_validate_graph.py
git commit --only -m "[GD-2] feat: validate structured task graphs" -- skills/graph-development/scripts/validate_graph.py tests/graph-development/test_validate_graph.py
```
