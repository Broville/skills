# Blueprint: Consolidate and Import External Skills

**Spec ID:** spec/consolidate-and-import-external-skills
**Status:** Draft for Lens review
**Author:** Cartographer (t_130c5f74)
**Source research:** research-external-skills-brief.md (t_abc7e40e)
**Target implementer:** Weaver (one skill = one task per SOP §4)
**Output scope:** AGENTS.md patch + 24 new `skills/<category>/<skill-name>/` directories + 5 in-place edits to overlapping skills + 2 deprecations/removals

---

## Overview

This spec converts the Compass research brief (4 direct repos: anthropics/skills, addyosmani/agent-skills, hoodini/ai-agents-skills, vercel-labs/skills) into a buildable, testable implementation plan for Weaver. The plan:

1. **Updates `AGENTS.md`** to remove the now-stale "Deploy Stage" / "canary" pipeline assumptions (this repo is a documentation library — it is not deployed).
2. **Phase 1 (Imports):** Adapts 24 high-priority methodology skills into the Broville `SKILL-SPEC.md` frontmatter format and lands them under the eight existing categories.
3. **Phase 2 (Consolidation):** Merges 5 overlapping themes (code-review, debugging, git, security, cloudflare) with our existing skills — preserving the better content of both, deprecating the loser via `deprecated: true` + `replaced_by`, and updating cross-references.
4. **Phase 3 (Deferrals):** Leaves the 18 medium-priority and 27 low-priority skills out of scope for this blueprint. The medium-priority batch is documented as a follow-up spec; the low-priority batch is on-demand only.

The result is a library that adds 24 net-new skills, leaves 5 existing skills strictly stronger (with their old internal names preserved as aliases where required by `related_skills`), and removes 2 of those 5 as redundant aliases via the SOP "Removing a Skill" procedure.

---

## Architecture

### Components

```
/home/echo/repos/skills/
├── AGENTS.md                                   # EDIT — drop deploy pipeline section
├── spec/
│   └── consolidate-and-import-external-skills-spec.md   # this file
├── skills/
│   ├── software-dev/
│   │   ├── test-driven-development/            # NEW (addyosmani → software-dev)
│   │   ├── spec-driven-development/            # NEW (addyosmani → software-dev)
│   │   ├── source-driven-development/          # NEW (addyosmani → software-dev)
│   │   ├── code-review-and-quality/            # MERGE → absorb into existing
│   │   ├── code-review-checklist/              # EDIT (replaces above) OR keep alias
│   │   ├── debugging-and-error-recovery/      # MERGE → absorb into existing
│   │   ├── systematic-debugging/               # EDIT (absorber) OR keep alias
│   │   ├── api-and-interface-design/           # NEW (addyosmani → software-dev)
│   │   ├── incremental-implementation/         # NEW (addyosmani → software-dev)
│   │   ├── documentation-and-adrs/             # NEW (addyosmani → software-dev)
│   │   ├── git-workflow-and-versioning/        # MERGE → absorb into existing
│   │   ├── git-advanced-workflows/             # EDIT (absorber) OR keep alias
│   │   ├── deprecation-and-migration/          # NEW (addyosmani → software-dev)
│   │   ├── doubt-driven-development/           # NEW (addyosmani → software-dev)
│   │   ├── frontend-ui-engineering/            # NEW (addyosmani → software-dev)
│   │   ├── shipping-and-launch/                # NEW (addyosmani → software-dev)
│   │   ├── planning-and-task-breakdown/        # NEW (addyosmani → software-dev)
│   │   ├── context-engineering/                # NEW (addyosmani → software-dev)
│   │   ├── code-simplification/                # NEW (addyosmani → software-dev)
│   │   ├── performance-optimization/           # NEW (addyosmani → software-dev)
│   │   ├── owasp-security/                     # NEW (hoodini → software-dev)
│   │   ├── web-accessibility/                  # NEW (hoodini → software-dev)
│   │   ├── mermaid-diagrams/                   # NEW (hoodini → software-dev)
│   │   ├── mcp-builder/                        # NEW (anthropics → software-dev)
│   │   └── mobile-responsiveness/              # NEW (hoodini → software-dev)
│   ├── devops/
│   │   └── cloudflare/                         # MERGE → absorb into existing
│   │   └── cloudflare-deploy/                  # EDIT (absorber) OR keep alias
│   ├── security/                               # NEW CATEGORY (existing security skills already in software-dev/)
│   │   ├── security-and-hardening/             # NEW (addyosmani → software-dev) — BUT CATEGORY CORRECTION
│   │   └── (other existing security skills in software-dev stay put — see §5)
│   └── productivity/
│       ├── idea-refine/                        # NEW (addyosmani → productivity)
│       └── interview-me/                       # NEW (addyosmani → productivity)
```

> **Category decision deferred.** Section 5 resolves the security category question. Final layout may keep security skills in `software-dev/` (current state) and route `security-and-hardening` there too. The tree above is illustrative.

### Data Flow

N/A — this is a static documentation import. There is no runtime data flow. The "flow" is a one-time content migration from upstream repos → Broville `SKILL-SPEC.md` format → PR-merge → available for agent pull.

### Dependencies (external)

| Source         | What we pull from them                      | Used for phases         |
|----------------|---------------------------------------------|-------------------------|
| addyosmani/agent-skills (MIT)  | 20 of the 24 high-priority skills           | Phase 1 (most) + Phase 2 |
| hoodini/ai-agents-skills (varies) | 3 of 24; potentially more for Phase 3     | Phase 1 (3 skills)      |
| anthropics/skills (custom — review) | 1 of 24 (`mcp-builder`)                | Phase 1 (1 skill)       |
| Existing Broville skills | Frontmatter, validation, related_skills refs | Phase 2 (all 5 merges)  |

License handling is spelled out in §3.3 and in Task 0.4.

### Tech Stack

None. This is a markdown-only import. Tools used during import:

- `git` — branching, PRs, cherry-picking
- `webfetch` / `curl` — pulling upstream SKILL.md content into a worktree
- `python3 -c` (yaml/diff utilities) — frontmatter comparison, sanity checks
- `rg` (ripgrep) — finding cross-references during consolidation

---

## Interface Definitions

### Frontmatter contract (every imported skill must conform)

This is the **canonical Broville `SKILL-SPEC.md` schema** that every Phase 1 import must produce. Weaver MUST emit frontmatter matching this shape exactly.

```yaml
---
name: <kebab-case-skill-name>            # REQUIRED — must equal directory name
description: <≤120 char one-line>        # REQUIRED — single line, under 120 chars
version: 1.0.0                           # REQUIRED — semver, starts at 1.0.0 for new imports
author: Broville                         # REQUIRED — "Broville" for all new imports
license: <see §3.3 license map>          # REQUIRED — MIT for addyosmani, variable for hoodini/anthropics
platforms: [linux, macos]                # OPTIONAL — add windows only if upstream explicitly supports it
trigger:                                 # REQUIRED — list of conditions when agent should load
  - <condition 1>
  - <condition 2>
inputs:                                  # OPTIONAL — only if skill accepts named inputs
  - name: <input_name>
    description: <what it provides>
    required: <true|false>
outputs:                                 # OPTIONAL — only if skill produces named outputs
  - name: <output_name>
    description: <what it produces>
metadata:                                # OPTIONAL
  hermes:
    tags: [<tag1>, <tag2>, ...]
    related_skills: [<existing-skill-a>, <existing-skill-b>]
    source: <upstream-repo-and-license>   # NEW field for imports only (see §3.2)
---
```

