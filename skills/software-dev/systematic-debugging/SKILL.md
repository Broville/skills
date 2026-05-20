---
name: systematic-debugging
description: 4-phase debugging methodology — understand, isolate, fix, verify — find root cause before attempting fixes
version: 1.0.0
author: Broville
license: MIT
platforms: [linux]
trigger:
  - Encountering any bug, test failure, or unexpected behavior
  - Needing to debug production issues, build failures, or integration problems
  - About to propose a fix without understanding root cause
  - Multiple fix attempts have failed
related_skills:
  - verification-before-completion
  - git-advanced-workflows
  - code-review-checklist
---

# Systematic Debugging

## Description

A structured 4-phase debugging methodology that prioritizes root cause understanding over quick fixes. Random patches waste time and create new bugs. This skill enforces investigation before remediation — find the root cause, then fix it.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## When to Use

- Test failures, bugs in production, unexpected behavior
- Performance problems, build failures, integration issues
- **Especially when:** under time pressure, multiple fixes have failed, the issue "seems simple"

## The Four Phases

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read Error Messages Carefully**
   - Don't skip past errors or warnings — they often contain the exact solution
   - Read stack traces completely; note line numbers, file paths, error codes
   ```bash
   # Run with verbose output to capture full error context
   npm test -- --verbose 2>&1 | tee test-output.log
   # or
   go test -v ./... 2>&1 | tee test-output.log
   ```

2. **Reproduce Consistently**
   - Can you trigger it reliably? What are the exact steps?
   - If not reproducible, gather more data — don't guess
   ```bash
   # Create a minimal reproduction script
   # Document exact environment, inputs, and state
   ```

3. **Check Recent Changes**
   ```bash
   # What changed that could cause this?
   git log --oneline -20
   git diff HEAD~5 HEAD -- suspicious-file.ts
   git diff main..HEAD
   ```

4. **Gather Evidence in Multi-Component Systems**
   - For each component boundary: log what enters and exits
   - Run once to gather evidence showing WHERE it breaks
   - Then analyze evidence to identify the failing component
   ```bash
   # Example: trace data through layers
   echo "=== Layer 1: Input data ==="
   echo "VAR_NAME: ${VAR_NAME:+SET}${VAR_NAME:-UNSET}"
   echo "=== Layer 2: Processing ==="
   env | grep VAR_NAME || echo "VAR_NAME not in environment"
   echo "=== Layer 3: Output check ==="
   # Verify at each boundary
   ```

5. **Trace Data Flow (Deep Call Stack)**
   - Where does the bad value originate?
   - What called this with the bad value?
   - Keep tracing up until you find the source
   - Fix at source, not at symptom

   See `references/root-cause-tracing.md` for the complete backward tracing technique.

### Phase 2: Pattern Analysis

**Find the pattern before fixing:**

1. **Find Working Examples** — Locate similar working code in the same codebase
2. **Compare Against References** — Read reference implementations completely, not skimming
3. **Identify Differences** — List every difference between working and broken, however small
4. **Understand Dependencies** — What settings, config, environment does this need?

### Phase 3: Hypothesis and Testing

**Scientific method:**

1. **Form Single Hypothesis** — State clearly: "I think X is the root cause because Y"
2. **Test Minimally** — Make the SMALLEST possible change to test the hypothesis; one variable at a time
3. **Verify Before Continuing** — Did it work? Yes → Phase 4. No → form a NEW hypothesis, don't stack fixes
4. **When You Don't Know** — Say "I don't understand X" rather than guessing

### Phase 4: Implementation

**Fix the root cause, not the symptom:**

1. **Create Failing Test Case**
   ```bash
   # Simplest possible reproduction
   # Automated test if possible, one-off script if no framework
   # You MUST have a failing test BEFORE fixing
   ```

2. **Implement Single Fix** — Address the root cause identified. ONE change at a time. No "while I'm here" improvements.

3. **Verify Fix Works**
   ```bash
   # Run the original failing test — must pass now
   # Run the full test suite — no regressions
   npm test
   ```

4. **If Fix Doesn't Work**
   - STOP. Count: how many fixes have you tried?
   - If < 3: Return to Phase 1 with new information
   - If ≥ 3: STOP and question the architecture

5. **If 3+ Fixes Failed: Question Architecture**
   - Each fix reveals new shared state/coupling problems
   - Fixes require "massive refactoring"
   - Each fix creates new symptoms elsewhere

   These patterns indicate a fundamentally wrong architecture — discuss with stakeholders before attempting more fixes.

## Red Flags — STOP and Follow Process

- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "One more fix attempt" (when already tried 2+)
- Each fix reveals a new problem in a different place

**ALL of these mean: STOP. Return to Phase 1.**

## Supporting Techniques

- **`references/root-cause-tracing.md`** — Trace bugs backward through call stack to find original trigger
- **`references/defense-in-depth.md`** — Add validation at multiple layers after finding root cause
- **`references/condition-based-waiting.md`** — Replace arbitrary timeouts with condition polling
- **`scripts/find_polluter.sh`** — Bisection script to find which test creates unwanted state

## Finding Test Pollution

Use the `scripts/find_polluter.sh` script to find which test creates unwanted files or state:

```bash
# Syntax: find_polluter.sh <file_or_dir_to_check> <test_pattern>
./scripts/find_polluter.sh '.git' 'src/**/*.test.ts'
```

This runs tests one-by-one and stops at the first test that creates the specified pollution.

## Pitfalls

1. **Guessing instead of investigating** — "It's probably X" is a hypothesis, not a conclusion. Test it before fixing.
2. **Stacking fixes** — Making multiple changes at once makes it impossible to know what worked. One change at a time.
3. **Fixing symptoms** — Error appears deep in the call stack but the root cause is upstream. Trace backward before fixing.
4. **Skipping the failing test** — Without a failing test, you can't confirm the fix works and can't prevent regression.
5. **Refusing to question architecture** — After 3+ failed fixes, the architecture is likely the problem. Stop fixing symptoms.

## Verification

1. **Reproduction confirmed:** The bug can be triggered reliably before the fix
2. **Root cause identified:** A specific, testable hypothesis explains why the bug occurs
3. **Failing test exists:** An automated test reproduces the bug
4. **Fix confirmed:** The failing test passes, full suite passes with no regressions
   ```bash
   # Verify the fix
   npm test  # or: go test ./..., pytest, etc.
   # Confirm no regressions
   git diff HEAD --stat  # review changes are minimal and targeted
   ```

## Cross-References

- **verification-before-completion** — Verify fix worked before claiming success
- **git-advanced-workflows** — Use `git bisect` for finding when a bug was introduced
- **code-review-checklist** — Review checklist for catching bugs before they ship