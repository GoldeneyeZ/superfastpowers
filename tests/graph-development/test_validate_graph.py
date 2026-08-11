"""Contract tests for the graph-development validator."""

from __future__ import annotations

import copy
import importlib.util
import json
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
    ) -> tempfile.TemporaryDirectory[str]:
        directory = tempfile.TemporaryDirectory()
        root = Path(directory.name)
        (root / "plan-progression.md").write_text(
            f"Graph format: {graph_format}\n", encoding="utf-8"
        )
        for node in graph.get("nodes", {}).values():
            task_file = root / node["task"]
            task_file.parent.mkdir(parents=True, exist_ok=True)
            task_file.write_text("# Task\n", encoding="utf-8")
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