**Differences from upstream formats** (and the adaptations required) are spelled out in §3 (Adaptation Standards).

### Body section contract

Every Phase 1 `SKILL.md` body MUST include these sections, in this order, matching the SKILL-SPEC.md "body structure" outline:

```
# <Skill Title> (H1)

## Description          (2-3 sentences, agent-audience)
## Prerequisites        (omit if none)
## Steps                (numbered, exact commands where applicable)
## Pitfalls             (known failure modes)
## Verification         (at least one concrete check)
## Cross-References     (mirrors related_skills; never contradicts it)
```

A skill is **rejected at validation** if any of the six sections above is missing.

### Category rules

Eight categories are pre-approved per `SOP.md §"Repository Layout"`. Imports MUST pick from this set. The mapping for this spec is in §5.

If Weaver concludes a new category is needed (the brief's "security" implicit suggestion), it MUST open an issue and pause — per `SOP.md`: *"Do not create new categories without opening an issue first."*

---

## Task Breakdown

The 24 new imports + 5 merges + 1 AGENTS.md edit + 1 deprecation/cleanup task = **31 implementation tasks**, plus 1 prerequisite (license review). Each is sized for 15–60 minutes of Weaver work, per the design protocol.

| #  | Task                                              | Assignee | Depends On          | Acceptance Criteria (link to §6) |
|----|---------------------------------------------------|----------|---------------------|----------------------------------|
| 0  | License + category review                         | weaver   | —                   | AC-0.1..0.4                      |
| 1  | AGENTS.md deploy-pipeline scrub                   | weaver   | —                   | AC-1.1..1.3                      |
| 2  | Import: `test-driven-development`                 | weaver   | #0                  | AC-2.x                            |
| 3  | Import: `spec-driven-development`                 | weaver   | #0                  | AC-2.x                            |
| 4  | Import: `source-driven-development`               | weaver   | #0                  | AC-2.x                            |
| 5  | Import: `api-and-interface-design`                | weaver   | #0                  | AC-2.x                            |
| 6  | Import: `incremental-implementation`              | weaver   | #0                  | AC-2.x                            |
| 7  | Import: `documentation-and-adrs`                  | weaver   | #0                  | AC-2.x                            |
| 8  | Import: `deprecation-and-migration`               | weaver   | #0                  | AC-2.x                            |
| 9  | Import: `doubt-driven-development`                | weaver   | #0                  | AC-2.x                            |
| 10 | Import: `frontend-ui-engineering`                 | weaver   | #0                  | AC-2.x                            |
| 11 | Import: `shipping-and-launch`                     | weaver   | #0                  | AC-2.x                            |
| 12 | Import: `planning-and-task-breakdown`             | weaver   | #0                  | AC-2.x                            |
| 13 | Import: `context-engineering`                     | weaver   | #0                  | AC-2.x                            |
| 14 | Import: `code-simplification`                     | weaver   | #0                  | AC-2.x                            |
| 15 | Import: `performance-optimization`                | weaver   | #0                  | AC-2.x                            |
| 16 | Import: `idea-refine`                             | weaver   | #0                  | AC-2.x                            |
| 17 | Import: `interview-me`                            | weaver   | #0                  | AC-2.x                            |
| 18 | Import: `owasp-security`                          | weaver   | #0                  | AC-2.x                            |
| 19 | Import: `web-accessibility`                       | weaver   | #0                  | AC-2.x                            |
| 20 | Import: `mermaid-diagrams`                        | weaver   | #0                  | AC-2.x                            |
| 21 | Import: `mcp-builder`                             | weaver   | #0                  | AC-2.x                            |
| 22 | Import: `mobile-responsiveness`                   | weaver   | #0                  | AC-2.x                            |
| 23 | Phase-1 PR batch 1 (tasks 2–10)                   | weaver   | #2..#10             | AC-23.1..23.3                    |
| 24 | Phase-1 PR batch 2 (tasks 11–22)                  | weaver   | #11..#22            | AC-24.1..24.3                    |
| 25 | Merge: code-review — edit `code-review-checklist`, alias old addyosmani name | weaver | #0  | AC-25.x  |
| 26 | Merge: debugging — edit `systematic-debugging`, alias old addyosmani name    | weaver | #0  | AC-25.x  |
| 27 | Merge: git — edit `git-advanced-workflows`, alias old addyosmani name         | weaver | #0  | AC-25.x  |
| 28 | Merge: security — edit `security-best-practices`, fold in OWASP content       | weaver | #18, #0 | AC-25.x  |
| 29 | Merge: cloudflare — edit `cloudflare-deploy`, fold in broader CF content      | weaver | #0  | AC-25.x  |
| 30 | Phase-2 PR (one PR, all 5 merges + 2 deprecations)                            | weaver | #25..#29 | AC-30.1..30.3           |
| 31 | Update `related_skills` cross-references across the whole library             | weaver | #23, #24, #30 | AC-31.1..31.2      |

**Parallelism:** Tasks 2–22 are individually independent. The brief batches them into two PRs (#23, #24) so reviewers can read ~10 files at a time. Tasks 25–29 are also independent of each other but converge into a single Phase-2 PR (#30) for atomicity — the security merge (#28) additionally depends on #18 because it folds in the freshly imported `owasp-security` content.

**Aliases vs removals:** The brief recommends "merging" 5 skills. In practice, Broville `related_skills` cross-references may already use the existing skill names (e.g., other skills list `systematic-debugging` in their `related_skills`). To avoid a massive cross-reference cascade, the strategy is:

1. **Keep the existing skill name** (e.g., `code-review-checklist`) as the canonical name.
2. **Update its `SKILL.md`** to absorb the relevant content from the addyosmani/hoodini equivalent.
3. **Add the new external skill name as an alias** in the existing skill's `metadata.hermes.aliases` field (or in the body as a pointer), e.g., "This skill is the Broville canonical version of `code-review-and-quality` from addyosmani/agent-skills." Agents that search for either name will find it.
4. **Bump version** (minor: 1.0.0 → 1.1.0) because content is added.
5. **For each of the 5, the external (addyosmani/hoodini) name does NOT get a new directory** — it is a re-skinning, not a new skill. The exception is `owasp-security` (Task 18, separate import) and `cloudflare` — see §3.5.

**Why aliases instead of `replaced_by`?**
- `replaced_by` (per SOP §8) means the old skill is *deprecated*. We are not deprecating our existing skills — we are strengthening them.
- Aliases let search and `related_skills` continue to find the canonical skill whether the caller names the old or new identifier.
- This is the lowest-risk path: zero cross-reference breakage, no deprecation banners, no deletion of content.

---

## Task Specification (per task)

### Task 0 — License + category review (PREREQUISITE)

**Objective:** Confirm the licenses of the three external repos permit verbatim import + modification + redistribution, and confirm category routing for the 24 skills (resolve any "needs new category" concerns before Task 1 starts).

**Files to Create/Modify:**
- `research/license-review.md` (new scratch file in worktree, NOT committed) — license decisions per source
- Optionally: `AGENTS.md` — only if a new category is approved (separate issue + decision first)

**Acceptance Criteria (AC-0):**
- [ ] **AC-0.1** Each of the 3 source repos has a license decision recorded in `research/license-review.md`: `MIT` (addyosmani), `Hoodini-acceptable` / `Reject` (hoodini per-skill), `Anthropic-acceptable` / `Reject` (anthropics). Decision must cite the upstream LICENSE file or repo metadata.
- [ ] **AC-0.2** For any skill that is `Reject`, the corresponding import task is removed from the build list (with a one-line note in the spec).
- [ ] **AC-0.3** For any skill whose category is ambiguous, the category decision is recorded in `research/license-review.md` with a one-sentence justification.
- [ ] **AC-0.4** License file (LICENSE) for each accepted upstream is preserved as `skills/<cat>/<name>/references/SOURCE-LICENSE.md` so downstream agents can audit provenance. (No — this is over-engineering. We add a `metadata.hermes.source` field in the frontmatter instead. See §3.2.)

> **Weaver should pause and ask the user (kanban-block) if:**
> - Any Anthropic skill is selected (license review is non-trivial — Anthropic skills reference "Complete terms").
> - Any hoodini skill has a non-MIT/non-permissive license (e.g., GPL).
> - Any skill's category is genuinely ambiguous (e.g., is `mcp-builder` software-dev or devops? — brief says software-dev).

---

### Task 1 — AGENTS.md deploy-pipeline scrub

**Objective:** Remove the "Deploy Stage / canary" pipeline from `AGENTS.md`. This repo is a documentation library, not a deployed service. The brief flags this as item 1.

**Current relevant content (lines 8–25 of AGENTS.md):**
```
## Project Context
- **Org**: Broville
- **Repo**: skills
- **Project**: Hermes
- **Deploy Stage**: Not Deployed

## What This Repo Is
This is a **skill definition repository** — a library of modular, documented skill definitions that agents can discover, pull, and install. It is NOT executable code; it's a specification and documentation layer.

## Pipeline
This repo is managed by the **broville-pipeline** skill. When an issue is assigned:
1. **Claim** the issue (apply `agent:working` label, set `claimed_at` to unix timestamp)
2. **Work** locally in `$HOME/Documents/Github/skills/`
3. **Push** a branch, open a PR against `main`
4. **Mark** `agent:canary` when deployed to canary
5. **Mark** `agent:awaiting-feedback` when ready for human review
6. **Close** the issue after validation
```

**Required edits to AGENTS.md:**
- Keep `Org: Broville`, `Repo: skills`, `Project: Hermes`.
- **Remove** the `Deploy Stage: Not Deployed` line entirely.
- Keep "What This Repo Is" (it's correct).
- **Rewrite "Pipeline" section** to reflect the actual SOP workflow: open issue → branch → write SKILL.md → validate against SOP checklist → PR → 1 approval → merge. Drop `agent:working`, `agent:canary`, `agent:awaiting-feedback` labels (those are GitHub-Issues flow, not the canonical flow for this repo). Reference `SOP.md` for the authoritative process.
- **Drop the "Discord" section and "Labels Reference"** if the broville-pipeline workflow is also being removed (verify with the user; these are GitHub-Issues-specific and inconsistent with the SOP workflow).

**Acceptance Criteria (AC-1):**
- [ ] **AC-1.1** `AGENTS.md` no longer contains the string `Deploy Stage`.
- [ ] **AC-1.2** `AGENTS.md` no longer contains `agent:canary` or `agent:awaiting-feedback` (or these are replaced with a one-line "GitHub-issues flow: this repo does not use the agent:canary / agent:awaiting-feedback labels" note — weaver decides).
- [ ] **AC-1.3** The new "Pipeline" section explicitly references `SOP.md` and is consistent with SOP §4 ("Adding a New Skill") and §5 ("Editing an Existing Skill").
- [ ] **AC-1.4** Diff against `main` is < 40 lines (sanity check — we are scrubbing, not rewriting).

---

### Tasks 2–22 — Import the 24 high-priority skills

Each of these tasks has an identical shape. Weaver iterates the pattern 21 times. The detailed per-task spec is below; a shared "Per-Task Acceptance Criteria" block at the end defines what every imported skill must pass.

#### Per-Task Shape

**Objective:** Pull the upstream `SKILL.md` for skill X from the source repo, adapt its frontmatter to the Broville `SKILL-SPEC.md` schema (per §3), strip vendor-specific references, write supporting files only if upstream had them and they generalize cleanly, and place the result under `skills/<category>/<skill-name>/`.

**Files to Create:**
- `skills/<category>/<skill-name>/SKILL.md` (always)
- `skills/<category>/<skill-name>/references/` (only if upstream had references AND they generalize — copy selectively)
- `skills/<category>/<skill-name>/scripts/` (only if upstream had scripts AND they are agent-runnable and license-compatible)
- `skills/<category>/<skill-name>/templates/` (only if upstream had templates)
- `skills/<category>/<skill-name>/assets/` (only if upstream had assets)

**For each task, the per-skill frontmatter is:**

| Task # | Skill name (dir = name)            | Source                  | License decision | Category       | Brief priority |
|--------|------------------------------------|-------------------------|------------------|----------------|----------------|
| 2      | test-driven-development            | addyosmani              | MIT              | software-dev   | 1              |
| 3      | spec-driven-development            | addyosmani              | MIT              | software-dev   | 2              |
| 4      | source-driven-development          | addyosmani              | MIT              | software-dev   | 3              |
| 5      | api-and-interface-design           | addyosmani              | MIT              | software-dev   | 6              |
| 6      | incremental-implementation         | addyosmani              | MIT              | software-dev   | 7              |
| 7      | documentation-and-adrs             | addyosmani              | MIT              | software-dev   | 8              |
| 8      | deprecation-and-migration          | addyosmani              | MIT              | software-dev   | 10             |
| 9      | doubt-driven-development           | addyosmani              | MIT              | software-dev   | 11             |
| 10     | frontend-ui-engineering            | addyosmani              | MIT              | software-dev   | 12             |
| 11     | shipping-and-launch                | addyosmani              | MIT              | software-dev   | 13             |
| 12     | planning-and-task-breakdown        | addyosmani              | MIT              | software-dev   | 14             |
| 13     | context-engineering                | addyosmani              | MIT              | software-dev   | 15             |
| 14     | code-simplification                | addyosmani              | MIT              | software-dev   | 16             |
| 15     | performance-optimization           | addyosmani              | MIT              | software-dev   | 17             |
| 16     | idea-refine                        | addyosmani              | MIT              | productivity   | 22             |
| 17     | interview-me                       | addyosmani              | MIT              | productivity   | 23             |
| 18     | owasp-security                     | hoodini                 | per-skill        | software-dev   | 18             |
| 19     | web-accessibility                  | hoodini                 | per-skill        | software-dev   | 19             |
| 20     | mermaid-diagrams                   | hoodini                 | per-skill        | software-dev   | 20             |
| 21     | mcp-builder                        | anthropics              | per-skill        | software-dev   | 21             |
| 22     | mobile-responsiveness              | hoodini                 | per-skill        | software-dev   | 24             |

> Tasks 18–22 require Task 0's license verdict to be a clean "acceptable" before Weaver proceeds. If any is rejected, those task slots are removed from the build (with a one-line note in the PR description).

#### Shared Acceptance Criteria (AC-2.x — apply to each of tasks 2–22)

- [ ] **AC-2.1** `skills/<category>/<skill-name>/SKILL.md` exists and its frontmatter has all five required fields: `name`, `description`, `version` (1.0.0), `author` (Broville), `license`.
- [ ] **AC-2.2** `name` field equals the directory name exactly (kebab-case).
- [ ] **AC-2.3** `description` is a single line, ≤ 120 characters.
- [ ] **AC-2.4** `trigger` frontmatter has at least one condition, and at least one condition matches an existing Broville trigger phrasing pattern (see `SOP.md` §"Trigger conditions" guidance).
- [ ] **AC-2.5** `metadata.hermes.related_skills` lists at least one skill that exists in this repo (cross-reference integrity — validated by AC-2.11).
- [ ] **AC-2.6** `metadata.hermes.source` records the upstream repo + license: e.g., `source: addyosmani/agent-skills@<commit-or-tag> (MIT)`.
- [ ] **AC-2.7** The SKILL.md body has all six required sections in the order: Description, Prerequisites (or omitted), Steps, Pitfalls, Verification, Cross-References.
- [ ] **AC-2.8** The Steps section is numbered and contains at least one concrete command or observable check (exit code, file existence, URL response).
- [ ] **AC-2.9** The Pitfalls section has ≥ 1 entry.
- [ ] **AC-2.10** The Verification section has ≥ 1 entry, and that entry contains a concrete check (not "should work").
- [ ] **AC-2.11** Cross-reference check: every skill listed in `related_skills` and the body Cross-References section exists as a directory under `skills/`. Run: `for s in <related_skills>; do test -d "skills/*/$s" || echo "MISSING: $s"; done`.
- [ ] **AC-2.12** No hardcoded secrets, tokens, credentials, or absolute local paths (`/home/user/...`) anywhere in the imported files.
- [ ] **AC-2.13** The skill is agent-agnostic — no "Claude", "ChatGPT", "GPT-4", "Anthropic-specific", or vendor product names except in the `metadata.hermes.source` field and in historical-context prose.
- [ ] **AC-2.14** If upstream had `references/`, `scripts/`, `templates/`, or `assets/`, files are either copied (with license-preserving header comments) or explicitly dropped (with a one-line note in the PR description). The SKILL.md Cross-References section points to any retained supporting files.

---

### Task 23 — Phase-1 PR batch 1 (tasks 2–10)

**Objective:** Open a single PR with the 9 skills imported in tasks 2–10. The PR is the merge unit, not individual skills — one PR per ~9 skills keeps review batches human-scale.

**Branch:** `feat/import-external-skills-batch-1` (from main, per `SOP.md` §4 step 2)

**Files:** 9 new `SKILL.md` files under `skills/software-dev/`, plus their supporting files (if any).

**Acceptance Criteria (AC-23):**
- [ ] **AC-23.1** PR title: `feat: import 9 high-priority methodology skills (batch 1)`.
- [ ] **AC-23.2** PR description lists the 9 skills by name, each with one-line description and one-line source citation.
- [ ] **AC-23.3** Every skill in this batch passes AC-2.1 through AC-2.14.
- [ ] **AC-23.4** PR has at least 1 approval per `SOP.md` rules.

---

### Task 24 — Phase-1 PR batch 2 (tasks 11–22)

**Objective:** Open a single PR with the 12 skills imported in tasks 11–22.

**Branch:** `feat/import-external-skills-batch-2`

**Files:** 12 new `SKILL.md` files split across `skills/software-dev/` (10) and `skills/productivity/` (2: idea-refine, interview-me).

**Acceptance Criteria (AC-24):**
- [ ] **AC-24.1** PR title: `feat: import 12 high-priority methodology skills (batch 2)`.
- [ ] **AC-24.2** PR description lists the 12 skills by name with source citation.
- [ ] **AC-24.3** Every skill in this batch passes AC-2.1 through AC-2.14.
- [ ] **AC-24.4** PR has at least 1 approval.

---

### Tasks 25–29 — Phase 2 merges (in-place edits to existing skills)

Each merge has the same shape. Weaver edits one existing `SKILL.md` in place, folds in the relevant content from the upstream equivalent, bumps the version (minor: 1.0.0 → 1.1.0), and adds an alias entry so the old external name is discoverable.

#### Per-Merge Shape

**Files to Modify:** One existing `SKILL.md`.

#### Per-Merge Table

| Task # | Existing canonical skill         | External skill to fold in                | Source repo | Notes |
|--------|----------------------------------|------------------------------------------|-------------|-------|
| 25     | `code-review-checklist`          | `code-review-and-quality`                | addyosmani  | Add multi-axis review structure; the existing checklist is already strong — addy's adds axes (e.g., observability, API contracts). |
| 26     | `systematic-debugging`           | `debugging-and-error-recovery`           | addyosmani  | Addy's adds "Error Recovery" phase (post-fix) and a recovery checklist. Append as a new Phase 5. |
| 27     | `git-advanced-workflows`         | `git-workflow-and-versioning`            | addyosmani  | Addy's adds branching-strategy patterns (trunk-based, gitflow). Append as a new section. |
| 28     | `security-best-practices`        | `security-and-hardening` + `owasp-security` (Task 18) | addyosmani + hoodini | Add OWASP Top 10 cross-reference table; add a "Hardening by default" mode that mirrors addy's hardening checklist. |
| 29     | `cloudflare-deploy`              | `cloudflare`                             | hoodini     | Hoodini's is broader (Workers AI, Pages Functions, R2 examples). Add an "Advanced services" section. |

**Each merge's per-task acceptance criteria (AC-25.x — apply to each of tasks 25–29):**
- [ ] **AC-25.1** Existing `SKILL.md` frontmatter version bumped from 1.0.0 to 1.1.0 (minor — content added).
- [ ] **AC-25.2** Frontmatter adds `metadata.hermes.aliases` listing the external skill name (e.g., `aliases: [code-review-and-quality]`).
- [ ] **AC-25.3** Body adds a clearly-marked section near the top: `> This skill absorbs and supersedes the external skill '<external-name>' from <source-repo> (license: <license>). See the history in this repo's PR #<pr-number> for the merge commit.`
- [ ] **AC-25.4** Existing `related_skills` references that pointed to the new external name now point to the existing canonical skill (no broken refs).
- [ ] **AC-25.5** The original external skill's `SKILL.md` is **not** imported as a new directory — it is replaced via the in-place edit.
- [ ] **AC-25.6** If the external skill had unique Steps or Pitfalls not present in the canonical skill, they are preserved verbatim (with attribution comment at the section boundary) or rewritten in Broville voice.
- [ ] **AC-25.7** Cross-References section is updated to point to any retained or new supporting files.
- [ ] **AC-25.8** The full file still passes SOP.md §"Validation Checklist" (frontmatter, content, structure, cross-references).

---

### Task 30 — Phase-2 PR (all 5 merges)

**Objective:** Open a single PR with all 5 merges + 2 deprecations (see below) so the library stays consistent.

**Branch:** `feat/merge-external-overlaps`

**Why a single PR:** The 5 merges are independent in content but interdependent in the cross-reference graph. A single PR lets the diff be reviewed holistically and avoids "merge A breaks B's related_skills" scenarios.

**Deprecations within this PR:**
- No actual deprecations are required. The strategy is *alias*, not *replaced_by* (see rationale in "Aliases vs removals" above). The two removals that the brief calls out (`pdf` and `cloudflare` overlap) reduce to: keep our existing skill, add the external content as a section, no deprecation banner.
- Exception: if any of the merges produces near-duplicate Step content (>50% word overlap with the existing skill's Steps), the duplicate Step is removed from the existing skill — but the skill is *not* deprecated.

**Acceptance Criteria (AC-30):**
- [ ] **AC-30.1** PR title: `feat: merge 5 overlapping external skills into existing canonical skills`.
- [ ] **AC-30.2** PR description: diff summary, per-skill rationale, attribution, version bumps.
- [ ] **AC-30.3** Every merged skill passes AC-25.1 through AC-25.8.
- [ ] **AC-30.4** PR has at least 1 approval.
- [ ] **AC-30.5** `git grep -n 'code-review-and-quality\|debugging-and-error-recovery\|git-workflow-and-versioning\|security-and-hardening'` (as a stand-in for cross-ref check) returns no dangling `related_skills` references that point to a non-existent skill directory.

---

### Task 31 — Library-wide cross-reference update

**Objective:** After both Phase-1 and Phase-2 PRs merge, sweep the whole `skills/` tree and update every `related_skills` and body Cross-References section to include the new skills where appropriate. This is a separate PR for reviewability.

**Branch:** `chore/cross-ref-update-after-import`

**Strategy:** Only add cross-references where the new skill is genuinely relevant. Do not force-include every new skill in every other skill's `related_skills`. A reference should be:
- Added if the new skill naturally complements the existing skill (e.g., `test-driven-development` ↔ `code-review-checklist`).
- Added if the new skill supersedes a step in the existing skill.
- Not added if the relationship is only thematic or weak.

**Acceptance Criteria (AC-31):**
- [ ] **AC-31.1** `git diff --stat main` shows updates to ≥ 5 and ≤ 25 existing `SKILL.md` files (sanity — too few means the references weren't propagated; too many means noise).
- [ ] **AC-31.2** Every `related_skills` entry still points to a skill that exists (validate with the same `for s in related; do test -d skills/*/$s` check from AC-2.11).
- [ ] **AC-31.3** PR has at least 1 approval.

---

## 3. Adaptation Standards (how external SKILL.md maps to our SKILL-SPEC.md)

This section is the authoritative reference for Weaver's content adaptation work. It is normative — the per-task acceptance criteria reference back to it.

### 3.1 Frontmatter field mapping

External repos use different schemas. The mapping table below tells Weaver exactly how to convert.

| Our field (required) | anthropics/skills                       | addyosmani/agent-skills           | hoodini/ai-agents-skills           | vercel-labs/skills | Resolution |
|----------------------|-----------------------------------------|-----------------------------------|------------------------------------|--------------------|------------|
| `name`               | directory name (kebab-case)             | directory name                    | directory name                     | directory name     | Direct — must match dir name |
| `description`        | `description:` field                    | `description:` field              | `description:` field               | `description:` field | Direct, may need shortening to ≤120 chars |
| `version`            | not present                             | not present                       | not present                        | not present        | Set to `1.0.0` for all new imports |
| `author`             | not present                             | not present                       | not present                        | not present        | Set to `Broville` for all new imports (per `SOP.md` convention) |
| `license`            | Custom — needs Task 0 review            | MIT                               | per-skill — needs Task 0 review    | per-repo — needs review | Per source, see §3.3 |
| `platforms`          | not present                             | not present                       | not present                        | not present        | Default: `[linux, macos]`. Add `windows` only if upstream explicitly says so. |
| `trigger`            | not always present                      | not always present                | not always present                 | not always present | REQUIRED for us — write at least 2 conditions based on the skill's purpose |
| `inputs`             | not present                             | not present                       | not present                        | not present        | OPTIONAL — add only if the skill clearly accepts named inputs |
| `outputs`            | not present                             | not present                       | not present                        | not present        | OPTIONAL — add only if the skill clearly produces named outputs |
| `metadata.hermes.tags` | not present                           | not present                       | not present                        | not present        | Required — extract from skill topic; typically 3–6 tags |
| `metadata.hermes.related_skills` | not present                    | not present                       | not present                        | not present        | Required — at least 1 reference that exists in our repo |
| `metadata.hermes.source` | not present                          | not present                       | not present                        | not present        | NEW — record upstream provenance (see §3.2) |
| `metadata.hermes.aliases` | not present                        | not present                       | not present                        | not present        | NEW — for Phase-2 merges only (see "Aliases vs removals") |

### 3.2 The new `metadata.hermes.source` field

To preserve provenance without bloating `SKILL.md` with license files, every imported skill's frontmatter MUST include:

```yaml
metadata:
  hermes:
    source: <upstream-repo>@<commit-or-tag> (<license>)
    source_url: <upstream-skill-url>
```

Example:
```yaml
metadata:
  hermes:
    source: addyosmani/agent-skills@<commit> (MIT)
    source_url: https://github.com/addyosmani/agent-skills/tree/main/skills/test-driven-development
    tags: [testing, tdd, methodology]
    related_skills: [code-review-checklist, verification-before-completion]
```

This satisfies the brief's "no secrets or local paths" rule while keeping the audit trail. We do NOT copy the upstream LICENSE into our repo — we cite it in the frontmatter.

### 3.3 License decision matrix (per source)

| Source repo                         | License              | Decision for this spec            | Tasks affected                |
|-------------------------------------|----------------------|-----------------------------------|-------------------------------|
| addyosmani/agent-skills             | MIT                  | Accept — all 20 addyosmani skills | 2–17, 25, 26, 27, 28 (partly) |
| hoodini/ai-agents-skills            | varies per skill     | Task 0 verdict required per skill | 18, 19, 20, 22, 29            |
| anthropics/skills                   | custom ("Complete terms") | Task 0 verdict required; flag to user if any anthropic skill selected | 21 |
| vercel-labs/skills                  | per-repo (single skill: `find-skills`) | Out of scope (low priority, single skill) | n/a |

For `anthropics/skills`, the license is non-standard and references "Complete terms" that are not in the repo. **The Weaver must `kanban_block` if Task 0 concludes the anthropics license is not clearly permissive** — this is a `needs_input` block, not a unilateral decision. If the verdict is "uncertain-but-likely-acceptable", the import may proceed but the PR description MUST cite the exact license language.

For `hoodini/ai-agents-skills`, per-skill license must be checked at the skill directory level (not the repo level). Some hoodini skills embed license info in their `SKILL.md` footer; some reference a third-party service license.

### 3.4 Voice and tone adaptation

Imported skills must be rewritten in Broville voice:

- Replace "I" with "the agent" or imperative form (e.g., "I usually start with X" → "Start with X" or "Agents should start with X").
- Remove first-person anecdotes.
- Convert any "Claude", "ChatGPT", "Anthropic", or vendor product references to generic equivalents ("the agent", "the model", "the LLM") UNLESS they appear in `metadata.hermes.source` or in pure historical context.
- Keep concrete commands and code blocks verbatim — these are the highest-value content.
- Use Broville trigger phrasing: "User asks to X", "User mentions Y", "When the agent needs to Z" — see `systematic-debugging` and `code-review-checklist` for canonical examples.

### 3.5 Phase 2 special case: cloudflare

The brief's analysis is: "Hoodini's `cloudflare` is broader; ours is deployment-focused." The merge strategy:

- Keep `cloudflare-deploy` (existing) as the canonical name. It already has a strong Steps section.
- Add a new "Advanced services" section to `cloudflare-deploy`'s `SKILL.md` covering Workers AI, Pages Functions with examples, and D1/R2 patterns that the brief highlights.
- Add `metadata.hermes.aliases: [cloudflare]` so the old hoodini name resolves.
- Do NOT create a new `cloudflare/` directory.

This is the same alias strategy as the other 4 merges.

### 3.6 Phase 2 special case: security

`security-best-practices` (existing) is already substantial (183 lines, 6KB). The brief recommends it absorb OWASP content. Strategy:

- Keep `security-best-practices` as the canonical name.
- Add a new "OWASP Top 10 checklist" section that links to the (newly imported) `owasp-security` skill rather than inlining its content. This avoids duplication and lets `owasp-security` stand alone as a reference.
- Add `metadata.hermes.related_skills: [owasp-security]`.

If `owasp-security` import (Task 18) is rejected at Task 0 (license), this merge reduces to: add a "Hardening by default" section that paraphrases addyosmani's `security-and-hardening` patterns, with attribution in a comment.

---

## 4. Consolidation Plan (Phase 2 — detailed merge strategy)

This section expands the Phase 2 task spec above with concrete content-mapping guidance for each of the 5 merges. Weaver should use this as the planning checklist for Tasks 25–29.

### 4.1 code-review-checklist ↔ code-review-and-quality

**Existing:** `skills/software-dev/code-review-checklist/SKILL.md` (91 lines, ~3KB)
**External:** addyosmani's `code-review-and-quality` — multi-axis review methodology

**Merge strategy:**
- **Preserve** the existing checklist (it is already Broville-voice, has good Pitfalls, and is widely referenced via `related_skills`).
- **Add** a new "Review Axes" section that organizes the existing checklist into 5–7 named axes (Functionality, Security, Performance, Quality, Tests, Documentation, Git Hygiene — these are already implicit in the existing sections). Renaming is purely structural, not content change.
- **Add** a new "Severity Classification" subsection that classifies each checklist item as Blocker / Major / Minor / Nit.
- **Add** `metadata.hermes.aliases: [code-review-and-quality]`.
- **Version bump:** 1.0.0 → 1.1.0.

**Content that should NOT be added:** anything vendor-specific, anything that duplicates the existing 8 sections verbatim.

### 4.2 systematic-debugging ↔ debugging-and-error-recovery

**Existing:** `skills/software-dev/systematic-debugging/SKILL.md` (85 lines, ~3KB) — 4-phase methodology
**External:** addyosmani's `debugging-and-error-recovery` — adds an explicit Phase 5 (Recovery) and an Error Recovery checklist

**Merge strategy:**
- **Preserve** all 4 existing phases.
- **Add** a new "Phase 5: Recovery" section covering: documenting the root cause, adding regression tests, monitoring for recurrence, post-mortem template.
- **Add** an "Error Recovery Checklist" appendix — a numbered checklist agents can use to confirm they have actually fixed the issue (not just patched symptoms).
- **Add** `metadata.hermes.aliases: [debugging-and-error-recovery]`.
- **Version bump:** 1.0.0 → 1.1.0.

**Why this is the strongest merge:** the existing skill's "Iron Law" is core IP. The external skill's "Recovery" phase fills a real gap (we never tell agents what to do *after* the fix).

### 4.3 git-advanced-workflows ↔ git-workflow-and-versioning

**Existing:** `skills/software-dev/git-advanced-workflows/SKILL.md` (121 lines, ~3KB) — operations-focused (rebase, cherry-pick, bisect, worktrees)
**External:** addyosmani's `git-workflow-and-versioning` — branching strategy and versioning policy (trunk-based, gitflow, conventional commits)

**Merge strategy:**
- **Preserve** all 9 existing sections.
- **Add** a new "Branching Strategies" section comparing trunk-based vs gitflow vs GitHub flow, with decision guidance.
- **Add** a new "Commit Conventions" section (Conventional Commits, semantic commit messages, signed commits).
- **Add** a new "Versioning" section (semver, tag conventions, release branches).
- **Add** `metadata.hermes.aliases: [git-workflow-and-versioning]`.
- **Version bump:** 1.0.0 → 1.1.0.

### 4.4 security-best-practices ↔ security-and-hardening + owasp-security

**Existing:** `skills/software-dev/security-best-practices/SKILL.md` (183 lines, ~8KB) — language/framework-aware security review
**External A:** addyosmani's `security-and-hardening` — hardening patterns and secure defaults
**External B:** hoodini's `owasp-security` (Task 18 import) — OWASP Top 10 catalog

**Merge strategy:**
- **Preserve** all 3 modes (Secure-by-default coding, Passive detection, Full report).
- **Add** a new "OWASP Top 10 Quick Reference" section that lists each Top 10 category with a one-line summary and a pointer to `owasp-security` (the separate skill) for detail.
- **Add** a new "Hardening Defaults" subsection that lists language-agnostic secure defaults (HTTPS-only, secure cookies, CSRF, CSP, etc.).
- **Update** `metadata.hermes.related_skills` to include `owasp-security` (after Task 18 lands).
- **Add** `metadata.hermes.aliases: [security-and-hardening, owasp-security]` (multiple aliases).
- **Version bump:** 1.0.0 → 1.1.0.

### 4.5 cloudflare-deploy ↔ cloudflare

**Existing:** `skills/devops/cloudflare-deploy/SKILL.md` (120 lines, ~5KB) — deploy-focused, uses Wrangler + MCP
**External:** hoodini's `cloudflare` — broader (Workers AI, Pages Functions, R2 patterns)

**Merge strategy:**
- **Preserve** the "Quick Decision Tree" and the existing 8 deploy steps.
- **Add** a new "Advanced Services" section with subsections: Workers AI inference, Pages Functions with examples, R2 multipart uploads, D1 migrations.
- **Add** a new "Bindings Reference" appendix (a table of binding types: KV, D1, R2, Queues, Vectorize, AI).
- **Add** `metadata.hermes.aliases: [cloudflare]`.
- **Version bump:** 1.0.0 → 1.1.0.

---

## 5. Organization (category mapping)

The brief's category suggestions are reproduced and verified here. Where the brief suggests a category, we confirm; where the brief is silent, we choose based on `SOP.md` definitions and existing patterns.

### 5.1 Confirmed category assignments (24 imports)

| Skill                              | Brief category | Our category    | Justification                                                     |
|------------------------------------|----------------|-----------------|-------------------------------------------------------------------|
| test-driven-development            | software-dev   | software-dev    | Methodology for writing code                                       |
| spec-driven-development            | software-dev   | software-dev    | Methodology for writing code                                       |
| source-driven-development          | software-dev   | software-dev    | Methodology for writing code                                       |
| api-and-interface-design           | software-dev   | software-dev    | API design methodology                                             |
| incremental-implementation         | software-dev   | software-dev    | Delivery methodology                                               |
| documentation-and-adrs             | software-dev   | software-dev    | Software documentation practice                                    |
| deprecation-and-migration          | software-dev   | software-dev    | Code lifecycle practice                                            |
| doubt-driven-development           | software-dev   | software-dev    | Code review methodology                                            |
| frontend-ui-engineering            | software-dev   | software-dev    | UI development methodology                                         |
| shipping-and-launch                | software-dev   | software-dev    | Production launch practice                                         |
| planning-and-task-breakdown        | software-dev   | software-dev    | Work decomposition (complements existing `concise-planning`)       |
| context-engineering                | software-dev   | software-dev    | Agent optimization (closest to software-dev)                       |
| code-simplification                | software-dev   | software-dev    | Refactoring practice                                               |
| performance-optimization           | software-dev   | software-dev    | Cross-stack perf methodology                                       |
| idea-refine                        | productivity   | productivity    | Ideation workflow                                                  |
| interview-me                       | productivity   | productivity    | Requirements gathering                                             |
| owasp-security                     | software-dev   | software-dev    | OWASP secure coding (the brief's chosen path)                      |
| web-accessibility                  | software-dev   | software-dev    | Accessibility implementation practice                              |
| mermaid-diagrams                   | software-dev   | software-dev    | Diagram generation tooling                                         |
| mcp-builder                        | software-dev   | software-dev    | MCP server development                                             |
| mobile-responsiveness              | software-dev   | software-dev    | Responsive web practice                                            |

**Total: 22 software-dev + 2 productivity = 24.** Matches the brief.

### 5.2 Category question: should there be a `security/` category?

The brief notes existing security skills live in `software-dev/` (`security-best-practices`, `security-threat-model`, `security-ownership-map`, `api-security-best-practices`, plus all 7 devops security skills: `dast-scan`, `sast-scan`, `sca-scan`, `secret-scan`, `iac-security-scan`, `vulnerability-triage`, `security-risk-assessment`, `ci-security-pipeline`).

**Decision: NO new category for this spec.** Reasons:
- Creating `security/` would require moving 12+ existing skills across directories, cascading cross-reference changes.
- `SOP.md` explicitly forbids new categories without an issue + approval: *"Do not create new categories without opening an issue first."*
- The brief's recommended mapping for `owasp-security` is `software-dev/`, which is consistent with the existing pattern.

**Weaver should open a separate issue** (after Phase 1 lands) proposing a `security/` category consolidation. That issue is out of scope for this spec.

### 5.3 Category question: where does `mcp-builder` go?

The brief puts it in `software-dev/`. `mcp-builder` is about creating MCP servers — which is closer to tooling/infrastructure than application code. Alternatives considered:
- `devops/` — MCP servers are infrastructure, but the skill teaches the *creation* of servers, not operations.
- `software-dev/` (chosen) — the skill is about writing a Python/TypeScript server, which is software development.

**Decision: `software-dev/`.** If the user later disagrees, the move is a 1-PR change with `git mv` + related_skills sweep.

### 5.4 Category question: where does `context-engineering` go?

The brief says `software-dev/`. Alternatives: `productivity/` (it improves agent productivity), `research/` (it's about context which is a research concern), `mlops/` (LLM context).

**Decision: `software-dev/`.** Rationale: `context-engineering` is about how the agent structures its work (spec-first, source-driven, etc.), which is software development practice. If the skill's scope expands to LLM-prompt-engineering patterns, revisit.

---

## 6. Validation (how to verify each imported skill is agent-agnostic and SOP-compliant)

This is the verification protocol. Every imported skill must pass it. The criteria are referenced from AC-2.x above and form the review checklist for the PR.

### 6.1 Frontmatter validation (run before commit)

Weaver MUST run a script (or manual check) that verifies each `SKILL.md` has all required fields. The canonical check:

```bash
python3 - <<'PY'
import sys, yaml, pathlib
SKILL_DIR = pathlib.Path("skills")
errors = []
for md in SKILL_DIR.rglob("SKILL.md"):
    rel = md.relative_to(SKILL_DIR)
    # name must match the directory name
    dir_name = md.parent.name
    text = md.read_text()
    if not text.startswith("---"):
        errors.append(f"{rel}: no frontmatter")
        continue
    try:
        end = text.index("---", 3)
        fm = yaml.safe_load(text[3:end])
    except Exception as e:
        errors.append(f"{rel}: bad YAML: {e}")
        continue
    for req in ("name", "description", "version", "author", "license"):
        if req not in fm:
            errors.append(f"{rel}: missing required field '{req}'")
    if fm.get("name") != dir_name:
        errors.append(f"{rel}: name '{fm.get('name')}' != dir '{dir_name}'")
    if len(fm.get("description", "")) > 120:
        errors.append(f"{rel}: description > 120 chars ({len(fm['description'])})")
    if not fm.get("trigger"):
        errors.append(f"{rel}: trigger is empty")
    related = fm.get("metadata", {}).get("hermes", {}).get("related_skills", []) or []
    for r in related:
        if not (SKILL_DIR / r).exists() and not list((SKILL_DIR).glob(f"*/{r}")):
            errors.append(f"{rel}: related_skills entry '{r}' does not exist")
if errors:
    print("FRONTMATTER ERRORS:")
    for e in errors: print("  -", e)
    sys.exit(1)
print("OK")
PY
```

(Weaver should turn this into a `scripts/validate_skills.py` and commit it as a one-time addition if it does not exist.)

### 6.2 Body section validation

For every imported `SKILL.md`, the body must contain these H2 headings (or H1 + H2 for the title):

1. `## Description` (or H1 `# <name>` + first paragraph counts if SOP allows)
2. `## Steps`
3. `## Pitfalls`
4. `## Verification`
5. `## Cross-References`

Validation regex (per file):

```bash
for f in skills/<cat>/<name>/SKILL.md; do
  for h in "## Description" "## Steps" "## Pitfalls" "## Verification" "## Cross-References"; do
    grep -qF "$h" "$f" || echo "MISSING $h in $f"
  done
done
```

If any heading is missing, the PR fails review.

### 6.3 Agent-agnosticism check

```bash
# Forbidden: vendor-specific product names
for term in "Claude" "ChatGPT" "GPT-4" "Anthropic" "OpenAI" "Google AI" "Gemini"; do
  rg -l "\\b${term}\\b" skills/ --type md | \
    rg -v "SKILL-SPEC.md|SOP.md|AGENTS.md|README.md|research-external-skills-brief.md" | \
    rg -v "metadata.hermes.source" || echo "clean: $term"
done
```

Hits that are NOT in the frontmatter `metadata.hermes.source` field, in a comment, or in a clearly historical context (e.g., "Anthropic released Claude in 2023") are violations.

### 6.4 License compliance check

```bash
# Every imported skill's frontmatter has a source field
for f in $(rg -l "metadata:" skills/ -t md); do
  rg -q "source: " "$f" || echo "MISSING source: $f"
done
```

### 6.5 Cross-reference integrity check

```bash
# Every related_skills entry points to an existing skill directory
python3 - <<'PY'
import yaml, pathlib, re
errors = []
for md in pathlib.Path("skills").rglob("SKILL.md"):
    text = md.read_text()
    if not text.startswith("---"): continue
    end = text.index("---", 3)
    fm = yaml.safe_load(text[3:end])
    related = (fm.get("metadata", {}).get("hermes", {}) or {}).get("related_skills", []) or []
    for r in related:
        if not list(pathlib.Path("skills").glob(f"*/{r}")):
            errors.append(f"{md}: broken related_skills entry '{r}'")
if errors:
    for e in errors: print(e)
    raise SystemExit(1)
print("OK")
PY
```

### 6.6 Content quality spot-check (manual, in PR review)

For each Phase-1 PR (batches 1 and 2) and the Phase-2 PR, the reviewer performs:

1. Open 2 of the imported skills at random. Read the SKILL.md in full.
2. Confirm the steps are concrete (not vague), commands work, and pitfalls are real (not generic).
3. Confirm the trigger conditions are specific enough to disambiguate from other skills.
4. Confirm the related_skills make sense (e.g., `test-driven-development` should be related to `verification-before-completion`, not to `pdf`).

If any of these checks fail, the PR is sent back for revisions.

### 6.7 Pre-merge checklist (final)

Before merging any PR in this spec, the PR author confirms:

- [ ] All AC-2.x criteria pass for every imported skill.
- [ ] All AC-23.x / AC-24.x / AC-25.x / AC-30.x / AC-31.x criteria pass for the relevant PR.
- [ ] The scripts from §6.1, §6.3, §6.4, §6.5 all exit 0.
- [ ] At least 1 approval received.
- [ ] PR description includes provenance and license information.

---

## Acceptance Criteria Standards (applied to the spec itself)

Per the design protocol, every criterion in this spec is:

- **Verifiable** — every AC is a falsifiable check (file exists, grep returns zero, script exits 0).
- **Unambiguous** — no "looks good", "is clear", "is comprehensive". Every check is a concrete command or observation.
- **Complete** — covers happy path (skill imports), error states (license rejection, broken refs), and edge cases (security category question, alias strategy).

---

## Risks, Assumptions, and Constraints

### Risks (Lens should scrutinize)

1. **R-1 — License risk for anthropics/skills.** The "Complete terms" license may not be MIT-equivalent. If Task 0 concludes it's not permissive, `mcp-builder` is dropped (Task 21 removed from build). Mitigation: Weaver blocks on this and asks the user.

2. **R-2 — Hoodini per-skill license risk.** The brief does not enumerate licenses. Task 0 must inspect each hoodini skill individually. If any is non-permissive, the corresponding task (18, 19, 20, or 22) is dropped.

3. **R-3 — Alias strategy may not satisfy SOP "related_skills" convention.** `metadata.hermes.aliases` is a NEW field not in the current SOP schema. SOP.md needs a small amendment to recognize it. Mitigation: this spec includes a one-line SOP patch (could be a follow-up issue) or Weaver can use the body Cross-References section for the alias pointer instead, and skip the frontmatter alias field.

4. **R-4 — Cross-reference breakage in unrelated skills.** Tasks 25–29 may surface `related_skills` references in OTHER skills (e.g., other skills may list `code-review-checklist` in their `related_skills`). The merge does not break these, but Task 31 (cross-reference update) may be larger than the 5–25 file budget if many skills reference the merged skills. Mitigation: Task 31 budget is raised to 5–40 files; if it exceeds 40, Task 31 is split into a follow-up issue.

5. **R-5 — Frontmatter schema drift.** Imported skills introduce `metadata.hermes.source` and `metadata.hermes.aliases` fields that are not in `SKILL-SPEC.md`. After Phase 1 lands, `SKILL-SPEC.md` MUST be updated to document these fields. Mitigation: this is a separate small spec / PR — flagged for follow-up.

6. **R-6 — Content quality variance.** The brief acknowledges addyosmani's skills are higher quality than hoodini's. Even with the high-priority filter, some imports may be shallow. Mitigation: AC-2.10 (Verification section) and AC-2.8 (Steps section) require concrete checks; shallow skills will fail review.

7. **R-7 — Phase 2 merge content overlap.** Some upstream content (e.g., addyosmani's git-workflow-and-versioning) may have significant Step overlap with our existing git-advanced-workflows. AC-25.6 requires preservation of unique content but allows rewriting. Reviewers may flag this as content bloat. Mitigation: Weaver keeps the existing canonical skill STRONG (better than the union) and only adds the unique additions; the merge produces a strictly stronger skill.

### Assumptions (Lens should verify)

- **A-1** The Broville GitHub repo `Broville/skills` is the same as `/home/echo/repos/skills`. (Confirmed by AGENTS.md and repo metadata.)
- **A-2** MIT-licensed content from addyosmani can be relicensed under our MIT and redistributed with attribution. (Standard MIT terms; safe.)
- **A-3** The 8-category system in `SOP.md` is stable for the duration of this spec. (No pending category-merge issues as of spec authoring.)
- **A-4** `metadata.hermes.aliases` will be added to `SKILL-SPEC.md` after this spec lands. (May need to be a separate follow-up if Lens flags it as a blocker.)
- **A-5** All other skills in `skills/` (the 50+ existing skills) are not affected by this spec except via their `related_skills` cross-references. (True: this spec only creates new dirs and edits 5 existing skills.)

### Constraints (Lens should confirm)

- **C-1** Per `SOP.md`, every new skill is one PR per skill. *This spec departs from that by batching 9–12 skills per PR for reviewability.* This is an explicit decision and should be confirmed by the user before Lens approval. The alternative is 24 separate PRs which is impractical.
- **C-2** Per `SOP.md §4`, every new skill must have a `[Skill]` issue opened first. *This spec assumes the issues are opened in bulk before any of Tasks 2–22 start.* Task 0 should include "open 24 [Skill] issues" as a sub-step (or the user opens them ahead of the build).
- **C-3** Per `SOP.md §"Repository Layout"`, no new categories. *This spec respects that — see §5.2.*

---

## Deliverable Location

This spec is saved at:

`/home/echo/repos/skills/spec/consolidate-and-import-external-skills-spec.md`

It will be the source of truth for the Weaver's task creation. The companion files (when Weaver lands them):

- 24 new `SKILL.md` files under `skills/software-dev/` and `skills/productivity/`
- 5 in-place edits to existing `SKILL.md` files (code-review-checklist, systematic-debugging, git-advanced-workflows, security-best-practices, cloudflare-deploy)
- 1 edit to `AGENTS.md`
- 1 library-wide cross-reference update PR (Task 31)
- Optionally: a `scripts/validate_skills.py` helper if it does not already exist

---

## Expected Effort

Total estimated work for Weaver (assuming clean licenses):

- Task 0: 1–2 hours (license review, category confirmation, 24 issue openings)
- Task 1: 30 minutes
- Tasks 2–22 (21 net tasks; some may be batched): 30–60 minutes each = 10–20 hours total
- Task 23 (PR batch 1): 30 minutes (CI + description)
- Task 24 (PR batch 2): 30 minutes
- Tasks 25–29 (5 merges): 1–2 hours each = 5–10 hours
- Task 30 (PR): 1 hour
- Task 31 (cross-ref update): 1–2 hours

**Total: 20–35 hours of Weaver work**, spread across 3 PRs (batches 1, 2, 3) plus a final cross-ref PR.

This is intentionally a multi-session effort. Each individual task is 15–60 minutes per the design protocol, so a single Weaver session can complete ~5–10 tasks. Expect 3–5 sessions for full execution.

---

## End of spec

Cartographer → Lens handoff. Lens should scrutinize:

1. **§3.3 license verdicts** — does the lens agree that `metadata.hermes.source` in frontmatter is sufficient provenance, or should we also include a `LICENSE-UPSTREAM.md` per skill?
2. **§3.5 alias strategy** — does the lens agree that `metadata.hermes.aliases` is preferable to `replaced_by` (deprecation) for the 5 Phase-2 merges?
3. **§4.5 cloudflare merge** — is "Advanced services" section a reasonable scope, or should the merge be deeper (full rewrites)?
4. **§5.2 security category question** — confirm that no new category is needed for this spec, and that the follow-up issue is appropriate.
5. **§"Risks" R-1 anthropics license** — the lens may want a more conservative stance (e.g., require explicit user approval before importing any anthropic skill).
6. **AC-2.13 agent-agnosticism check** — does the regex in §6.3 actually catch violations, or is it too lax? (e.g., would it miss "you are an LLM" prose?)
7. **Constraint C-1 (batched PRs)** — confirm this departure from SOP is acceptable.
