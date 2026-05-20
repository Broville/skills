---
name: systematic-debugging
description: 4-phase debugging methodology — understand, isolate, fix, verify — find root cause before attempting fixes
version: 1.0.0
author: Broville
license: MIT
platforms: [linux, macos]
trigger:
  - Encountering any bug, test failure, or unexpected behavior
  - Needing to debug production issues, build failures, or integration problems
  - About to propose a fix without understanding root cause
  - Multiple fix attempts have failed
metadata:
  hermes:
    tags: [debugging, root-cause, methodology, troubleshooting]
    related_skills: [verification-before-completion, git-advanced-workflows, code-review-checklist]
---

# Systematic Debugging

## Description

A structured 4-phase debugging methodology that prioritizes root cause understanding over quick fixes. Random patches waste time and create new bugs.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## The Four Phases

### Phase 1: Root Cause Investigation

1. **Read Error Messages Carefully** — stack traces, line numbers, error codes
2. **Reproduce Consistently** — exact steps, environment, state
3. **Check Recent Changes** — `git log --oneline -20`, `git diff`
4. **Gather Evidence in Multi-Component Systems** — log at each boundary
5. **Trace Data Flow** — keep tracing up until you find the source

### Phase 2: Pattern Analysis

1. Find working examples in the same codebase
2. Compare against references
3. Identify every difference
4. Understand dependencies

### Phase 3: Hypothesis and Testing

1. Form single hypothesis — "I think X is the root cause because Y"
2. Test minimally — smallest possible change, one variable at a time
3. Verify before continuing
4. When you don't know — say "I don't understand X" rather than guessing

### Phase 4: Implementation

1. Create failing test case
2. Implement single fix — ONE change at a time
3. Verify fix works (original test AND full suite)
4. If fix doesn't work after 3 attempts — question architecture

## Red Flags — STOP and Follow Process

- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "One more fix attempt" (when already tried 2+)

## Pitfalls

1. **Guessing instead of investigating** — "It's probably X" is a hypothesis, not a conclusion
2. **Stacking fixes** — One change at a time
3. **Fixing symptoms** — Trace backward before fixing
4. **Skipping the failing test** — Without it, you can't confirm or prevent regression
5. **Refusing to question architecture** — After 3+ failed fixes, the architecture is likely the problem

## Verification

1. Bug can be triggered reliably before the fix
2. Root cause hypothesis is specific and testable
3. Failing test reproduces the bug
4. Fix passes the failing test AND the full suite