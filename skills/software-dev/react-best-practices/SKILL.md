---
name: "react-best-practices"
description: "Apply impact-ranked React and Next.js performance rules when writing, reviewing, or optimizing applications."
license: "MIT"
compatibility: "Open Agent Skills format for Codex, Claude Code, Gemini CLI, Cursor, OpenCode, GitHub Copilot, and compatible hosts. Runtime tools are listed in Prerequisites."
metadata:
  author: "Broville"
  version: "2.0.0"
  platforms: "[\"linux\",\"macos\",\"windows\"]"
  triggers: "[\"User asks to write, review, or optimize React or Next.js code\",\"React code has waterfalls, bundle growth, slow rendering, or excessive rerenders\",\"A React or Next.js performance change needs prioritized, source-backed guidance\"]"
  inputs: "[{\"name\":\"target\",\"description\":\"Repository, route, component, or change set to inspect\",\"required\":true},{\"name\":\"observed_problem\",\"description\":\"Measured symptom, failing budget, or user-visible performance concern\",\"required\":false}]"
  outputs: "[{\"name\":\"prioritized_findings\",\"description\":\"Evidence-backed findings ordered by expected impact\"},{\"name\":\"verified_changes\",\"description\":\"Implemented improvements with before-and-after evidence when fixes are requested\"}]"
  tags: "[\"react\",\"nextjs\",\"performance\",\"bundles\",\"rendering\"]"
  related-skills: "[\"performance-optimization\",\"react-composition-patterns\",\"frontend-ui-engineering\",\"verification-before-completion\"]"
  source: "vercel-labs/agent-skills@063bee94c3f4df8453406c830b0a7df0f2860278 (MIT)"
  source-url: "https://github.com/vercel-labs/agent-skills/tree/063bee94c3f4df8453406c830b0a7df0f2860278/skills/react-best-practices"
---

# React Best Practices

## Description

Apply Vercel Engineering's 70 impact-ranked rules to React and Next.js implementation, review, and optimization. Use this skill for framework-specific decisions; use `performance-optimization` for cross-stack diagnosis and keep repository conventions authoritative.

## Prerequisites

- A React or Next.js repository with its lockfile and project instructions available.
- The repository's existing build, test, lint, profiling, and bundle-analysis commands.
- A reproducible symptom or baseline before changing code for performance-only work.

## Steps

1. Confirm the target actually uses React or Next.js and record the installed versions.

   ```bash
   node -e "const p=require('./package.json'); console.log({react:p.dependencies?.react||p.devDependencies?.react,next:p.dependencies?.next||p.devDependencies?.next})"
   ```

   Expected result: the relevant declared versions are printed. Resolve workspace manifests or lockfile versions when the root manifest is not authoritative.

2. Read repository instructions and establish the narrowest evidence that represents the reported problem: request timing, bundle output, React Profiler trace, rerender count, Core Web Vital, or a focused test. Do not start with low-impact micro-optimizations when no problem is observed.

3. Select only the applicable files under `references/rules/`, starting with the highest-impact category that matches the evidence:

   ```bash
   rg --files "<skill-dir>/references/rules" | sort
   ```

   Expected result: 70 vendored rule files across `async-`, `bundle-`, `server-`, `client-`, `rerender-`, `rendering-`, `js-`, and `advanced-` prefixes. Read the individual rule before applying it.

4. Review in impact order:

   1. eliminate avoidable request and component waterfalls;
   2. reduce shipped or traced bundle size;
   3. correct server work, caching, serialization, and request isolation;
   4. deduplicate client fetching and global work;
   5. remove measured rerender and rendering costs;
   6. consider JavaScript or advanced patterns only when profiling supports them.

5. Implement the smallest project-consistent change. Preserve correctness, caching semantics, authentication boundaries, hydration behavior, and supported React/Next.js versions. Treat each rule's examples as patterns to adapt, not code to paste blindly.

6. Re-run the exact baseline from step 2 and compare like-for-like conditions. If the result is noisy or unchanged, report that honestly and revert speculative complexity unless it has an independently justified correctness benefit.

7. Run the repository's focused tests, required full suite, build, and:

   ```bash
   git diff --check
   ```

   Expected result: behavior remains correct, required checks pass, and any claimed performance improvement has fresh measurement evidence.

## Pitfalls

- **Framework drift:** Do not apply Next.js-only APIs to other React frameworks or unsupported Next.js versions.
- **React-version drift:** Rules mentioning React 19 APIs apply only after the installed version and framework support are confirmed.
- **Cargo-cult memoization:** `memo`, `useMemo`, and `useCallback` add complexity and can be neutral or harmful without a measured rerender cost.
- **Cache correctness:** Cross-request caches can leak data or serve stale authorization-sensitive results. Preserve request and tenant boundaries.
- **Synthetic-only wins:** A local microbenchmark is not proof of a field improvement; distinguish lab, profiler, and real-user evidence.
- **Rule overreach:** User requirements, repository architecture, and correctness constraints override a generic optimization rule.

## Verification

1. The installed framework versions and affected execution boundary are recorded.
2. Every finding cites the applicable vendored rule and observed code or runtime evidence.
3. Fixes preserve behavior and pass focused plus repository-required checks.
4. Performance claims include the same metric, workload, environment, and before/after values.
5. No React 19, Next.js, caching, or server-component assumption was applied without version and context confirmation.

## Cross-References

- `performance-optimization` — cross-stack measurement and bottleneck analysis.
- `react-composition-patterns` — scalable component APIs and state ownership.
- `frontend-ui-engineering` — framework-agnostic UI implementation.
- `verification-before-completion` — fresh evidence before completion claims.
- `references/rules/` — 70 pinned Vercel rule files; read only the applicable files.
- `references/PROVENANCE.md` — source pin and adaptation notes.
- `references/UPSTREAM-LICENSE.txt` — upstream MIT license.
