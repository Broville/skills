---
name: one-three-one-rule
description: Structured decision-making framework for technical proposals and trade-off analysis — one problem statement, three options with pros/cons, and one recommendation with definition of done and implementation plan.
version: 1.0.0
author: Broville
license: MIT
platforms: [linux]
trigger:
  - Asked for a "1-3-1" analysis or response
  - Said "give me options" or "what are my choices" for a technical decision
  - Facing multiple viable approaches with meaningful trade-offs
  - Need a decision proposal to share with a team or stakeholder
related_skills:
  - concise-planning
  - systematic-debugging
  - verification-before-completion
---

# 1-3-1 Rule

## Description

A methodology-only skill for structured decision-making. When a task has multiple viable approaches and the user needs a clear recommendation, this skill produces a concise 1-3-1 format: **one** clear problem statement, **three** distinct options with trade-offs, and **one** concrete recommendation with definition of done and an implementation plan. Use it for architecture decisions, tool selection, refactoring strategies, and migration paths.

Do NOT use for simple questions with one obvious answer, debugging sessions, or tasks where the user has already decided on an approach.

## Prerequisites

- Clear understanding of the decision context (project, constraints, priorities)
- Access to project documentation or codebase for informed recommendations

## Steps

### Step 1: State the Problem (One Sentence)

Write a single concise sentence describing the core decision or desired outcome.

Rules:
- Focus on the **what**, not the **how** — no implementation details, tool names, or specific technologies
- If you need "and", you're describing two problems — pick one
- Keep it tight and unambiguous

```markdown
**Problem:** [One sentence stating the core decision or desired outcome.]
```

### Step 2: Present Three Options (A, B, C)

Present exactly three distinct, viable approaches. Each gets a brief description, pros, and cons.

Rules:
- Options must represent **genuinely different strategies**, not minor variations of the same approach
- Pros and cons must be specific and honest — no straw-man options
- If only two real options exist, say so and explain why the third is not viable

```markdown
**Options:**

- **Option A: [Name]**
  - Description: [1-2 sentences]
  - Pros: [list specific advantages]
  - Cons: [list specific disadvantages]

- **Option B: [Name]**
  - Description: [1-2 sentences]
  - Pros: [list specific advantages]
  - Cons: [list specific disadvantages]

- **Option C: [Name]**
  - Description: [1-2 sentences]
  - Pros: [list specific advantages]
  - Cons: [list specific disadvantages]
```

### Step 3: Make One Recommendation

State which option you recommend and **why**, based on the user's context and priorities.

Rules:
- Be direct — this is professional judgment, not a hedge
- Explain the reasoning in terms of the user's stated priorities and constraints
- Acknowledge trade-offs you're accepting with this choice

```markdown
**Recommendation:** Option [A/B/C]. [1-3 sentences explaining why this option is best given the user's context.]
```

### Step 4: Define Done

List specific, verifiable success criteria for the recommended option. These are concrete outcomes — not vague aspirations.

```markdown
**Definition of Done:**
- [ ] [Concrete, testable criterion 1]
- [ ] [Concrete, testable criterion 2]
- [ ] [Concrete, testable criterion 3]
```

If the user picks a different option, revise this section to match.

### Step 5: Plan the Implementation

Provide concrete steps to execute the recommended option, including specific commands, tools, or actions where applicable.

```markdown
**Implementation Plan:**
1. [Specific step with commands or actions]
2. [Specific step with commands or actions]
3. [Specific step with commands or actions]
4. [Specific step with commands or actions]
5. [Verification step — tests, checks, or confirmations]
```

If the user picks a different option, revise this section to match.

### Step 6: Write the 1-3-1 Document

Save the complete 1-3-1 to a file for reference and sharing.

```bash
mkdir -p .hermes/decisions
cat > .hermes/decisions/131-$(date +%Y%m%d)-[topic].md << 'EOF'
# 1-3-1: [title]

**Problem:** [one sentence]

**Options:**
- Option A: ...
- Option B: ...
- Option C: ...

**Recommendation:** Option [X]. [reasoning]

**Definition of Done:**
- [ ] ...
- [ ] ...

**Implementation Plan:**
1. ...
2. ...
3. ...
EOF
```

## Pitfalls

1. **Describing the solution in the problem statement** — The problem should state *what* you need, not *how* to solve it. "We need to add retry logic" is a solution; "API calls fail intermittently under load" is a problem.
2. **Creating straw-man options** — All three options must be genuinely viable. If one option is obviously bad, you're not helping the user make a real decision — you're manipulating them toward your preferred choice.
3. **Hedging the recommendation** — The whole point is to make a clear call. "It depends" or "both options have merit" is not a recommendation. Pick one and justify it. If the user disagrees, they can override.
4. **Vague definition of done** — "The system works better" is not verifiable. "All external API calls retry up to 3 times on 429/502/503/504" is.

## Verification

1. **Problem is exactly one sentence** and describes what, not how
2. **Exactly three options** with pros and cons for each
3. **Single recommendation** that picks one option with clear reasoning
4. **Definition of Done** lists concrete, verifiable criteria
5. **Implementation Plan** includes specific steps, not just goals
6. **Document saved** to `.hermes/decisions/`:
   ```bash
   ls .hermes/decisions/131-*.md
   ```