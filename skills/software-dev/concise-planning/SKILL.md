---
name: concise-planning
description: Generate a clear, actionable, atomic plan for coding tasks — write to .hermes/plans/, no execution until plan is confirmed
version: 1.0.0
author: Broville
license: MIT
platforms: [linux]
trigger:
  - Asked to create a plan for a coding task
  - Need to break down a feature or project into actionable steps
  - Want a structured checklist before starting implementation
  - Complex task that needs scoping before executing
related_skills:
  - systematic-debugging
  - verification-before-completion
  - deployment-procedures
---

# Concise Planning

## Description

A simple planning methodology: turn a request into a single, actionable plan with atomic steps. Write the plan to `.hermes/plans/` in the project root. **No execution** — only planning. The plan is reviewed and confirmed before any work begins.

## Steps

### Step 1: Scan Context

- Read `README.md`, docs, and relevant code files in the project
- Identify constraints: language, frameworks, test setup, deployment target
- Understand the current project structure

```bash
# Scan project structure
ls -la
cat README.md 2>/dev/null || echo "No README found"
find . -name "package.json" -o -name "requirements.txt" -o -name "Cargo.toml" -o -name "go.mod" | head -5
```

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

The plan stays in `.hermes/plans/` for reference. It is not committed unless the project chooses to track it.

## Checklist Guidelines

- **Atomic**: Each step should be a single logical unit of work. If a step has "and" in it, split it.
- **Verb-first**: "Add...", "Refactor...", "Verify...", "Create...", "Remove..."
- **Concrete**: Name specific files or modules when possible. Avoid vague steps like "improve code".
- **Ordered**: Steps must be done in sequence — later steps depend on earlier ones.
- **Validatable**: At least one step must verify the result (test, build, lint, etc.)

## Pitfalls

1. **Planning too broadly** — Each plan should cover one coherent task. If the scope grows, split into multiple plans.
2. **Vague action items** — Steps like "improve performance" are not actionable. Specify: "Add index on orders.user_id column" or "Cache user profile lookups in Redis."
3. **Skipping the validation step** — Every plan must include at least one verification action. Without it, you can't confirm success.
4. **Executing during planning** — The planning phase is read-only. No code changes until the plan is confirmed.

## Verification

1. **Plan file exists:**
   ```bash
   ls .hermes/plans/*.md
   ```
2. **Plan contains required sections:** Approach, Scope (In/Out), Action Items, Open Questions
3. **Action items are atomic and verb-first:** Each step is a single action with a clear verb
4. **Scope is bounded:** Clear "In" and "Out" lists preventing scope creep