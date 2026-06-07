---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes
---

# Systematic Debugging

## Overview

Random fixes waste time, create bugs. Quick patches mask root issues.

**Core principle:** ALWAYS find root cause before fixes. Symptom fixes fail.

**Violating letter of this process violates spirit of debugging.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If Phase 1 incomplete, cannot propose fixes.

## When to Use

Use for ANY technical issue:
- Test failures
- Production bugs
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

**Use this ESPECIALLY when:**
- Time pressure makes guessing tempting
- "Just one quick fix" seems obvious
- Multiple fixes already tried
- Previous fix failed
- Issue not fully understood

**Don't skip when:**
- Issue seems simple (simple bugs have root causes too)
- You're in hurry (rush guarantees rework)
- Manager wants fix NOW (systematic beats thrash)

## The Four Phases

Complete each phase before next.

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read Error Messages Carefully**
   - Don't skip errors/warnings
   - Often contain exact solution
   - Read full stack traces
   - Note line numbers, file paths, error codes

2. **Reproduce Consistently**
   - Can you trigger reliably?
   - Exact steps?
   - Every time?
   - If not reproducible → gather more data, don't guess

3. **Check Recent Changes**
   - What changed that could cause this?
   - Git diff, recent commits
   - New dependencies, config changes
   - Environment differences

4. **Gather Evidence in Multi-Component Systems**

   **WHEN system has multiple components (CI → build → signing, API → service → database):**

   **BEFORE proposing fixes, add diagnostic instrumentation:**
   ```
   For EACH component boundary:
     - Log what data enters component
     - Log what data exits component
     - Verify environment/config propagation
     - Check state at each layer

   Run once to gather evidence showing WHERE it breaks
   THEN analyze evidence to identify failing component
   THEN investigate that specific component
   ```

   **Example (multi-layer system):**
   ```bash
   # Layer 1: Workflow
   echo "=== Secrets available in workflow: ==="
   echo "IDENTITY: ${IDENTITY:+SET}${IDENTITY:-UNSET}"

   # Layer 2: Build script
   echo "=== Env vars in build script: ==="
   env | grep IDENTITY || echo "IDENTITY not in environment"

   # Layer 3: Signing script
   echo "=== Keychain state: ==="
   security list-keychains
   security find-identity -v

   # Layer 4: Actual signing
   codesign --sign "$IDENTITY" --verbose=4 "$APP"
   ```

   **This reveals:** Failing layer (secrets → workflow ✓, workflow → build ✗)

5. **Trace Data Flow**

   **WHEN error is deep in call stack:**

   See `root-cause-tracing.md` in this directory for the complete backward tracing technique.

   **Quick version:**
   - Where bad value originates?
   - What called this with bad value?
   - Trace up until source found
   - Fix source, not symptom

### Phase 2: Pattern Analysis

**Find pattern before fixing:**

1. **Find Working Examples**
   - Locate similar working code in same codebase
   - What works similar to broken thing?

2. **Compare Against References**
   - If implementing pattern, read reference implementation COMPLETELY
   - Don't skim; read every line
   - Understand pattern fully before applying

3. **Identify Differences**
   - What's different between working and broken?
   - List every difference, however small
   - Don't assume "that can't matter"

4. **Understand Dependencies**
   - What other components needed?
   - What settings, config, environment?
   - What assumptions?

### Phase 3: Hypothesis and Testing

**Scientific method:**

1. **Form Single Hypothesis**
   - State clearly: "I think X is the root cause because Y"
   - Write it down
   - Specific, not vague

2. **Test Minimally**
   - Smallest possible change to test hypothesis
   - One variable at time
   - Don't fix multiple things at once

3. **Verify Before Continuing**
   - Worked? Yes → Phase 4
   - Failed? Form NEW hypothesis
   - DON'T stack fixes

4. **When You Don't Know**
   - Say "I don't understand X"
   - Don't pretend
   - Ask for help
   - Research more

### Phase 4: Implementation

**Fix root cause, not symptom:**

1. **Create Failing Test Case**
   - Simplest reproduction
   - Automated test if possible
   - One-off test script if no framework
   - MUST exist before fixing
   - Use the `superfastpowers:test-driven-development` skill for writing proper failing tests

2. **Implement Single Fix**
   - Address identified root cause
   - ONE change at time
   - No "while I'm here" improvements
   - No bundled refactoring

3. **Verify Fix**
   - Test passes now?
   - Other tests still pass?
   - Issue actually resolved?

4. **If Fix Doesn't Work**
   - STOP
   - Count fixes tried
   - If < 3: Return to Phase 1, re-analyze with new info
   - **If ≥ 3: STOP and question the architecture (step 5 below)**
   - DON'T attempt Fix #4 without architectural discussion

5. **If 3+ Fixes Failed: Question Architecture**

   **Pattern indicating architectural problem:**
   - Each fix reveals new shared state/coupling/problem elsewhere
   - Fixes require "massive refactoring"
   - Each fix creates new symptoms elsewhere

   **STOP and question fundamentals:**
   - Is pattern fundamentally sound?
   - Are we "sticking with it through sheer inertia"?
   - Refactor architecture vs. keep fixing symptoms?

   **Discuss with your human partner before attempting more fixes**

   This is NOT failed hypothesis; this is wrong architecture.

## Red Flags - STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals new problem in different place**

**ALL of these mean: STOP. Return to Phase 1.**

**If 3+ fixes failed:** Question the architecture (see Phase 4.5)

## your human partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Is that not happening?" - You assumed without verifying
- "Will it show us...?" - Should have added evidence gathering
- "Stop guessing" - You're proposing fixes without understanding
- "Ultrathink this" - Question fundamentals, not just symptoms
- "We're stuck?" (frustrated) - Approach isn't working

**When you see these:** STOP. Return to Phase 1.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging FASTER than guess-and-check thrash. |
| "Just try this first, then investigate" | First fix sets pattern. Do right from start. |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees bugs. Read completely. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question pattern, don't fix again. |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare | Identify differences |
| **3. Hypothesis** | Form theory, test minimally | Confirmed or new hypothesis |
| **4. Implementation** | Create test, fix, verify | Bug resolved, tests pass |

## When Process Reveals "No Root Cause"

If systematic investigation shows issue truly environmental, timing-dependent, or external:

1. Process completed
2. Document what you investigated
3. Implement appropriate handling (retry, timeout, error message)
4. Add monitoring/logging for future investigation

**But:** 95% of "no root cause" cases are incomplete investigation.

## Supporting Techniques

Techniques part of systematic debugging, available in this directory:

- **`root-cause-tracing.md`** - Trace bugs backward through call stack to original trigger
- **`defense-in-depth.md`** - Add validation at multiple layers after finding root cause
- **`condition-based-waiting.md`** - Replace arbitrary timeouts with condition polling

**Related skills:**
- **superfastpowers:test-driven-development** - For creating failing test case (Phase 4, Step 1)
- **superfastpowers:verification-before-completion** - Verify fix worked before claiming success

## Real-World Impact

From debugging sessions:
- Systematic approach: 15-30 minutes to fix
- Random fixes approach: 2-3 hours thrashing
- First-time fix rate: 95% vs 40%
- New bugs introduced: Near zero vs common
