---
name: playwright
description: Automate browser interactions with native tools first, using the standalone Playwright CLI skill as a fallback.
version: 1.1.0
author: Broville
license: MIT
platforms:
  - linux
  - macos
  - windows
trigger:
  - User asks to automate browser interactions or web flows
  - User asks to test a web application flow end-to-end
  - User asks to fill forms programmatically or extract data from web pages
  - User asks to capture screenshots of web pages
  - User mentions browser automation, browser testing, or UI flow debugging
inputs:
  - name: url
    description: Starting URL for browser navigation
    required: true
  - name: action
    description: Browser action to perform (navigate, click, type, fill, screenshot, snapshot)
    required: true
outputs:
  - name: page_state
    description: Current page state (DOM snapshot, accessibility tree, or screenshot)
  - name: extracted_data
    description: Data extracted from the page
metadata:
  hermes:
    tags:
      - browser
      - automation
      - testing
      - playwright
      - web
    related_skills:
      - screenshot
      - playwright-cli
---

# Playwright

## Description

Automate browser interactions for testing web flows, filling forms, extracting data, and capturing page state. This skill supports two approaches:

1. **Native Browser Tools (Primary)** — Use `browser_navigate`, `browser_click`, `browser_snapshot`, `browser_vision`, and similar tools when available in the agent's environment. These provide direct browser control without external dependencies.

2. **Playwright CLI (Fallback)** — Load the standalone `playwright-cli` skill when native browser tools are unavailable or the user explicitly requests the CLI. It pins the executable version and owns CLI-specific safety, command, session, tracing, and test-debugging guidance.

Always prefer native browser tools when they are available. Fall back to the Playwright CLI only when needed.

## Prerequisites

### Path 1: Native Browser Tools (Primary)

Check if native browser tools are available in your environment:

- `browser_navigate` — Navigate to a URL
- `browser_click` — Click an element
- `browser_snapshot` — Capture accessibility tree or DOM snapshot
- `browser_vision` — Capture a visual screenshot
- Additional tools: `browser_type`, `browser_fill`, `browser_scroll`, etc.

If these tools are available, no additional setup is required. Proceed to the native flow.

### Path 2: Playwright CLI (Fallback)

Load the related `playwright-cli` skill and follow its prerequisites and pinned invocation. Verify Node.js/npm availability first:

```bash
command -v npx >/dev/null 2>&1 && echo "npx available" || echo "npx not found"

# If missing, install Node.js first:
node --version
npm --version

# Verify the pinned CLI without a global installation:
npx --yes @playwright/cli@0.1.19 --version
```

Expected result: `0.1.19`. Do not use the former wrapper path; this skill has no bundled CLI script.

## Steps

### Path 1: Native Browser Tools

#### 1. Navigate to the starting page

Use the `browser_navigate` tool with the target URL.

#### 2. Capture page state

Use `browser_snapshot` to get the accessibility tree or DOM structure. This provides stable element identifiers for interaction.

#### 3. Interact with elements

Use `browser_click` to click buttons, links, or other interactive elements. Use `browser_type` or `browser_fill` to enter text into form fields.

#### 4. Re-snapshot after navigation

After any action that changes the page significantly (navigation, form submission, modal open/close, tab switch), capture a new snapshot. Element identifiers can become stale after DOM changes.

#### 5. Verify results

Use `browser_snapshot` or `browser_vision` to confirm the expected state of the page after interactions.

### Path 2: Playwright CLI

#### 1. Load the CLI-specific workflow

Read and follow `playwright-cli`. The examples below use its pinned v0.1.19 invocation.

#### 2. Open the page

```bash
npx --yes @playwright/cli@0.1.19 open https://example.com
```

#### 3. Snapshot to get element references

```bash
npx --yes @playwright/cli@0.1.19 snapshot
```

#### 4. Interact using element refs from the snapshot

```bash
npx --yes @playwright/cli@0.1.19 click e3
npx --yes @playwright/cli@0.1.19 fill e1 "user@example.com"
npx --yes @playwright/cli@0.1.19 fill e2 "test-password"
npx --yes @playwright/cli@0.1.19 click e5
```

#### 5. Re-snapshot after significant changes

```bash
npx --yes @playwright/cli@0.1.19 snapshot
```

Refs become stale after navigation or DOM changes. Always re-snapshot after such events.

#### 6. Capture artifacts (optional)

```bash
npx --yes @playwright/cli@0.1.19 screenshot
npx --yes @playwright/cli@0.1.19 tracing-start
# ...interactions...
npx --yes @playwright/cli@0.1.19 tracing-stop
```

### Common Patterns

#### Form fill and submit

**Native:**
1. Navigate to form URL
2. Snapshot the page
3. Fill each form field using `browser_fill`
4. Click the submit button using `browser_click`
5. Snapshot the result page

**CLI:**
```bash
npx --yes @playwright/cli@0.1.19 open https://example.com/form
npx --yes @playwright/cli@0.1.19 snapshot
npx --yes @playwright/cli@0.1.19 fill e1 "user@example.com"
npx --yes @playwright/cli@0.1.19 fill e2 "test-password"
npx --yes @playwright/cli@0.1.19 click e3
npx --yes @playwright/cli@0.1.19 snapshot
```

#### Multi-page workflow

1. Navigate to the starting page
2. Snapshot and interact
3. After navigation or page transition, re-snapshot
4. Continue interactions on the new page
5. Repeat for each step in the flow

#### Debugging with screenshots

Use `browser_vision` (native) or the pinned `playwright-cli screenshot` workflow to capture visual state when text-based snapshots are insufficient for understanding page layout.

## Pitfalls

- **Stale element references**: Element IDs (like `e3` in CLI mode) become invalid after any DOM change. Always re-snapshot after navigation, clicks that change the UI, modal open/close, or tab switches. When a ref fails, snapshot again immediately.
- **Headless mode limitations**: Some pages render differently in headless mode. Use `--headed` flag with CLI or visual mode with native tools when visual verification is needed. Screenshots may reveal rendering issues that snapshots don't show.
- **Dynamic content timing**: Pages with dynamic content may need a moment to render after navigation. If a snapshot shows incomplete content, wait briefly and re-snapshot.
- **Authentication state**: Browser sessions may not persist authentication between separate invocations of CLI commands. Plan flows to include login steps when needed, or use the same browser session throughout.

## Verification

1. **Tool availability check**:
   ```bash
   # For CLI path: verify the pinned playwright-cli version
   npx --yes @playwright/cli@0.1.19 --version
   # Expected: 0.1.19
   ```

2. **Basic navigation works**:
   ```bash
   # CLI path
   npx --yes @playwright/cli@0.1.19 open https://example.com
   npx --yes @playwright/cli@0.1.19 snapshot
   # Expected: page content displayed with element references
   ```

3. **Interaction produces expected result**:
   For any form fill or click action, snapshot the page afterward and confirm the expected state change occurred.

4. **Screenshot capture works**:
   ```bash
   npx --yes @playwright/cli@0.1.19 screenshot
   # Expected: screenshot file created or displayed
   ```

## Cross-References

- **screenshot** (`monitoring/screenshot`) — For desktop-level screenshot capture (not browser-specific)
- **playwright-cli** (`software-dev/playwright-cli`) — Pinned CLI commands, sessions, traces, test debugging, and safety boundaries
- CLI command reference: `references/cli.md`
- Workflow patterns and troubleshooting: `references/workflows.md`
