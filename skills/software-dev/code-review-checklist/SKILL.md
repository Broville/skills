---
name: code-review-checklist
description: Comprehensive code review checklist covering functionality, security, performance, code quality, tests, documentation, and git hygiene
version: 1.0.0
author: Broville
license: MIT
platforms: [linux, macos]
trigger:
  - Reviewing pull requests or code changes
  - Conducting code audits
  - Establishing code review standards
  - Wanting to ensure nothing is missed in reviews
metadata:
  hermes:
    tags: [code-review, checklist, security, quality]
    related_skills: [systematic-debugging, verification-before-completion]
---

# Code Review Checklist

## Description

A systematic checklist for conducting thorough code reviews. Each category includes concrete good/bad examples.

## Pre-Review
- Read the PR description and linked issues
- Understand what problem is being solved
- Check if CI/CD tests pass
- Pull the branch and run key functionality locally

## Functionality Review
- Code solves the stated problem
- All acceptance criteria are met
- Edge cases and error cases are handled
- User input is validated
- No logical errors or bugs
- Error messages are clear and helpful (no stack traces/credentials in responses)
- Failed operations are rolled back or cleaned up

## Security Review
- All user inputs are validated
- SQL injection prevented (parameterized queries)
- XSS prevented (escape output)
- No hardcoded secrets, API keys, or tokens
- Environment variables used for secrets
- CSRF protection in place
- File uploads validated (type, size, content)
- Auth checks present where needed
- Sensitive data encrypted

## Performance Review
- No N+1 database queries
- Database access optimized (proper indexes)
- No memory leaks (listeners cleaned up, streams closed)
- Caching used appropriately
- Efficient algorithms chosen

## Code Quality Review
- Code is easy to understand
- Variable and function names are descriptive
- Complex logic has comments explaining "why"
- Functions are small and focused (single responsibility)
- DRY principle followed
- Proper separation of concerns
- No dead code or commented-out code
- No magic numbers (use named constants)

## Test Review
- New code has corresponding tests
- Tests cover edge cases
- Tests are meaningful and deterministic
- All tests pass

## Documentation Review
- Code comments explain "why", not "what"
- API documentation updated
- README updated if needed
- Breaking changes documented

## Git Review
- Commit messages are clear and descriptive
- No merge conflicts
- Branch is up to date with main
- No unnecessary files committed (build artifacts, local config)
- No secrets or credentials in the diff

## Pitfalls
1. **Missing edge cases** — Test null, empty, boundary inputs
2. **Security tunnel vision** — Use the security checklist systematically
3. **Nitpicking style over substance** — Automate formatting with linters
4. **Approving without reading** — Every review should add value
5. **Ignoring tests** — Require tests for all new functionality