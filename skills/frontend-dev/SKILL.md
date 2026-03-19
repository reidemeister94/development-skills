---
name: frontend-dev
description: "Frontend development. Use for React, Next.js, Raycast extensions, Vite-based frontend projects."
user-invocable: true
allowed-tools: Glob, Read, Grep, Bash, Task, Skill, Edit, Write, EnterPlanMode
---

# Frontend Development

**Announce:** "I'm using the frontend-dev skill. Following the mandatory 7-phase workflow."

---

## PRE-STEP: FRAMEWORK DETECTION — GATE

**Before starting the workflow, you MUST detect the frontend framework.** Do NOT skip this step. Do NOT assume a framework without checking.

### Step 1: Check configuration files and package.json dependencies

Examine the project root for config files and `package.json` dependencies. Match the **first row** that applies.

**ALWAYS read [patterns/typescript.md](patterns/typescript.md) as a base** — it applies to every frontend framework.

| Signal | Framework | Pattern Files to Read (+ typescript.md) |
|--------|-----------|----------------------------------------|
| `next.config.*` or `app/layout.tsx` exists | **Next.js** | [patterns/react.md](patterns/react.md) + [patterns/nextjs.md](patterns/nextjs.md) |
| `@raycast/api` in deps | **Raycast** | [patterns/react.md](patterns/react.md) + [environments/raycast.md](environments/raycast.md) |
| `vite.config.*` + `react` in deps | **React + Vite** | [patterns/react.md](patterns/react.md) + [environments/vite.md](environments/vite.md) |
| `*.tsx`/`*.jsx` + `react` in deps | **React** | [patterns/react.md](patterns/react.md) |
| `vue` in deps or `vite.config.*` + `vue` | **Vue** | [patterns/typescript.md](patterns/typescript.md) (no Vue-specific patterns yet) |
| `svelte` in deps or `svelte.config.*` | **Svelte** | [patterns/typescript.md](patterns/typescript.md) (no Svelte-specific patterns yet) |
| `@angular/core` in deps | **Angular** | [patterns/typescript.md](patterns/typescript.md) (no Angular-specific patterns yet) |

> **Note:** Frameworks without dedicated pattern files use general TypeScript patterns. Consider creating `patterns/[framework].md` for team-specific standards.

### Step 2: State detection result

**State:** "Detected framework: **[Framework Name]**. Reading pattern files: [list of files]."

If no framework matches, ask: "I couldn't auto-detect your frontend framework. Which are you using?"

**Gate:** Framework detected and pattern files identified. **Only after detection**, proceed to the workflow.

---

## MANDATORY: Read and Follow the Shared Workflow

**You MUST read [workflow.md](../../shared/workflow.md) NOW** and follow ALL 7 phases defined there. The sections below provide frontend-specific inputs for each phase.

**Phase 1:** Read [patterns/typescript.md](patterns/typescript.md) FIRST (always), then ALL framework-specific pattern files identified in Framework Detection.

**If you lost workflow.md from context:** Re-read `../../shared/workflow.md` NOW before continuing.

---

## Frontend-Specific Configuration

### Verification Commands (Phase 2 + Phase 5)

WORKFLOW STATE Verification line: `npm run build, npm run lint, npm test`

**Phase 5 Tier A commands** — use the commands appropriate for the detected framework:

| Framework | Type Check | Build | Lint | Test |
|-----------|-----------|-------|------|------|
| Next.js | (included in build) | `npm run build` | `npm run lint` | `vitest`/`jest` |
| React + Vite | `tsc --noEmit` | `vite build` | `eslint` | `vitest` |
| Raycast | `ray build` | (included) | `eslint` | — |

### Implementation Rules (Phase 4)

- **Schema structure** — Zod CRUD variants per entity (CreateInput/UpdateInput/Output), domain-driven `schemas.ts`, types derived via `z.infer`, composition over deep extends chains
- **Minimize complexity** — Map/Set lookups over array scans, avoid unnecessary re-renders
- **Preserve compatibility** — `.transform()` for renamed fields, `.default()` for new fields, preserve exported signatures and component props

### Staff Review Configuration (Phase 6)

- **Detected framework:** The framework detected in the pre-step
- **Patterns file paths:** Paths to `patterns/typescript.md` AND the framework-specific pattern file(s)

---

## Anti-Rationalization (Frontend-Specific)

Add these to the shared workflow's anti-rationalization check:

| Your thought | Reality |
|---|---|
| "I know this is a React project, I don't need to read the pattern files" | The pattern files contain TEAM-SPECIFIC standards, not general knowledge. Read them. |
| "Framework detection is obvious, I'll skip it" | Detection MUST be explicit and stated. Wrong detection = wrong patterns = wrong code. |
| "I'll use the same verification commands for all frameworks" | Each framework has specific build/type-check commands. Check the table. |
| "This framework isn't in the detection table, I'll just wing it" | If the framework isn't listed, ASK the user. Do not guess. |
| "The pattern file for this framework doesn't exist yet, so I'll skip it" | State that the pattern file is missing and use general TypeScript + component best practices. Suggest creating the pattern file. |

### Red Flags (Frontend-Specific)

- Starting Phase 1 without completing Framework Detection
- Reading only one pattern file when the detection table says to read two
- Hardcoding Next.js patterns (Server Components, App Router) for a non-Next.js React project
- Using `useEffect` for data fetching in a Next.js project (should use Server Components)
- Using "use client" everywhere in a Next.js project

---

## Quality Checklist (Frontend-Specific)

Add these to the shared workflow's verification checklist:

- [ ] Framework detected and stated
- [ ] `typescript.md` read (always)
- [ ] Framework-specific pattern files read
- [ ] TypeScript strict mode, no `any` types
- [ ] Framework-specific standards from pattern files followed
