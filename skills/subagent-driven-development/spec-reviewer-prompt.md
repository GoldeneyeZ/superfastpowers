# Spec Compliance Reviewer Prompt Template

Use template when dispatching spec compliance reviewer subagent.

**Purpose:** Verify implementer built requested work only (nothing more/less)

```
Task tool (general-purpose):
  description: "Review spec compliance for Task N"
  prompt: |
    You are reviewing whether an implementation matches its specification.

    ## What Was Requested

    [FULL TEXT of task requirements]

    ## What Implementer Claims They Built

    [From implementer's report]

    ## Task Package Context

    Task package directory: [path/to/tasks/<TASK-ID>/, if present]

    [Paste task package context.md if present]

    ## CRITICAL: Do Not Trust the Report

    The implementer report and `context.md` may be incomplete, inaccurate, stale,
    or optimistic. Use them as a map, not as proof. You MUST verify everything
    independently.

    **DO NOT:**
    - Take their word for what they implemented
    - Trust their claims about completeness
    - Accept their interpretation of requirements
    - Assume `context.md` lists every relevant file

    **DO:**
    - Read the actual code they wrote
    - Use the task package directory and `context.md` to find the task commit and likely relevant files
    - Compare `context.md` against the actual diff for missing or inaccurate file lists
    - Compare actual implementation to requirements line by line
    - Check for missing pieces they claimed to implement
    - Look for extra features they didn't mention

    ## Your Job

    Read the implementation code and verify:

    **Missing requirements:**
    - Did they implement everything that was requested?
    - Are there requirements they skipped or missed?
    - Did they claim something works but didn't actually implement it?

    **Extra/unneeded work:**
    - Did they build things that weren't requested?
    - Did they over-engineer or add unnecessary features?
    - Did they add "nice to haves" that weren't in spec?

    **Misunderstandings:**
    - Did they interpret requirements differently than intended?
    - Did they solve the wrong problem?
    - Did they implement the right feature but wrong way?

    **Context package hygiene:**
    - Did the implementer replace the pending commit SHA with the final task commit SHA or reviewed range?
    - Does `context.md` list files created and modified by the task?
    - Does it include additional files that were relevant to the task, if any?
    - Are verification commands/results recorded?

    **Verify by reading code, not by trusting report.**

    Report:
    - ✅ Spec compliant (if everything matches after code inspection)
    - ❌ Issues found: [list specifically what's missing or extra, with file:line references]
    - Context package issues, if any
```
