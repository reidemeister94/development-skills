---
name: python-dev
description: "Python development. Use for Python, FastAPI, Pydantic, asyncpg, pytest, pandas, SQLAlchemy."
user-invocable: true
allowed-tools: Glob, Read, Grep, Bash, Task, Skill, Edit, Write, EnterPlanMode
---

# Python Development

**Announce:** "I'm using the python-dev skill. Following the mandatory 7-phase workflow."

## MANDATORY: Read and Follow the Shared Workflow

**You MUST read [workflow.md](../../shared/workflow.md) NOW** and follow ALL 7 phases defined there. The sections below provide Python-specific inputs for each phase.

Read [patterns.md](patterns.md) during Phase 1.

**If you lost workflow.md from context:** Re-read `../../shared/workflow.md` NOW before continuing.

---

## Python-Specific Configuration

### Verification Commands (Phase 2 + Phase 5)

WORKFLOW STATE Verification line: `pytest, ruff check, ruff format --check`

**Phase 5 Tier A commands:**
- `pytest` — run tests
- `ruff check` — linting
- `ruff format --check` — formatting
- Coverage target: 70-80%

**Phase 5 Tier B additional MCP verifications:**
- PostgreSQL MCP → Query DB state before/after

### Implementation Rules (Phase 4)

- **Model structure** — Pydantic CRUD variants per entity (Base/Create/Update/Read), domain-driven `schemas.py`, AppBaseModel with ConfigDict, composition over deep inheritance
- **Minimize complexity** — generators for large data, dict lookups over list scans
- **Preserve compatibility** — Aliases for renamed fields, defaults for new fields, preserve public signatures, re-export moved symbols

### Staff Review Configuration (Phase 6)

- **Patterns file path:** Path to this skill's `patterns.md`

---

## Anti-Rationalization (Python-Specific)

Add these to the shared workflow's anti-rationalization check:

| Your thought | Reality |
|---|---|
| "Python's duck typing means I don't need strict types" | Type hints are mandatory. The team uses Pydantic and strict typing per patterns.md. No exceptions. |
| "I'll add tests later" | Tests are required before Phase 5. Write them during implementation. |
| "The type checker will catch everything" | Type checkers catch type errors, not logic bugs, race conditions, or API contract violations. Verification and review are still mandatory. |

### Red Flags (Python-Specific)

- Expressing satisfaction before running `pytest`

---

## Quality Checklist (Python-Specific)

Add these to the shared workflow's verification checklist:

- [ ] Type hints use built-in types (not `typing.List`, `typing.Dict`)
- [ ] Pydantic for all structured data
- [ ] No global state or hidden dependencies
- [ ] DataFrames copied before mutation
- [ ] Python 3.13+ features where appropriate
- [ ] `ruff check` passes
- [ ] `ruff format` applied
- [ ] `pytest` passes (or alternative verification documented)
