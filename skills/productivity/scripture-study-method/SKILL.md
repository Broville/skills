---
name: scripture-study-method
description: Study Scripture with context, sources, and user ownership.
version: 1.0.0
author: Broville
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Bible, exegesis, hermeneutics, SOAP, research]
    related_skills: [helloao-bible-api, bible-study-facilitation, bible-study-app-development]
trigger:
  - When a user asks to read, research, compare, or structure study of a biblical passage.
  - When an agent needs to prepare sourced Scripture-study notes or a personal study template.
inputs:
  - name: passage-and-purpose
    description: Biblical reference, chosen translation if known, and intended study format.
    required: true
outputs:
  - name: source-packet-or-study-template
    description: Cited study resources and prompts without generated theological conclusions.
---

# Scripture Study Method

## Description

Use this skill for careful, source-aware study of Scripture. The agent gathers text, context, language data, and questions; the user retains responsibility for interpretation, application, and prayer.

## Method

Work in this order:

1. **Exegesis:** establish what the text communicated in its literary, historical, linguistic, and canonical context.
2. **Hermeneutics:** test possible readings against genre, authorial intent, the wider canon, and the distinction between description and prescription.
3. **Response:** offer blank prompts for personal reflection only after the first two stages. Do not generate the user's response or prayer.

## Steps

1. **Establish scope and translation.** Confirm the passage, purpose (reading, research packet, group study, or personal template), and the user's preferred licensed translation. If no preference is given, use the placeholder `[bible-translation]` until the user or project chooses one. Completion: the study names its passage, translation, and purpose.
2. **Read context before extracting details.** Read the whole unit, surrounding verses, book flow, and genre. Note speaker, audience, setting, argument, repeated terms, contrasts, and literary structure. Completion: observations distinguish what the text says from later inference.
3. **Collect source material.** Retrieve text only from a source whose terms permit the intended use. When the Free Use Bible API meets the user's translation and license needs, load `helloao-bible-api` and use its discovery-first workflow for text, public-domain commentary, and datasets. Gather original-language data separately from a reputable, licensed corpus. Record source title, URL or publication details, access date, and relevant license or attribution. Completion: every source can be independently located and checked.
4. **Perform word studies responsibly.** Start with the actual form and its immediate syntax, then lemma, morphology, lexical range, and other uses in the relevant corpus. Do not derive a passage meaning from an identifier, dictionary gloss, or etymology alone. Completion: each word-study claim identifies its evidence and limits.
5. **Test interpretations.** Keep genre, historical setting, authorial intent, immediate context, canonical context, and progressive revelation in view. Preserve genuine ambiguity; do not force a conclusion simply because a user asked a question. Completion: conclusions, if supplied by the user, are clearly distinct from source evidence and unresolved alternatives.
6. **Provide a study structure.** For a deep study, organize full text (within license limits), observations, key terms, source packet, cross-references, cultural context, translation notes, reflection questions, and sources. For a personal SOAP study, use the blank template below. Completion: the output is useful without claiming to be the final theological answer.
7. **Store portably.** Use the user's chosen notes system or a plain Markdown file. Do not assume a specific vault, agent profile, directory hierarchy, or automation tool. Completion: all citations and user-owned fields travel with the study.

## SOAP Template

```markdown
## SOAP — Personal Response

### Scripture
> [Key verse or short passage] — [reference] ([bible-translation])

### Observation
- What does the text say?
- What repeated words, images, commands, or questions stand out?

[User fills in.]

### Application
- What response does the passage call me to consider?
- What concrete next step should I examine?

[User fills in.]

### Prayer
[User composes a prayer.]
```

## Pitfalls

- Beginning with a preferred application instead of reading the passage in context.
- Treating poetry, narrative, prophecy, and letters as if they use language in the same way.
- Making claims about ancient culture, grammar, or manuscript variants without a citation.
- Using a lexical identifier, concordance number, or English gloss as a complete word study.
- Publishing text or commentary without confirming its license and attribution requirements.
- Presenting agent-generated material as sourced scholarship or user-authored reflection.

## Verification

- The study identifies the passage, translation, intended use, and every external source.
- Context, genre, and historical setting are considered before interpretation.
- Linguistic and historical claims have verifiable citations.
- Translation and licensing choices are documented rather than assumed.
- SOAP observation, application, and prayer fields remain blank for the user.
- The file contains no private names, machine paths, proprietary agent references, or platform-specific commands.
