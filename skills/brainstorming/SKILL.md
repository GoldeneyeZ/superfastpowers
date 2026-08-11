---
name: brainstorming
description: Use when a requested feature has unresolved product, behavior, or architecture choices.
---

# Brainstorming

## Goal

Resolve decisions blocking implementation. Scale discussion to uncertainty.

## Fast Workflow

1. Inspect relevant project context.
2. Identify unresolved choices.
3. Ask only questions whose answers materially change implementation; batch closely related questions when useful.
4. For meaningful trade-offs, present concise options plus recommendation.
5. Summarize chosen design at proportional detail.
6. Proceed once user confirms material choices, or immediately when request already determines them.

Small, explicit changes do not require a design document, multiple approaches, repeated section approvals, or a separate planning phase.

## When a Written Spec Helps

Write a spec for cross-component features, durable public behavior, migrations, or architecture decisions. Otherwise keep design in conversation or implementation plan.

Review written spec once for ambiguity, contradictions, missing acceptance criteria, and scope. Fix inline. Commit only if user requested commits or normal workflow calls for it.

## Principles

- YAGNI.
- Follow existing project patterns.
- Avoid unrelated refactors.
- Prefer reversible decisions.
- Ask rather than assume only when wrong assumption materially changes result.
- Visual companion optional; use only when visual interaction materially improves decision.

## Handoff

Use `writing-plans` only for genuinely multi-step work. Small approved changes may proceed directly to implementation.
