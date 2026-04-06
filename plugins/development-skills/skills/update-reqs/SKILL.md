---
name: update-reqs
description: "Use when user wants to update requirements.in or requirements-dev.in with latest PyPI versions while preserving version patterns. Handles both update-reqs and update-reqs-dev use cases."
user-invocable: true
---

# Update Requirements

Updates a `requirements*.in` file with latest package versions from PyPI while preserving version specifier patterns.

**Target file:** `$ARGUMENTS` if provided, otherwise `requirements.in`. Pass `requirements-dev.in` to update dev dependencies.

## How It Works

For each package in the target file:

1. **Parse the version pattern** to understand the "fixed part":
   - `fastapi==0.128.*` → fixed: `0.128`, wildcard at patch level
   - `commitizen==4.*` → fixed: `4`, wildcard at minor level
   - `pytest==8.*` → fixed: `8`, wildcard at minor level

2. **Query PyPI** for the latest version

3. **Update while preserving pattern**:
   - `fastapi==0.128.*` with latest `0.130.0` → `fastapi==0.130.*`
   - `commitizen==4.*` with latest `4.5.0` → `commitizen==4.*` (already allows 4.x)

## Execution Steps

1. Determine target file: use `$ARGUMENTS` if set, otherwise default to `requirements.in`
2. Read the target file from the current project
3. For each line with a package version:
   - Skip git dependencies (lines with `@` or `git+`)
   - Parse package name and version pattern
   - Fetch latest version from PyPI: `curl -s https://pypi.org/pypi/{package}/json | jq -r .info.version`
   - Calculate new version with same pattern depth
4. Show diff of proposed changes
5. Apply changes after user confirmation

## Version Pattern Rules

| Original | Latest on PyPI | Result |
|----------|----------------|--------|
| `pkg==1.2.*` | `1.5.3` | `pkg==1.5.*` |
| `pkg==1.*` | `2.3.0` | `pkg==2.*` |
| `pkg==1.2.3` | `1.5.3` | `pkg==1.5.3` |

## Skip These Lines

- Git dependencies: `pkg @ git+https://...`
- Comments: Lines starting with `#`
- Empty lines
- Extras without version: `pkg[extra]`

## Example Output

```
Checking requirements-dev.in for updates...

Package          Current    Latest     Status
pytest           8.*        8.4.0      OK (already matches)
ruff             0.*        0.9.2      OK (already matches)
commitizen       4.*        4.5.0      OK (already matches)

Apply updates? [y/N]
```
