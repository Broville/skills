# Intelligence Brief: External Skill Repositories Research

**Date**: 2025-07-31  
**Researcher**: Compass  
**Task**: t_abc7e40e

---

## Summary

Five external repositories were deep-dived to catalog available agent skills, identify overlaps, and recommend imports for the Broville skills library. The four direct repos contain 81 unique skills. The fifth (VoltAgent/awesome-agent-skills) is a curated index of 1,183+ skills from 193+ organizations — a discovery resource, not a direct skill source. Of the 81 direct skills, 1 overlaps with our existing library (pdf), and significant thematic overlaps exist between external repos and our current catalog. The highest-value imports are generalized software-dev methodology skills from addyosmani/agent-skills and select devops/security skills from hoodini/ai-agents-skills.

---

## Repository Catalog

### 1. anthropics/skills (17 skills)

**URL**: https://github.com/anthropics/skills  
**Focus**: Claude-specific productivity, document handling, and creative tools  
**Quality**: Official Anthropic skills; high quality, well-structured SKILL.md format  
**License**: Custom license (requires review — "Complete terms" referenced in several skills)

| Skill | Domain | Description | Overlap |
|-------|--------|-------------|---------|
| algorithmic-art | creative | p5.js generative art with seeded randomness | None |
| brand-guidelines | creative | Anthropic brand colors/typography | Vendor-specific |
| canvas-design | creative | Visual art in PNG/PDF formats | None |
| claude-api | software-dev | Claude API/SDK reference | Vendor-specific |
| doc-coauthoring | productivity | Collaborative document editing workflow | None |
| docx | productivity | Create/edit/analyze Word documents | None |
| frontend-design | creative | UI/UX design guidance | Thematic overlap with frontend-ui-engineering |
| internal-comms | productivity | Status reports, newsletters, FAQs | None |
| mcp-builder | software-dev | Create MCP servers for external APIs | None |
| pdf | productivity | PDF read/create/edit/forms | **OVERLAPS our pdf skill** |
| pptx | productivity | PowerPoint creation/editing | None |
| skill-creator | software-dev | Guide for creating new skills | Thematic overlap with our SOP |
| slack-gif-creator | creative | Animated GIFs for Slack | Niche |
| theme-factory | creative | Theme styling for artifacts | None |
| web-artifacts-builder | creative | React/Tailwind/shadcn HTML artifacts | None |
| webapp-testing | software-dev | Playwright-based web app testing | Overlaps our playwright skill |
| xlsx | productivity | Excel spreadsheet handling | None |

### 2. addyosmani/agent-skills (24 skills)

**URL**: https://github.com/addyosmani/agent-skills  
**Focus**: Software development methodology and workflow skills  
**Quality**: Excellent — well-structured, methodology-focused, agent-agnostic  
**License**: MIT  
**Notable**: Includes evals/, agents/, hooks/, and references/ directories beyond SKILL.md

| Skill | Domain | Description | Overlap |
|-------|--------|-------------|---------|
| api-and-interface-design | software-dev | Stable API/interface design | Thematic with our api-security-best-practices |
| browser-testing-with-devtools | software-dev | Chrome DevTools MCP testing | Complements our playwright |
| ci-cd-and-automation | devops | CI/CD pipeline setup | Thematic with our deployment-procedures |
| code-review-and-quality | software-dev | Multi-axis code review | **Strong overlap with our code-review-checklist** |
| code-simplification | software-dev | Refactoring for clarity | None |
| context-engineering | software-dev | Agent context optimization | None |
| debugging-and-error-recovery | software-dev | Systematic root-cause debugging | **Strong overlap with our systematic-debugging** |
| deprecation-and-migration | software-dev | Managing deprecation/migration | None |
| documentation-and-adrs | software-dev | ADRs and documentation | None |
| doubt-driven-development | software-dev | Adversarial review methodology | None |
| frontend-ui-engineering | software-dev | Production-quality UI development | Thematic with frontend-design |
| git-workflow-and-versioning | software-dev | Git workflow practices | **Overlap with our git-advanced-workflows** |
| idea-refine | productivity | Structured ideation/divergent-convergent | None |
| incremental-implementation | software-dev | Incremental delivery patterns | None |
| interview-me | productivity | Requirements extraction via interviewing | None |
| observability-and-instrumentation | devops | Logging/metrics/tracing/alerting | Thematic with our monitoring skills |
| performance-optimization | software-dev | Full-stack performance tuning | None |
| planning-and-task-breakdown | software-dev | Work decomposition | Thematic with our concise-planning |
| security-and-hardening | software-dev | Security vulnerability hardening | **Overlap with our security skills** |
| shipping-and-launch | software-dev | Production launch checklists | Thematic with our deployment-procedures |
| source-driven-development | software-dev | Implementation grounded in official docs | None |
| spec-driven-development | software-dev | Spec-first development | None |
| test-driven-development | software-dev | TDD methodology | None |
| using-agent-skills | software-dev | Meta-skill for skill discovery | None |

