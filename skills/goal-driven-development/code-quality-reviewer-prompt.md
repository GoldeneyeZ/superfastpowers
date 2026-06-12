# Goal-Driven Code Quality Reviewer Prompt Template

Use for code quality review phase of packaged task.

Only run after spec compliance is `checked`.

```
Phase: Review code quality for [TASK-ID]

Instructions:
    You review code quality for [TASK-ID].

    ## Task Package

    Task directory: [path/to/tasks/<TASK-ID>/]
    Context file: [path/to/tasks/<TASK-ID>/context.md]
    Code quality review file: [path/to/tasks/<TASK-ID>/code-quality.md]
    Implementer handoff file: [path/to/tasks/<TASK-ID>/implementer-handoff.md]
    Plan progression file: [path/to/plan-progression.md]

    ## Task Context

    [Paste context.md contents]

    ## Spec Review

    [Paste spec-review.md contents showing Result: checked]

    ## Your Job

    Review committed implementation for:
    - Correctness risks spec review missed
    - Test quality and meaningful assertions
    - Maintainability
    - Clear names and focused files
    - Fit with existing project patterns
    - Overbroad changes or unrelated refactors
    - Accurate `context.md` commit/range, file list, verification evidence

    Do not relitigate spec compliance unless quality issue exposes spec miss.
    Only edit this task's code quality and task status fields in `plan-progression.md`.

    ## If Quality Review Passes

    Write `code-quality.md` with:
    - Result: checked
    - Evidence reviewed
    - Short notes: why implementation is maintainable and tested

    If minor non-blocking notes exist, write:
    - Result: checked-with-minor-notes
    - Minor notes that do not block task
    - Evidence reviewed

    Update this task in `plan-progression.md`:
    - Code quality: checked OR checked-with-minor-notes
    - Task status: complete
    - Next action: Task complete; continue to next task.

    Do not write new failure handoff.

    ## If Quality Review Fails

    Write `code-quality.md` with:
    - Result: failed
    - Issues grouped by Critical, Important, Minor
    - File:line refs where possible
    - Evidence reviewed

    Write `implementer-handoff.md` with:
    - Review type: quality
    - Required fixes
    - Files or areas to inspect
    - Acceptance criteria for re-review

    Update this task in `plan-progression.md`:
    - Code quality: failed
    - Task status: implementing
    - Next action: Fix quality findings in this task's `code-quality.md`.

    Handoff must be actionable and concise. Implementer works from it directly.

    ## Report Format

    - **Result:** checked | failed
    - Review file updated? yes/no, with path
    - Handoff updated? yes/no, with path
    - `plan-progression.md` updated? yes/no
    - One-sentence next action for controller
```
