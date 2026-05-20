---
name: code-review-checklist
description: Comprehensive code review checklist covering functionality, security, performance, code quality, tests, documentation, and git hygiene
version: 1.0.0
author: Broville
license: MIT
platforms: [linux]
trigger:
  - Reviewing pull requests or code changes
  - Conducting code audits
  - Establishing code review standards for a team
  - Wanting to ensure nothing is missed in reviews
related_skills:
  - systematic-debugging
  - api-security-best-practices
  - verification-before-completion
  - git-advanced-workflows
---

# Code Review Checklist

## Description

A systematic checklist for conducting thorough code reviews. Helps reviewers ensure code quality, catch bugs, identify security issues, and maintain consistency. Each category includes concrete good/bad examples.

## How to Use

1. **Understand the context** — Read the PR description, linked issues, and understand the problem being solved
2. **Check tests first** — Verify tests pass and cover new code
3. **Run the code locally** — When possible, test functionality directly
4. **Work through each checklist category** — Don't skip sections
5. **Provide specific, actionable feedback** — Include examples

## Pre-Review

- [ ] Read the PR description and linked issues
- [ ] Understand what problem is being solved
- [ ] Check if CI/CD tests pass
- [ ] Pull the branch and run key functionality locally

## Functionality Review

### Requirements

- [ ] Code solves the stated problem
- [ ] All acceptance criteria are met
- [ ] Edge cases are handled
- [ ] Error cases are handled
- [ ] User input is validated

### Logic

- [ ] No logical errors or bugs
- [ ] Conditions are correct (no off-by-one errors)
- [ ] Loops terminate correctly
- [ ] Recursion has proper base cases
- [ ] State management is correct

### Error Handling

- [ ] Errors are caught appropriately
- [ ] Error messages are clear and helpful
- [ ] Errors don't expose sensitive information (no stack traces, internal paths, or credentials in error responses)
- [ ] Failed operations are rolled back or cleaned up
- [ ] Logging is appropriate (not too verbose, not silent on failures)

**Bad — Missing validation:**
```javascript
function createUser(email, password) {
  // No validation!
  return db.users.create({ email, password });
}
```

**Good — Proper validation:**
```javascript
function createUser(email, password) {
  if (!email || !isValidEmail(email)) {
    throw new Error('Invalid email address');
  }
  if (!password || password.length < 8) {
    throw new Error('Password must be at least 8 characters');
  }
  return db.users.create({ email, password });
}
```

## Security Review

### Input Validation

- [ ] All user inputs are validated
- [ ] SQL injection is prevented (use parameterized queries)
- [ ] XSS is prevented (escape output)
- [ ] CSRF protection is in place
- [ ] File uploads are validated (type, size, content)

### Authentication and Authorization

- [ ] Authentication is required where needed
- [ ] Authorization checks are present (user can access this resource?)
- [ ] Passwords are hashed (never stored plain text)
- [ ] Sessions are managed securely
- [ ] Tokens expire appropriately

### Data Protection

- [ ] Sensitive data is encrypted
- [ ] No hardcoded secrets, API keys, or tokens
- [ ] Environment variables are used for secrets
- [ ] Personal data follows privacy regulations
- [ ] Database credentials are secure

### Dependencies

- [ ] No known vulnerable dependencies
- [ ] Dependencies are up to date
- [ ] Unnecessary dependencies are removed
- [ ] Dependency versions are pinned

**Bad — SQL injection risk:**
```javascript
const query = `SELECT * FROM users WHERE email = '${email}'`;
db.query(query);
```

**Good — Parameterized query:**
```javascript
const query = 'SELECT * FROM users WHERE email = $1';
db.query(query, [email]);
```

**Bad — Hardcoded secret:**
```javascript
const API_KEY = 'sk-abc123def456';
```

**Good — Environment variable:**
```javascript
const API_KEY = process.env.API_KEY;
if (!API_KEY) {
  throw new Error('API_KEY environment variable is required');
}
```

## Performance Review

- [ ] No unnecessary database queries (N+1 problems)
- [ ] Database access is optimized (proper indexes, query patterns)
- [ ] No memory leaks (event listeners cleaned up, streams closed)
- [ ] Caching is used appropriately
- [ ] Efficient algorithms chosen (appropriate time/space complexity)

## Code Quality Review

### Readability

- [ ] Code is easy to understand
- [ ] Variable names are descriptive
- [ ] Function names explain what they do
- [ ] Complex logic has comments explaining "why"
- [ ] Magic numbers are replaced with named constants

### Structure

- [ ] Functions are small and focused (single responsibility)
- [ ] Code follows DRY principle (Don't Repeat Yourself)
- [ ] Proper separation of concerns
- [ ] Consistent code style
- [ ] No dead code or commented-out code

**Bad — Unclear naming:**
```javascript
function calc(a, b, c) {
  return a * b + c;
}
```

**Good — Descriptive naming:**
```javascript
function calculateTotalPrice(quantity, unitPrice, tax) {
  return quantity * unitPrice + tax;
}
```

**Bad — Function doing too much:**
```javascript
function processOrder(order) {
  // Validate, calculate, charge, email, update inventory — all in one
}
```

**Good — Separated concerns:**
```javascript
function processOrder(order) {
  validateOrder(order);
  const total = calculateOrderTotal(order);
  const payment = processPayment(total);
  sendOrderConfirmation(order.email);
  updateInventory(order.items);
  return { orderId: order.id, total };
}
```

## Test Review

- [ ] New code has corresponding tests
- [ ] Tests cover edge cases
- [ ] Tests are meaningful (not just asserting true === true)
- [ ] All tests pass
- [ ] Test coverage is adequate
- [ ] Tests are deterministic (not flaky)

## Documentation Review

- [ ] Code comments explain "why", not "what"
- [ ] API documentation is updated
- [ ] README is updated if needed
- [ ] Breaking changes are documented
- [ ] Migration guide provided if needed

## Git Review

- [ ] Commit messages are clear and descriptive
- [ ] No merge conflicts
- [ ] Branch is up to date with main
- [ ] No unnecessary files committed (build artifacts, local config)
- [ ] .gitignore is properly configured
- [ ] No secrets or credentials in the diff

## Review Comment Templates

### Requesting Changes

```markdown
**Issue:** [Describe the problem]

**Current code:**
[Show problematic code]

**Suggested fix:**
[Show improved code]

**Why:** [Explain why this is better]
```

### Asking Questions

```markdown
**Question:** [Your question]
**Context:** [Why you're asking]
**Suggestion:** [If you have one]
```

## Pitfalls

1. **Missing edge cases** — Code works for the happy path but fails on null, empty, or boundary inputs. Ask "What if...?" questions for every path.
2. **Security tunnel vision** — Focusing only on logic bugs and missing injection risks, auth bypasses, or data leaks. Use the security checklist systematically.
3. **Nitpicking style over substance** — Style preferences (formatting, naming conventions) should be automated by linters. Focus review effort on correctness, security, and architecture.
4. **Approving without reading** — Skimming code and approving. Every review should add value or confirm correctness.
5. **Ignoring tests** — Untested code will cause problems. Require tests for all new functionality.

## Verification

1. **All checklist categories covered** — Functionality, security, performance, code quality, tests, docs, git
2. **No unresolved security concerns** — Input validation, auth, data protection, dependencies checked
3. **Tests are adequate** — New code tested, edge cases covered, tests pass
   ```bash
   # Verify tests pass
   npm test && echo "All tests pass"
   # Check coverage
   npm run test:coverage
   ```
4. **CI pipeline green** — All checks pass on the PR
   ```bash
   gh pr checks <PR_NUMBER>
   ```