### 3. hoodini/ai-agents-skills (39 skills)

**URL**: https://github.com/hoodini/ai-agents-skills  
**Focus**: Broad mix — platform/vendor skills, creative tools, infrastructure  
**Quality**: Mixed — some skills are well-structured, others are niche/vendor-specific  
**License**: Varies per skill (many include external service dependencies)

| Skill | Domain | Description | Overlap |
|-------|--------|-------------|---------|
| analytics-metrics | data | Data visualization dashboards | None |
| aws-account-management | devops | AWS Organizations/IAM/billing | Vendor-specific |
| aws-harness | devops | AWS Bedrock AgentCore | Vendor-specific |
| aws-strands | mlops | AWS Strands Agents SDK | Vendor-specific |
| bun | software-dev | Bun JS runtime | Vendor-specific |
| cinematic-scrub-landing | creative | Cinematic scroll-scrub landing pages | Niche |
| cloudflare | devops | Cloudflare Workers/Pages/D1/R2 | **Overlap with our cloudflare-deploy** |
| copilot-docs | software-dev | GitHub Copilot instructions | Vendor-specific |
| copilot-sdk | software-dev | GitHub Copilot SDK | Vendor-specific |
| director | creative | AI video directing pipeline | Niche |
| fal-ai | creative | fal.ai serverless AI generation | Vendor-specific |
| figma | creative | Figma API design automation | Vendor-specific |
| github-trending | devops | GitHub trending dashboard | Niche |
| google-workspace-cli | productivity | Google Workspace CLI | Vendor-specific |
| honest-agent | software-dev | Anti-sycophancy for AI agents | Experimental |
| image-master | creative | AI image prompt engineering | None |
| langchain | mlops | LangChain/LangGraph orchestration | None |
| local-llm-router | mlops | Local LLM routing (Ollama, etc.) | None |
| mermaid-diagrams | software-dev | Mermaid diagram generation | None |
| meta-ads | marketing | Meta Ads Marketing API | Vendor-specific |
| mobile-responsiveness | software-dev | Responsive/mobile-first dev | None |
| mongodb | data | MongoDB patterns/aggregation | None |
| nano-banana-pro | creative | Gemini 3 image generation | Vendor-specific |
| owasp-security | security | OWASP Top 10 secure coding | **Overlap with our security skills** |
| parallax-landing-page | creative | Video-to-scroll landing page | Niche |
| railway | devops | Railway deployment | Vendor-specific |
| shabbat-times | productivity | Jewish calendar/Shabbat API | Very niche |
| ux-design-systems | software-dev | Design tokens/components/theming | None |
| vercel | devops | Vercel deployment | Vendor-specific |
| video-edit | creative | Video editing with captions | Niche |
| video-to-landing-page | creative | Video to landing page | Niche |
| web-accessibility | software-dev | WCAG accessibility patterns | None |
| x-twitter-scraper | research | X/Twitter data extraction | Niche |
| yuv-decks | creative | YUV.AI branded presentations | Brand-specific |
| yuv-design-system | creative | YUV.AI design system | Brand-specific |
| yuv-pilot | creative | YUV.AI orchestrator | Brand-specific |
| yuv-reel-covers | creative | YUV.AI Instagram covers | Brand-specific |
| yuv-video-director | creative | YUV.AI video pipeline | Brand-specific |
| yuv-viral-video | creative | YUV.AI viral video creation | Brand-specific |

