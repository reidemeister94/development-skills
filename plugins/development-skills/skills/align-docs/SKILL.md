---
name: align-docs
description: "Use when user wants to align docs with the current project status or new discoveries"
user-invocable: true
allowed-tools: Glob, Read, Edit, Write, Bash
---
# Align Docs

Align all project documentation with actual disk state.

## Core Pillars

1. **Maximize simplicity.** Small improvement + ugly complexity = not worth it.
2. **All signal, zero noise.** Deduplicate; link to single source of truth.
3. **CLAUDE.md = cheat sheet.** Tables, code snippets, direct statements. Maximize density.

## Execution Checklist

### Step 1: Inventory — diff docs against disk

| Check | How |
|-------|-----|
| **Project structure** (CLAUDE.md) | `ls` root → compare with structure tree |
| **Plugin versions** (CLAUDE.md, MEMORY.md) | Read each `plugins/*/.claude-plugin/plugin.json` |
| **Skills per plugin** (READMEs) | `ls plugins/*/skills/` → compare with skills table |
| **Agents per plugin** (READMEs) | `ls plugins/*/agents/` → compare with agents table |
| **Shared files** (READMEs) | `ls plugins/*/shared/` → verify architecture matches |
| **Conventions & paths** (CLAUDE.md) | Verify every path exists |
| **Cross-references** | Check doc links point to existing files |

### Step 2: Fix misalignments

| Document | Purpose | What to check |
|----------|---------|---------------|
| **CLAUDE.md** | Project-wide, loaded every conversation | Structure, versions, paths, conventions |
| **MEMORY.md** | Cross-session memory | Versions, stable facts, iteration numbers |
| **Plugin READMEs** | Plugin-specific docs | Skills, agents, architecture, quick start |
| **docs/chronicles/** | Narrative records | Only if referencing incorrect content |
| **Other docs/** | Domain docs | Only if stale |

### Step 3: Remove noise

- Delete entries referencing nonexistent things
- Deduplicate: keep in one place, link from others
- Remove empty sections or placeholders
