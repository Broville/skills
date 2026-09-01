---
name: bible-study-facilitation
description: Build flexible, discussion-first group Bible studies.
version: 1.0.0
author: Broville
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Bible, group-study, facilitation, discussion]
    related_skills: [scripture-study-method, bible-study-app-development]
trigger:
  - When a user asks for a leader-ready Bible study for a group.
  - When a facilitator needs discussion questions on a passage or theme.
inputs:
  - name: passage-and-setting
    description: Passage or theme, group context, time available, and leader preferences.
    required: true
outputs:
  - name: facilitation-guide
    description: A timed, modular leader guide with sourced prompts and questions.
---

# Bible Study Facilitation

## Description

Use this skill to prepare a flexible leader guide for a group studying a biblical passage. It prioritizes the text, discussion, and participant discovery; the agent organizes sourced material and asks questions rather than supplying theological conclusions or group applications.

## Steps

1. **Anchor the session.** Gather the passage or theme, available time, group makeup, setting, series context, and desired balance of reading and discussion. Default to a 35-minute guide only when no time is supplied. Completion: the guide states its audience, duration, and passage boundary.
2. **Gather a resource packet.** Obtain the complete passage from a licensed source selected by the user or project; read its immediate context; identify structure, repeated terms, historical context, cross-references, and any licensed commentary or language resources. Separate direct source material from agent-generated organizational text. Completion: every non-obvious claim has a source citation.
3. **Build questions in order.** Start with observation, then interpretation, then response. Ask textual, open-ended, inclusive questions that a new participant can answer and an experienced participant can deepen. Do not insert answers into the guide. Completion: every question is tied to a textual observation or cited resource.
4. **Structure modular blocks.** Use the following default arc and mark blocks as Core, Recommended, or Optional: opening; reading; observation; interpretation; canonical connections; God/Christ-focused reflection; response prompts; and closing. Add time estimates that total the session length. Completion: a leader can skip or extend a block without breaking the study.
5. **Add leader notes carefully.** Provide citations, textual pointers, vocabulary to define, and common misreadings as prompts for the leader to evaluate. Do not write a sermon, prayer, theological verdict, or prescribed personal response. Completion: notes distinguish source material from facilitation guidance.
6. **Prepare a portable output.** Save the guide wherever the user keeps study materials, using a descriptive file name and a format their tools can read. Do not assume a specific note application, repository, directory structure, or agent framework. Completion: the guide can be used without access to private tooling.

## Default 35-Minute Arc

| Block | Time | Priority |
|---|---:|---|
| Opening and expectations | 3 min | Core |
| Read the passage | 3 min | Core |
| Observation | 8 min | Core |
| Interpretation | 10 min | Core |
| Canonical connections | 5 min | Recommended |
| God/Christ-focused reflection | 2 min | Recommended |
| Response prompts | 3 min | Recommended |
| Closing | 1 min | Optional |
| **Total** | **35 min** | |

For shorter sessions, reduce optional blocks before cutting time in the text. For longer sessions, expand the same blocks or add manuscript marking, a focused word study, or additional participant discussion.

## Question Design

- **Observation:** What is repeated? Who acts or speaks? What changes? What contrasts or questions appear?
- **Interpretation:** How does the immediate context shape this phrase? What would the first audience have recognized? Which details support the reading?
- **Canonical connections:** Where do parallel images, themes, or quotations occur elsewhere in Scripture? What does each passage contribute?
- **Response:** What response does the group see the passage inviting? What further questions should the group carry forward?

## Pitfalls

- Asking application questions before the group has observed and interpreted the text.
- Replacing discussion with an agent-written lecture or assumed theological conclusion.
- Quoting commentary or copyrighted text without a source and permission check.
- Treating a fixed time plan as more important than clear reading and participant engagement.
- Forcing every passage into the same genre, structure, or Christological connection.

## Verification

- The passage is read in immediate context and is sourced under the chosen translation's terms.
- The guide has timed, prioritized blocks that total the requested duration.
- Questions progress from observation to interpretation to response and contain no answer key.
- Every historical, linguistic, or commentary claim cites its source.
- The output contains no personal names, private vault paths, system-specific commands, or assumed agent tooling.

## Supporting Files

- `references/group-study-methods.md` — adaptable group-study patterns and when to use them.
