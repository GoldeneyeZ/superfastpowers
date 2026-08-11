# Superfastpowers

Superfastpowers is a complete software development methodology for your coding agents, built on top of a set of composable skills and some initial instructions that make sure your agent uses them.

## Quickstart

Give your agent Superfastpowers: [Claude Code](#claude-code), [Codex CLI](#codex-cli), [Codex App](#codex-app), [Factory Droid](#factory-droid), [Gemini CLI](#gemini-cli), [OpenCode](#opencode), [Cursor](#cursor), [GitHub Copilot CLI](#github-copilot-cli).

## How it works

It starts from the moment you fire up your coding agent. As soon as it sees that you're building something, it *doesn't* just jump into trying to write code. Instead, it steps back and asks you what you're really trying to do. 

Once it's teased a spec out of the conversation, it shows it to you in chunks short enough to actually read and digest. 

After you've signed off on the design, your agent puts together an implementation plan that's clear enough for an enthusiastic junior engineer with poor taste, no judgement, no project context, and an aversion to testing to follow. It emphasizes true red/green TDD, YAGNI (You Aren't Gonna Need It), and DRY. 

Next up, once you say "go", it recommends *Goal-Driven Bypass*: agents implement every task, then run one plan-wide spec review and one plan-wide code-quality review before final integration. This reduces repeated review overhead while preserving completion gates. You can choose gated per-task feedback instead.

There's a bunch more to it, but that's the core of the system. And because the skills trigger automatically, you don't need to do anything special. Your coding agent just has Superfastpowers.


## Sponsorship

If Superfastpowers has helped you do stuff that makes money and you are so inclined, I'd greatly appreciate it if you'd consider [sponsoring my opensource work](https://github.com/sponsors/obra).

Thanks! 

- Jesse


## Installation

Installation differs by harness. If you use more than one, install Superfastpowers separately for each one.

### Claude Code

Superfastpowers is available via the [official Claude plugin marketplace](https://claude.com/plugins/superfastpowers)

#### Official Marketplace

- Install the plugin from Anthropic's official marketplace:

  ```bash
  /plugin install superfastpowers@claude-plugins-official
  ```

#### Superfastpowers Marketplace

The Superfastpowers marketplace provides Superfastpowers and some other related plugins for Claude Code.

- Register the marketplace:

  ```bash
  /plugin marketplace add obra/superfastpowers-marketplace
  ```

- Install the plugin from this marketplace:

  ```bash
  /plugin install superfastpowers@superfastpowers-marketplace
  ```

### Codex CLI

Superfastpowers is available via the [official Codex plugin marketplace](https://github.com/openai/plugins).

- Open the plugin search interface:

  ```bash
  /plugins
  ```

- Search for Superfastpowers:

  ```bash
  superfastpowers
  ```

- Select `Install Plugin`.

### Codex App

Superfastpowers is available via the [official Codex plugin marketplace](https://github.com/openai/plugins).

- In the Codex app, click on Plugins in the sidebar.
- You should see `Superfastpowers` in the Coding section.
- Click the `+` next to Superfastpowers and follow the prompts.

### Factory Droid

- Register the marketplace:

  ```bash
  droid plugin marketplace add https://github.com/obra/superfastpowers
  ```

- Install the plugin:

  ```bash
  droid plugin install superfastpowers@superfastpowers
  ```

### Gemini CLI

- Install the extension:

  ```bash
  gemini extensions install https://github.com/obra/superfastpowers
  ```

- Update later:

  ```bash
  gemini extensions update superfastpowers
  ```

### OpenCode

OpenCode uses its own plugin install; install Superfastpowers separately even if you
already use it in another harness.

- Tell OpenCode:

  ```
  Fetch and follow instructions from https://raw.githubusercontent.com/obra/superfastpowers/refs/heads/main/.opencode/INSTALL.md
  ```

- Detailed docs: [docs/README.opencode.md](docs/README.opencode.md)

### Cursor

- In Cursor Agent chat, install from marketplace:

  ```text
  /add-plugin superfastpowers
  ```

- Or search for "superfastpowers" in the plugin marketplace.

### GitHub Copilot CLI

- Register the marketplace:

  ```bash
  copilot plugin marketplace add obra/superfastpowers-marketplace
  ```

- Install the plugin:

  ```bash
  copilot plugin install superfastpowers@superfastpowers-marketplace
  ```

## The Basic Workflow

1. **brainstorming** - Activates before writing code. Refines rough ideas through questions, explores alternatives, presents design in sections for validation. Saves design document.

2. **writing-plans** - Activates with approved design. Breaks work into bite-sized tasks (2-5 minutes each). Every task has exact file paths, complete code, verification steps.

3. **goal-driven-development**, **subagent-driven-development**, or **executing-plans** - Activates with plan. Goal-Driven Bypass is recommended for elapsed time: implement all tasks, then two plan-wide review phases. Goal-Driven Gated and Subagent-Driven preserve per-task review feedback; Inline executes with checkpoints.

4. **graph-development** — Executes validated structured task graphs: linear agent continuity, parallel branches, durable parent continuations, parent-owned joins and commits. It is an optional execution workflow for plans that include graph artifacts; Goal-Driven Bypass remains the recommended default.

When `writing-plans` creates graph artifacts, choose `json`, `markdown`, or `both`; the default is `both`. Graph Development reads the validated graph artifacts when that workflow is selected.

5. **test-driven-development** - Activates during implementation. Enforces RED-GREEN-REFACTOR: write failing test, watch it fail, write minimal code, watch it pass, commit. Deletes code written before tests.

6. **requesting-code-review** - Activates at execution-mode review points: between tasks for gated workflows, plan-wide after implementation for Goal-Driven Bypass. Reports issues by severity; critical issues block progress.

7. **finishing-a-development-branch** - Activates when tasks complete. Verifies tests, presents options (merge/PR/keep/discard), and performs the selected cleanup.

**The agent checks for relevant skills before any task.** Mandatory workflows, not suggestions.

## What's Inside

### Skills Library

**Testing**
- **test-driven-development** - RED-GREEN-REFACTOR cycle (includes testing anti-patterns reference)

**Debugging**
- **systematic-debugging** - 4-phase root cause process (includes root-cause-tracing, defense-in-depth, condition-based-waiting techniques)
- **verification-before-completion** - Ensure it's actually fixed

**Collaboration** 
- **brainstorming** - Socratic design refinement
- **writing-plans** - Detailed implementation plans
- **graph-development** - Executes validated structured task graphs
- **goal-driven-development** - Policy-driven execution. Bypass (recommended for speed) performs two plan-wide review phases instead of two per task; Gated preserves early per-task feedback.
- **executing-plans** - Batch execution with checkpoints
- **dispatching-parallel-agents** - Concurrent subagent workflows
- **requesting-code-review** - Pre-review checklist
- **receiving-code-review** - Responding to feedback
- **using-git-worktrees** - Explicit opt-in worktree setup and safety
- **finishing-a-development-branch** - Merge/PR decision workflow
- **subagent-driven-development** - Fresh subagent with two-stage review per task (spec compliance, then code quality)

**Meta**
- **writing-skills** - Create new skills following best practices (includes testing methodology)
- **using-superfastpowers** - Introduction to the skills system

## Philosophy

- **Test-Driven Development** - Write tests first, always
- **Systematic over ad-hoc** - Process over guessing
- **Complexity reduction** - Simplicity as primary goal
- **Evidence over claims** - Verify before declaring success

Read [the original release announcement](https://blog.fsck.com/2025/10/09/superfastpowers/).

## Contributing

The general contribution process for Superfastpowers is below. Keep in mind that we don't generally accept contributions of new skills and that any updates to skills must work across all of the coding agents we support.

1. Fork the repository
2. Switch to the 'dev' branch
3. Create a branch for your work
4. Follow the `writing-skills` skill for creating and testing new and modified skills
5. Submit a PR, being sure to fill in the pull request template.

See `skills/writing-skills/SKILL.md` for the complete guide.

## Updating

Superfastpowers updates are somewhat coding-agent dependent, but are often automatic.

## License

MIT License - see LICENSE file for details

## Community

Superfastpowers is built by [Jesse Vincent](https://blog.fsck.com) and the rest of the folks at [Prime Radiant](https://primeradiant.com).

- **Discord**: [Join us](https://discord.gg/35wsABTejz) for community support, questions, and sharing what you're building with Superfastpowers
- **Issues**: https://github.com/obra/superfastpowers/issues
- **Release announcements**: [Sign up](https://primeradiant.com/superfastpowers/) to get notified about new versions
