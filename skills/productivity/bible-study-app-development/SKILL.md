---
name: "bible-study-app-development"
description: "Design evidence-first, local-first Bible study apps."
license: "MIT"
compatibility: "Open Agent Skills format for Codex, Claude Code, Gemini CLI, Cursor, OpenCode, GitHub Copilot, and compatible hosts. Runtime tools are listed in Prerequisites."
metadata:
  author: "Broville"
  version: "2.0.0"
  platforms: "[\"linux\",\"macos\",\"windows\"]"
  triggers: "[\"When a user asks to plan, source, document, or build a Bible study application.\",\"When a Bible-reading product needs source governance, AI boundaries, or offline content design.\"]"
  inputs: "[{\"name\":\"product-context\",\"description\":\"Intended users, platforms, constraints, and existing project context.\",\"required\":true}]"
  outputs: "[{\"name\":\"product-definition\",\"description\":\"Source-backed product documents and implementation constraints.\"}]"
  tags: "[\"Bible\",\"product-design\",\"source-governance\",\"local-first\"]"
  related-skills: "[\"helloao-bible-api\",\"scripture-study-method\",\"bible-study-facilitation\"]"
---

# Bible Study App Development

## Description

Use this skill to define a Bible-study product before implementation. It creates an evidence-first, licensing-aware, local-first foundation while keeping interpretation, application, and prayer under the user's control.

Do not use this skill to write a sermon, devotional, or theological conclusion. Use it to gather verified resources and design the product that presents them.

## Principles

1. **Evidence first.** Every factual, historical, linguistic, or textual claim shown by the product must link to a vetted source.
2. **License first.** Use public-domain or clearly licensed content; record attribution and redistribution terms before shipping it.
3. **Local first.** The reader should work offline after the user installs a minimal content pack. Sync remains optional.
4. **Source boundaries.** Treat sources without redistribution permission as search/link targets. Do not scrape, mirror, or train on them automatically.
5. **User-owned interpretation.** An agent may gather passages, source excerpts, cross-references, and language data. It must not present theological conclusions, personal application, prayers, or finished teaching as the user's work.
6. **Original-language fidelity.** When supported, preserve token-level surface form, lemma, transliteration, morphology, gloss, and identifier data.

## Steps

1. **Establish the product boundary.** Record target users, platforms, accessibility needs, account model, offline expectations, and the distinction between MVP and later work. Mark open questions rather than inventing answers.
2. **Create the product-definition set.** Use `templates/product-definition-bundle.md` to create a product outline, source registry, translation evaluation record, and architecture decision log. Completion: every core decision is either recorded as `DECIDED` or explicitly `OPEN`.
3. **Create and maintain a source registry.** For each translation, corpus, lexicon, commentary, cultural dataset, and remote source, record its status (`CANDIDATE`, `REVIEW`, `APPROVED`, or `REJECTED`), license, attribution, redistribution rights, data format, provenance, and access method. Evaluate the Free Use Bible API through `helloao-bible-api` as a candidate for text, public-domain commentary, and cross-reference data; it remains subject to the same source approval process. Completion: no product integration depends on an unapproved source.
4. **Evaluate translation candidates.** Compare candidate translations for textual transparency, ambiguity preservation, consistency, and treatment of difficult passages. Perform representative passage-level checks across both Testaments using the actual source text. Completion: the chosen default is documented with evidence, or remains unset.
5. **Design content packs.** Define minimal installable packs for Bible text and optional packs for original-language corpora, lexicons, commentaries, cultural data, and reading plans. Each pack needs an identifier, version, language, size, license, attribution, source URL, dependencies, and offline/remote status. Completion: a reader can identify what is required and what is optional without relying on network access.
6. **Set AI boundaries.** Permit source retrieval, citation assembly, cross-reference discovery, language-data display, and blank study templates. Prohibit unsourced claims, automatic ingestion of remote-only sources, personal applications, prayers, sermons, devotionals, and doctrinal conclusions. Completion: each AI feature has a source and boundary statement.
7. **Design user data and sync.** Record provenance for every user-created clip: source URL, title, access date, and attribution. Prefer merge-aware operations for notes and highlights; use simple conflict resolution only for settings where loss is acceptable. Completion: concurrent edits do not silently erase user work.
8. **Document architecture decisions.** Choose technologies based on the deployment constraints rather than a prescribed stack. Record alternatives, rationale, consequences, and unresolved risks. Completion: another team can implement the product without hidden platform assumptions.

## Reference Architecture

Use token-level data when word study or interlinear display is in scope:

```text
verse: canonical_id, reference
word_token: verse_id, position, surface_form, transliteration, lemma,
            lexical_identifier, morphology, gloss
```

Keep core reading separate from optional research data. A live API may be useful for discovery, but downloadable data is usually more reliable for offline text and original-language analysis.

## Pitfalls

- Assuming a text API also supplies parsing or lexicons; verify each data capability separately.
- Treating public access as permission to redistribute; license and attribution are separate checks.
- Selecting a translation because an endpoint happens to expose it rather than evaluating it.
- Allowing generated text to look like sourced scholarship or user-authored reflection.
- Using last-write-wins for rich notes and losing edits from another device.
- Making remote-source material part of the local corpus without explicit permission.

## Verification

- The product definition names its target users, MVP boundary, and open decisions.
- Every integrated source is `APPROVED` and has a documented license, attribution, and redistribution decision.
- Every downloadable pack declares dependencies and offline behavior.
- Every AI capability states allowed inputs, required citations, and forbidden output types.
- A second agent can read the documents and identify no machine-local paths, secrets, proprietary tooling, or unverified source assumptions.

## Supporting Files

- `templates/product-definition-bundle.md` — portable starting structure for the product documents.
