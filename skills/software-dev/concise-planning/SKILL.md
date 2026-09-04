---
name: "concise-planning"
description: "Generate a clear, actionable, atomic plan for coding tasks — write to .agent-artifacts/plans/, no execution until plan is confirmed"
license: "MIT"
compatibility: "Open Agent Skills format for Codex, Claude Code, Gemini CLI, Cursor, OpenCode, GitHub Copilot, and compatible hosts. Runtime tools are listed in Prerequisites."
metadata:
  author: "Broville"
  version: "2.0.0"
  platforms: "[\"linux\",\"macos\"]"
  triggers: "[\"Asked to create a plan for a coding task\",\"Need to break down a feature or project into actionable steps\",\"Want a structured checklist before starting implementation\",\"Complex task that needs scoping before executing\"]"
  inputs: "[]"
  outputs: "[]"
  tags: "[\"planning\",\"task-breakdown\",\"project-management\"]"
  related-skills: "[\"systematic-debugging\",\"verification-before-completion\"]"
---

# Concise Planning

## Description

A simple planning methodology: turn a request into a single, actionable plan with atomic steps. Write the plan to `.agent-artifacts/plans/` in the project root. **No execution** — only planning. The plan is reviewed and confirmed before any work begins.

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
mkdir -p .agent-artifacts/plans
# Write plan to .agent-artifacts/plans/<descriptive-name>.md
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

## Verification

Confirm the plan has a bounded scope, ordered atomic actions, named validation evidence, and no unresolved question that blocks the first action. If the user requested a plan artifact, verify the file exists at the agreed location and re-read it before reporting completion.