### 4. vercel-labs/skills (1 skill)

**URL**: https://github.com/vercel-labs/skills  
**Focus**: Skill discovery meta-tool  
**Quality**: Single skill, well-structured

| Skill | Domain | Description | Overlap |
|-------|--------|-------------|---------|
| find-skills | software-dev | Discover and install agent skills | Meta-skill |

### 5. VoltAgent/awesome-agent-skills (1,183+ indexed entries)

**URL**: https://github.com/VoltAgent/awesome-agent-skills  
**Focus**: Curated index/directory of agent skills across the ecosystem  
**Nature**: This is NOT a skill repository. It is an "awesome list" that links to external skill repos  
**Notable entries by category**: Official skills from Anthropic, Stripe, Cloudflare, Netlify, Sentry, Expo, Hugging Face, Figma, Google, Trail of Bits, MongoDB, Apollo, Auth0, Redis, NVIDIA, and many more  
**Key categories in the index**:
- Testing (40+ test framework skills by TestMu AI)
- Security (Trail of Bits, OWASP, cybersecurity skills)
- Platform/Cloud (AWS, Cloudflare, Vercel, Netlify, Firebase)
- Frontend (Angular, React, SwiftUI, Flutter, design systems)
- DevOps/CI (GitHub Actions, deployment skills)
- Context Engineering (9 skills by muratcankoylan)
- Specialized domains (legal, health, finance, music, genealogy, etc.)
- LLM/Agent frameworks (VoltAgent, LangChain, MCP)

---

## Duplicate and Overlap Analysis

### Direct Overlaps with Our Repo

| Our Skill | External Equivalent | Source | Recommendation |
|-----------|-------------------|--------|----------------|
| pdf | pdf | anthropics/skills | Evaluate merging — Anthropic's may have richer features |
| playwright | webapp-testing | anthropics/skills | Complementary — both use Playwright |
| code-review-checklist | code-review-and-quality | addyosmani | **Merge candidate** — Addy's is more comprehensive |
| systematic-debugging | debugging-and-error-recovery | addyosmani | **Merge candidate** — Addy's covers similar ground |
| git-advanced-workflows | git-workflow-and-versioning | addyosmani | **Merge candidate** — overlapping scope |
| security-best-practices | security-and-hardening | addyosmani | Complementary — different angles |
| security-best-practices | owasp-security | hoodini | Complementary — OWASP-specific |
| api-security-best-practices | api-and-interface-design | addyosmani | Complementary — one is security, one is design |
| cloudflare-deploy | cloudflare | hoodini | **Overlapping** — ours is deployment-focused, theirs is broader |
| concise-planning | planning-and-task-breakdown | addyosmani | Complementary — ours is conciseness, theirs is decomposition |
| deployment-procedures | shipping-and-launch | addyosmani | Complementary — ours is procedures, theirs is launch |

### Cross-Repo Overlaps

| Skill Area | Repos Containing It | Assessment |
|------------|-------------------|------------|
| Frontend design | anthropics (frontend-design), addyosmani (frontend-ui-engineering), hoodini (ux-design-systems) | 3 repos — generalize and consolidate |
| Web testing | anthropics (webapp-testing), addyosmani (browser-testing-with-devtools) | Different angles — Playwright vs DevTools |
| Security | addyosmani (security-and-hardening), hoodini (owasp-security) | Complementary — general vs OWASP |
| Deployment/infra | hoodini (cloudflare, vercel, railway) | All vendor-specific, but useful as platform skills |
| Video/creative | hoodini (7 YUV.* + director + video-edit + parallax) | Mostly YUV.AI brand-specific — low value |

---

## Recommended Import Candidates

