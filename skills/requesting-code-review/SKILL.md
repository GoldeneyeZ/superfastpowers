---
name: requesting-code-review
description: Use when a completed change needs an independent or focused review before integration.
---

# Requesting Code Review

## Default

Review combined completed diff once. Self-review is enough for small low-risk changes; independent reviewer helps for security, concurrency, public APIs, migrations, or large changes.

Do not require review after every task, separate spec and quality reviewers, review artifacts, or full workflow restarts.

## Review Input

- concise requirements;
- base and head range or current diff;
- changed paths;
- focused test results;
- known risks.

Use `code-reviewer.md` when delegating.

## Review Focus

- requirements and correctness;
- security or data-loss risks;
- regressions/integration;
- maintainability proportional to scope;
- test gaps.

Classify findings: blocking, important, minor. Fix blocking/important findings in scope. Incorrect finding → reject with evidence. Focused fix → rerun affected checks; no mandatory re-review unless risk remains.

## Completion

One accepted review plus green relevant tests. More review only by evidence or explicit request.
