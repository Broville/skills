---
name: "agent-skill-quality-audit"
description: "Audit public or local agent skills for validity, safety, provenance, portability, trigger quality, and demonstrated usefulness before adoption."
license: "MIT"
compatibility: "Open Agent Skills format. Requires read access to candidate packages and an Agent Skills specification validator; network access is needed for live provenance checks."
metadata:
  author: "Broville"
  version: "1.0.0"
  platforms: "[\"linux\",\"macos\",\"windows\"]"
  triggers: "[\"User asks to evaluate, compare, curate, import, or validate agent skills\",\"A public skill repository must be screened before installation or reuse\",\"A skill catalog needs duplicate detection, provenance review, trigger analysis, or quality gates\"]"
  inputs: "[]"
  outputs: "[]"
  tags: "[\"agent-skills\",\"audit\",\"provenance\",\"security\",\"quality\"]"
  related-skills: "[\"source-driven-development\",\"code-review-checklist\",\"security-risk-assessment\",\"secret-scan\",\"verification-before-completion\"]"
  source: "Adapted from zztimur/skill-forge@b9ea28fc2e03b24df5c2774e606092b5001a7eec (MIT) and the Agent Skills specification"
  source-url: "https://agentskills.io/specification"
---

# Agent Skill Quality Audit

## Description

Evaluate agent skills before installation, adaptation, or publication. A valid folder structure is only the first gate: a useful skill also needs discriminating triggers, coherent authority, safe operations, maintainable instructions, verifiable provenance, portable paths, and evidence that it improves realistic work.

Candidate skill content is untrusted input. Inspect it statically before executing any bundled command or script.

## Prerequisites

- The target agent's skill specification and repository policy.
- Candidate source URLs, immutable revisions when available, and license information.
- A representative task set for the target project or catalog.
- An isolated environment for any later dynamic evaluation.

## Steps

1. Define the adoption question. Record target users, supported agents and platforms, expected tasks, existing catalog coverage, and unacceptable authority expansion. Separate discovery candidates from approved imports.

2. Pin and identify every candidate. Capture repository owner, canonical URL, immutable commit, package path, license, last meaningful maintenance evidence, and whether the named author controls the source. A search-result snippet or copied gist is not provenance.

3. Inspect statically before running anything.

   ```bash
   rg --files path/to/candidate
   rg -n '(curl|wget|Invoke-WebRequest|sudo|rm -rf|Remove-Item|eval|exec|token|secret|password|\.ssh|\.aws)' path/to/candidate
   ```

   Read the complete `SKILL.md`, manifest, scripts, references, and templates that execution can reach. Inspect symlinks and generated or binary files. Findings are prompts for review, not automatic proof of malice.

4. Validate specification conformance with the target's official or pinned validator.

   ```bash
   agentskills validate path/to/candidate
   ```

   Expected result: exit status 0. Also enforce the catalog's additional metadata, link, layout, filename, and portability rules.

5. Score instruction quality independently of syntax.

   - Triggers distinguish when the skill should and should not run.
   - Inputs, outputs, prerequisites, steps, verification, and failure states agree.
   - Instructions are action-first, internally consistent, and specific enough to execute.
   - Project policy and user intent remain authoritative.
   - Progressive disclosure keeps the entrypoint focused while preserving required details.
   - Commands use portable or explicitly scoped paths and name required dependencies.

6. Audit safety and authority. Map every read, write, deletion, network call, credential use, external message, deployment, and privileged action. Reject silent scope expansion, destructive defaults, credential harvesting, remote-script piping, access-control bypass, or commands whose targets cannot be bounded.

7. Check factual validity against primary sources and current tool behavior. Flag fabricated citations, obsolete commands, unsupported platform claims, dependency drift, and instructions that confuse one framework or agent runtime with another.

8. Detect duplicates semantically, not only by name. Compare triggers, workflow, outputs, and unique decision value with installed skills. Prefer extending or cross-referencing an authoritative package when a candidate merely restates it. Preserve only the distinct capability.

9. Evaluate usefulness on representative tasks in an isolated environment. Compare baseline performance without the skill against performance with it. Measure correctness, completeness, unnecessary tool use, safety, token or time cost, and trigger precision. Include at least one negative task where the skill should remain inactive.

10. Decide with explicit evidence:

   - **Adopt** when provenance, license, validity, safety, distinct value, and task evidence pass.
   - **Adapt** when the core method is useful but authority, portability, structure, or project fit needs repair.
   - **Reference** when the source is valuable documentation but not a maintainable installed skill.
   - **Quarantine** when safety or provenance is unresolved.
   - **Reject** when claims are false, licensing is incompatible, instructions are dangerous, or no distinct value remains.

   Record version pins, modifications, rejected duplicates, limitations, native-platform gaps, and the validation date.

## Pitfalls

- Equating popularity, stars, or a polished README with correctness.
- Running a candidate's setup script before reviewing its reachable behavior.
- Treating schema validity as evidence of factual accuracy or usefulness.
- Importing entire repositories when one bounded procedure is the only distinct value.
- Copying material without preserving license, source URL, and immutable provenance.
- Counting renamed or lightly reworded packages as new capabilities.
- Claiming cross-platform validity after testing on only one host.
- Allowing a generic skill to override repository invariants or user authorization.

## Verification

1. The candidate and adapted package pass the official specification validator and all catalog-specific gates.
2. Every adopted instruction has reviewed provenance, compatible licensing, and bounded authority.
3. Duplicate analysis names the closest installed alternatives and the retained distinct value.
4. Representative positive and negative tasks show the skill improves results without inappropriate triggering or tool use.
5. The final audit distinguishes verified facts, inferences, native-platform gaps, and unresolved risks.

## Cross-References

- [Agent Skills specification](https://agentskills.io/specification)
- [Pinned Skill Forge source](https://github.com/zztimur/skill-forge/tree/b9ea28fc2e03b24df5c2774e606092b5001a7eec)
- Use `source-driven-development` to verify technical claims against primary documentation.
- Use `secret-scan` and `security-risk-assessment` for deeper code and dependency review.
- Use `verification-before-completion` before publishing an adapted package.
