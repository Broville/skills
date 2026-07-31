# AGENTS.md — skills

This file provides instructions for autonomous agents working on this repository.

## Project Context

- **Org**: Broville
- **Repo**: skills
- **Project**: Hermes

## What This Repo Is

This is a **skill definition repository** — a library of modular, documented skill definitions that agents can discover, pull, and install. It is NOT executable code; it's a specification and documentation layer.

## Pipeline

This repo follows the process defined in [SOP.md](./SOP.md). When a skill issue is assigned:

1. **Open or claim** the `[Skill]` issue.
2. **Create a branch** from `main` (`feat/<skill-name>` for new skills, `fix/<skill-name>-<short-desc>` for edits).
3. **Write or edit** the `SKILL.md` following [SKILL-SPEC.md](./SKILL-SPEC.md).
4. **Validate locally** — run the checks in SOP.md § Validation Checklist.
5. **Open a PR** against `main` and request 1 approval.
6. **Merge** only after approval.

This repository is a documentation library, not a deployed service, so it does not use canary deployment or runtime feedback labels.

## Skill Authoring Rules

Every skill MUST have:

1. **SKILL.md** with complete YAML frontmatter (name, description, version, triggers, inputs, outputs)
2. **Trigger conditions** — explicit list of when an agent should load this skill
3. **Pitfalls section** — common mistakes and how to avoid them
4. **Verification steps** — how to confirm the skill produced correct results
5. **Related skills** — cross-references to other skills in this repo

### Naming Conventions

- **Directory names**: kebab-case (e.g., `systematic-debugging/`)
- **Categories**: one of `devops`, `software-dev`, `mlops`, `data`, `research`, `creative`, `productivity`, `monitoring`
- **SKILL.md**: always exactly `SKILL.md` (uppercase)

### File Structure

```
skills/skill-name/
├── SKILL.md           # Required — the skill definition
├── references/        # Optional — supporting reference docs
├── templates/         # Optional — template files the skill produces
├── scripts/           # Optional — executable scripts the skill runs
└── assets/            # Optional — static assets (images, diagrams)
```

## Standard Operating Procedures

**All agents must read and follow [SOP.md](./SOP.md) before interacting with this repo.** It defines the authoritative process for:

- **Adding** a new skill (issue → branch → SKILL.md → validate → PR → merge)
- **Editing** an existing skill (issue → version bump → validate → PR → merge)
- **Removing** a skill (issue → check dependents → delete → PR → merge)
- **Pulling** a skill for use (locate → read SKILL.md in full → execute → verify)
- **Deprecating** a skill (add `deprecated: true` + `replaced_by` → PR → merge)
- **Skill discovery** (by category, by trigger match, by search, by related skills)

**Key rules:**

1. **No direct commits to `main`** — always use a branch and PR
2. **Every skill must have a `SKILL.md`** with complete frontmatter, triggers, steps, pitfalls, and verification
3. **No secrets or local paths** in any skill file
4. **Validate before merging** — use the checklist in SOP.md § Validation Checklist
5. **Patch after use** — if you discover a gap while pulling a skill, open an issue and PR the fix after the session

## Conventions

- **Branch naming**: `feat/<skill-name>`, `fix/<skill-name>-<short-desc>`, `docs/<skill-name>-<short-desc>`, `chore/remove-<skill-name>`
- **Commit style**: Conventional commits (`feat:`, `fix:`, `docs:`, `chore:`)
- **PRs**: Require 1 approval; stale reviews are dismissed
- **Issues**: Use the YAML form templates; do not create blank issues