# Skill Specification

This document defines the canonical format for all skills in this repository.

## SKILL.md Frontmatter

Every `SKILL.md` must begin with YAML frontmatter enclosed in `---`. All fields listed as **required** must be present.

### Required Fields

| Field          | Type          | Description                                         |
|---------------|---------------|-----------------------------------------------------|
| `name`        | string        | Kebab-case skill name (must match directory name)  |
| `description` | string        | One-line summary of what the skill does              |
| `version`     | semver string | Current version (e.g., `1.0.0`)                     |
| `author`      | string        | Author name or org                                   |
| `license`     | string        | License identifier (e.g., `MIT`)                    |

### Optional Fields

| Field          | Type          | Description                                         |
|---------------|---------------|-----------------------------------------------------|
| `platforms`   | string[]      | Supported platforms: `linux`, `macos`, `windows`     |
| `metadata`    | object        | Extended metadata (see below)                       |
| `trigger`     | string[]      | When an agent should activate this skill             |
| `inputs`      | object[]      | Named inputs the skill accepts                       |
| `outputs`     | object[]      | Named outputs the skill produces                     |

### Metadata Object

The `metadata` field supports nested objects. The `hermes` key is reserved for Hermes agent metadata:

```yaml
metadata:
  hermes:
    tags: [tag1, tag2]           # Searchable tags
    related_skills: [skill-x]    # Cross-references to other skills
```

### Inputs and Outputs

Each input/output entry has this structure:

```yaml
inputs:
  - name: repo_path
    description: Absolute path to the git repository
    required: true

outputs:
  - name: report_url
    description: Published report URL on pages.eaglepass.io
```

## SKILL.md Body Structure

After frontmatter, the body should follow this outline (sections marked with ★ are required):

### ★ Title (H1)

Skill name as an H1 heading.

### ★ Description

2-3 sentences explaining what the skill does and when to use it. Write for an agent audience — be precise about trigger conditions and expected outcomes.

### Prerequisites

Tools, access, or environment the skill requires. If this section is missing, the skill has no external prerequisites.

### ★ Steps

Numbered steps with exact commands and expected output. Each step should be independently verifiable.

### Pitfalls

Common mistakes, edge cases, and gotchas. Every known failure mode should have an entry here.

### ★ Verification

How to confirm the skill worked correctly. Must include at least one concrete check (command exit code, file existence, URL response, etc.).

### Cross-References

Links to related skills, external docs, or internal resources. Use `related_skills` in frontmatter for automated cross-referencing.

## Directory Conventions

- **`references/`** — Supporting documentation that the skill references (API docs, architecture notes, etc.)
- **`templates/`** — Template files the skill produces or uses (config files, boilerplate)
- **`scripts/`** — Executable scripts the skill runs (shell, Python, etc.)
- **`assets/`** — Static assets (images, diagrams, SVGs)

All files in these directories should be referenced from `SKILL.md` so agents know they exist and how to use them.

## Versioning

Skills follow [Semantic Versioning](https://semver.org/):

- **Patch** (`1.0.1`): Fix a step, add a pitfall, correct a typo
- **Minor** (`1.1.0`): Add a new step, new input/output, new reference
- **Major** (`2.0.0`): Breaking change — renamed skill, removed step, changed trigger conditions

When updating a skill, update the `version` field in frontmatter.

## Validation Checklist

Before merging a skill PR, verify:

- [ ] `SKILL.md` frontmatter has all required fields
- [ ] `name` matches the directory name
- [ ] `version` is valid semver
- [ ] Steps include exact commands with expected output
- [ ] Pitfalls section documents known failure modes
- [ ] Verification section has at least one concrete check
- [ ] `related_skills` entries point to skills that actually exist
- [ ] Supporting files are referenced from `SKILL.md`
- [ ] No hardcoded secrets, tokens, or credentials