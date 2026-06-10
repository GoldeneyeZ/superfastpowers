# Goal-Driven Spec Reviewer Prompt Template

Use as instructions for the spec compliance review phase of a packaged task.

```
Phase: Review spec compliance for [TASK-ID]

Instructions:
    You are reviewing whether [TASK-ID] matches its specification.

    ## Task Package

    Task directory: [path/to/tasks/<TASK-ID>/]
    Context file: [path/to/tasks/<TASK-ID>/context.md]
    Spec review file: [path/to/tasks/<TASK-ID>/spec-review.md]
    Implementer handoff file: [path/to/tasks/<TASK-ID>/implementer-handoff.md]
    Plan progression file: [path/to/plan-progression.md]

    ## Task Context

    [Paste context.md contents]

    ## Implementer Report

    [Paste implementer report]

    ## CRITICAL: Verify Independently

    Do not trust the implementer report or `context.md` as proof. Use them as a map.
    Read the actual code and compare it against the task requirements.

    ## Your Job

    Check:
    - Missing requirements
    - Extra or unrequested behavior
    - Misunderstood requirements
    - Incorrect or stale `context.md` details
    - Missing commit SHA, reviewed range, file list, or verification evidence

    Only edit this task's spec review fields in `plan-progression.md`.

    ## If Spec Review Passes

    Write `spec-review.md` with:
    - Result: checked
    - Evidence reviewed
    - Short notes on why the implementation matches the task

    Update this task in `plan-progression.md`:
    - Spec review: checked
    - Task status: quality-checking
    - Next action: Run code quality review.

    Do not write a new failure handoff.

    ## If Spec Review Fails

    Write `spec-review.md` with:
    - Result: failed
    - Specific findings with file:line references where possible
    - Missing or extra behavior
    - Evidence reviewed

    Write `implementer-handoff.md` with:
    - Review type: spec
    - Required fixes
    - Files or areas to inspect
    - Acceptance criteria for re-review

    Update this task in `plan-progression.md`:
    - Spec review: failed
    - Code quality: unchecked
    - Task status: implementing
    - Next action: Fix spec findings in this task's `spec-review.md`.

    Keep the handoff actionable and concise. The implementer should be able to work from it directly.

    ## Report Format

    - **Result:** checked | failed
    - Review file updated? yes/no, with path
    - Handoff updated? yes/no, with path
    - `plan-progression.md` updated? yes/no
    - One-sentence next action for the controller
```
