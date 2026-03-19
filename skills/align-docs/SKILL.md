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
| **Plugin list + versions** (CLAUDE.md, MEMORY.md) | Read each `plugins/*/.claude-plugin/plugin.json` → compare with documented versions |
| **Skills per plugin** (plugin READMEs) | `ls plugins/*/skills/` → compare with the skills table in each `plugins/*/README.md` |
| **Agents per plugin** (plugin READMEs) | `ls plugins/*/agents/` → compare with the agents table in each `plugins/*/README.md` |
| **Shared files** (plugin READMEs) | `ls plugins/*/shared/` → verify any documented architecture matches actual files |
| **Conventions & paths** (CLAUDE.md) | Verify every path/filename mentioned in CLAUDE.md actually exists |
| **Cross-references** | Check that links between docs (e.g., "see docs/README.md") point to files that exist |

### Step 2: Fix misalignments

For each mismatch found in Step 1, update the doc to match reality:

| Document | Purpose | What to check |
|----------|---------|---------------|
| **CLAUDE.md** | Project-wide knowledge loaded every conversation | Structure tree, plugin versions, paths, conventions, references to external files |
| **MEMORY.md** | Cross-session memory | Plugin versions, stable facts, testing iteration numbers |
| **Plugin READMEs** | Plugin-specific docs | Skills table, agents table, architecture description, quick start commands |
| **docs/chronicles/** | Narrative records | Only update if a chronicle references something now incorrect |
| **Other docs/** | Domain documentation | Only update if content is stale |

### Step 3: Remove noise

- Delete doc entries that reference things that no longer exist
- Deduplicate: if the same info appears in multiple places, keep it in one and link from the others
- Remove empty sections or placeholder content
