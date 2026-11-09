---
name: "card-game-balance-simulation"
description: "Analyze card-game probability, economy, variance, and strategic balance with exact calculations and reproducible simulations. Use when tuning decks, effects, resources, odds, or matchup health."
license: "MIT"
compatibility: "Open Agent Skills format for Codex, Claude Code, Gemini CLI, OpenCode, GitHub Copilot, and compatible hosts. Use a calculator, spreadsheet, or local programming language when available; no bundled dependency is required."
metadata:
  author: "Broville contributors"
  version: "1.0.0"
  platforms: "[\"linux\",\"macos\",\"windows\"]"
  triggers: "[\"A card game needs probability or expected-value analysis\",\"Decks, cards, resources, or matchups need balance tuning\",\"A designer wants seeded simulations or sensitivity analysis\"]"
  inputs: "[{\"name\":\"rules_specification\",\"description\":\"Formal rules, card catalog, deck lists, and legal action boundaries\",\"required\":true},{\"name\":\"balance_questions\",\"description\":\"Specific risks such as runaway leaders, non-games, dead cards, or matchup skew\",\"required\":true}]"
  outputs: "[{\"name\":\"balance_report\",\"description\":\"Exact calculations, simulation methodology, metrics, and findings\"},{\"name\":\"tuning_recommendations\",\"description\":\"Smallest rule or parameter changes with predicted trade-offs\"}]"
  tags: "[\"card-games\",\"probability\",\"simulation\",\"balance\",\"statistics\"]"
  related-skills: "[\"card-game-concept-loop\",\"card-game-rules-engineering\",\"card-game-playtesting-iteration\"]"
  source: "Broville original; iterative playtest framing informed by Game Studies"
  source-url: "https://www.gamestudies.org/0501/davis_steury_pagulayan/"
---

# Card-Game Balance and Seeded Simulation

## Description

Use exact math where the state space is tractable and reproducible seeded simulation where it is not. Measure decisions and player outcomes separately: a balanced win rate can still conceal dominant lines, non-games, runaway leaders, or uninteresting choices. Simulated agents are diagnostic instruments, not substitutes for human players.

## Prerequisites

- A deterministic rules specification and versioned card/deck data.
- Explicit balance questions and the metrics that would answer them.
- A calculator, spreadsheet, or local programming environment; record tool and seed details.

## Steps

1. Freeze the rules and data version. Record assumptions, unknowns, player count, mulligan policy, first-player policy, and action policy before calculating.
2. Identify exact subproblems: hypergeometric draw odds, expected resource gain, damage/healing bounds, combo probability, card availability by turn, and worst-case or best-case paths. Show formulas and units; do not report unexplained percentages.
3. Build a small reference model of state transitions. Separate random events from decisions and log the state before and after each transition.
4. Define agent policies as hypotheses, not “optimal play”: random legal, greedy, heuristic, scripted archetype, and search-limited policies where appropriate. State what each policy cannot represent.
5. Use independent seeds per batch and retain the seed list, sample size, confidence interval or error estimate, and stopping rule. Repeat batches to detect unstable conclusions.
6. Measure more than win rate: first-player advantage, game length, score spread, resource starvation, mulligan quality, dead-card rate, comeback frequency, early lockouts, action diversity, and frequency of dominant lines.
7. Run sensitivity analysis by changing one parameter at a time, then selected interactions. Prefer the smallest change that improves the target metric without damaging the player promise.
8. Check adversarial and boundary cases: perfect draws, worst draws, empty deck, maximum resources, simultaneous triggers, illegal-target pressure, and repeated loops. Exact bounds are often more useful than average results.
9. Compare simulation findings against human playtests. If they disagree, inspect the agent policy, information assumptions, and incentives before changing rules.
10. Report uncertainty and limitations plainly. Hand changes to `card-game-rules-engineering` for rule consistency and to `card-game-playtesting-iteration` for human validation.

## Pitfalls

- **False precision:** A simulated 52.1% win rate is not meaningful without policy, seed, sample size, and uncertainty.
- **Agent monoculture:** One heuristic can reward one deck's assumptions rather than game health.
- **Win-rate tunnel vision:** Track agency, tempo, non-games, and decision diversity.
- **Unseeded claims:** If a result cannot be reproduced, treat it as a lead, not evidence.
- **Policy leakage:** Do not let an agent use hidden information a human player would not have.
- **Overfitting:** Avoid tuning to one fixed matchup matrix or one small sample.
- **Math by intuition:** Calculate draw odds and resource curves; do not “eyeball” them.

## Verification

1. Every reported statistic includes rule/data version, policy, sample size, seed strategy, and uncertainty or a reason exact math applies.
2. At least one result is reproduced from a recorded seed or exact formula.
3. Boundary cases and conservation/termination checks pass.
4. Recommendations identify expected benefit, trade-off, and the metric that should move.
5. The report explicitly separates simulated-agent evidence from human-play evidence.

## Cross-References

- `card-game-concept-loop` — metrics must serve the intended player promise.
- `card-game-rules-engineering` — simulation must implement the canonical rules and edge cases.
- `card-game-playtesting-iteration` — validate quantitative hypotheses with real players.
- Game Studies, [A survey method for assessing perceptions of a game](https://www.gamestudies.org/0501/davis_steury_pagulayan/) — consumer playtesting and perception measures.
- Game Studies, [Balancing Risk and Reward to Develop an Optimal Hot-Hand Game](https://gamestudies.org/1101/articles/williams_nesbitt_eidels_elliott) — iterative balancing context; do not copy its game or claims beyond the cited discussion.
