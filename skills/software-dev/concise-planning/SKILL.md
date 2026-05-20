---
name: concise-planning
description: Generate a clear, actionable, atomic plan for coding tasks — write to .hermes/plans/, no execution until plan is confirmed
version: 1.0.0
author: Broville
license: MIT
platforms: [linux, macos]
trigger:
  - Asked to create a plan for a coding task
  - Need to break down a feature or project into actionable steps
  - Want a structured checklist before starting implementation
  - Complex task that needs scoping before executing
metadata:
  hermes:
    tags: [planning, task-breakdown, project-management]
    related_skills: [systematic-debugging, verification-before-completion]
---

# Concise Planning

## Description

A simple planning methodology: turn a request into a single, actionable plan with atomic steps. Write the plan to `.hermes/plans/` in the project root. **No execution** — only planning. The plan is reviewed and confirmed before any work begins.

## Steps

### Step 1: Scan Context
- Read `README.md`, docs, and relevant code files
- Identify constraints: language, frameworks, test setup, deployment target

### Step 2: Minimal Interaction
- Ask **at most 1–2 questions** and only if truly blocking
- Make reasonable assumptions for non-blocking unknowns
- Document assumptions in the plan

### Step 3: Generate Plan

Create a structured plan with this format:

```markdown
# Plan: <title>

<1-3 sentence approach: what and why>

## Scope

- In: <what this plan covers>
- Out: <what this plan does NOT cover>

## Action Items

1. [ ] <Discovery step — understand existing code>
2. [ ] <Implementation step — specific file/module>
3. [ ] <Implementation step — specific file/module>
4. [ ] <Implementation step — specific file/module>
5. [ ] <Validation — test/verify the changes>
6. [ ] <Commit/publish step>

## Open Questions

- <Question 1 (max 3)>
```

### Step 4: Write Plan to File

```bash
mkdir -p .hermes/plans
# Write plan to .hermes/plans/<descriptive-name>.md
```

## Checklist Guidelines

- **Atomic**: Each step should be a single logical unit. If a step has "and" in it, split it.
- **Verb-first**: "Add...", "Refactor...", "Verify...", "Create...", "Remove..."
- **Concrete**: Name specific files or modules. Avoid "improve code".
- **Ordered**: Later steps depend on earlier ones.
- **Validatable**: At least one step must verify the result.

## Pitfalls

1. **Planning too broadly** — Each plan covers one coherent task
2. **Vague action items** — "Improve performance" is not actionable
3. **Skipping validation** — Every plan must include at least one verification action
4. **Executing during planning** — Planning phase is read-only