---
name: "card-game-rules-engineering"
description: "Turn a card-game concept into complete, deterministic, readable rules with explicit state, timing, edge cases, and accessibility safeguards. Use when drafting, auditing, or revising card-game rules."
license: "MIT"
compatibility: "Open Agent Skills format for Codex, Claude Code, Gemini CLI, Cursor, OpenCode, GitHub Copilot, and compatible hosts. No runtime dependency is required."
metadata:
  author: "Broville contributors"
  version: "1.0.0"
  platforms: "[\"linux\",\"macos\",\"windows\"]"
  triggers: "[\"A card game needs a formal rules document\",\"Rules contain timing or interaction ambiguity\",\"A prototype needs edge-case and state auditing\"]"
  inputs: "[{\"name\":\"concept_brief\",\"description\":\"The intended player promise, loop, components, and hypotheses\",\"required\":true},{\"name\":\"card_catalog\",\"description\":\"Card names, quantities, effects, symbols, and intended roles\",\"required\":false}]"
  outputs: "[{\"name\":\"rules_specification\",\"description\":\"Setup, turn structure, timing, resolution, scoring, end state, and glossary\"},{\"name\":\"edge_case_register\",\"description\":\"Ambiguities, invariants, and resolved corner cases\"}]"
  tags: "[\"card-games\",\"rules\",\"specification\",\"timing\",\"accessibility\"]"
  related-skills: "[\"card-game-concept-loop\",\"card-game-balance-simulation\",\"card-game-playtesting-iteration\"]"
  source: "Broville original; accessibility baseline from W3C WCAG 2.2"
  source-url: "https://www.w3.org/WAI/WCAG22/Understanding/intro"
---

# Card-Game Rules Engineering

## Description

Produce rules that two independent readers can apply to the same game state and reach the same result. Treat the game as a state machine: name state, legal actions, timing windows, resolution order, invariants, and terminal conditions. The rules should be concise for players while retaining an audit trail for designers.

## Prerequisites

- A concept brief and intended player experience.
- A component/card inventory or explicit placeholders.
- A chosen terminology policy: one term per concept, with a glossary for exceptions.

## Steps

1. Define the state vector: player zones, hands, decks, discard/exile areas, resources, scores, statuses, turn number, active player, pending effects, and hidden information.
2. Define setup as an ordered procedure. Specify shuffle boundaries, starting hands, first-player selection, mulligans, replacement draws, and what remains public.
3. Define the turn skeleton with numbered phases and priority windows. For every window, state who may act, what ends the window, whether responses can nest, and how simultaneous effects are ordered.
4. Define card effect grammar: cost, target, condition, effect, duration, destination, and replacement behavior. Distinguish “may,” “must,” “up to,” “exactly,” and “then.”
5. Specify illegal actions and failure behavior. A failed optional effect should not silently become a different effect; state whether costs are paid before validation and whether partial resolution is allowed.
6. Establish invariants and conservation rules, such as no card existing in two zones, resources not becoming negative, finite deck counts, and a bounded path to game end. If an effect intentionally breaks an invariant, state the exception explicitly.
7. Resolve simultaneity with a deterministic policy: active-player order, timestamp, stack, simultaneous reveal, or designer-defined priority. Include a worked example for the hardest interaction.
8. Define scoring, tie-breaks, concession, stalemate, missed triggers, and incomplete information. Ensure the win condition cannot depend on hidden adjudication.
9. Add an accessibility pass: every important state has a text, shape, icon, position, or tactile alternative; do not make color the only signal; avoid unnecessary real-time requirements; keep terms and layout predictable. W3C's perceivable, operable, understandable, and robust principles are a useful reference for digital/hybrid surfaces.
10. Produce two layers: a player-facing rules document and a designer-facing edge-case register. Send unresolved balance questions to `card-game-balance-simulation` and observed confusion to `card-game-playtesting-iteration`.

## Pitfalls

- **Hidden timing:** “When” and “after” windows are not interchangeable.
- **Undefined ownership:** State who controls an effect and who chooses targets.
- **Partial resolution ambiguity:** Specify what happens when one target becomes invalid.
- **Infinite loops:** Require a progress measure or declare a loop-break rule.
- **Keyword overload:** Reuse a keyword only when its timing and scope are stable.
- **Color-only information:** Pair colors with labels, symbols, patterns, or text.
- **Rules patchwork:** Edit the canonical rule and its examples together; stale examples are contradictory rules.

## Verification

1. Two independent adjudications of each worked example produce identical results.
2. Every action has a legal timing window, cost, target rule, and resolution outcome.
3. Zone conservation, resource bounds, and termination assumptions are documented.
4. Setup, first turn, scoring, tie, concession, and stalemate are unambiguous.
5. A player can access core information without relying on color, sound, or fine motor speed alone.

## Cross-References

- `card-game-concept-loop` — source of player promise and loop constraints.
- `card-game-balance-simulation` — test the quantitative consequences of formal rules.
- `card-game-playtesting-iteration` — observe whether people interpret and apply the rules as intended.
- W3C, [WCAG 2.2](https://www.w3.org/TR/wcag/) and [Understanding the Four Principles](https://www.w3.org/WAI/WCAG22/Understanding/intro) — accessibility reference; tabletop games may require additional accommodations.
