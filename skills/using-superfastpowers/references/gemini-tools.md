# Gemini CLI Tool Mapping

Skills use Claude Code tool names. When skill mentions one, use platform equivalent:

| Skill references | Gemini CLI equivalent |
|-----------------|----------------------|
| `Read` (file reading) | `read_file` |
| `Write` (file creation) | `write_file` |
| `Edit` (file editing) | `replace` |
| `Bash` (run commands) | `run_shell_command` |
| `Grep` (search file content) | `grep_search` |
| `Glob` (search files by name) | `glob` |
| `TodoWrite` (task tracking) | `write_todos` |
| `Skill` tool (invoke a skill) | `activate_skill` |
| `WebSearch` | `google_web_search` |
| `WebFetch` | `web_fetch` |
| `Task` tool (dispatch subagent) | `@agent-name` (see [Subagent support](#subagent-support)) |

## Subagent support

Gemini CLI supports subagents via `@` syntax. Use built-in `@generalist` for any task — all tools, follows prompt.

When skill names agent type, use `@generalist` with full prompt from skill prompt template:

| Skill instruction | Gemini CLI equivalent |
|-------------------|----------------------|
| `Task tool (superfastpowers:implementer)` | `@generalist` with the filled `implementer-prompt.md` template |
| `Task tool (superfastpowers:spec-reviewer)` | `@generalist` with the filled `spec-reviewer-prompt.md` template |
| `Task tool (superfastpowers:code-reviewer)` | `@code-reviewer` (bundled agent) or `@generalist` with the filled review prompt |
| `Task tool (superfastpowers:code-quality-reviewer)` | `@generalist` with the filled `code-quality-reviewer-prompt.md` template |
| `Task tool (general-purpose)` with inline prompt | `@generalist` with your inline prompt |

### Prompt filling

Skills provide prompt templates with placeholders like `{WHAT_WAS_IMPLEMENTED}` or `[FULL TEXT of task]`. Fill all placeholders, pass complete prompt to `@generalist`. Template contains agent role, review criteria, expected output format — `@generalist` follows it.

### Parallel dispatch

Gemini CLI supports parallel subagent dispatch. If skill asks multiple independent subagent tasks in parallel, request all `@generalist` or named subagent tasks together in same prompt. Keep dependent tasks sequential; don't serialize independent tasks just for simpler history.

## Additional Gemini CLI tools

Gemini CLI-only tools:

| Tool | Purpose |
|------|---------|
| `list_directory` | List files and subdirectories |
| `save_memory` | Persist facts to GEMINI.md across sessions |
| `ask_user` | Request structured input from user |
| `tracker_create_task` | Rich task management: create, update, list, visualize |
| `enter_plan_mode` / `exit_plan_mode` | Switch to read-only research mode before edits |