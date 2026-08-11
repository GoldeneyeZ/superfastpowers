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
