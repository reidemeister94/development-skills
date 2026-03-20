---
name: align-docs
description: "Use when user wants to align docs with the current project status or new discoveries"
user-invocable: true
---
# Align Docs

Align all project documentation with the actual state on disk.

## CRITICAL: Always read before starting the docs alignment - Core Pillars

1. **Maximize simplicity, minimize complexity.** All else being equal, simpler is better. A small improvement that adds ugly complexity is not worth it. Removing something and getting equal or better results is a simplification win. Weigh complexity cost against improvement magnitude.
2. **All signal, zero noise.** everything must earn its place. If it doesn't add value, remove it. If there is duplication of information and documentation among the docs, remove it and link to the single source of truth.
3. **Make CLAUDE.md a cheat sheet, not a novel.** Favor tables, code snippets, and direct statements over prose. Only write things that are immediately actionable or universally relevant. Maximize information density, minimize text.

## Execution Checklist

Run every step. Do not skip any.

### Step 1: Inventory — diff docs against disk

Collect the actual state of the project by reading the filesystem. Compare against what each doc claims.

| Check | How |
|-------|-----|
| **Project structure** (CLAUDE.md) | `ls` root dirs/files → compare with the structure tree in CLAUDE.md |
| **Plugin version** (CLAUDE.md, MEMORY.md) | Read `.claude-plugin/plugin.json` → compare with documented version |
| **Skills** (README) | `ls skills/` → compare with the skills table in README.md |
| **Agents** (README) | `ls agents/` → compare with the agents table in README.md |
| **Shared files** (README) | `ls shared/` → verify documented architecture matches actual files |
| **Hooks** (README) | `ls hooks/` + read `hooks/hooks.json` → compare with hooks table in README.md |
| **Conventions & paths** (CLAUDE.md) | Verify every path/filename mentioned in CLAUDE.md actually exists |
| **Cross-references** | Check that links between docs (e.g., "see docs/README.md") point to files that exist |

### Step 2: Fix misalignments

For each mismatch found in Step 1, update the doc to match reality:

| Document | Purpose | What to check |
|----------|---------|---------------|
| **CLAUDE.md** | Project-wide knowledge loaded every conversation | Structure tree, version, paths, conventions |
| **MEMORY.md** | Cross-session memory | Plugin version, stable facts, testing iteration numbers |
| **README.md** | Public-facing docs | Skills table, agents table, hooks table, architecture description |
| **docs/chronicles/** | Narrative records | Only update if a chronicle references something now incorrect |

### Step 3: Remove noise

- Delete doc entries that reference things that no longer exist
- Deduplicate: if the same info appears in multiple places, keep it in one and link from the others
- Remove empty sections or placeholder content
