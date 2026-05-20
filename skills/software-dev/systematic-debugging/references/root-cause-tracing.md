# Root Cause Tracing

Bugs often manifest deep in the call stack. Your instinct is to fix where the error appears, but that's treating a symptom.

**Core principle:** Trace backward through the call chain until you find the original trigger, then fix at the source.

## The Tracing Process

### 1. Observe the Symptom
```
Error: git init failed in /Users/jesse/project/packages/core
```

### 2. Find Immediate Cause
What code directly causes this?
```python
await exec_file('git', ['init'], { cwd: project_dir })
```

### 3. Ask: What Called This?
Trace the call chain upward — who provided the bad value?

### 4. Keep Tracing Up
Where did the invalid value come from? Trace it to its origin.

### 5. Find Original Trigger
The source is where the invalid value was first introduced — that's where to fix.

## Adding Stack Traces

When you can't trace manually, add instrumentation:

```python
import traceback

def git_init(directory: str):
    print(f"DEBUG git init: directory={directory}, cwd={os.getcwd()}")
    print(f"Stack: {''.join(traceback.format_stack())}")
    # ... proceed
```

Run and capture output:
```bash
npm test 2>&1 | grep 'DEBUG git init'
# or
pytest -s 2>&1 | grep 'DEBUG'
```

## Key Principle

**NEVER fix just where the error appears.** Trace back to find the original trigger.

After fixing at the source, add validation at each layer the data passes through (see `defense-in-depth.md`).