# Playwright Workflows and Troubleshooting

## Common Workflows

### Login Flow

1. Open the login page
2. Snapshot to get form element refs
3. Fill username and password fields
4. Click the submit button
5. Snapshot to verify redirect to dashboard
6. If redirected back to login, check for error messages

### Data Extraction

1. Navigate to the target page
2. Snapshot to identify the data elements
3. Extract text content using element refs
4. If pagination exists, navigate to next page and repeat
5. Write extracted data to a structured file (JSON, CSV)

### Step-by-Step Testing

1. Open the starting page of the flow
2. Snapshot to verify initial state
3. Perform each step of the user flow
4. Snapshot after each step to verify expected changes
5. On failure, capture a screenshot for debugging

## Troubleshooting

### Element ref is stale

This happens when the DOM changes between snapshot and interaction. Always re-snapshot after navigation, form submissions, or dynamic content changes.

### Page loads slowly

Some pages need time for JavaScript rendering. If a snapshot shows incomplete content, wait and re-snapshot. The CLI handles basic wait-for-network-idle, but custom timing may be needed.

### Authentication not persisting

Browser sessions may not persist auth between separate CLI invocations. Plan flows to include login steps, or use the same session throughout a multi-step workflow.

### Headless rendering differences

Some pages render differently without a display. Use `--headed` flag when visual verification is important. Screenshots may reveal rendering issues that text snapshots don't show.

### Timeout on interaction

Increase timeout if the CLI times out waiting for an element. This is common with slow networks or heavy JavaScript pages. Try snapshotting first to verify the element exists.