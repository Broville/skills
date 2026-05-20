---
name: verification-before-completion
description: Mandatory verify-before-claiming-done gate — run verification commands and confirm output before making any success claims
version: 1.0.0
author: Broville
license: MIT
platforms: [linux, macos]
trigger:
  - About to claim work is complete, fixed, or passing
  - Ready to commit, push, or create a PR
  - Expressing satisfaction or confidence about a task
metadata:
  hermes:
    tags: [verification, quality, testing, completion]
    related_skills: [systematic-debugging, code-review-checklist]
---

# Verification Before Completion

## Description

Claiming work is complete without verification wastes time and erodes trust. This skill enforces a strict gate: evidence before assertions, always.

**Core principle:** Evidence before claims, always.

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this session, you cannot claim it passes.

## The Gate Function

Before claiming ANY status or expressing satisfaction:

1. **IDENTIFY**: What command proves this claim?
2. **RUN**: Execute the FULL command (fresh, complete)
3. **READ**: Full output, check exit code, count failures
4. **VERIFY**: Does output confirm the claim?
5. **ONLY THEN**: Make the claim

## Common Claims and Required Evidence

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Requirements met | Line-by-line checklist | Tests passing but gaps |

## Steps

### Before Claiming Tests Pass
```bash
npm test  # Run full suite, check exit code AND output
```

### Before Claiming Linter Clean
```bash
npm run lint  # Exit code 0 AND zero errors
```

### Before Claiming Build Succeeds
```bash
npm run build  # Exit code 0 AND no errors
```

### Before Claiming Bug Fixed
1. Run the test that reproduces the original bug
2. Verify it passes now
3. Verify no other tests broke (full suite)

### Before Claiming Requirements Met
- Re-read the requirements
- Create a checklist of each requirement
- Verify each one individually with evidence

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | Run the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ compiler |

## Pitfalls

1. **Trusting stale results** — Re-run after changes
2. **Partial verification** — Only running related tests misses regressions
3. **Confusing "looks correct" with "is correct"** — Running it is verification
4. **Skipping the red-green cycle** — A test that always passes proves nothing