# AGENTS.md — skills

This file provides instructions for autonomous agents working on this repository.

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
├── templates/          # Optional — template files the skill produces
├── scripts/            # Optional — executable scripts the skill runs
└── assets/             # Optional — static assets (images, diagrams)
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

## Reports

All briefs, reports, and status updates are published to **pages.eaglepass.io** using the Liquid Glass design system (dark mode, self-contained HTML).

## Discord

- **Channel**: #skills under Projects category
- **Origin thread**: Used for autopilot issue tracking

## Labels Reference

| Label                   | Color   | Purpose                                    |
|-------------------------|---------|--------------------------------------------|
| `priority:critical`    | #B60205 | Blocks core functionality                  |
| `priority:high`        | #D93F0B | Pick up before medium/low                  |
| `priority:medium`      | #FBCA04 | Default priority                           |
| `agent:working`        | #5319E7 | Agent claimed, actively working             |
| `agent:canary`         | #1D76DB | Deployed to canary for validation          |
| `agent:awaiting-feedback` | #0E8A16 | Waiting for human validation             |
| `claimed_at`           | #6B6B6B | Unix timestamp when issue was claimed      |
| `discord:thread`       | #8E44AD | Discord thread ID for this issue           |
| `discord:last`          | #27AE60 | Last Discord message ID seen by agent      |