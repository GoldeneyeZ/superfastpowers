---
name: writing-skills
description: Use when creating, editing, or reviewing reusable agent skills.
---

# Writing Skills

## Goal

Create a clear, discoverable skill quickly. Prefer a small useful skill over a process campaign.

## Fast Workflow

1. State trigger and expected behavior in one sentence each.
2. Inspect one or two adjacent skills for repository conventions.
3. Write or edit `SKILL.md` directly.
4. Add supporting files only when they prevent the main skill from becoming unwieldy.
5. Run one focused review and relevant fast deterministic checks.
6. Fix findings once, rerun checks, finish.

Do not require task packages, baseline failure sessions, multiple clean sessions, adversarial campaigns, separate review agents, staged review gates, or evaluation reports unless the human explicitly requests them.

## Skill Shape

```yaml
---
name: skill-name
description: Use when [specific trigger conditions].
---
```

Recommended body:

- Goal or overview
- Preconditions, if any
- Short workflow
- Safety constraints
- Examples or quick reference only when useful

Keep most skills below 250 lines. Move large reference material out only when needed.

## Description Rules

- Start with `Use when`.
- Describe trigger conditions, not full workflow.
- Include terms agents will search for.
- Avoid vague claims such as “helps with development.”

## Review Checklist

- Frontmatter parses; name matches directory.
- Trigger is specific and discoverable.
- Instructions are executable and non-contradictory.
- No unnecessary mandatory ceremony.
- Commands, file paths, and linked references exist.
- Safety rules are proportional to actual risk.
- Skill does not duplicate another skill without reason.

One reviewer or one self-review is enough by default. Review actual diff once. Do not restart completed review stages because a later review finds a focused issue; fix issue, run affected checks, finish.

## Testing

Default checks:

```bash
python3 /home/goldeneye/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/<skill-name>
git diff --check
```

Add a fast deterministic test when skill includes a parser, script, stable file contract, or regression-prone logic. Avoid external model/harness tests by default. Never require repeated live-agent runs for ordinary skill changes.

## Completion

Report changed files, focused checks, known limitations. Show diff when requested. No eval report, progression file, or review artifact required.
