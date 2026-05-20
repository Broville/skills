# Standard Operating Procedures — Agent Skill Management

This document defines the **authoritative process** for all agents (Hermes, Echo, Pixel, etc.) interacting with the skills repository. Follow these procedures exactly. Deviations cause skill drift, broken cross-references, and agent confusion.

---

## Table of Contents

1. [Overview](#overview)
2. [Terminology](#terminology)
3. [Repository Layout](#repository-layout)
4. [Adding a New Skill](#adding-a-new-skill)
5. [Editing an Existing Skill](#editing-an-existing-skill)
6. [Removing a Skill](#removing-a-skill)
7. [Pulling a Skill for Use](#pulling-a-skill-for-use)
8. [Deprecating a Skill](#deprecating-a-skill)
9. [Skill Discovery](#skill-discovery)
10. [Validation Checklist](#validation-checklist)
11. [Error Handling](#error-handling)

---

## Overview

This repo is the **single source of truth** for agent skill definitions. Skills are not code — they are structured markdown documents that tell agents how to accomplish specific tasks. Every skill must be **discoverable**, **documented**, **versioned**, and **verifiable**.

**Key principle**: If a skill isn't in this repo, it doesn't exist for agent purposes. Local-only skills are development drafts; they must be published here before they are considered authoritative.

---

## Terminology

| Term | Definition |
|------|-----------|
| **Skill** | A self-contained `SKILL.md` plus optional supporting files in a named directory |
| **Category** | A top-level grouping directory under `skills/` (e.g., `devops/`, `research/`) |
| **Skill directory** | The folder containing a skill's `SKILL.md` and supporting files |
| **Frontmatter** | YAML metadata at the top of `SKILL.md` (name, version, triggers, inputs, outputs) |
| **Related skill** | Another skill listed in the `related_skills` frontmatter field |
| **Agent** | Any autonomous system (Hermes, Echo, Pixel, Cadence) that reads or writes skills |
| **Pull** | The act of reading a skill from this repo into an agent's context for execution |
| **Publish** | The act of merging a skill into `main` via PR, making it available for pull |

---

## Repository Layout

```
skills/
├── README.md                  → Repo overview, structure, lifecycle
├── SOP.md                     → This file — operating procedures
├── SKILL-SPEC.md              → Canonical skill format specification
├── AGENTS.md                  → Agent-specific instructions
├── LICENSE                    → MIT
├── .github/ISSUE_TEMPLATE/    → Issue templates (bug, feature, skill, docs)
└── skills/
    └── <category>/
        └── <skill-name>/
            ├── SKILL.md           → Required — the skill definition
            ├── references/        → Optional — supporting reference docs
            ├── templates/         → Optional — template files
            ├── scripts/           → Optional — executable scripts
            └── assets/            → Optional — static assets
```

The eight categories are:

| Category | Purpose |
|----------|---------|
| `devops` | Infrastructure, deployment, operations |
| `software-dev` | Software development, testing, review |
| `mlops` | ML ops, model training, serving |
| `data` | Data engineering, ETL, pipelines |
| `research` | Research, discovery, literature review |
| `creative` | Content generation, design, writing |
| `productivity` | Productivity, docs, automation |
| `monitoring` | Observability, alerting, health checks |

**Do not create new categories without opening an issue first.** Category bloat defeats discoverability.

---

## Adding a New Skill

### Prerequisites

- You have identified a recurring task that warrants a reusable skill
- You know which category it belongs to (see table above)
- You have tested the procedure end-to-end at least once

### Procedure

1. **Open an issue** using the `[Skill]` issue template. Include:
   - Skill name (kebab-case)
   - Category
   - Trigger conditions (when should an agent load this skill?)
   - Brief description of what the skill does

2. **Create a branch** from `main`:
   ```
   git checkout main && git pull origin main
   git checkout -b feat/<skill-name>
   ```

3. **Create the skill directory**:
   ```
   mkdir -p skills/<category>/<skill-name>
   cd skills/<category>/<skill-name>
   ```

4. **Write `SKILL.md`** following the [SKILL-SPEC.md](./SKILL-SPEC.md) format. Every `SKILL.md` must include:
   - YAML frontmatter with **all required fields** (`name`, `description`, `version`, `author`, `license`)
   - `trigger` — explicit conditions for when an agent should load this skill
   - Numbered **steps** with exact commands and expected output
   - **Pitfalls** section documenting known failure modes
   - **Verification** section with at least one concrete check
   - `related_skills` — cross-references to existing skills in this repo

5. **Add supporting files** (if needed):
   - `references/` — Documentation the skill cites
   - `templates/` — Template files the skill produces
   - `scripts/` — Executable scripts the skill runs
   - `assets/` — Static assets (images, diagrams)

6. **Validate locally**:
   - Read through `SKILL.md` — can an agent follow these steps without asking clarifying questions?
   - Check that `related_skills` entries point to skills that **actually exist** in this repo
   - Verify all file references in `SKILL.md` point to files that exist in the skill directory
   - Check that the `name` field matches the directory name exactly (kebab-case)

7. **Commit and push**:
   ```
   git add skills/<category>/<skill-name>/
   git commit -m "feat: add <skill-name> skill"
   git push origin feat/<skill-name>
   ```

8. **Open a PR** against `main`. Include:
   - Reference to the `[Skill]` issue (e.g., "Closes #5")
   - Summary of what the skill does
   - Category justification
   - Confirmation that validation checklist passes

9. **After merge**: Update the issue status to `agent:awaiting-feedback`. The skill is now published and available for pull.

### What NOT to do

- **Do not** commit skills directly to `main` — always use a PR
- **Do not** create a skill without triggers — agents need to know when to load it
- **Do not** hardcode secrets, tokens, or credentials in any skill file
- **Do not** create a category that doesn't exist — open an issue first
- **Do not** reference local paths like `/home/user/...` — use relative paths within the skill directory

---

## Editing an Existing Skill

### When to edit

- A step has become outdated (command changed, API updated, tool renamed)
- A new pitfall was discovered during use
- A new related skill was published that should be cross-referenced
- The skill's trigger conditions changed
- A verification step is no longer valid

### Procedure

1. **Open an issue** describing what needs to change and why. Use the `[Docs]` template for documentation fixes or `[Enhancement]` for behavioral changes.

2. **Bump the version** in `SKILL.md` frontmatter:
   - **Patch** (`1.0.1`): Fix a step, add a pitfall, correct a typo
   - **Minor** (`1.1.0`): Add a new step, new input/output, new reference
   - **Major** (`2.0.0`): Breaking change — renamed skill, removed step, changed triggers

3. **Create a branch** and make your edits:
   ```
   git checkout -b fix/<skill-name>-<short-description>
   ```
   or
   ```
   git checkout -b docs/<skill-name>-<short-description>
   ```

4. **Update `related_skills`** in other skills if this edit changes the relationship graph (e.g., if you renamed a skill that others reference).

5. **Validate** using the same checklist as adding a new skill (see [Validation Checklist](#validation-checklist)).

6. **Commit, push, PR** — same as adding a new skill.

### Special case: Patching a skill in-session

If you discover a pitfall or fix while **using** a skill (during an active agent session):

1. Note the change needed
2. After the session, open an issue with the fix details
3. Create a PR with the patch — **do not skip the PR process**
4. If the fix is urgent and blocking, self-approve and merge, but still open the PR for the audit trail

This applies to Hermes local skills stored in `~/.hermes/profiles/neo/skills/` too — after patching locally, the corresponding skill in this repo should also be updated to keep the canonical version in sync.

---

## Removing a Skill

### When to remove

- The skill is obsolete (tool no longer exists, approach superseded)
- The skill is a duplicate of another skill
- The skill has been merged into another skill (consolidation)

### Procedure

1. **Open an issue** using the `[Skill]` template with the change type set to "Remove skill". Include:
   - The skill name and category
   - Reason for removal
   - If merging into another skill, which one (the "absorber")

2. **Check for dependents**: Search the entire repo for references to this skill:
   ```
   grep -r "skill-name" skills/ --include="*.md"
   ```
   If other skills list this skill in their `related_skills`, update them to remove the reference (or point to the absorber skill if merging).

3. **Create a branch**:
   ```
   git checkout -b chore/remove-<skill-name>
   ```

4. **Delete the skill directory**:
   ```
   git rm -r skills/<category>/<skill-name>/
   ```

5. **Commit and push**:
   ```
   git commit -m "chore: remove <skill-name> skill — obsolete/superseded"
   git push origin chore/remove-<skill-name>
   ```

6. **Open a PR** referencing the removal issue.

### Do NOT

- Remove a skill without checking for dependents first
- Remove a skill without an issue documenting the reason
- Leave dangling `related_skills` references to the removed skill

---

## Pulling a Skill for Use

### Overview

"Pulling" a skill means reading it from this repo into agent context for execution. Agents pull skills on-demand — they do not clone the entire repo every time.

### Pull Procedure

1. **Identify the category** you need. If unsure, check `README.md` for the category table or use skill discovery (see below).

2. **Locate the skill directory**:
   ```
   skills/<category>/<skill-name>/SKILL.md
   ```

3. **Read `SKILL.md`** in full. Pay special attention to:
   - **Frontmatter** — `trigger` conditions confirm this is the right skill
   - **Prerequisites** — ensure all required tools and access are available
   - **Steps** — follow them exactly in order
   - **Pitfalls** — review before starting to avoid known failure modes
   - **Related skills** — you may need to load these too

4. **Load supporting files** if the `SKILL.md` references them:
   - Check `references/` for supplementary documentation
   - Check `templates/` for files the skill produces
   - Check `scripts/` for executable scripts the skill runs

5. **Execute** the steps in order. If a step fails:
   - Check the **Pitfalls** section for known fixes
   - If the failure isn't documented, note it and patch the skill after the session (see [Editing](#editing-an-existing-skill))

6. **Verify** using the skill's **Verification** section. Do not skip this step.

### Important rules for agents pulling skills

- **Always read the full `SKILL.md`** — do not skim. Frontmatter contains critical metadata.
- **Check version** — if the skill version is a major version behind the current version, check if breaking changes affect you.
- **Report gaps** — if a skill is missing a step, has a wrong command, or an undocumented pitfall, that's a bug. Open an issue after the session.
- **Do not modify files in this repo during pull** — pull is read-only execution. If you need to edit, follow the editing procedure.

---

## Deprecating a Skill

When a skill should no longer be used but is kept for reference:

1. Add a `deprecated: true` field to the frontmatter
2. Add a `replaced_by` field pointing to the successor skill (if one exists)
3. Add a deprecation notice at the top of the `SKILL.md` body:

   ```markdown
   > **⚠️ DEPRECATED** — This skill is no longer maintained.
   > Use [`replacement-skill`](../other-category/replacement-skill/) instead.
   > See issue #XX for details.
   ```

4. Commit and merge via PR (same process as editing)

Deprecated skills remain in the repo but agents should refuse to load them unless explicitly asked.

---

## Skill Discovery

Agents need to find the right skill quickly. Use these strategies:

### By category

Navigate to the category directory and scan `SKILL.md` frontmatter `description` fields:

```
skills/devops/        → Infrastructure, deployment, ops
skills/software-dev/  → Development, testing, review
skills/mlops/         → ML ops, training, serving
skills/data/          → Data engineering, ETL
skills/research/      → Research, discovery, literature
skills/creative/      → Content generation, design
skills/productivity/  → Docs, automation, productivity
skills/monitoring/    → Observability, alerting, health
```

### By trigger match

The `trigger` field in each `SKILL.md` defines when an agent should load that skill. When deciding which skill to pull:

1. Read `README.md` for the category overview
2. For each candidate skill, check if the `trigger` conditions match the current task
3. Prefer the most specific skill over a general one

### By search

Use GitHub search or local grep:

```bash
# Search skill names and descriptions
grep -r "description:" skills/ --include="SKILL.md"

# Search trigger conditions
grep -r "trigger:" skills/ -A3 --include="SKILL.md"

# Search for a specific topic
grep -r "docker" skills/ --include="SKILL.md"
```

### By related skills

When you load one skill, check its `related_skills` field. These are intentionally cross-referenced — loading a related skill in the same session is often the right move.

---

## Validation Checklist

Before merging any skill PR, verify **every** item:

### Frontmatter

- [ ] `name` matches the directory name exactly (kebab-case)
- [ ] `description` is a single line, under 120 characters
- [ ] `version` is valid semver (`MAJOR.MINOR.PATCH`)
- [ ] `author` is set
- [ ] `license` is set (typically `MIT`)
- [ ] `trigger` lists at least one condition
- [ ] `related_skills` references only skills that exist in the repo
- [ ] `inputs` and `outputs` are documented if the skill accepts/produces them

### Content

- [ ] Steps include **exact commands** with expected output
- [ ] Steps are numbered and ordered
- [ ] Pitfalls section documents **known failure modes**
- [ ] Verification section has **at least one concrete check** (exit code, file existence, URL response)
- [ ] No hardcoded secrets, tokens, or credentials
- [ ] No absolute local paths (`/home/user/...`)
- [ ] All referenced files exist in the skill directory

### Structure

- [ ] Skill is in the correct category directory
- [ ] Supporting files are in the right subdirectory (`references/`, `templates/`, `scripts/`, `assets/`)
- [ ] All files are referenced from `SKILL.md`
- [ ] No orphan files — every file in the skill directory is referenced

### Cross-references

- [ ] `related_skills` entries point to skills that exist
- [ ] If this skill replaces an old one, the old skill is deprecated with `replaced_by`
- [ ] If other skills reference this skill, their frontmatter is updated

---

## Error Handling

### Skill not found

If you can't find a skill for your task:
1. Check all categories — the skill may be in a different category than expected
2. Search `SKILL.md` descriptions and triggers
3. Check `related_skills` of the closest-matching skill
4. If nothing matches, open a `[Skill]` issue proposing a new one

### Skill steps fail

If a skill's steps don't work:
1. Check the **Pitfalls** section for known issues
2. Check the **skill version** — you may be using an outdated version
3. Check the **Verification** section — are you running in the right environment?
4. If the failure is not documented, open a `[Bug]` issue after the session

### Skill conflicts

If two skills have overlapping triggers:
1. Prefer the **more specific** skill (e.g., `k8s-debug` over `container-debug`)
2. Check `related_skills` — one may explicitly reference the other
3. If truly conflicting, open an `[Enhancement]` issue to clarify trigger conditions

### Skill references broken link

If a `related_skills` entry points to a skill that doesn't exist:
1. The referenced skill may have been removed — check closed issues and PRs
2. It may be a typo — search for similar names
3. Open a `[Docs]` issue to fix the reference