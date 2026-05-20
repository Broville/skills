---
name: adversarial-ux-test
description: Roleplay the worst-case user for your product — browse the app as a hostile persona, find every UX pain point, then filter through a pragmatism layer to separate real problems from noise. Creates actionable tickets from genuine issues only.
version: 1.0.0
author: Broville
license: MIT
platforms: [linux]
trigger:
  - Asked to run a UX review or adversarial test on an app
  - Want to dogfood a product by simulating a hostile user persona
  - Need to identify UX friction points before a launch or demo
  - Request to find usability problems in a deployed or staging application
related_skills:
  - systematic-debugging
  - concise-planning
  - verification-before-completion
---

# Adversarial UX Test

## Description

A methodology-only skill for adversarial user-experience testing. Roleplay the worst-case user for your product — someone who hates technology, doesn't want your software, and finds every reason to complain. Then filter their feedback through a pragmatism layer to separate real UX problems from "I hate computers" noise. Think of it as an automated "mom test" — but angry.

Most QA finds bugs. This skill finds **friction**. A technically correct app can still be unusable. The adversarial persona catches confusing terminology, too many steps, missing onboarding, accessibility issues, cold-start problems, and conversion-killing friction. The pragmatism filter ensures you only file tickets for genuine issues, not persona noise.

## Prerequisites

- A deployed or staging URL for the application under test
- Browser tool access for navigating the app
- Project context (README, docs) for understanding the app's purpose

## Steps

### Step 1: Define the Persona

If no persona is provided, generate one by answering these questions:

1. **Who is the HARDEST user for this product?** (age 50+, non-technical role, decades of experience doing it "the old way")
2. **What is their tech comfort level?** (WhatsApp-only, paper notebooks, spouse set up their email)
3. **What is the ONE thing they need to accomplish?** (their core job, not your feature list)
4. **What would make them give up?** (too many clicks, jargon, slow, confusing)
5. **How do they talk when frustrated?** (blunt, sweary, dismissive, sighing)

Write a specific persona (name, age, role, constraints, voice). The persona must be specific enough to stay in character for 20 minutes of testing.

```bash
# Create persona document
mkdir -p .hermes/ux-reviews
cat > .hermes/ux-reviews/persona.md << 'EOF'
# Persona: [Name]

- Age: [age]
- Role: [role/occupation]
- Tech comfort: [level]
- Core task: [one thing they came to do]
- Dealbreakers: [what makes them quit]
- Voice: [how they speak when frustrated]
EOF
```

### Step 2: Browse as the Persona

Fully inhabit the persona and attempt their **actual tasks** on the app:

1. Navigate to the app URL
2. Attempt the persona's core task (not a feature tour)
3. Test these friction categories:
   - **First impression** — would they bother past the landing page?
   - **Core workflow** — the ONE thing they need to do most often
   - **Error recovery** — what happens when they do something wrong?
   - **Readability** — text size, contrast, information density
   - **Speed** — does it feel faster than their current method?
   - **Terminology** — any jargon they wouldn't understand?
   - **Navigation** — can they find their way back?
4. Take screenshots of every pain point
5. Check browser console for JS errors on every page
6. Count clicks to accomplish the persona's ONE task (5+ is a RED finding)

```bash
# Take screenshots of pain points during testing
# (use browser screenshot tool or native screenshot commands)
mkdir -p .hermes/ux-reviews/screenshots

# Check for console errors on each page
# (use browser console tool to capture JS errors)
```

### Step 3: Write the Rant in Character

Write feedback AS THE PERSONA — in their voice, with their frustrations. This is not a bug report. This is a real human venting.

```markdown
[PERSONA NAME]'s Review of [PRODUCT]

Overall: [Would they keep using it? Yes/No/Maybe with conditions]

THE GOOD (grudging admission):
- [things even they have to admit work]

THE BAD (legitimate UX issues):
- [real problems that would stop them from using the product]

THE UGLY (showstoppers):
- [things that would make them uninstall/cancel immediately]

SPECIFIC COMPLAINTS:
1. [Page/feature]: "[quote in persona voice]" — [what happened, expected]
2. ...

VERDICT: "[one-line persona quote summarizing their experience]"
```

