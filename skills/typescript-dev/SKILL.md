---
name: typescript-dev
description: "TypeScript development. Use for TypeScript, Node.js, Express, Fastify, Zod, vitest, jest. Backend, CLI, libraries only — no frontend frameworks."
user-invocable: true
allowed-tools: Glob, Read, Grep, Bash, Task, Skill, Edit, Write, EnterPlanMode
---

# TypeScript Development

**Announce:** "I'm using the typescript-dev skill. Following the mandatory 7-phase workflow."

## MANDATORY: Read and Follow the Shared Workflow

**You MUST read [workflow.md](../../shared/workflow.md) NOW** and follow ALL 7 phases defined there. The sections below provide TypeScript-specific inputs for each phase.

Read [patterns.md](patterns.md) during Phase 1.

**If you lost workflow.md from context:** Re-read `../../shared/workflow.md` NOW before continuing.

---

## TypeScript-Specific Configuration

### Verification Commands (Phase 2 + Phase 5)

WORKFLOW STATE Verification line: `tsc --noEmit, eslint, vitest/jest`

**Phase 5 Tier A commands:**
- `tsc --noEmit` — type checking
- `eslint` — linting
- `vitest` or `jest` — tests
- Coverage target: 70-80%

**Phase 5 Tier B additional MCP verifications:**
- PostgreSQL MCP → Query DB state before/after

### Implementation Rules (Phase 4)

- **Schema structure** — Zod CRUD variants per entity (CreateInput/UpdateInput/Output), domain-driven `schemas.ts`, types derived via `z.infer`, composition over deep extends chains
- **Minimize complexity** — Map/Set lookups over array scans
- **Preserve compatibility** — `.transform()` for renamed fields, `.default()` for new fields, preserve exported signatures, re-export moved symbols

### Staff Review Configuration (Phase 6)

- **Patterns file path:** Path to this skill's `patterns.md`

---

## TypeScript-Specific Rules

- Types are erased at runtime — external data needs Zod validation
- Fix type errors during implementation, not after
- No positive claim without running `tsc --noEmit`

---

## Quality Checklist (TypeScript-Specific)

Add these to the shared workflow's verification checklist:

- [ ] Using TypeScript 5.x+ features where appropriate
- [ ] `strict: true` enabled in tsconfig.json
- [ ] No `any` types (or explicitly justified)
- [ ] Proper type guards for runtime checks
- [ ] Zod or similar for external data validation
- [ ] ESM imports with proper extensions
- [ ] `tsc --noEmit` passes (no type errors)
- [ ] `eslint` passes
- [ ] Tests pass (`vitest`/`jest`)
