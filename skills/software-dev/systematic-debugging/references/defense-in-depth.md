# Defense-in-Depth Validation

When you fix a bug caused by invalid data, adding validation at one place feels sufficient. But that single check can be bypassed by different code paths, refactoring, or mocks.

**Core principle:** Validate at EVERY layer data passes through. Make the bug structurally impossible.

## The Four Layers

### Layer 1: Entry Point Validation
Reject obviously invalid input at API boundary:
```python
def create_project(name: str, working_directory: str):
    if not working_directory or not working_directory.strip():
        raise ValueError("working_directory cannot be empty")
    if not os.path.exists(working_directory):
        raise ValueError(f"working_directory does not exist: {working_directory}")
    # ... proceed
```

### Layer 2: Business Logic Validation
Ensure data makes sense for this operation:
```python
def initialize_workspace(project_dir: str, session_id: str):
    if not project_dir:
        raise ValueError("project_dir required for workspace initialization")
    # ... proceed
```

### Layer 3: Environment Guards
Prevent dangerous operations in specific contexts:
```python
import os
from pathlib import Path

def git_init(directory: str):
    if os.environ.get("NODE_ENV") == "test":
        normalized = os.path.normpath(os.path.resolve(directory))
        tmp_dir = os.path.normpath(tempfile.gettempdir())
        if not normalized.startswith(tmp_dir):
            raise RuntimeError(f"Refusing git init outside temp dir during tests: {directory}")
    # ... proceed
```

### Layer 4: Debug Instrumentation
Capture context for forensics when other layers fail:
```python
import traceback

def git_init(directory: str):
    print(f"DEBUG git init: dir={directory}, cwd={os.getcwd()}")
    print(f"Stack: {''.join(traceback.format_stack())}")
    # ... proceed
```

## Applying the Pattern

1. Trace the data flow — where does the bad value originate? Where is it used?
2. Map all checkpoints — list every point data passes through
3. Add validation at each layer — entry, business, environment, debug
4. Test each layer — try to bypass layer 1, verify layer 2 catches it

All four layers are necessary. Different code paths, mocks, and edge cases can bypass any single layer.