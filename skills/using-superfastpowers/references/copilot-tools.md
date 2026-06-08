# Copilot CLI Tool Mapping

Skills use Claude Code tool names. Map to platform equivalent:

| Skill references | Copilot CLI equivalent |
|-----------------|----------------------|
| `Read` (read files) | `view` |
| `Write` (create files) | `create` |
| `Edit` (edit files) | `edit` |
| `Bash` (run commands) | `bash` |
| `Grep` (search content) | `grep` |
| `Glob` (search names) | `glob` |
| `Skill` tool (invoke skill) | `skill` |
| `WebFetch` | `web_fetch` |
| `Task` tool (subagent) | `task` with `agent_type: "general-purpose"` or `"explore"` |
| Multiple `Task` calls (parallel) | Multiple `task` calls |
| Task status/output | `read_agent`, `list_agents` |
| `TodoWrite` (task tracking) | `sql` with built-in `todos` table |
| `WebSearch` | No equivalent — use `web_fetch` with a search engine URL |
| `EnterPlanMode` / `ExitPlanMode` | No equivalent — stay in main session |

## Async shell sessions

Copilot CLI supports persistent async shell sessions. No direct Claude Code equivalent:

| Tool | Purpose |
|------|---------|
| `bash` with `async: true` | Start long-running command in background |
| `write_bash` | Send input to running async session |
| `read_bash` | Read async session output |
| `stop_bash` | Terminate async session |
| `list_bash` | List all active shell sessions |

## Additional Copilot CLI tools

| Tool | Purpose |
|------|---------|
| `store_memory` | Persist codebase facts for future sessions |
| `report_intent` | Update UI status line with current intent |
| `sql` | Query session SQLite database (todos, metadata) |
| `fetch_copilot_cli_documentation` | Look up Copilot CLI docs |
| GitHub MCP tools (`github-mcp-server-*`) | Native GitHub API access (issues, PRs, code search) |