Save the rant to `.hermes/ux-reviews/rant.md`.

### Step 4: Apply the Pragmatism Filter

Step OUT of character. Evaluate each complaint as a product person:

- **RED: REAL UX BUG** — Any user would have this problem, not just grumpy ones. Fix it.
- **YELLOW: VALID BUT LOW PRIORITY** — Real issue but only for extreme users. Note it.
- **WHITE: PERSONA NOISE** — "I hate computers" talking, not a product problem. Skip it.
- **GREEN: FEATURE REQUEST** — Good idea hidden in the complaint. Consider it.

Filter criteria:
1. Would a 35-year-old competent-but-busy user have the same complaint? → RED
2. Is this a genuine accessibility issue (font size, contrast, click targets)? → RED
3. Is this "I want it to work like paper" resistance to digital? → WHITE
4. Is this a real workflow inefficiency the persona stumbled on? → YELLOW or RED
5. Would fixing this add complexity for the 80% who are fine? → WHITE
6. Does the complaint reveal a missing onboarding moment? → GREEN

**This filter is MANDATORY.** Never ship raw persona complaints as tickets.

Save the filtered assessment to `.hermes/ux-reviews/assessment.md`.

### Step 5: Create Actionable Tickets

For **RED** and **GREEN** items only:
- Clear, actionable title
- Include the persona's verbatim quote (entertaining + memorable)
- The real UX issue underneath (objective)
- A suggested fix (actionable)
- Tag: `ux-review`

For **YELLOW** items: one catch-all ticket with all notes.

**WHITE** items appear in the report only. No tickets.

**Max 10 tickets per session** — focus on the worst issues.

```bash
# Write tickets file
cat > .hermes/ux-reviews/tickets.md << 'EOF'
# UX Review Tickets

## RED: [title]
- Quote: "[persona quote]"
- Issue: [objective description]
- Fix: [suggested action]
- Tag: ux-review

## GREEN: [title]
...

## YELLOW: [catch-all]
...
EOF
```

### Step 6: Compile the Report

Deliver a complete report combining all artifacts:

1. The persona rant (Step 3) — entertaining and visceral
2. The filtered assessment (Step 4) — pragmatic and actionable
3. Tickets created (Step 5) — with specific recommendations
4. Screenshots of key issues

```bash
cat > .hermes/ux-reviews/report.md << 'EOF'
# Adversarial UX Test Report

## Persona
[paste persona.md]

## Rant (in character)
[paste rant.md]

## Pragmatism Filter
[paste assessment.md]

## Tickets
[paste tickets.md]

## Screenshots
- [list of screenshot files with descriptions]
EOF
```

## Pitfalls

1. **Skipping the pragmatism filter** — Raw persona complaints are entertaining but not actionable. The filter is what makes this skill useful instead of just cathartic. Without it, you'd file tickets for "print this page" buttons everywhere.
2. **Using a too-tech-savvy persona** — If the persona has zero complaints, they're too comfortable. Make them older, less patient, more set in their ways. The best findings come from genuine friction unexpected by developers.
3. **Testing with a pre-seeded admin account** — The cold-start experience (empty states, no demo content) is where most friction lives. Always register as a NEW user when possible.
4. **Feature touring instead of task testing** — Don't browse features. The persona has ONE job. Can they do it? Everything else is secondary.
5. **Mixing perspectives during Steps 2-3** — Stay in character during the browsing and rant phases. Break character only at Step 4. Mixing perspectives produces muddled findings.

## Verification

1. **Report file exists:**
   ```bash
   ls -la .hermes/ux-reviews/report.md
   ```
2. **Report contains all required sections:** Persona, Rant, Assessment, Tickets, Screenshots
3. **Pragmatism filter was applied:** Every complaint is classified as RED/YELLOW/WHITE/GREEN
4. **At most 10 tickets** — more indicates insufficient filtering
5. **Each RED ticket has:** a verbatim quote, objective issue, suggested fix, and `ux-review` tag