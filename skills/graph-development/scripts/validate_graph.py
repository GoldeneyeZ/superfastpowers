#!/usr/bin/env python3
"""Validate Graph Development task packages without third-party dependencies."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import Counter
from pathlib import Path


class GraphValidationError(ValueError):
    """Raised when a graph artifact cannot be loaded or parsed."""


_NODE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
_POLICY_VALUE = re.compile(r"^\s*Graph (?P<name>format|review mode):\s*(?P<value>\S+)\s*$", re.MULTILINE | re.IGNORECASE)
_FILE_DECLARATION = re.compile(
    r"^\s*-\s+(?:Create|Modify|Test):\s+`(?P<path>[^`]+)`\s*$"
)
_LINE_RANGE = re.compile(r":\d+(?:-\d+)?$")


def load_policy(package_root: Path) -> tuple[str, str]:
    """Return graph format and review mode from plan-progression.md."""
    path = package_root / "plan-progression.md"
    if not path.is_file():
        raise GraphValidationError(f"missing plan progression file: {path}")

    values = {"format": "both", "review mode": "bypass"}
    for match in _POLICY_VALUE.finditer(path.read_text(encoding="utf-8")):
        values[match.group("name").lower()] = match.group("value").lower()
    return values["format"], values["review mode"]


def _reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise GraphValidationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json_graph(path: Path) -> dict:
    """Load JSON and return a mapping; raise stable validation errors."""
    if not path.is_file():
        raise GraphValidationError(f"missing JSON graph: {path}")
    try:
        loaded = json.loads(
            path.read_text(encoding="utf-8"), object_pairs_hook=_reject_duplicate_keys
        )
    except GraphValidationError:
        raise
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise GraphValidationError(f"malformed JSON graph: {path}: {error}") from error
    if not isinstance(loaded, dict):
        raise GraphValidationError("JSON graph must be an object")
    return loaded


def _compact_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def _fork_templates(sequence: list, location: str, records: list[dict]) -> list:
    rendered = []
    for index, element in enumerate(sequence):
        item_location = f"{location}[{index}]"
        if not isinstance(element, dict) or set(element) != {"parallel"}:
            rendered.append(element)
            continue
        parallel = element["parallel"]
        fork_id = f"F{len(records) + 1}"
        record = {"id": fork_id, "location": item_location, "branches": [], "join": ""}
        records.append(record)
        if isinstance(parallel, dict):
            branches = parallel.get("branches")
            if isinstance(branches, list):
                record["branches"] = [
                    {
                        "sequence": _fork_templates(
                            branch.get("sequence", [])
                            if isinstance(branch, dict)
                            else [],
                            f"{item_location}.parallel.branches[{branch_index}].sequence",
                            records,
                        )
                    }
                    for branch_index, branch in enumerate(branches)
                ]
            record["join"] = parallel.get("join", "")
        rendered.append({"fork": fork_id})
    return rendered


def _mermaid_id(node_id: str) -> str:
    return "N_" + re.sub(r"[^A-Za-z0-9_]", "_", node_id)


def _render_mermaid(graph: dict) -> list[str]:
    nodes = graph.get("nodes") if isinstance(graph, dict) else {}
    flow = graph.get("flow") if isinstance(graph, dict) else {}
    lines = ["flowchart TD"]
    if isinstance(nodes, dict):
        for node_id in sorted(nodes):
            lines.append(f'    {_mermaid_id(node_id)}["{node_id}"]')

    counter = 0

    def connect(sequence: object, predecessors: list[str]) -> list[str]:
        nonlocal counter
        if not isinstance(sequence, list):
            return predecessors
        current = predecessors
        for element in sequence:
            if isinstance(element, str):
                target = _mermaid_id(element)
                for predecessor in current:
                    lines.append(f"    {predecessor} --> {target}")
                current = [target]
                continue
            if not isinstance(element, dict) or not isinstance(element.get("parallel"), dict):
                continue
            counter += 1
            fork = f"Fork_{counter}"
            lines.append(f"    {fork}{{Fork {counter}}}")
            for predecessor in current:
                lines.append(f"    {predecessor} --> {fork}")
            parallel = element["parallel"]
            tails = []
            for branch in parallel.get("branches", []):
                tails.extend(connect(branch.get("sequence"), [fork]) if isinstance(branch, dict) else [fork])
            join = parallel.get("join")
            if isinstance(join, str):
                join_target = _mermaid_id(join)
                for tail in tails:
                    lines.append(f"    {tail} --> {join_target}")
                current = [join_target]
        return current

    if isinstance(flow, dict):
        connect(flow.get("sequence"), [])
    return lines


def render_markdown(graph: dict) -> str:
    """Render metadata, node table, fork table, and Mermaid mirror."""
    nodes = graph.get("nodes") if isinstance(graph, dict) else {}
    flow = graph.get("flow") if isinstance(graph, dict) else {}
    records: list[dict] = []
    root_sequence = _fork_templates(
        flow.get("sequence", []) if isinstance(flow, dict) else [],
        "flow.sequence",
        records,
    )
    lines = [
        "# Task Graph",
        "",
        f"- Version: {graph.get('version', '') if isinstance(graph, dict) else ''}",
        "- Format: markdown",
        "- Source: task-graph.json",
        "",
        "## Nodes",
        "",
        "| ID | Task | Writes |",
        "| --- | --- | --- |",
    ]
    if isinstance(nodes, dict):
        for node_id in sorted(nodes):
            node = nodes[node_id]
            task = node.get("task", "") if isinstance(node, dict) else ""
            writes = node.get("writes", []) if isinstance(node, dict) else []
            write_cell = "<br>".join(writes) if isinstance(writes, list) else ""
            lines.append(f"| {node_id} | {task} | {write_cell} |")
    lines.extend(
        [
            "",
            "## Forks",
            "",
            "| ID | Location | Branches | Join |",
            "| --- | --- | --- | --- |",
            f"| ROOT | flow.sequence | {_compact_json(root_sequence)} |  |",
        ]
    )
    for record in records:
        lines.append(
            "| {id} | {location} | {branches} | {join} |".format(
                id=record["id"],
                location=record["location"],
                branches=_compact_json(record["branches"]),
                join=record["join"],
            )
        )
    lines.extend(["", "## Mermaid", "", "```mermaid", *_render_mermaid(graph), "```", ""])
    return "\n".join(lines)


def _markdown_tables(text: str) -> dict[tuple[str, ...], list[list[str]]]:
    tables: dict[tuple[str, ...], list[list[str]]] = {}
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        if not (line.startswith("|") and line.endswith("|")):
            index += 1
            continue
        header = tuple(cell.strip() for cell in line[1:-1].split("|"))
        if index + 1 >= len(lines) or not re.fullmatch(
            r"\|\s*(?:---\s*\|\s*)+", lines[index + 1].strip()
        ):
            index += 1
            continue
        rows = []
        index += 2
        while index < len(lines):
            row = lines[index].strip()
            if not (row.startswith("|") and row.endswith("|")):
                break
            cells = [cell.strip() for cell in row[1:-1].split("|")]
            if len(cells) != len(header):
                raise GraphValidationError("malformed Markdown table row")
            rows.append(cells)
            index += 1
        tables[header] = rows
    return tables


def parse_markdown(path: Path) -> dict:
    """Parse only documented node/fork tables into canonical graph data."""
    if not path.is_file():
        raise GraphValidationError(f"missing Markdown graph: {path}")
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise GraphValidationError(f"malformed Markdown graph: {path}: {error}") from error
    version_match = re.search(r"^\s*- Version:\s*(.+?)\s*$", text, re.MULTILINE)
    format_match = re.search(r"^\s*- Format:\s*(.+?)\s*$", text, re.MULTILINE)
    source_match = re.search(r"^\s*- Source:\s*(.+?)\s*$", text, re.MULTILINE)
    if version_match is None or format_match is None or source_match is None:
        raise GraphValidationError("malformed Markdown metadata")
    try:
        version = int(version_match.group(1))
    except ValueError as error:
        raise GraphValidationError("malformed Markdown version") from error
    if format_match.group(1) != "markdown":
        raise GraphValidationError("unsupported Markdown format")
    if source_match.group(1) != "task-graph.json":
        raise GraphValidationError("unsupported Markdown source")

    tables = _markdown_tables(text)
    node_rows = tables.get(("ID", "Task", "Writes"))
    fork_rows = tables.get(("ID", "Location", "Branches", "Join"))
    if node_rows is None or fork_rows is None:
        raise GraphValidationError("unsupported Markdown graph description")

    nodes = {}
    for node_id, task, writes in node_rows:
        if node_id in nodes:
            raise GraphValidationError(f"duplicate Markdown node: {node_id}")
        nodes[node_id] = {
            "task": task,
            "writes": [] if not writes else writes.split("<br>"),
        }

    root_sequence = None
    forks = {}
    for fork_id, location, branches_cell, join in fork_rows:
        try:
            decoded = json.loads(branches_cell)
        except json.JSONDecodeError as error:
            raise GraphValidationError(f"malformed Markdown fork {fork_id}") from error
        if fork_id == "ROOT":
            if location != "flow.sequence" or join or root_sequence is not None:
                raise GraphValidationError("malformed Markdown root flow")
            root_sequence = decoded
            continue
        if fork_id in forks or not re.fullmatch(r"F[1-9][0-9]*", fork_id):
            raise GraphValidationError(f"malformed Markdown fork ID: {fork_id}")
        forks[fork_id] = {"branches": decoded, "join": join}
    if root_sequence is None:
        raise GraphValidationError("missing Markdown root flow")

    used_forks: Counter[str] = Counter()

    def expand(sequence: object) -> list:
        if not isinstance(sequence, list):
            raise GraphValidationError("malformed Markdown sequence")
        result = []
        for element in sequence:
            if isinstance(element, dict) and set(element) == {"fork"}:
                fork_id = element["fork"]
                if not isinstance(fork_id, str) or fork_id not in forks:
                    raise GraphValidationError("unknown Markdown fork reference")
                used_forks[fork_id] += 1
                fork = forks[fork_id]
                branches = fork["branches"]
                if not isinstance(branches, list):
                    raise GraphValidationError(f"malformed Markdown fork {fork_id}")
                result.append(
                    {
                        "parallel": {
                            "branches": [
                                {"sequence": expand(branch.get("sequence"))}
                                if isinstance(branch, dict)
                                else _bad_markdown_branch(fork_id)
                                for branch in branches
                            ],
                            "join": fork["join"],
                        }
                    }
                )
            else:
                result.append(element)
        return result

    sequence = expand(root_sequence)
    unused = sorted(fork_id for fork_id in forks if used_forks[fork_id] != 1)
    if unused:
        raise GraphValidationError(f"unreachable or reused Markdown fork: {', '.join(unused)}")
    return {"version": version, "nodes": nodes, "flow": {"sequence": sequence}}


def _bad_markdown_branch(fork_id: str) -> dict:
    raise GraphValidationError(f"malformed Markdown fork {fork_id}")


def _valid_relative_path(value: object) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = Path(value)
    return (
        not path.is_absolute()
        and ".." not in path.parts
        and "." not in path.parts
        and path.as_posix() == value
    )


def _task_write_declarations(task_path: Path, node_id: str) -> tuple[set[str], list[str]]:
    """Return normalized repository writes declared by a task package."""
    try:
        lines = task_path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as error:
        return set(), [f"node {node_id} cannot read task declarations: {error}"]

    headings = [index for index, line in enumerate(lines) if line.strip() == "**Files:**"]
    if len(headings) != 1:
        return set(), [f"node {node_id} missing repository write declarations"]

    declarations: set[str] = set()
    errors: list[str] = []
    for line in lines[headings[0] + 1 :]:
        if not line.strip():
            break
        match = _FILE_DECLARATION.fullmatch(line)
        if match is None:
            errors.append(
                f"node {node_id} malformed repository write declaration: {line.strip()}"
            )
            continue
        declared_path = _LINE_RANGE.sub("", match.group("path"))
        if not _valid_relative_path(declared_path):
            errors.append(
                f"node {node_id} malformed repository write declaration: {line.strip()}"
            )
            continue
        declarations.add(declared_path)
    if not declarations and not errors:
        errors.append(f"node {node_id} missing repository write declarations")
    return declarations, errors


def validate_graph(graph: dict, package_root: Path) -> list[str]:
    """Return deterministic schema, structure, package, and ownership errors."""
    errors: list[str] = []
    if not isinstance(graph, dict):
        return ["graph must be an object"]
    unexpected_graph_fields = sorted(set(graph) - {"version", "nodes", "flow"})
    if unexpected_graph_fields:
        errors.append(
            f"graph has unsupported fields: {', '.join(unexpected_graph_fields)}"
        )
    if graph.get("version") != 1 or isinstance(graph.get("version"), bool):
        errors.append("unsupported graph version; expected 1")
    nodes = graph.get("nodes")
    if not isinstance(nodes, dict) or not nodes:
        errors.append("missing nodes")
        nodes = {}
    flow = graph.get("flow")
    if not isinstance(flow, dict) or not isinstance(flow.get("sequence"), list):
        errors.append("missing flow sequence")
        flow = {"sequence": []}
    else:
        unexpected_flow_fields = sorted(set(flow) - {"sequence"})
        if unexpected_flow_fields:
            errors.append(
                f"flow has unsupported fields: {', '.join(unexpected_flow_fields)}"
            )

    writes_by_node: dict[str, set[str]] = {}
    for node_id in sorted(nodes):
        node = nodes[node_id]
        if not isinstance(node_id, str) or not _NODE_ID.fullmatch(node_id):
            errors.append(f"invalid node ID: {node_id}")
            continue
        if not isinstance(node, dict):
            errors.append(f"node {node_id} must be an object")
            continue
        unexpected_node_fields = sorted(set(node) - {"task", "writes"})
        if unexpected_node_fields:
            errors.append(
                f"node {node_id} has unsupported fields: "
                f"{', '.join(unexpected_node_fields)}"
            )
        task = node.get("task")
        task_path: Path | None = None
        declared_writes: set[str] = set()
        declaration_errors: list[str] = []
        if not _valid_relative_path(task):
            errors.append(f"node {node_id} has invalid task path")
        else:
            expected_task = Path("tasks") / node_id / "task.md"
            if Path(task) != expected_task:
                errors.append(f"node {node_id} task must be {expected_task.as_posix()}")
            task_path = package_root / task
            if not task_path.is_file():
                errors.append(f"node {node_id} missing task file: {task}")
            else:
                declared_writes, declaration_errors = _task_write_declarations(
                    task_path, node_id
                )
                errors.extend(declaration_errors)
            context_path = task_path.parent / "context.md"
            if not context_path.is_file():
                errors.append(f"node {node_id} missing context file: {context_path.relative_to(package_root)}")
        writes = node.get("writes")
        if not isinstance(writes, list) or not writes:
            errors.append(f"node {node_id} must own at least one write path")
            writes_by_node[node_id] = set()
            continue
        valid_writes = set()
        for write in writes:
            if not _valid_relative_path(write):
                errors.append(f"node {node_id} has invalid write path: {write}")
                continue
            if write in valid_writes:
                errors.append(f"node {node_id} duplicates write path: {write}")
            valid_writes.add(write)
        writes_by_node[node_id] = valid_writes
        if (
            task_path is not None
            and task_path.is_file()
            and not declaration_errors
            and valid_writes != declared_writes
        ):
            graph_only = sorted(valid_writes - declared_writes)
            task_only = sorted(declared_writes - valid_writes)
            details = []
            if graph_only:
                details.append(f"graph-only: {', '.join(graph_only)}")
            if task_only:
                details.append(f"task-only: {', '.join(task_only)}")
            errors.append(
                f"node {node_id} writes do not match task declarations: "
                + "; ".join(details)
            )

    seen: Counter[str] = Counter()
    declared_joins: set[str] = set()

    def add_node(node_id: object, forbidden_joins: set[str]) -> tuple[list[str], set[str]]:
        if not isinstance(node_id, str):
            errors.append("flow node reference must be a string")
            return [], set()
        if node_id in forbidden_joins:
            errors.append(f"join must not appear inside its branches: {node_id}")
        if node_id not in nodes:
            errors.append(f"flow references unknown node: {node_id}")
            return [], set()
        seen[node_id] += 1
        return [node_id], set(writes_by_node.get(node_id, set()))

    def walk_sequence(sequence: object, forbidden_joins: set[str]) -> tuple[list[str], set[str]]:
        if not isinstance(sequence, list):
            errors.append("flow sequence must be a list")
            return [], set()
        ordered: list[str] = []
        writes: set[str] = set()
        for element in sequence:
            if isinstance(element, str):
                element_nodes, element_writes = add_node(element, forbidden_joins)
            elif isinstance(element, dict) and set(element) == {"parallel"}:
                element_nodes, element_writes = walk_parallel(element["parallel"], forbidden_joins)
            else:
                errors.append("flow element must be a node ID or parallel block")
                element_nodes, element_writes = [], set()
            ordered.extend(element_nodes)
            writes.update(element_writes)
        return ordered, writes

    def walk_parallel(parallel: object, forbidden_joins: set[str]) -> tuple[list[str], set[str]]:
        if not isinstance(parallel, dict):
            errors.append("parallel block must be an object")
            return [], set()
        unexpected_parallel_fields = sorted(set(parallel) - {"branches", "join"})
        if unexpected_parallel_fields:
            errors.append(
                "parallel block has unsupported fields: "
                f"{', '.join(unexpected_parallel_fields)}"
            )
        branches = parallel.get("branches")
        join = parallel.get("join")
        if not isinstance(branches, list) or len(branches) < 2:
            errors.append("parallel block must contain at least two branches")
            branches = branches if isinstance(branches, list) else []
        if not isinstance(join, str) or not join:
            errors.append("parallel block missing join")
            join = ""
        elif join in forbidden_joins or join in declared_joins:
            errors.append(f"crossing or reused join: {join}")
        declared_joins.add(join)

        branch_results = []
        for branch in branches:
            if not isinstance(branch, dict) or set(branch) != {"sequence"}:
                errors.append("parallel branch must contain only a sequence")
                branch_results.append(([], set()))
                continue
            branch_results.append(walk_sequence(branch["sequence"], forbidden_joins | {join}))
        for left_index, (_, left_writes) in enumerate(branch_results):
            for _, right_writes in branch_results[left_index + 1 :]:
                overlap = sorted(left_writes & right_writes)
                if overlap:
                    errors.append(f"concurrent write overlap: {', '.join(overlap)}")
        if not join:
            return [], set().union(*(writes for _, writes in branch_results)) if branch_results else set()
        join_nodes, join_writes = add_node(join, forbidden_joins)
        all_nodes = [node for branch_nodes, _ in branch_results for node in branch_nodes]
        all_nodes.extend(join_nodes)
        all_writes = set(join_writes)
        for _, branch_writes in branch_results:
            all_writes.update(branch_writes)
        return all_nodes, all_writes

    walk_sequence(flow["sequence"], set())
    for node_id, count in sorted(seen.items()):
        if count > 1:
            errors.append(f"node {node_id} referenced more than once")
    for node_id in sorted(nodes):
        if seen[node_id] == 0:
            errors.append(f"node {node_id} not reachable from flow")
    return errors


def _graph_topology(graph: dict) -> dict:
    """Return only execution topology, excluding task metadata and ownership."""
    nodes = graph.get("nodes", {})
    return {
        "nodes": sorted(nodes) if isinstance(nodes, dict) else [],
        "flow": graph.get("flow"),
    }


def _topology_predecessors(topology: dict) -> tuple[set[str], dict[str, set[str]]]:
    """Return topology nodes and direct predecessor sets."""
    raw_nodes = topology.get("nodes", []) if isinstance(topology, dict) else []
    nodes = set(raw_nodes) if isinstance(raw_nodes, list) else set()
    predecessors = {node_id: set() for node_id in nodes if isinstance(node_id, str)}
    flow = topology.get("flow", {}) if isinstance(topology, dict) else {}

    def walk(sequence: object, incoming: set[str]) -> set[str]:
        current = set(incoming)
        if not isinstance(sequence, list):
            return current
        for element in sequence:
            if isinstance(element, str):
                predecessors.setdefault(element, set()).update(current)
                current = {element}
                continue
            if not isinstance(element, dict) or set(element) != {"parallel"}:
                continue
            parallel = element["parallel"]
            if not isinstance(parallel, dict):
                continue
            tails: set[str] = set()
            branches = parallel.get("branches", [])
            if isinstance(branches, list):
                for branch in branches:
                    if isinstance(branch, dict):
                        tails.update(walk(branch.get("sequence"), current))
            join = parallel.get("join")
            if isinstance(join, str):
                predecessors.setdefault(join, set()).update(tails)
                current = {join}
        return current

    if isinstance(flow, dict):
        walk(flow.get("sequence"), set())
    return nodes, predecessors


def _affected_downstream(previous: dict, current: dict) -> set[str]:
    """Return current nodes whose predecessors changed, plus their descendants."""
    old_nodes, old_predecessors = _topology_predecessors(previous)
    new_nodes, new_predecessors = _topology_predecessors(current)
    affected = old_nodes - new_nodes
    affected.update(
        node_id
        for node_id in new_nodes
        if node_id not in old_nodes
        or old_predecessors.get(node_id, set()) != new_predecessors.get(node_id, set())
    )
    successors: dict[str, set[str]] = {}
    for predecessors in (old_predecessors, new_predecessors):
        for node_id, direct_predecessors in predecessors.items():
            for predecessor in direct_predecessors:
                successors.setdefault(predecessor, set()).add(node_id)
    queue = list(affected)
    while queue:
        node_id = queue.pop()
        for successor in successors.get(node_id, set()):
            if successor not in affected:
                affected.add(successor)
                queue.append(successor)
    return affected


def _load_graph_state(package_root: Path) -> tuple[dict | None, list[str]]:
    path = package_root / "graph-state.json"
    if not path.exists():
        return None, []
    try:
        state = json.loads(
            path.read_text(encoding="utf-8"), object_pairs_hook=_reject_duplicate_keys
        )
    except GraphValidationError as error:
        return None, [f"malformed graph state: {error}"]
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        return None, [f"malformed graph state: {path}: {error}"]
    if not isinstance(state, dict):
        return None, ["graph state must be an object"]
    errors = []
    unexpected = sorted(set(state) - {"version", "started", "topology", "invalidated"})
    if unexpected:
        errors.append(f"graph state has unsupported fields: {', '.join(unexpected)}")
    if state.get("version") != 1 or isinstance(state.get("version"), bool):
        errors.append("unsupported graph state version; expected 1")
    if not isinstance(state.get("started"), bool):
        errors.append("graph state started must be boolean")
    topology = state.get("topology")
    if not isinstance(topology, dict) or set(topology) != {"nodes", "flow"}:
        errors.append("graph state topology must contain nodes and flow")
    elif (
        not isinstance(topology["nodes"], list)
        or not topology["nodes"]
        or any(
            not isinstance(node_id, str) or not _NODE_ID.fullmatch(node_id)
            for node_id in topology["nodes"]
        )
        or len(set(topology["nodes"])) != len(topology["nodes"])
    ):
        errors.append("graph state topology nodes must be unique node IDs")
    elif (
        not isinstance(topology["flow"], dict)
        or set(topology["flow"]) != {"sequence"}
        or not isinstance(topology["flow"]["sequence"], list)
    ):
        errors.append("graph state topology flow must contain a sequence")
    invalidated = state.get("invalidated")
    if (
        not isinstance(invalidated, list)
        or any(not isinstance(node_id, str) for node_id in invalidated)
        or len(set(invalidated)) != len(invalidated)
    ):
        errors.append("graph state invalidated must be a list of unique node IDs")
    return (state if not errors else None), errors


def _context_graph_status(package_root: Path, graph: dict, node_id: str) -> str | None:
    node = graph["nodes"].get(node_id)
    context_path = (
        package_root / Path(node["task"]).parent / "context.md"
        if node is not None
        else package_root / "tasks" / node_id / "context.md"
    )
    match = re.search(
        r"^Graph status:\s*(pending|running|implemented|blocked|reviewed|complete)\s*$",
        context_path.read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    return match.group(1) if match is not None else None


def _execution_started(package_root: Path, graph: dict) -> bool:
    for node_id in sorted(graph["nodes"]):
        try:
            status = _context_graph_status(package_root, graph, node_id)
        except (OSError, UnicodeDecodeError):
            continue
        if status is not None and status != "pending":
            return True
    return False


def _validate_topology_state(graph: dict, package_root: Path) -> list[str]:
    state, errors = _load_graph_state(package_root)
    if errors:
        return errors
    execution_started = _execution_started(package_root, graph)
    if state is None:
        return ["execution started but graph-state.json is missing"] if execution_started else []
    if execution_started and not state["started"]:
        return ["execution started but graph state is not started"]
    if not state["started"]:
        return []
    current = _graph_topology(graph)
    if state["topology"] == current:
        return []
    affected = _affected_downstream(state["topology"], current)
    current_nodes = set(graph["nodes"])
    previous_nodes = set(state["topology"]["nodes"])
    invalidated = set(state["invalidated"])
    unknown = sorted(invalidated - current_nodes - previous_nodes)
    if unknown:
        errors.append(f"graph state invalidates unknown nodes: {', '.join(unknown)}")
    missing = sorted(affected - invalidated)
    if missing:
        errors.append(
            "topology changed after execution started; downstream state not invalidated: "
            + ", ".join(missing)
        )
    for node_id in sorted(affected & invalidated):
        try:
            status = _context_graph_status(package_root, graph, node_id)
        except (OSError, UnicodeDecodeError):
            status = None
        if status != "pending":
            errors.append(
                f"topology-invalidated node {node_id} must have Graph status pending"
            )
    return errors


def _validate_clean_owned_paths(graph: dict, package_root: Path) -> list[str]:
    """Reject tracked or untracked changes under graph-owned repository paths."""
    result = subprocess.run(
        ["git", "-C", str(package_root), "rev-parse", "--show-toplevel"],
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        return []
    repository_root = Path(result.stdout.strip())
    owned_paths = sorted(
        {
            write
            for node in graph["nodes"].values()
            for write in node["writes"]
        }
    )
    errors = []
    for owned_path in owned_paths:
        status = subprocess.run(
            [
                "git",
                "-C",
                str(repository_root),
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
                "--",
                owned_path,
            ],
            check=False,
            text=True,
            capture_output=True,
        )
        if status.returncode != 0:
            errors.append(f"cannot inspect graph-owned path: {owned_path}")
        elif status.stdout:
            errors.append(f"dirty graph-owned path: {owned_path}")
    return errors


def validate_package(package_root: Path) -> list[str]:
    """Load selected artifacts, compare mirrors, and validate package."""
    try:
        graph_format, review_mode = load_policy(package_root)
    except GraphValidationError as error:
        return [str(error)]
    errors = []
    if graph_format not in {"json", "markdown", "both"}:
        errors.append(f"unsupported Graph format: {graph_format}")
    if review_mode not in {"bypass", "gated"}:
        errors.append(f"unsupported Graph review mode: {review_mode}")
    if errors:
        return errors

    json_graph = None
    markdown_graph = None
    if graph_format in {"json", "both"}:
        try:
            json_graph = load_json_graph(package_root / "task-graph.json")
        except GraphValidationError as error:
            errors.append(str(error))
    if graph_format in {"markdown", "both"}:
        try:
            markdown_graph = parse_markdown(package_root / "task-graph.md")
        except GraphValidationError as error:
            errors.append(str(error))
    if errors:
        return errors
    if graph_format == "both" and json_graph != markdown_graph:
        errors.append("mismatched Markdown mirror")
    graph = json_graph if json_graph is not None else markdown_graph
    if graph is None:
        return errors
    errors.extend(validate_graph(graph, package_root))
    if errors:
        return errors
    errors.extend(_validate_clean_owned_paths(graph, package_root))
    errors.extend(_validate_topology_state(graph, package_root))
    return errors


def main() -> int:
    """Print one error per line; return 0 when valid, 1 when invalid."""
    parser = argparse.ArgumentParser(description="Validate a Graph Development task package.")
    parser.add_argument("package_root", type=Path)
    args = parser.parse_args()
    errors = validate_package(args.package_root)
    if errors:
        for error in errors:
            print(error)
        return 1
    print("Task graph valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
