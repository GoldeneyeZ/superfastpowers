# Superfastpowers Contributor Guidelines

## Working Style

- Use the smallest workflow proportional to change risk.
- Implement focused changes directly; avoid process artifacts unless they add clear value.
- Run focused tests, then one final verification pass.
- Do not require task-package decomposition, multi-session evaluations, staged review gates, repeated gate invalidation, or sequential subagent reviews unless the human explicitly requests them.
- Stop expanding review scope after acceptance criteria pass. Record unrelated findings separately.
- Prefer one implementation pass and one review pass.

## Pull Requests

- Target `dev`, not `main`.
- Keep one coherent problem per PR.
- Complete the PR template with accurate information.
- Search open and closed PRs for duplicates before submission.
- Disclose agent/model/harness use honestly.
- Show the complete diff to the human and obtain explicit approval before opening the PR.

## Quality

- Solve a real, described problem.
- Preserve zero-dependency core unless adding a supported harness requires otherwise.
- Add tests proportional to behavior changed.
- Never fabricate results, sessions, or compatibility claims.
- Domain-specific or fork-specific features belong outside upstream core unless maintainers explicitly request them.
