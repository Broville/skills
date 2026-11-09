---
name: "card-game-concept-loop"
description: "Invent an original card game around a focused player promise, repeatable core loop, and testable constraints. Use when a user wants a new card-game concept, pitch, prototype brief, or design space exploration."
license: "MIT"
compatibility: "Open Agent Skills format for Codex, Claude Code, Gemini CLI, Cursor, OpenCode, GitHub Copilot, and compatible hosts. No runtime dependency is required."
metadata:
  author: "Broville contributors"
  version: "1.0.0"
  platforms: "[\"linux\",\"macos\",\"windows\"]"
  triggers: "[\"User asks to invent an original card game\",\"A card-game prototype needs a focused core loop\",\"A design brief needs several differentiated card-game concepts\"]"
  inputs: "[{\"name\":\"design_brief\",\"description\":\"Audience, player count, session length, setting constraints, and desired feeling\",\"required\":true},{\"name\":\"constraints\",\"description\":\"Deck, component, platform, accessibility, legal, or production limits\",\"required\":false}]"
  outputs: "[{\"name\":\"concept_brief\",\"description\":\"Original premise, player promise, core loop, win condition, and prototype boundary\"},{\"name\":\"design_hypotheses\",\"description\":\"Explicit assumptions that can be tested in rules and playtests\"}]"
  tags: "[\"card-games\",\"game-design\",\"ideation\",\"core-loop\",\"originality\"]"
  related-skills: "[\"card-game-rules-engineering\",\"card-game-balance-simulation\",\"card-game-playtesting-iteration\"]"
  source: "Broville original; informed by W3C WCAG 2.2 and MIT Journal of Design and Science"
  source-url: "https://www.w3.org/TR/wcag/"
---

# Card-Game Concept and Core Loop

## Description

Turn a brief into one or more original, buildable card-game concepts. Optimize for a clear player promise and a small loop that can be explained, prototyped, and measured. Do not imitate a named game's setting, terminology, signature mechanics, artwork, faction identities, or distinctive presentation; abstract design goals into generic constraints and recombine them into a new design.

## Prerequisites

- A design brief with intended audience and play context.
- Stated player count, target session length, and physical or digital component limits when known.
- A way to record assumptions and unresolved questions.

## Steps

1. Extract constraints into a table: players, session length, complexity, interaction level, randomness tolerance, component budget, accessibility needs, and content boundaries.
2. Write the player promise in one sentence: “Players feel/do X by making Y under pressure Z.” Reject promises that describe only theme or aesthetics.
3. Select one primary tension and at most two supporting tensions, such as commitment versus flexibility, information versus tempo, or cooperation versus private incentives.
4. Draft the loop as observable actions:
   1. Acquire or reveal information.
   2. Choose a constrained action.
   3. Resolve a meaningful consequence.
   4. Update public and private state.
   5. Create a new decision with changed incentives.
5. Define the smallest prototype: card types, setup, turn order, player choices, resolution, scoring, end condition, and one example turn. Remove lore and effects that do not serve the loop.
6. State the source of agency and the source of uncertainty separately. A player must be able to improve outcomes through decisions; randomness must create variation, not hide an unearned result.
7. Define three falsifiable hypotheses, for example: “Players can identify a worthwhile risk within 30 seconds,” “No player is eliminated before the final third,” or “The public information creates at least two plausible lines.”
8. Run an originality and accessibility pass: use new names and combinations, avoid confusingly similar trade dress or protected assets, provide non-color identifiers, readable text, and alternatives for sensory-only cues. W3C's principles are a useful baseline, not a complete tabletop accessibility review.
9. Hand the brief to `card-game-rules-engineering` before adding content volume, and to `card-game-playtesting-iteration` once a playable loop exists.

## Pitfalls

- **Theme-first drift:** A setting cannot substitute for a decision loop.
- **Mechanic soup:** More mechanisms do not create depth; each one must change a decision or consequence.
- **Reference cloning:** Borrow high-level goals, not recognizable names, art, factions, layouts, or signature sequences.
- **Unbounded scope:** Prototype the loop with plain cards before adding asymmetric decks or campaign content.
- **Fake agency:** If the best action is obvious or outcomes ignore choices, revise the information and consequence structure.
- **Accessibility as polish:** Do not make color, tiny text, audio, or rapid timing the sole channel for core information.

## Verification

1. A stranger can state the player promise, turn loop, win condition, and prototype boundary without author assistance.
2. Every proposed component or rule is mapped to a decision, tension, or readable state change.
3. At least three hypotheses have observable pass/fail measures.
4. The concept names what it intentionally does not copy and includes non-color communication for important information.
5. The concept is ready to express as a finite rules document with no unresolved contradictions.

## Cross-References

- `card-game-rules-engineering` — convert the concept into precise, executable rules.
- `card-game-balance-simulation` — estimate probability, swing, and strategy before expensive production.
- `card-game-playtesting-iteration` — test whether the intended experience appears in real play.
- W3C, [Web Content Accessibility Guidelines 2.2](https://www.w3.org/TR/wcag/) — accessibility principles and testable criteria used here as a baseline for digital or hybrid interfaces.
- MIT Journal of Design and Science, [Gaming the System](https://jods.mitpress.mit.edu/pub/014suqrf/download/pdf) — rules as the designed system of play; use as conceptual background, not a template.
