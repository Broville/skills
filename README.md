# Broville Skills

A modular, documented repository of portable [Agent Skills](https://agentskills.io/) for Codex, Claude Code, Gemini CLI, Cursor, OpenCode, GitHub Copilot, and other standards-compatible hosts.

## Purpose

This repo stores **skill packages** that autonomous agents can discover, install, and execute. Each package has one provider-neutral `SKILL.md` plus any relative scripts, references, templates, or assets it needs. Agent-specific discovery paths are handled at installation time; the skill itself is not forked per provider.

## Repository Structure

```
Broville/skills/
├── README.md              → This file
├── AGENTS.md              → Agent instructions for working in this repo
├── SKILL-SPEC.md          → Skill specification format and conventions
├── scripts/                → Cross-agent validation and installation
├── skills/
│   └── category/skill-name/
│       ├── SKILL.md        → Skill entrypoint (required)
│       ├── references/     → Supporting reference docs
│       ├── templates/      → Template files the skill produces
│       ├── scripts/        → Executable scripts the skill runs
│       └── assets/         → Static assets (images, diagrams)
└── .github/
    ├── ISSUE_TEMPLATE/     → Issue templates for this repo
    └── workflows/          → Linux, macOS, and Windows validation
```

## Skill Categories

| Category       | Description                                          |
|---------------|------------------------------------------------------|
| `devops`      | Infrastructure, deployment, operations               |
| `software-dev`| Software development, testing, review                |
| `mlops`       | ML ops, model training, serving                      |
| `data`        | Data engineering, ETL, pipelines                    |
| `data-science`| Notebooks, experiments, and analytical workflows     |
| `finance`     | Financial analysis and modeling                      |
| `health`      | Health and fitness workflows                         |
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

Every skill uses only standard root fields. Broville's version, trigger, input, output, and relationship data live in the standard's string-to-string `metadata` map; structured values are JSON strings.

```yaml
---
name: skill-name
description: What this skill does and when an agent should load it.
license: MIT
compatibility: Open Agent Skills format. Runtime requirements are listed in Prerequisites.
metadata:
  author: Broville
  version: "1.0.0"
  platforms: '["linux","macos","windows"]'
  triggers: '["User asks about X","Task involves Y"]'
  inputs: '[{"name":"input_name","description":"What this input provides","required":true}]'
  outputs: '[{"name":"output_name","description":"What this skill produces"}]'
  tags: '["tag1","tag2"]'
  related-skills: '["other-skill"]'
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

## Install for an Agent

Install one or more complete packages into a project using the host's supported discovery path:

```bash
python scripts/install_skills.py --agent codex --workspace /path/to/project --skill frontend-ui-engineering
python scripts/install_skills.py --agent claude --workspace /path/to/project --skill frontend-ui-engineering
python scripts/install_skills.py --agent gemini --workspace /path/to/project --skill frontend-ui-engineering
python scripts/install_skills.py --agent cursor --workspace /path/to/project --skill frontend-ui-engineering
python scripts/install_skills.py --agent opencode --workspace /path/to/project --skill frontend-ui-engineering
python scripts/install_skills.py --agent copilot --workspace /path/to/project --skill frontend-ui-engineering
```

Omit `--skill` to install the full catalog. Use `--target /path/to/skills` for another compatible host. Existing targets are preserved unless `--force` is explicit.

## Validate

```bash
python -m pip install PyYAML skills-ref
python scripts/validate_skills.py
python scripts/test_install_skills.py
```

The checks combine the official Agent Skills validator with repository policy and run on Linux, macOS, and Windows in CI.

## Adding a New Skill

1. Pick the right category directory under `skills/`
2. Create a directory named after the skill (kebab-case, e.g., `my-new-skill/`)
3. Add a standard-compatible `SKILL.md` with complete repository metadata and documentation
4. Add any supporting files in `references/`, `templates/`, `scripts/`, or `assets/`
5. Open a PR against `main`

## Removing a Skill

1. Open a `[Skill Removal]` issue listing the skill and reason
2. Delete the skill directory
3. Update any `metadata.related-skills` references in other skills
4. Merge the PR

## Documentation Priority

Documentation is a first-class concern in this repo:

- Every skill must have a complete `SKILL.md`
- Every skill must encode **triggers** in `metadata.triggers` (when an agent should load it)
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
