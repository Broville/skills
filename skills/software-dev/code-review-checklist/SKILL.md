---
name: code-review-checklist
description: Multi-axis code review checklist with severity classification for functionality, security, quality, and tests
version: 1.1.0
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
    aliases: [code-review-and-quality]
---

# Code Review Checklist

> This skill absorbs and supersedes the external skill `code-review-and-quality` from addyosmani/agent-skills (license: MIT). See the history in this repo's PR for the merge commit.

## Description

A systematic, multi-axis checklist for conducting thorough code reviews. Each finding is classified by severity so reviewers can distinguish blockers from nits.

## Steps

1. **Read the PR context.** Read the PR description, linked issues, and acceptance criteria before looking at code.
2. **Check CI status.** Verify that the branch's automated tests, linting, and builds pass before spending time on manual review.
3. **Pull the branch locally.** Run the key functionality or test paths that the change touches.
4. **Review each axis.** Walk through the Review Axes below in order: Functionality, Security, Performance, Quality, Tests, Documentation, Git Hygiene.
5. **Classify every finding.** Label each issue as Blocker, Major, Minor, or Nit using the Severity Classification definitions.
6. **Resolve blockers first.** Ensure all Blocker items are fixed or explicitly accepted before approving the PR.
7. **Approve or request changes.** Leave meaningful review comments; do not approve without reading the diff.

## Review Axes

### Functionality
| Severity | Check |
|----------|-------|
| Blocker | Code solves the stated problem |
| Blocker | All acceptance criteria are met |
| Major | Edge cases and error cases are handled |
| Major | User input is validated |
| Major | No logical errors or bugs |
| Major | Error messages are clear and helpful (no stack traces/credentials in responses) |
| Major | Failed operations are rolled back or cleaned up |

### Security
| Severity | Check |
|----------|-------|
| Blocker | All user inputs are validated |
| Blocker | SQL injection prevented (parameterized queries) |
| Blocker | XSS prevented (escape output) |
| Blocker | No hardcoded secrets, API keys, or tokens |
| Blocker | Auth checks present where needed |
| Major | Environment variables used for secrets |
| Major | CSRF protection in place |
| Major | File uploads validated (type, size, content) |
| Major | Sensitive data encrypted |

### Performance
| Severity | Check |
|----------|-------|
| Major | No N+1 database queries |
| Major | Database access optimized (proper indexes) |
| Major | No memory leaks (listeners cleaned up, streams closed) |
| Minor | Caching used appropriately |
| Minor | Efficient algorithms chosen |

### Quality
| Severity | Check |
|----------|-------|
| Major | Code is easy to understand |
| Minor | Variable and function names are descriptive |
| Minor | Complex logic has comments explaining "why" |
| Major | Functions are small and focused (single responsibility) |
| Major | DRY principle followed |
| Major | Proper separation of concerns |
| Minor | No dead code or commented-out code |
| Minor | No magic numbers (use named constants) |

### Tests
| Severity | Check |
|----------|-------|
| Blocker | New code has corresponding tests |
| Major | Tests cover edge cases |
| Major | Tests are meaningful and deterministic |
| Blocker | All tests pass |

### Documentation
| Severity | Check |
|----------|-------|
| Minor | Code comments explain "why", not "what" |
| Major | API documentation updated |
| Major | README updated if needed |
| Major | Breaking changes documented |

### Git Hygiene
| Severity | Check |
|----------|-------|
| Minor | Commit messages are clear and descriptive |
| Blocker | No merge conflicts |
| Major | Branch is up to date with main |
| Minor | No unnecessary files committed (build artifacts, local config) |
| Blocker | No secrets or credentials in the diff |

## Severity Classification

- **Blocker** — Must be fixed before merge. Risks correctness, security, or deployability.
- **Major** — Should be fixed before merge unless there is an explicit, justified exception.
- **Minor** — Should be addressed pre-merge if trivial; can be deferred with a tracked follow-up.
- **Nit** — Preference or style suggestion; optional, often automate-able with linters.

## Pitfalls
1. **Missing edge cases** — Test null, empty, boundary inputs
2. **Security tunnel vision** — Use the security checklist systematically
3. **Nitpicking style over substance** — Automate formatting with linters
4. **Approving without reading** — Every review should add value
5. **Ignoring tests** — Require tests for all new functionality
6. **Severity inflation** — Treating every suggestion as a blocker slows teams down; reserve Blocker for real correctness/security risks

## Verification
- Every changed file has at least one reviewer comment or approval
- All Blocker items are resolved before merge
- CI passes and the test suite is green

## Cross-References
- Related skills: [`systematic-debugging`](../systematic-debugging/) and [`verification-before-completion`](../verification-before-completion/)
- External predecessor: `code-review-and-quality` from addyosmani/agent-skills (MIT), now aliased by this skill
