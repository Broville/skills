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
├── .agents/plugins/
│   └── marketplace.json    → ChatGPT desktop / Codex marketplace catalog
├── skills/
│   └── category/
│       ├── .codex-plugin/plugin.json → Installable category plugin
│       └── skill-name/
│           ├── SKILL.md    → Skill entrypoint (required)
│           ├── .codex-plugin/plugin.json → Installable individual plugin
│           ├── references/ → Supporting reference docs
│           ├── templates/  → Template files the skill produces
│           ├── scripts/    → Executable scripts the skill runs
│           └── assets/     → Static assets (images, diagrams)
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

## Add as a ChatGPT / Codex Marketplace

This repository exposes **129 plugin choices: 11 category bundles and 118 individual
skills** through `.agents/plugins/marketplace.json`. Bundles retain their existing
IDs (`broville-<category>`) and source paths (`./skills/<category>`). Individual
plugins use `broville-skill-<skill-name>` and point directly to
`./skills/<category>/<skill-name>`. Both use the native Codex compatibility
manifest `.codex-plugin/plugin.json` with `skills: "./"`. Native recursive
discovery includes the root `SKILL.md` of an individual plugin and all skill
directories in a bundle. Each skill and its supporting files have one canonical
source in this repository.

Every listing carries its category label and searchable category keywords. In
the current desktop client, a local marketplace is a flat searchable list;
search for `creative`, `data science`, or `software-dev` to navigate by category.
Views that group plugins by listing category can use those labels. Custom
category metadata does not create nested folders or guarantee category tabs.
Search `category-bundle` or `individual-skill` to narrow the install choices.

After these files are published to the selected Git ref, open **Plugins → Add
Marketplace** in a supported desktop client and enter
`https://github.com/Broville/skills`. Select **Broville Skills**, then install the
bundles or individual plugins you want. UI labels and availability can vary by client and
workspace. The supported CLI registration flow is:

```bash
codex plugin marketplace add Broville/skills --ref main
codex plugin list --marketplace broville-skills --available --json
```

For a local catalog review without changing the registered Git source, use
per-command overrides (supported by Codex CLI 0.159.2):

```bash
codex -c 'marketplaces.broville-local-review.source_type="local"' \
  -c 'marketplaces.broville-local-review.source="/absolute/path/to/skills-checkout"' \
  plugin list --marketplace broville-skills --available --json
```

Registration adds a source; installing a plugin is a separate action. Restart
the desktop app if the source does not appear, then use the plugin directory to
install a plugin and start a new chat. For example, the CLI can install the
software development category with
`codex plugin add broville-software-dev@broville-skills`, or one skill with
`codex plugin add broville-skill-frontend-ui-engineering@broville-skills`.
Use these install commands only when ready to change the host's installed plugins.

### Bundle and individual overlap

Choose a bundle or individual plugins for the same skills. Installing both
creates separate plugin identities and can create separate installed copies of
the same skill. Do not depend on automatic deduplication: current Codex skill
merging removes duplicate physical paths, which does not guarantee deduplication
across separate plugin caches. You can combine a bundle in one category with
individual skills from other categories. Related skill references remain skill
names; they do not install another plugin automatically.

The nested individual manifests are packaging metadata inside a bundle; they
are not extra catalog installs when the bundle is selected. Actual discovery
and behavior with overlapping enabled installs should be checked in a separate
host smoke test before recommending that configuration.

Workspace administrators use **Admin → Plugins → Add → Import marketplace**
with the repository URL, an empty Path, and the desired branch/tag/commit.
Workspace import has its own access and installation policies.

### Maintenance and limits

- Keep the marketplace and every referenced skill directory in a
  Git checkout; a sparse checkout containing only `.agents/plugins` is incomplete.
- Bump a category plugin's `version` when releasing changes to its skills or
  supporting files. Continue versioning individual skills as specified in the SOP;
  each individual plugin's version follows its skill's `metadata.version`.
  Run `python scripts/build_marketplace.py` after adding, changing, or removing
  skills to regenerate individual manifests and catalog entries. Bundle manifests
  remain maintained separately; the generator preserves their IDs and sources.
