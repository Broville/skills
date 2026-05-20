---
name: verification-before-completion
description: Mandatory verify-before-claiming-done gate — run verification commands and confirm output before making any success claims
version: 1.0.0
author: Broville
license: MIT
platforms: [linux]
trigger:
  - About to claim work is complete, fixed, or passing
  - Ready to commit, push, or create a PR
  - Delegating completed work to another agent or person
  - Expressing satisfaction or confidence about a task
related_skills:
  - systematic-debugging
  - code-review-checklist
  - deployment-procedures
---

# Verification Before Completion

## Description

Claiming work is complete without verification wastes time and erodes trust. This skill enforces a strict gate: evidence before assertions, always. No completion claims without fresh, verified evidence.

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
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. **ONLY THEN**: Make the claim

Skip any step = claiming without verifying.

## Common Claims and Required Evidence

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Requirements met | Line-by-line checklist | Tests passing but gaps in requirements |

## Steps

### Step 1: Before Claiming Tests Pass

```bash
# Run the full test suite and read the output
npm test    # or: pytest, go test ./..., etc.

# Check: exit code 0 AND "X tests passed, 0 failed" in output
# Do NOT claim "tests pass" until you see this
```

### Step 2: Before Claiming Linter Clean

```bash
# Run linter and check for zero errors
npm run lint    # or: eslint ., flake8, etc.

# Exit code 0 AND zero errors in output
```

### Step 3: Before Claiming Build Succeeds

```bash
# Run the build command
npm run build    # or: cargo build, go build, etc.

# Exit code 0 AND no errors in output
# Linter passing does NOT mean build passes
```

### Step 4: Before Claiming Bug Fixed

```bash
# 1. Run the test that reproduces the original bug
# 2. Verify it passes now
# 3. Verify no other tests broke (full suite)
npm test

# WITHOUT the fix, the test MUST fail (red-green cycle)
```

### Step 5: Before Claiming Requirements Met

```bash
# Re-read the requirements document
# Create a checklist of each requirement
# Verify each one individually with evidence
# Report gaps or completion — nothing in between
```

## Red Flags — STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!")
- About to commit/push/PR without verification
- Trusting a process exit code without reading the output
- Relying on partial verification (only one test, only linter)
- Thinking "just this once" is acceptable

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | Run the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ compiler |
| "Partial check is enough" | Partial proves nothing |
| "I'm tired" | Exhaustion is not an excuse |

## Pitfalls

1. **Trusting stale results** — A test that passed 10 minutes ago may not pass now after changes. Re-run.
2. **Partial verification** — Running only related tests instead of the full suite misses regressions in unrelated areas.
3. **Confusing "looks correct" with "is correct"** — Reading the code is not verification. Running it is verification.
4. **Skipping the red-green cycle** — A regression test that always passes proves nothing. Verify the test fails without the fix.

## Verification

1. **For test claims:** Full suite output visible with exit code 0 and zero failures
   ```bash
   npm test && echo "VERIFIED: All tests pass"
   ```
2. **For build claims:** Build command exit code 0 and no error output
   ```bash
   npm run build && echo "VERIFIED: Build succeeds"
   ```
3. **For bug-fix claims:** Original reproduction test passes AND full suite passes
   ```bash
   # Step 1: Verify bug reproduction test passes
   # Step 2: Verify full suite passes
   npm test && echo "VERIFIED: Bug fix confirmed"
   ```
4. **For requirement claims:** Each requirement checked against evidence with line-by-line status