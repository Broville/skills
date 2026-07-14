# Broville Skills

A modular, documented repository of agent skills — designed for easy add/remove lifecycle and agent-pullable consumption.

## Purpose

This repo stores **skill definitions** that autonomous agents can pull, install, and execute. Each skill is self-contained with its own documentation, so agents can discover what's available and how to use it.

## Repository Structure

```
skills/
├── README.md              → This file
├── AGENTS.md              → Agent instructions for working in this repo
├── SKILL-SPEC.md          → Skill specification format and conventions
├── skills/
│   ├── category/
│   │   └── skill-name/
│   │       ├── SKILL.md       → Skill definition (required)
│   │       ├── references/    → Supporting reference docs
│   │       ├── templates/     → Template files the skill produces
│   │       ├── scripts/       → Executable scripts the skill runs
│   │       └── assets/        → Static assets (images, diagrams)
└── .github/
    └── ISSUE_TEMPLATE/    → Issue templates for this repo
```

## Skill Categories

| Category       | Description                                          |
|---------------|------------------------------------------------------|
| `devops`      | Infrastructure, deployment, operations               |
| `software-dev`| Software development, testing, review                |
| `mlops`       | ML ops, model training, serving                      |
| `data`        | Data engineering, ETL, pipelines                    |
| `research`   | Research, discovery, literature review               |
| `creative`    | Content generation, design, writing                 |
| `productivity`| Productivity, docs, automation                       |
| `monitoring`  | Observability, alerting, health checks               |

## Skill Lifecycle

1. **Propose** — Open a `[Skill]` issue describing the skill, its trigger, and expected behavior
2. **Develop** — Create the skill directory under the appropriate category
3. **Document** — Write the `SKILL.md` with full frontmatter, steps, and pitfalls
4. **Review** — PR against `main`; at least one approval required
5. **Publish** — Merge makes the skill available for agents to pull
6. **Maintain** — Patch when steps become outdated; skills are living docs

## SKILL.md Format

Every skill must have a `SKILL.md` with YAML frontmatter:

```yaml
---
name: skill-name
description: One-line description of what this skill does.
version: 1.0.0
author: Broville
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [tag1, tag2]
    related_skills: [other-skill]
trigger:
  - when the user asks about X
  - when task involves Y
inputs:
  - name: input_name
    description: What this input provides
    required: true
outputs:
  - name: output_name
    description: What this skill produces
---

# Skill Title

## Description
Detailed explanation of what the skill does and when to use it.

## Prerequisites
- Tool X installed
- Access to Y

## Steps
1. Step one with exact commands
2. Step two with expected output
3. Verification step

## Pitfalls
- Common mistake and how to avoid it

## Verification
How to confirm the skill worked correctly.
```

See [SKILL-SPEC.md](./SKILL-SPEC.md) for the full specification.

## Adding a New Skill

1. Pick the right category directory under `skills/`
2. Create a directory named after the skill (kebab-case, e.g., `my-new-skill/`)
3. Add `SKILL.md` with full frontmatter and documentation
4. Add any supporting files in `references/`, `templates/`, `scripts/`, or `assets/`
5. Open a PR against `main`

## Removing a Skill

1. Open a `[Skill Removal]` issue listing the skill and reason
2. Delete the skill directory
3. Update any `related_skills` references in other skills
4. Merge the PR

## Documentation Priority

Documentation is a first-class concern in this repo:

- Every skill must have a complete `SKILL.md`
- Every skill must list **triggers** (when an agent should load it)
- Every skill must list **pitfalls** (common mistakes)
- Every skill must include a **verification** section
- Cross-references between related skills must be maintained

## Contributing

See [AGENTS.md](./AGENTS.md) for agent-specific instructions and [SOP.md](./SOP.md) for the full Standard Operating Procedures covering add, edit, remove, pull, deprecate, and discover skills.

For human contributors:

1. Fork the repo
2. Create a feature branch (`feat/skill-name`, `fix/skill-name-desc`, `docs/description`, or `chore/remove-skill-name`)
3. Make your changes
4. Validate using the checklist in [SOP.md § Validation Checklist](./SOP.md#validation-checklist)
5. Open a PR against `main`
6. Ensure CI passes and at least one review approves

## License

MIT — see [LICENSE](./LICENSE) for details.