- Run `codex plugin marketplace upgrade broville-skills` to refresh a registered
  Git source after publication, then use the client's update/reinstall flow.
  Plugins are loaded from installed copies; changes to the checkout do not prove
  an installed copy was refreshed.
- These are skills-only plugins. Installing them does not provide Python/Node
  dependencies, CLIs, credentials, external services, MCP connections, or OS
  capabilities required by a skill. Read each skill's Prerequisites.
- Related skills can live in another category. Install those skills or bundles when a
  workflow needs them; `metadata.related-skills` does not install dependencies.
- Avoid installing the same skills through both marketplace plugins and the raw
  skill installer in one host; this can produce duplicate discovery.
- This uses the supported Codex compatibility format to retain existing paths.
  It is intended for repo/local marketplaces, not a ready-made submission to the
  universal public directory. For broader plugin portability or directory
  submission, export the selected skills to a self-contained Agent Plugins package
  with root `plugin.json` and `skills/<name>/SKILL.md`, preserving supporting
  files and applicable license notices, then complete listing/review requirements.

See OpenAI's [plugin packaging and marketplace documentation](https://developers.openai.com/plugins/build/plugins),
[Codex manifest fields](https://developers.openai.com/plugins/deploy/submission#package-identity-and-components),
and [workspace import documentation](https://developers.openai.com/codex/enterprise/plugin-management).

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
The installer copies the complete skill content but omits each skill root's
`.codex-plugin` wrapper. This preserves raw Agent Skills discovery across hosts
without introducing plugin namespaces into those copies.

## Validate

```bash
python -m pip install PyYAML skills-ref
python scripts/validate_skills.py
python scripts/test_install_skills.py
python scripts/validate_marketplace.py
python scripts/build_marketplace.py --check
python scripts/test_marketplace.py
```

The checks combine the official Agent Skills validator with repository policy and
run on Linux, macOS, and Windows in CI. Marketplace validation checks JSON,
identities, versions, contained paths, listing metadata, and complete skill
coverage without installing or executing a plugin. Package checks archive and
extract all 129 choices, verify skill/supporting file bytes, exercise invalid
catalogs and metadata regeneration, and check distinct paths for overlapping
bundle/individual copies. They simulate packaging; they do not certify desktop
runtime loading. Desktop installation and
runtime behavior require a separate host smoke test.

## Adding a New Skill

1. Pick the right category directory under `skills/`
2. Create a directory named after the skill (kebab-case, e.g., `my-new-skill/`)
3. Add a standard-compatible `SKILL.md` with complete repository metadata and documentation
4. Add any supporting files in `references/`, `templates/`, `scripts/`, or `assets/`
5. Run `python scripts/build_marketplace.py`, bump the affected bundle version, and validate
6. Open a PR against `main`

## Removing a Skill

1. Open a `[Skill Removal]` issue listing the skill and reason
2. Delete the skill directory
3. Update any `metadata.related-skills` references in other skills
4. Regenerate the marketplace, bump the affected bundle version, and validate
5. Merge the PR

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

Original repository material is MIT — see [LICENSE](./LICENSE). Imported packages retain their own licenses, including Apache-2.0 and CC-BY-SA-4.0. See [THIRD-PARTY-NOTICES.md](./THIRD-PARTY-NOTICES.md); a bundle does not relicense its included skills.

## Security incident audits

Use [security-incident-audit](skills/devops/security-incident-audit/SKILL.md) for a bounded, read-only investigation of suspected account, organization, repository, or automation compromise. It produces accessible green/yellow/red reports with clear next-help prompts and explicit coverage limits. It is provider-neutral, needs no private agent tools, and does not authorize remediation or install itself.

Example request: “Use security-incident-audit to review unexpected activity in my authorized repositories during the period I specify. Ask for missing scope and access decisions first, then complete the read-only audit and explain the results without technical jargon.”


## Homeschool teaching and administration

The productivity category includes 32 document-only homeschool and education packages.
They need no new service, executable, hook or messaging account. Install individual
packages or the productivity bundle; follow each skill’s inputs and verification steps.

| Task | Starting skills |
|---|---|
| Plan a year or unit | [Scope and sequence](skills/productivity/scope-and-sequence-designer/SKILL.md), [backwards design](skills/productivity/backwards-design-unit-planner/SKILL.md), [coverage audit](skills/productivity/coverage-audit/SKILL.md), [curriculum crosswalk](skills/productivity/curriculum-crosswalk/SKILL.md) |
| Prepare and assess lessons | [K–12 preparation](skills/productivity/k12-lesson-prep/SKILL.md), [understanding checks](skills/productivity/k12-check-for-understanding/SKILL.md), [quiz generator](skills/productivity/quiz-generator/SKILL.md), [criterion rubrics](skills/productivity/criterion-referenced-rubric-generator/SKILL.md) |
| Support individual learners | [Differentiation](skills/productivity/differentiation-adapter/SKILL.md), [UDL options](skills/productivity/udl-options-designer/SKILL.md), [work analysis](skills/productivity/gap-analysis-from-student-work/SKILL.md), [feedback](skills/productivity/student-feedback-writer/SKILL.md), [error analysis](skills/productivity/error-analysis-protocol/SKILL.md) |
| Build retention and independence | [Retrieval practice](skills/productivity/retrieval-practice-generator/SKILL.md), [spaced practice](skills/productivity/spaced-practice-scheduler/SKILL.md), [worked examples](skills/productivity/worked-example-fading-designer/SKILL.md), [hints](skills/productivity/progressive-hint-ladder/SKILL.md), [goals](skills/productivity/goal-setting-protocol-designer/SKILL.md) |
| Read, write and evaluate sources | [Comprehension](skills/productivity/reading-comprehension-strategy-selector/SKILL.md), [disciplinary writing](skills/productivity/disciplinary-writing-scaffold/SKILL.md), [source credibility](skills/productivity/source-credibility-evaluation-protocol/SKILL.md) |
| Teach early years and mixed ages | [Three-part lessons](skills/productivity/three-part-lesson-designer/SKILL.md), [mixed-age tasks](skills/productivity/mixed-age-learning-task-designer/SKILL.md), [prepared environment](skills/productivity/prepared-environment-designer/SKILL.md), [work cycles](skills/productivity/uninterrupted-work-cycle-designer/SKILL.md), [outdoor learning](skills/productivity/outdoor-learning-sequence-designer/SKILL.md), [crafts](skills/productivity/arts-crafts/SKILL.md) |
| Keep household learning records | [Lesson logs](skills/productivity/homeschool-lesson-log/SKILL.md), [time ledger](skills/productivity/homeschool-time-log/SKILL.md), [reading log](skills/productivity/homeschool-reading-log/SKILL.md), [weekly review](skills/productivity/homeschool-weekly-review/SKILL.md), [record queries](skills/productivity/homeschool-records-query/SKILL.md) |

The records workflows use the household’s existing private files or document tools.
They preserve hand edits, distinguish plans from completed work, and never infer missing
hours or grades. They do not certify legal compliance or provide jurisdiction-specific
filing, transcript-credit rules, diagnosis, automatic scheduling or financial accounting.
Those tasks require current primary sources and the family’s context. Existing
[pdf](skills/productivity/pdf/SKILL.md), [memento-flashcards](skills/productivity/memento-flashcards/SKILL.md)
and [youtube-transcript](skills/productivity/youtube-transcript/SKILL.md) can support suitable learning workflows.

The [research and security report](research/homeschool-skills-research.html),
[machine-readable intake](research/homeschool-skills-intake.json), and
[scan policy](research/homeschool-skill-scan-policy.yaml) record the searched sources,
selection decisions, pinned revisions, package hashes and exact security limits.
