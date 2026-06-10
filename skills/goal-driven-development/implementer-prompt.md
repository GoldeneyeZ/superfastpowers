# Goal-Driven Implementer Prompt Template

Use as instructions for the implementer phase of a packaged task.

```
Phase: Implement [TASK-ID]: [task name]

Instructions:
    You are implementing [TASK-ID]: [task name].

    ## Task Package

    Task directory: [path/to/tasks/<TASK-ID>/]
    Context file: [path/to/tasks/<TASK-ID>/context.md]
    Implementer handoff file: [path/to/tasks/<TASK-ID>/implementer-handoff.md]
    Plan progression file: [path/to/plan-progression.md]

    ## Task Context

    [Paste context.md contents]

    ## Current Handoff

    [Paste implementer-handoff.md if it exists. If it does not exist, say "No active handoff."]

    ## Your Job

    1. Implement exactly what the task package requires, or fix exactly what the handoff requests.
    2. Inspect any files needed to complete the task correctly.
    3. Write or update tests as needed.
    4. Run verification commands.
    5. Commit your work using the required task ID prefix.
    6. Update `context.md` before reporting back.
    7. Update your task section in `plan-progression.md`.
    8. Clear `implementer-handoff.md` if you fixed an active handoff.

    Only edit your task section in `plan-progression.md`.

    When implementation or review-fix work is ready for review, set:
    - Implementer: checked
    - Task status: spec-checking
    - Next action: Run spec review.

    ## Context File Update

    Before reporting back, update `context.md` with:
    - Final task commit SHA or reviewed commit range
    - Files created
    - Files modified
    - Additional files inspected or relevant to the task
    - Verification commands run and results
    - Current implementation notes needed by reviewers

    If you are fixing review findings, include what changed in response to
    `implementer-handoff.md`.

    ## Handoff Cleanup

    If `implementer-handoff.md` contained active requested fixes, clear it before
    reporting DONE by replacing it with:
    - Status: resolved
    - Resolved by commit/range
    - One-sentence summary of the fix

    ## Commit Requirement

    Prefer one commit per task. Prefix the commit message subject with `[<TASK-ID>]`.

    Example:
    `git commit -m "[GD-3] fix: handle failed spec handoff"`

    If you are fixing review findings and repository policy permits, amend the
    task commit. If follow-up commits are unavoidable, record the reviewed range
    in `context.md`.

    ## Before You Begin

    Ask questions if requirements, acceptance criteria, or handoff instructions are unclear.
    Do not guess.

    ## Before Reporting Back: Self-Review

    Review your work for completeness, quality, discipline, and test coverage. Fix issues you find before reporting.

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
