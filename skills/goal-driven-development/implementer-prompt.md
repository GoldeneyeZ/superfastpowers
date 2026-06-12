# Goal-Driven Implementer Prompt Template

Use for implementer phase of packaged task.

```
Phase: Implement [TASK-ID]: [task name]

Instructions:
    You implement [TASK-ID]: [task name].

    ## Task Package

    Task directory: [path/to/tasks/<TASK-ID>/]
    Context file: [path/to/tasks/<TASK-ID>/context.md]
    Implementer handoff file: [path/to/tasks/<TASK-ID>/implementer-handoff.md]
    Plan progression file: [path/to/plan-progression.md]

    ## Task Context

    [Paste context.md contents]

    ## Current Handoff

    [Paste implementer-handoff.md if it exists. If absent, say "No active handoff."]

    ## Your Job

    1. Implement exactly task package requires, or fix exactly handoff requests.
    2. Inspect files needed for correct work.
    3. Write or update tests as needed.
    4. Run verification commands.
    5. Commit work with required task ID prefix.
    6. Update `context.md` before report.
    7. Update your task section in `plan-progression.md`.
    8. Clear `implementer-handoff.md` if active handoff fixed.

    Only edit your task section in `plan-progression.md`.

    When implementation or review-fix work is review-ready, set:
    - Implementer: checked
    - Task status: spec-checking
    - Next action: Run spec review.

    ## Context File Update

    Before report, update `context.md` with:
    - Final task commit SHA or reviewed commit range
    - Files created
    - Files modified
    - Additional files inspected or relevant
    - Verification commands run and results
    - Current implementation notes reviewers need

    If fixing review findings, include what changed for `implementer-handoff.md`.

    ## Handoff Cleanup

    If `implementer-handoff.md` had active requested fixes, clear it before reporting DONE by replacing it with:
    - Status: resolved
    - Resolved by commit/range
    - One-sentence fix summary

    ## Commit Requirement

    Prefer one commit per task. Prefix commit subject with `[<TASK-ID>]`.

    Example:
    `git commit -m "[GD-3] fix: handle failed spec handoff"`

    If fixing review findings and repo policy permits, amend task commit. If follow-up commits unavoidable, record reviewed range in `context.md`.

    ## Before You Begin

    Ask if requirements, acceptance criteria, or handoff instructions unclear.
    Do not guess.

    ## Before Reporting Back: Self-Review

    Review completeness, quality, discipline, test coverage. Fix issues before report.

    ## Report Format

    - **Status:** DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
    - What you implemented or fixed
    - What you tested and test results
    - Files changed
    - `context.md` updated? yes/no, with path
    - `implementer-handoff.md` cleared or not applicable? yes/no, with path
    - `plan-progression.md` updated? yes/no
    - Commit SHA or reviewed range
    - Concerns or questions
```
