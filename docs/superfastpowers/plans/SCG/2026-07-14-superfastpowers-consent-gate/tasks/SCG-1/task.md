### Task 1: Add conversation-scoped automatic-skill consent

<TASK-ID>SCG-1</TASK-ID>

**Files:**
- Modify: `skills/using-superfastpowers/SKILL.md`
- Create: `tests/claude-code/test-using-superfastpowers-consent.sh`
- Modify: `docs/superfastpowers/plans/SCG/2026-07-14-superfastpowers-consent-gate/tasks/SCG-1/context.md`

- [ ] Write static failing contract test for bootstrap exception, one prompt per conversation, waiting, yes/no/silence, and explicit requests.
- [ ] Run it and confirm failure comes from missing consent contract.
- [ ] Record five behavioral RED scenarios from unmodified skill.
- [ ] Add minimal consent gate before existing automatic invocation rule; gate flow on affirmative consent.
- [ ] Run static test and confirm pass.
- [ ] Repeat behavioral scenarios; close only observed loopholes; rerun.
- [ ] Run static regression suite.
- [ ] Update `context.md` with commits, files, and verification evidence.
- [ ] Commit as `feat: require consent for automatic skill use`.
