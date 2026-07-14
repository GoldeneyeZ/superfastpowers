# Superfastpowers Conversation Consent Gate

## Problem

`using-superfastpowers` currently requires agents to invoke every relevant skill before any response or action. Users therefore receive automatic Superfastpowers behavior without first choosing whether to enable it for the conversation.

## Goal

Ask once per conversation before automatically invoking any Superfastpowers skill other than the bootstrap itself. Preserve normal automatic skill discovery after consent and preserve direct use of explicitly requested skills.

## Consent Model

`using-superfastpowers` remains the bootstrap exception because it must load before it can request consent. On its first activation in a conversation, it asks:

> Use Superfastpowers skills automatically for this conversation?

The agent must wait for the answer before automatically invoking another Superfastpowers skill.

- **Yes:** Record consent for the current conversation, then apply existing automatic skill-selection rules.
- **No:** Record refusal for the current conversation and do not automatically invoke Superfastpowers skills.
- **No answer:** Treat consent as unresolved. Do not automatically invoke another Superfastpowers skill.

Consent is conversation-scoped. Once answered, the agent must not ask again during that conversation.

## Explicit Skill Requests

An explicit request to use a named Superfastpowers skill is not automatic invocation. The agent may invoke that requested skill even when automatic use was declined. Explicit invocation does not enable unrelated automatic skills and does not change the stored conversation preference.

## Skill Changes

Update `skills/using-superfastpowers/SKILL.md` only:

1. Change frontmatter trigger wording to describe the conversation-start consent gate without summarizing its implementation.
2. Add an early, prominent consent gate before the existing mandatory automatic-invocation rule.
3. Scope the existing “must invoke” language to conversations where consent was granted, while retaining requested-skill behavior.
4. Update the decision flow and rationalization guidance so agents cannot interpret silence, task urgency, or prior-conversation consent as current consent.

No harness-specific hooks or bootstrap loaders change. They still load `using-superfastpowers`; the skill controls whether subsequent skills auto-run.

## Behavioral Tests

Use adversarial pressure scenarios before and after editing:

1. **Unresolved consent:** User gives a normal implementation request. Agent must ask before invoking `brainstorming` or another automatic skill.
2. **Consent granted:** User answers yes. Agent must not ask again and must resume existing automatic skill behavior.
3. **Consent declined:** User answers no. Agent must not ask again and must complete later tasks without automatic Superfastpowers skills.
4. **Explicit request after decline:** User names a Superfastpowers skill. Agent may invoke only the requested skill; automatic use remains disabled.
5. **Pressure:** Urgent task, “just do it,” or simple-question framing must not bypass unresolved consent.

RED captures baseline behavior from the unmodified skill. GREEN repeats identical scenarios after the minimal edit. REFACTOR adds only counters required by observed failures, then reruns the affected scenarios.

## Compatibility

Harnesses may continue injecting or loading `using-superfastpowers` at session start. Existing acceptance tests expecting immediate `brainstorming` auto-trigger will need revised expectations: the first observable behavior becomes the consent prompt, and `brainstorming` follows only after affirmative consent.

## Out of Scope

- Persistent preferences across conversations
- Harness-level settings or UI
- Consent prompts before explicitly requested skills
- Changes to non-Superfastpowers skills
- Changes to skill installation or discovery