### HIGH PRIORITY — Generalized, Agent-Agnostic Skills (24)

These are methodology/workflow skills that apply to ANY agent and ANY project. They fill gaps in our library with high-quality, well-structured content.

1. **test-driven-development** (addyosmani) → `software-dev/` — TDD methodology
2. **spec-driven-development** (addyosmani) → `software-dev/` — Spec-first workflow
3. **source-driven-development** (addyosmani) → `software-dev/` — Docs-grounded coding
4. **debugging-and-error-recovery** (addyosmani) → `software-dev/` — Systematic debugging (merge with our systematic-debugging)
5. **code-review-and-quality** (addyosmani) → `software-dev/` — Multi-axis review (merge with our code-review-checklist)
6. **api-and-interface-design** (addyosmani) → `software-dev/` — Stable API design
7. **incremental-implementation** (addyosmani) → `software-dev/` — Incremental delivery
8. **documentation-and-adrs** (addyosmani) → `software-dev/` — ADRs and docs
9. **git-workflow-and-versioning** (addyosmani) → `software-dev/` — Git practices (merge with our git-advanced-workflows)
10. **deprecation-and-migration** (addyosmani) → `software-dev/` — Sunsetting patterns
11. **doubt-driven-development** (addyosmani) → `software-dev/` — Adversarial review
12. **frontend-ui-engineering** (addyosmani) → `software-dev/` — Production UI development
13. **shipping-and-launch** (addyosmani) → `software-dev/` — Launch checklists
14. **planning-and-task-breakdown** (addyosmani) → `software-dev/` — Work decomposition
15. **context-engineering** (addyosmani) → `software-dev/` — Agent context optimization
16. **code-simplification** (addyosmani) → `software-dev/` — Code clarity refactoring
17. **performance-optimization** (addyosmani) → `software-dev/` — Full-stack perf
18. **owasp-security** (hoodini) → `software-dev/` — OWASP Top 10 (complements our security skills)
19. **web-accessibility** (hoodini) → `software-dev/` — WCAG accessibility
20. **mermaid-diagrams** (hoodini) → `software-dev/` — Mermaid diagram generation
21. **mcp-builder** (anthropics) → `software-dev/` — MCP server creation
22. **idea-refine** (addyosmani) → `productivity/` — Structured ideation
23. **interview-me** (addyosmani) → `productivity/` — Requirements extraction
24. **mobile-responsiveness** (hoodini) → `software-dev/` — Responsive/mobile-first

### MEDIUM PRIORITY — Useful but More Specific (18)

1. **ci-cd-and-automation** (addyosmani) → `devops/`
2. **observability-and-instrumentation** (addyosmani) → `devops/`
3. **ux-design-systems** (hoodini) → `software-dev/`
4. **frontend-design** (anthropics) → `creative/`
5. **doc-coauthoring** (anthropics) → `productivity/`
6. **docx** (anthropics) → `productivity/`
7. **pptx** (anthropics) → `productivity/`
8. **xlsx** (anthropics) → `productivity/`
9. **internal-comms** (anthropics) → `productivity/`
10. **theme-factory** (anthropics) → `creative/`
11. **web-artifacts-builder** (anthropics) → `creative/`
12. **algorithmic-art** (anthropics) → `creative/`
13. **canvas-design** (anthropics) → `creative/`
14. **image-master** (hoodini) → `creative/`
15. **langchain** (hoodini) → `mlops/`
16. **local-llm-router** (hoodini) → `mlops/`
17. **mongodb** (hoodini) → `data/`
18. **analytics-metrics** (hoodini) → `data/`

### LOW PRIORITY — Vendor-Specific, Niche, or Brand-Specific (27)

All AWS, Vercel, Railway, Copilot, Bun, YUV.AI, and other vendor/brand-specific skills. These can be imported on-demand if a specific project needs them.

### Not Recommended for Import

