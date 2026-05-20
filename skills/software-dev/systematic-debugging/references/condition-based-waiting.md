# Condition-Based Waiting

Flaky tests often guess at timing with arbitrary delays. This creates race conditions where tests pass on fast machines but fail under load or in CI.

**Core principle:** Wait for the actual condition you care about, not a guess about how long it takes.

## When to Use

- Tests have arbitrary delays (`setTimeout`, `sleep`, `time.sleep()`)
- Tests are flaky (pass sometimes, fail under load)
- Tests timeout when run in parallel
- Waiting for async operations to complete

**Don't use when:** Testing actual timing behavior (debounce, throttle intervals).

## Quick Patterns

| Scenario | Pattern |
|----------|---------|
| Wait for event | `waitFor(() => events.find(e => e.type === 'DONE'))` |
| Wait for state | `waitFor(() => machine.state === 'ready')` |
| Wait for count | `waitFor(() => items.length >= 5)` |
| Wait for file | `waitFor(() => fs.existsSync(path))` |

## Generic Implementation

```python
import time

def wait_for(condition, description, timeout_ms=5000, poll_ms=10):
    """Poll until condition is truthy or timeout."""
    start = time.time()
    while True:
        result = condition()
        if result:
            return result
        if (time.time() - start) * 1000 > timeout_ms:
            raise TimeoutError(f"Timeout waiting for {description} after {timeout_ms}ms")
        time.sleep(poll_ms / 1000)
```

```javascript
async function waitFor(condition, description, timeoutMs = 5000) {
  const start = Date.now();
  while (true) {
    const result = condition();
    if (result) return result;
    if (Date.now() - start > timeoutMs) {
      throw new Error(`Timeout waiting for ${description} after ${timeoutMs}ms`);
    }
    await new Promise(r => setTimeout(r, 10)); // Poll every 10ms
  }
}
```

## Common Mistakes

- **Polling too fast** (`setTimeout(check, 1)`) — wastes CPU. Fix: Poll every 10ms
- **No timeout** — Loop forever if condition never met. Fix: Always include timeout with clear error
- **Stale data** — Cache state before loop. Fix: Call getter inside loop for fresh data