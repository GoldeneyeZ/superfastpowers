---
name: using-superfastpowers
description: Use when starting any conversation - establishes how to find and use skills, requiring Skill tool invocation before ANY response including clarifying questions
---

<SUBAGENT-STOP>
Dispatched subagent with specific task: skip this skill.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
Even 1% chance skill applies? Invoke it.

IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.

Not negotiable. Not optional. No rationalizing out.
</EXTREMELY-IMPORTANT>

## Instruction Priority

Superfastpowers skills override default system prompt behavior, but **user instructions always take precedence**:

1. **User's explicit instructions** (CLAUDE.md, GEMINI.md, AGENTS.md, direct requests) — highest priority
2. **Superfastpowers skills** — override default system behavior where they conflict
3. **Default system prompt** — lowest priority

If CLAUDE.md, GEMINI.md, or AGENTS.md says "don't use TDD" and skill says "always use TDD," follow user instructions. User controls.

## How to Access Skills

**In Claude Code:** Use the `Skill` tool. Invoked skill content loads—follow directly. Never use Read tool on skill files.

**In Copilot CLI:** Use the `skill` tool. Skills auto-discovered from installed plugins. `skill` tool works like Claude Code's `Skill` tool.

**In Gemini CLI:** Skills activate via `activate_skill` tool. Gemini loads skill metadata at session start; activates full content on demand.

**In other environments:** Check platform docs for skill loading.

## Platform Adaptation

Skills use Claude Code tool names. Non-CC platforms: see `references/copilot-tools.md` (Copilot CLI), `references/codex-tools.md` (Codex) for tool equivalents. Gemini CLI users get tool mapping automatically via GEMINI.md.

# Using Skills

## The Rule

**Invoke relevant or requested skills BEFORE any response or action.** Even 1% chance skill might apply means invoke skill to check. If wrong for situation, no need use it.

```dot
digraph skill_flow {
    "User message received" [shape=doublecircle];
    "About to EnterPlanMode?" [shape=doublecircle];
    "Already brainstormed?" [shape=diamond];
    "Invoke brainstorming skill" [shape=box];
    "Might any skill apply?" [shape=diamond];
    "Invoke Skill tool" [shape=box];
    "Announce: 'Using [skill] to [purpose]'" [shape=box];
    "Has checklist?" [shape=diamond];
    "Create TodoWrite todo per item" [shape=box];
    "Follow skill exactly" [shape=box];
    "Respond (including clarifications)" [shape=doublecircle];

    "About to EnterPlanMode?" -> "Already brainstormed?";
    "Already brainstormed?" -> "Invoke brainstorming skill" [label="no"];
    "Already brainstormed?" -> "Might any skill apply?" [label="yes"];
    "Invoke brainstorming skill" -> "Might any skill apply?";

    "User message received" -> "Might any skill apply?";
    "Might any skill apply?" -> "Invoke Skill tool" [label="yes, even 1%"];
    "Might any skill apply?" -> "Respond (including clarifications)" [label="definitely not"];
    "Invoke Skill tool" -> "Announce: 'Using [skill] to [purpose]'";
    "Announce: 'Using [skill] to [purpose]'" -> "Has checklist?";
    "Has checklist?" -> "Create TodoWrite todo per item" [label="yes"];
    "Has checklist?" -> "Follow skill exactly" [label="no"];
    "Create TodoWrite todo per item" -> "Follow skill exactly";
}
```

## Red Flags

These thoughts mean STOP—rationalizing:

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions are tasks. Check skills. |
| "I need more context first" | Skill check BEFORE clarifying questions. |
| "Let me explore the codebase first" | Skills tell HOW to explore. Check first. |
| "I can check git/files quickly" | Files lack conversation context. Check skills. |
| "Let me gather information first" | Skills tell HOW to gather info. |
| "This doesn't need a formal skill" | If skill exists, use it. |
| "I remember this skill" | Skills evolve. Read current version. |
| "This doesn't count as a task" | Action = task. Check skills. |
| "The skill is overkill" | Simple things become complex. Use it. |
| "I'll just do this one thing first" | Check BEFORE anything. |
| "This feels productive" | Undisciplined action wastes time. Skills prevent. |
| "I know what that means" | Knowing concept ≠ using skill. Invoke it. |

## Skill Priority

When multiple skills could apply, use order:

1. **Process skills first** (brainstorming, debugging) - determine HOW to approach task
2. **Implementation skills second** (frontend-design, mcp-builder) - guide execution

"Let's build X" → brainstorming first, then implementation skills.
"Fix this bug" → debugging first, then domain-specific skills.

## Skill Types

**Rigid** (TDD, debugging): Follow exactly. Don't adapt away discipline.

**Flexible** (patterns): Adapt principles to context.

Skill itself tells which.

## User Instructions

Instructions say WHAT, not HOW. "Add X" or "Fix Y" doesn't mean skip workflows.
