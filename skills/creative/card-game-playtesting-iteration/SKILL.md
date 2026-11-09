---
name: "card-game-playtesting-iteration"
description: "Plan ethical, structured card-game playtests and turn observations into prioritized rule changes without confusing player preference with design evidence. Use when testing, diagnosing, or iterating a card-game prototype."
license: "MIT"
compatibility: "Open Agent Skills format for Codex, Claude Code, Gemini CLI, OpenCode, GitHub Copilot, and compatible hosts. No runtime dependency is required; use consent-aware notes and reproducible test records."
metadata:
  author: "Broville contributors"
  version: "1.0.0"
  platforms: "[\"linux\",\"macos\",\"windows\"]"
  triggers: "[\"A card-game prototype needs playtesting\",\"Players are confused or disengaged and the cause is unclear\",\"A rules or balance change needs iterative validation\"]"
  inputs: "[{\"name\":\"prototype\",\"description\":\"Playable rules version, components, setup, and known hypotheses\",\"required\":true},{\"name\":\"test_context\",\"description\":\"Player profile, session limits, accessibility needs, and questions to answer\",\"required\":true}]"
  outputs: "[{\"name\":\"playtest_plan\",\"description\":\"Session protocol, measures, consent/accessibility notes, and observation prompts\"},{\"name\":\"iteration_log\",\"description\":\"Evidence-linked findings, prioritized changes, and next-test criteria\"}]"
  tags: "[\"card-games\",\"playtesting\",\"iteration\",\"research\",\"accessibility\"]"
  related-skills: "[\"card-game-concept-loop\",\"card-game-rules-engineering\",\"card-game-balance-simulation\"]"
  display-name: "Card Game Playtesting"
  source: "Broville original; informed by Game Studies consumer playtest research and W3C WCAG 2.2"
  source-url: "https://www.gamestudies.org/0501/davis_steury_pagulayan/"
---

# Card-Game Playtesting and Iteration

## Description

Test whether the rules produce the intended decisions and experience. Use a staged protocol: self-test, guided test, blind rules test, and comparative iteration. Record observable behavior and player interpretation separately from preferences. Simulated agents can expose quantitative risks, but they are not real players and cannot replace human play.

## Prerequisites

- A versioned playable prototype and rules sheet.
- One to three hypotheses with observable measures.
- A consent-aware plan for recruiting, recording, compensation, privacy, and accessibility accommodations.

## Steps

1. Write a test card for each hypothesis: question, predicted signal, counter-signal, minimum evidence, and the rule change that would follow.
2. Run a self-test for setup time, missing information, impossible states, loops, component errors, and rules contradictions. Fix obvious defects before involving participants.
3. Run guided sessions with a neutral facilitator. Explain only the approved rules, note every question and workaround, and do not rescue a player by silently changing the rules.
4. Run blind-rule sessions: provide the rules, then observe whether participants can set up, identify legal choices, resolve effects, and explain the goal. Distinguish bad writing from bad mechanism.
5. Collect mixed evidence: time to first meaningful choice, repeated questions, illegal actions, skipped options, game length, score trajectory, perceived agency, tension, accessibility barriers, and post-session explanation of the loop.
6. Ask open questions before leading ones: “What were you trying to do?” and “What did you think would happen?” Avoid asking whether a player “liked” a feature until after behavior and interpretation are recorded.
7. Segment findings by player familiarity, role, accessibility need, and test condition. Protect personal data; keep notes necessary for the design decision and remove identifying details.
8. Classify findings as rules comprehension, usability/accessibility, balance, pacing, agency, theme, or preference. Prioritize issues that block understanding or invalidate the core loop.
9. Change one major variable at a time when diagnosing cause. Keep a versioned iteration log with hypothesis, change, evidence, result, and next criterion. Re-test regressions and edge cases.
10. Compare human findings with `card-game-balance-simulation`, then revise through `card-game-rules-engineering`. Stop iterating when the acceptance criteria hold across varied players, not when the designer is merely tired of testing.

## Pitfalls

- **Leading participants:** Defending the design contaminates evidence.
- **Friend-only validation:** Familiar players compensate for unclear rules and may share the designer's assumptions.
- **Preference conflation:** “I dislike take-that” is not the same as “the rule is confusing.”
- **Fixing in session:** Ad hoc patches prevent comparison between versions.
- **Overfitting to one player:** Preserve dissent and test across relevant audiences.
- **Ignoring accessibility:** A game that works only with color, tiny print, audio, rapid timing, or fine motor control has an incomplete design.
- **Unsafe research:** Obtain consent, minimize data, and make participation voluntary and interruptible.

## Verification

1. Each hypothesis has a recorded measure and a predeclared interpretation rule.
2. At least one blind-rule session tests comprehension independently of the designer's explanation.
3. Findings distinguish observed behavior, stated interpretation, preference, and facilitator inference.
4. Every accepted change has a version, rationale, evidence, and regression check.
5. The final report includes accessibility barriers, participant limitations, and unresolved uncertainty.

## Cross-References

- `card-game-concept-loop` — hypotheses must test the intended player promise.
- `card-game-rules-engineering` — convert observed ambiguity into precise rules changes.
- `card-game-balance-simulation` — compare human evidence with reproducible quantitative diagnostics.
- Game Studies, [A survey method for assessing perceptions of a game](https://www.gamestudies.org/0501/davis_steury_pagulayan/) — consumer playtesting and perception measurement.
- W3C, [WCAG 2.2](https://www.w3.org/TR/wcag/) — accessibility principles and testable criteria for digital or hybrid game surfaces; not a complete tabletop standard.
