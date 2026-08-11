"""Contract tests for the graph-development validator."""

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = (
    REPOSITORY_ROOT / "skills/graph-development/scripts/validate_graph.py"
)


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_graph", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load validator from {VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VALIDATOR = load_validator()
validate_package = VALIDATOR.validate_package
render_markdown = VALIDATOR.render_markdown


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


class ValidateGraphContractTest(unittest.TestCase):
    def make_package(
        self,
        graph: dict,
        graph_format: str = "json",
        *,
        json_graph: dict | None = None,
        markdown: str | None = None,
        task_declarations: dict[str, str] | None = None,
    ) -> tempfile.TemporaryDirectory[str]:
        directory = tempfile.TemporaryDirectory()
        root = Path(directory.name)
        (root / "plan-progression.md").write_text(
            f"Graph format: {graph_format}\n", encoding="utf-8"
        )
        for node_id, node in graph.get("nodes", {}).items():
            task_file = root / node["task"]
            task_file.parent.mkdir(parents=True, exist_ok=True)
            declarations = "\n".join(
                f"- Modify: `{path}`" for path in node.get("writes", [])
            )
            if task_declarations and node_id in task_declarations:
                declarations = task_declarations[node_id]
            task_file.write_text(
                f"# Task\n\n**Files:**\n{declarations}\n\n- [ ] Step\n",
                encoding="utf-8",
            )
            (task_file.parent / "context.md").write_text("# Context\n", encoding="utf-8")
        if json_graph is not None:
            (root / "task-graph.json").write_text(
                json.dumps(json_graph), encoding="utf-8"
            )
        if markdown is not None:
            (root / "task-graph.md").write_text(markdown, encoding="utf-8")
        self.addCleanup(directory.cleanup)
        return directory

    def valid_package(self, graph_format: str) -> Path:
        directory = self.make_package(
            VALID_GRAPH,
            graph_format,
            json_graph=VALID_GRAPH if graph_format in {"json", "both"} else None,
            markdown=render_markdown(VALID_GRAPH)
            if graph_format in {"markdown", "both"}
            else None,
        )
        return Path(directory.name)

    def git(self, root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(root), *args],
            check=True,
            text=True,
            capture_output=True,
        )

    def commit_package(self, root: Path) -> None:
        self.git(root, "init", "-q")
        self.git(root, "config", "user.name", "Graph Test")
        self.git(root, "config", "user.email", "graph-test@example.invalid")
        for node in VALID_GRAPH["nodes"].values():
            owned_path = root / node["writes"][0]
            owned_path.parent.mkdir(parents=True, exist_ok=True)
            owned_path.write_text("clean\n", encoding="utf-8")
        self.git(root, "add", ".")
        self.git(root, "commit", "-qm", "fixture")

    def write_graph_state(
        self,
        root: Path,
        graph: dict,
        invalidated: list[str],
        statuses: dict[str, str],
    ) -> None:
        state = {
            "version": 1,
            "started": True,
            "topology": {
                "nodes": sorted(graph["nodes"]),
                "flow": graph["flow"],
            },
            "invalidated": invalidated,
        }
        (root / "graph-state.json").write_text(json.dumps(state), encoding="utf-8")
        for node_id, status in statuses.items():
            context = root / "tasks" / node_id / "context.md"
            context.write_text(
                "# Context\n\n## Graph State\n\n"
                f"Graph status: {status}\n"
                "Logical parent: root\n"
                "Changed paths: none\n"
                "Verification: none\n"
                "Checkpoint: none\n"
                "Failure: none\n"
                "Commit/range: pending\n",
                encoding="utf-8",
            )

    def replace_graph_artifacts(self, root: Path, graph: dict, graph_format: str) -> None:
        if graph_format in {"json", "both"}:
            (root / "task-graph.json").write_text(json.dumps(graph), encoding="utf-8")
        if graph_format in {"markdown", "both"}:
            (root / "task-graph.md").write_text(render_markdown(graph), encoding="utf-8")

    def assert_error(self, graph: dict, fragment: str) -> None:
        directory = self.make_package(graph, json_graph=graph)
        self.assertTrue(
            any(fragment in error for error in validate_package(Path(directory.name))),
            f"expected {fragment!r} in validation errors",
        )

    def test_valid_json_graph_has_no_errors(self) -> None:
        self.assertEqual(validate_package(self.valid_package("json")), [])

    def test_valid_both_graph_has_no_errors(self) -> None:
        self.assertEqual(validate_package(self.valid_package("both")), [])

    def test_valid_markdown_graph_has_no_errors(self) -> None:
        self.assertEqual(validate_package(self.valid_package("markdown")), [])

    def test_clean_committed_packages_pass_in_every_format(self) -> None:
        for graph_format in ("json", "markdown", "both"):
            with self.subTest(graph_format=graph_format):
                root = self.valid_package(graph_format)
                self.commit_package(root)
                self.assertEqual(validate_package(root), [])

    def test_rejects_dirty_graph_owned_path_with_stable_cli_error(self) -> None:
        root = self.valid_package("json")
        self.commit_package(root)
        (root / "src/base.py").write_text("dirty\n", encoding="utf-8")

        result = subprocess.run(
            ["python3", str(VALIDATOR_PATH), str(root)],
            check=False,
            text=True,
            capture_output=True,
        )

        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "dirty graph-owned path: src/base.py\n")

    def test_rejects_started_topology_change_without_downstream_invalidation(self) -> None:
        root = self.valid_package("json")
        self.write_graph_state(
            root,
            VALID_GRAPH,
            [],
            {"GD-1": "complete", "GD-2": "complete", "GD-3": "pending", "GD-4": "pending"},
        )
        changed = copy.deepcopy(VALID_GRAPH)
        changed["flow"]["sequence"] = ["GD-1", "GD-2", "GD-3", "GD-4"]
        self.replace_graph_artifacts(root, changed, "json")

        self.assertIn(
            "topology changed after execution started; downstream state not invalidated: GD-3, GD-4",
            validate_package(root),
        )

    def test_rejects_started_context_without_graph_state(self) -> None:
        root = self.valid_package("json")
        context = root / "tasks/GD-1/context.md"
        context.write_text(
            "# Context\n\n## Graph State\n\nGraph status: running\n",
            encoding="utf-8",
        )

        self.assertIn(
            "execution started but graph-state.json is missing",
            validate_package(root),
        )

    def test_accepts_started_topology_change_with_downstream_invalidation(self) -> None:
        root = self.valid_package("json")
        self.write_graph_state(
            root,
            VALID_GRAPH,
            ["GD-3", "GD-4"],
            {"GD-1": "complete", "GD-2": "complete", "GD-3": "pending", "GD-4": "pending"},
        )
        changed = copy.deepcopy(VALID_GRAPH)
        changed["flow"]["sequence"] = ["GD-1", "GD-2", "GD-3", "GD-4"]
        self.replace_graph_artifacts(root, changed, "json")

        self.assertEqual(validate_package(root), [])

    def test_rejects_invalidated_downstream_node_not_reset_to_pending(self) -> None:
        root = self.valid_package("json")
        self.write_graph_state(
            root,
            VALID_GRAPH,
            ["GD-3", "GD-4"],
            {"GD-1": "complete", "GD-2": "complete", "GD-3": "implemented", "GD-4": "pending"},
        )
        changed = copy.deepcopy(VALID_GRAPH)
        changed["flow"]["sequence"] = ["GD-1", "GD-2", "GD-3", "GD-4"]
        self.replace_graph_artifacts(root, changed, "json")

        self.assertIn(
            "topology-invalidated node GD-3 must have Graph status pending",
            validate_package(root),
        )

    def test_rejects_removed_started_node_without_explicit_invalidation(self) -> None:
        root = self.valid_package("json")
        previous = copy.deepcopy(VALID_GRAPH)
        previous["flow"]["sequence"] = ["GD-1", "GD-2", "GD-3", "GD-4"]
        self.write_graph_state(
            root,
            previous,
            [],
            {"GD-1": "complete", "GD-2": "complete", "GD-3": "complete", "GD-4": "complete"},
        )
        changed = copy.deepcopy(VALID_GRAPH)
        del changed["nodes"]["GD-4"]
        changed["flow"]["sequence"] = ["GD-1", "GD-2", "GD-3"]
        self.replace_graph_artifacts(root, changed, "json")

        self.assertIn(
            "topology changed after execution started; downstream state not invalidated: GD-4",
            validate_package(root),
        )

    def test_rejects_malformed_graph_state_topology_without_crashing(self) -> None:
        root = self.valid_package("json")
        malformed = {
            "version": 1,
            "started": True,
            "topology": {"nodes": [["GD-1"]], "flow": VALID_GRAPH["flow"]},
            "invalidated": [],
        }
        (root / "graph-state.json").write_text(
            json.dumps(malformed), encoding="utf-8"
        )

        self.assertIn(
            "graph state topology nodes must be unique node IDs",
            validate_package(root),
        )

    def test_rendered_markdown_declares_format(self) -> None:
        self.assertIn("- Format: markdown", render_markdown(VALID_GRAPH))

    def test_rejects_duplicate_flow_node(self) -> None:
        graph = copy.deepcopy(VALID_GRAPH)
        graph["flow"]["sequence"].append("GD-1")
        self.assert_error(graph, "referenced more than once")

    def test_rejects_node_absent_from_flow(self) -> None:
        graph = copy.deepcopy(VALID_GRAPH)
        graph["nodes"]["GD-5"] = {
            "task": "tasks/GD-5/task.md",
            "writes": ["src/unreachable.py"],
        }
        self.assert_error(graph, "not reachable from flow")

    def test_rejects_one_branch_parallel(self) -> None:
        graph = copy.deepcopy(VALID_GRAPH)
        graph["flow"]["sequence"][1]["parallel"]["branches"] = [
            {"sequence": ["GD-2"]}
        ]
        self.assert_error(graph, "at least two branches")

    def test_rejects_join_reused_inside_branch(self) -> None:
        graph = copy.deepcopy(VALID_GRAPH)
        graph["flow"]["sequence"][1]["parallel"]["branches"][0]["sequence"].append(
            "GD-4"
        )
        self.assert_error(graph, "join must not appear inside its branches")

    def test_rejects_nested_crossing_join(self) -> None:
        graph = copy.deepcopy(VALID_GRAPH)
        graph["nodes"]["GD-5"] = {
            "task": "tasks/GD-5/task.md",
            "writes": ["src/nested.py"],
        }
        graph["flow"]["sequence"][1]["parallel"]["branches"][0]["sequence"] = [
            {
                "parallel": {
                    "branches": [
                        {"sequence": ["GD-2"]},
                        {"sequence": ["GD-5"]},
                    ],
                    "join": "GD-4",
                }
            }
        ]
        self.assert_error(graph, "crossing or reused join")

    def test_rejects_concurrent_write_overlap(self) -> None:
        graph = copy.deepcopy(VALID_GRAPH)
        graph["nodes"]["GD-3"]["writes"] = ["src/left.py"]
        self.assert_error(graph, "concurrent write overlap")

    def test_rejects_repeated_separator_write_alias(self) -> None:
        graph = copy.deepcopy(VALID_GRAPH)
        graph["nodes"]["GD-2"]["writes"] = ["src/shared.py"]
        graph["nodes"]["GD-3"]["writes"] = ["src//shared.py"]
        self.assert_error(graph, "invalid write path: src//shared.py")

    def test_rejects_leading_dot_write_alias(self) -> None:
        graph = copy.deepcopy(VALID_GRAPH)
        graph["nodes"]["GD-2"]["writes"] = ["src/shared.py"]
        graph["nodes"]["GD-3"]["writes"] = ["./src/shared.py"]
        self.assert_error(graph, "invalid write path: ./src/shared.py")

    def test_rejects_missing_task_file(self) -> None:
        directory = self.make_package(VALID_GRAPH, json_graph=VALID_GRAPH)
        (Path(directory.name) / "tasks/GD-2/task.md").unlink()
        self.assertTrue(
            any(
                "missing task file" in error
                for error in validate_package(Path(directory.name))
            )
        )

    def test_rejects_missing_context_file(self) -> None:
        directory = self.make_package(VALID_GRAPH, json_graph=VALID_GRAPH)
        (Path(directory.name) / "tasks/GD-2/context.md").unlink()
        self.assertTrue(
            any(
                "missing context file" in error
                for error in validate_package(Path(directory.name))
            )
        )

    def test_rejects_empty_writes(self) -> None:
        graph = copy.deepcopy(VALID_GRAPH)
        graph["nodes"]["GD-1"]["writes"] = []
        self.assert_error(graph, "must own at least one write path")

    def test_rejects_missing_task_write_declarations(self) -> None:
        directory = self.make_package(
            VALID_GRAPH,
            json_graph=VALID_GRAPH,
            task_declarations={"GD-1": ""},
        )
        self.assertTrue(
            any(
                "missing repository write declarations" in error
                for error in validate_package(Path(directory.name))
            )
        )

    def test_rejects_malformed_task_write_declaration(self) -> None:
        directory = self.make_package(
            VALID_GRAPH,
            json_graph=VALID_GRAPH,
            task_declarations={"GD-1": "- Modify: src/base.py"},
        )
        self.assertTrue(
            any(
                "malformed repository write declaration" in error
                for error in validate_package(Path(directory.name))
            )
        )

    def test_rejects_task_and_graph_write_mismatch(self) -> None:
        directory = self.make_package(
            VALID_GRAPH,
            json_graph=VALID_GRAPH,
            task_declarations={"GD-1": "- Modify: `src/declared.py`"},
        )
        self.assertTrue(
            any(
                "writes do not match task declarations" in error
                for error in validate_package(Path(directory.name))
            )
        )

    def test_rejects_unknown_node_field(self) -> None:
        graph = copy.deepcopy(VALID_GRAPH)
        graph["nodes"]["GD-1"]["owner"] = "unexpected"
        self.assert_error(graph, "unsupported fields")

    def test_rejects_unknown_flow_field(self) -> None:
        graph = copy.deepcopy(VALID_GRAPH)
        graph["flow"]["edge"] = "unexpected"
        self.assert_error(graph, "unsupported fields")

    def test_rejects_missing_json_graph(self) -> None:
        directory = self.make_package(VALID_GRAPH)
        self.assertTrue(
            any("missing JSON" in error for error in validate_package(Path(directory.name)))
        )

    def test_rejects_missing_markdown_graph(self) -> None:
        directory = self.make_package(VALID_GRAPH, "markdown")
        self.assertTrue(
            any("missing Markdown" in error for error in validate_package(Path(directory.name)))
        )

    def test_rejects_unsupported_graph_format(self) -> None:
        directory = self.make_package(VALID_GRAPH, "yaml", json_graph=VALID_GRAPH)
        self.assertTrue(
            any("unsupported Graph format" in error for error in validate_package(Path(directory.name)))
        )

    def test_rejects_malformed_json(self) -> None:
        directory = self.make_package(VALID_GRAPH)
        (Path(directory.name) / "task-graph.json").write_text("{", encoding="utf-8")
        self.assertTrue(
            any("malformed JSON" in error for error in validate_package(Path(directory.name)))
        )

    def test_rejects_missing_markdown_format(self) -> None:
        markdown = render_markdown(VALID_GRAPH).replace(
            "- Format: markdown\n", ""
        )
        directory = self.make_package(
            VALID_GRAPH,
            "markdown",
            markdown=markdown,
        )
        self.assertTrue(
            any(
                "malformed Markdown metadata" in error
                for error in validate_package(Path(directory.name))
            )
        )

    def test_rejects_invalid_markdown_format(self) -> None:
        markdown = render_markdown(VALID_GRAPH).replace(
            "- Format: markdown",
            "- Format: free-form",
        )
        directory = self.make_package(
            VALID_GRAPH,
            "markdown",
            markdown=markdown,
        )
        self.assertTrue(
            any(
                "unsupported Markdown format" in error
                for error in validate_package(Path(directory.name))
            )
        )

    def test_rejects_mismatched_markdown_mirror(self) -> None:
        changed_graph = copy.deepcopy(VALID_GRAPH)
        changed_graph["nodes"]["GD-1"]["writes"] = ["src/other.py"]
        directory = self.make_package(
            VALID_GRAPH,
            "both",
            json_graph=VALID_GRAPH,
            markdown=render_markdown(changed_graph),
        )
        self.assertTrue(
            any(
                "mismatched Markdown mirror" in error
                for error in validate_package(Path(directory.name))
            )
        )


if __name__ == "__main__":
    unittest.main()
