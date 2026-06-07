# Codex Tool Mapping

Skills use Claude Code tool names. When skill names them, use platform equivalent:

| Skill references | Codex equivalent |
|-----------------|------------------|
| `Task` tool (dispatch subagent) | `spawn_agent` (see [Subagent dispatch requires multi-agent support](#subagent-dispatch-requires-multi-agent-support)) |
| Multiple `Task` calls (parallel) | Multiple `spawn_agent` calls |
| Task returns result | `wait_agent` |
| Task completes automatically | `close_agent` to free slot |
| `TodoWrite` (task tracking) | `update_plan` |
| `Skill` tool (invoke a skill) | Skills load native — follow instructions |
| `Read`, `Write`, `Edit` (files) | Use native file tools |
| `Bash` (run commands) | Use native shell tools |

## Subagent dispatch requires multi-agent support

Add to Codex config (`~/.codex/config.toml`):

```toml
[features]
multi_agent = true
```

Enables `spawn_agent`, `wait_agent`, and `close_agent` for skills like `dispatching-parallel-agents` and `subagent-driven-development`.

Legacy: Codex before `rust-v0.115.0` exposed spawned-agent waiting as `wait`. Current Codex uses `wait_agent` for spawned agents. `wait` now belongs to code-mode `exec/wait`, resumes yielded exec cell by `cell_id`; not spawned-agent result tool.

## Environment Detection

Skills creating worktrees or finishing branches should detect environment with read-only git commands first:

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

- `GIT_DIR != GIT_COMMON` → already in a linked worktree (skip creation)
- `BRANCH` empty → detached HEAD (cannot branch/push/PR from sandbox)

See `using-git-worktrees` Step 0 and `finishing-a-development-branch` Step 1 for signal use.

## Codex App Finishing

When sandbox blocks branch/push (detached HEAD in external worktree), agent commits work and tells user to use App native controls:

- **"Create branch"** — names the branch, then commit/push/PR via App UI
- **"Hand off to local"** — transfers work to the user's local checkout

Agent can still run tests, stage files, and output suggested branch names, commit messages, PR descriptions for user copy.