- **claude-api** — Anthropic-specific API reference, not a generalized skill
- **brand-guidelines** — Anthropic-specific branding
- **slack-gif-creator** — Extremely niche
- **shabbat-times** — Very niche
- **All 7 YUV.* skills** — Brand-specific to YUV.AI
- **director, video-edit, video-to-landing-page, parallax-landing-page, cinematic-scrub-landing** — Niche video/landing page skills

---

## Awesome-Agent-Skills Index Analysis

The VoltAgent/awesome-agent-skills repository is a **curated directory**, not a skill source. Key findings:

- **1,183+ skills** from **193+ organizations/individuals**
- Includes official skills from: Anthropic, Google, Stripe, Cloudflare, Netlify, Sentry, Expo, Hugging Face, Figma, Trail of Bits, MongoDB, Apollo, Auth0, Redis, NVIDIA, DuckDB, WordPress, Microsoft, OpenAI, Binance, etc.
- Major skill clusters:
  - **Testing**: 40+ TestMu AI skills covering every major test framework
  - **Security**: Trail of Bits cybersecurity, OWASP, defense-in-depth
  - **Context Engineering**: 9 skills (context fundamentals, degradation, compression, optimization, multi-agent, memory, tool design, evaluation)
  - **Platform/Cloud**: AWS, Cloudflare, Vercel, Netlify, Firebase, Supabase
  - **Frontend**: Angular, React, SwiftUI, Flutter, design systems
  - **Specialized**: Legal, health, finance, music, genealogy, materials science, A-share trading, VMware, Solana, n8n automation

**Recommendation**: Use awesome-agent-skills as a **discovery index**. When we need a specific domain skill, search this index first. Don't bulk-import — the quality varies widely and many skills are vendor-specific.

---

## Risks and Unknowns

1. **License compatibility**: Anthropic's skills reference "Complete terms" — must review before import. Addyosmani is MIT. Hoodini varies. Awesome list entries link to external repos with their own licenses.
2. **Skill format differences**: Each repo uses slightly different SKILL.md frontmatter. Our repo requires specific fields (version, author, license, triggers). Imported skills must be adapted to our SKILL-SPEC.md format.
3. **Quality variance**: Addyosmani's skills are methodology-focused and well-structured. Hoodini's are a mixed bag. Anthropic's are polished but often Claude-specific. Awesome list entries are unvetted.
4. **Vendor lock-in**: Many skills tie to specific services (AWS, Vercel, Cloudflare, Meta, Google). These should be generalized or kept separate as platform-specific skills.
5. **Brand-specific content**: YUV.AI skills (7 in hoodini) and Anthropic brand-guidelines are brand-specific and not appropriate for general import.
6. **Merge complexity**: 5 skills in our repo have strong thematic overlap with external skills. Merging requires careful content comparison rather than simple replacement.

---

## Constraints

- Our repo uses 8 categories: devops, software-dev, mlops, data, research, creative, productivity, monitoring (+ finance, health from existing skills). New categories require an issue.
- SOP.md requires all skills to follow SKILL-SPEC.md format with specific frontmatter.
- No direct commits to main — all changes via branch and PR.
- Skills must be agent-agnostic and generalizable, not vendor-specific.

---

## Recommendations for Cartographer

1. **Phase 1 — High-priority methodology skills**: Import and adapt the 24 high-priority skills from addyosmani (20), hoodini (3), and anthropics (1). These fill clear gaps in our library with generalized, platform-agnostic content.
2. **Phase 2 — Merge overlapping skills**: Compare and merge the 5 overlapping skills (code-review, debugging, git, security, cloudflare) with our existing versions.
3. **Phase 3 — Medium-priority skills**: Evaluate and import the 18 medium-priority skills on a per-need basis.
4. **Phase 4 — On-demand from awesome index**: Use VoltAgent/awesome-agent-skills as a discovery index. When a specific domain skill is needed, evaluate and import individually.
5. **Skip low-priority**: Vendor-specific, brand-specific, and niche skills should not be imported unless a specific project requires them.
6. **Format adaptation**: All imports must be reformatted to match our SKILL-SPEC.md frontmatter (name, description, version, author, license, triggers, inputs, outputs).