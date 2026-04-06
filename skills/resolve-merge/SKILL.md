---
name: resolve-merge
description: "Use when the user asks to resolve merge conflicts, fix a failed merge, rebase conflict, or run /resolve-merge. Use when git status shows UU/AA/DD conflicts, when there are <<<<<<< conflict markers, when git merge or git pull failed with CONFLICT, or when numbered docs/plans need renumbering after merge. Triggers on: merge conflict, conflict markers, both modified, git merge failed, rebase conflict, resolve conflicts."
user-invocable: true
allowed-tools: Glob, Grep, Read, Bash, Edit, Write
---

# Resolve Merge Conflicts

**Announce:** "I'm using the resolve-merge skill. Systematic merge conflict resolution."

## Prerequisites

Verify merge state:

```bash
git rev-parse MERGE_HEAD
```

If not in a merge, STOP with: "No merge in progress."

---

## Phase 1: Assess Conflict Landscape

### 1a: Categorize all conflicts

Run `git status --short` and group files by conflict type:

| Code | Meaning | Strategy |
|------|---------|----------|
| DD | Both deleted | `git rm` — accept deletion |
| AU | Added by us (HEAD) | Evaluate: duplicate or unique? |
| UA | Added by them (MERGE_HEAD) | Evaluate: duplicate or unique? |
| UU | Both modified | Manual content resolution |
| DU | Deleted by us, modified by them | Accept theirs (`git checkout --theirs` + `git add`) |
| UD | Modified by us, deleted by them | Accept deletion (`git rm`) |
| AA | Both added same path | Content resolution needed |
| R | Renamed | Usually auto-resolved |

### 1b: Separate docs from code

Split conflicts into two groups:

- **Numbered docs:** files in `docs/plans/` and `docs/chronicles/` (renumbering conflicts)
- **Code files:** everything else (source files, config, lock files)

Display a summary table:

```
=== Merge Conflict Summary ===
Merging: [MERGE_HEAD branch] → [HEAD branch]
Total conflicts: N

Numbered docs: N (plans: N, chronicles: N)
Code files: N

By type: DD=N, AU=N, UA=N, UU=N, DU=N, UD=N, AA=N
```

---

## Phase 2: Resolve Numbered Docs (plans + chronicles)

**Skip this phase if no numbered doc conflicts exist.**

This handles projects using numbered doc files:

- Plans: `docs/plans/NNNN__YYYY-MM-DD__implementation_plan__slug.md` + `docs/plans/NNNN__research.md`
- Chronicles: `docs/chronicles/NNNN__YYYY-MM-DD__slug.md`

Both branches may have independently renumbered these files, causing conflicts.

### 2a: Build file inventories

```bash
git ls-tree -r --name-only HEAD -- docs/plans/ docs/chronicles/ | sort
git ls-tree -r --name-only MERGE_HEAD -- docs/plans/ docs/chronicles/ | sort
```

### 2b: Extract slugs and find unique files

Extract the slug from each file. Compare slug sets between OURS and THEIRS to find:

- **Shared slugs** (same content, different numbers)
- **OURS-only slugs** (files unique to HEAD)
- **THEIRS-only slugs** (files unique to MERGE_HEAD)

### 2c: Choose the base numbering

Compare OURS vs THEIRS numbering for quality:

- Count duplicate numbers (two different slugs at the same number)
- Count gaps in the sequence
- The side with **fewer duplicates and fewer gaps** is the cleaner numbering

Default heuristic: **prefer THEIRS** (the branch being merged in) — typically renumbered more recently, reduces diff surface.

Display the choice and ask for confirmation:

```
Numbering analysis:
  OURS: N plans, M chronicles (X duplicates, Y gaps)
  THEIRS: N plans, M chronicles (X duplicates, Y gaps)

Recommended base: THEIRS
OURS-only files to add: [list slugs]
THEIRS-only files to add: [list slugs]

Proceed? [y/n]
```

### 2d: Execute the resolution

Process conflicts in order:

1. **DD files** → `git rm`
2. **UA files** (theirs added) → `git checkout --theirs` + `git add`
3. **AU files** (ours added) → if slug exists in THEIRS at different number → `git rm` (duplicate); if OURS-unique → `git add`
4. **DU files** → `git checkout --theirs` + `git add`
5. **UD files** → `git rm`
6. **UU files** in docs → `git checkout --theirs` + `git add`
7. **AA files** in docs → `git checkout --theirs` + `git add`

### 2e: Place OURS-unique files

For each OURS-only slug, check for number collisions with THEIRS files. If collision, rename to next available number. If not, keep as-is.

Verify: no gaps, no duplicate numbers.

---

## Phase 3: Fix Internal References

After renumbering, internal cross-references will be stale.

### 3a: Fix research references in plan files

Each plan should reference its **own** number's research file (e.g., plan 0015 → `0015__research.md`). Handle all reference formats:

- `NNNN__research.md`
- `NNNN**research.md` (bold markdown)
- `NNNN\_\_research.md` (escaped underscores)

### 3b: Fix chronicle self-references

Each chronicle has a self-reference line like `> Chronicle: NNNN__...`. Verify the number matches the filename.

### 3c: Fix cross-plan and cross-chronicle references

Some plans reference other plans or chronicles by number. Verify each referenced file exists. If not, find the correct file by slug and update.

### 3d: Check for leftover conflict markers

```bash
grep -rn '<<<<<<< \|=======\|>>>>>>> ' docs/plans/ docs/chronicles/
```

Resolve any found by picking the correct side.

### 3e: Stage all doc fixes

```bash
git add docs/plans/ docs/chronicles/
```

---

## Phase 4: Resolve Code File Conflicts

Handle each UU/AA code file individually.

### Common patterns

**CHANGELOG.md** — Combine unique entries from both sides, remove duplicates, keep sorted by category.

**Lock files** (package-lock.json, poetry.lock, etc.) — Do NOT manually merge. Accept one side, regenerate:

```bash
# Example for npm:
git checkout --ours package-lock.json && npm install
# If ERESOLVE: git checkout --theirs package-lock.json && npm install
```

**Source files** — Read each conflicted file and resolve based on context:

- Import order conflicts: pick either side (formatter will sort)
- Logic conflicts: understand both changes and merge semantically
- If both sides changed the same code differently: analyze intent and combine

### Stage all code fixes

```bash
git add [resolved files]
```

---

## Phase 5: Verify

### 5a: No unresolved conflicts

```bash
git status --short | grep -E "^(UU|DD|AU|UA|DU|UD|AA)"
```

Must return empty.

### 5b: No conflict markers in tracked files

```bash
grep -rn '<<<<<<< \|=======\|>>>>>>> ' . --include="*.md" --include="*.ts" --include="*.tsx" --include="*.py" --include="*.json" --include="*.java" --include="*.swift" | grep -v node_modules | grep -v '.next' | grep -v __pycache__
```

### 5c: Numbering integrity (if docs were resolved)

Verify plans and chronicles have sequential numbers with no gaps and no duplicates.

### 5d: Reference integrity (if docs were resolved)

Verify all research refs point to own number, chronicle self-refs match filename, cross-references are valid.

### 5e: Project build/lint check

Run the project's standard verification commands if known (e.g., type checker, linter).

### 5f: Display final summary

```
=== Merge Resolution Complete ===
Conflicts resolved: N
  Docs renumbered: N plans, M chronicles
  Code files merged: N
  Internal references fixed: N
  OURS-unique files preserved: [list]
  THEIRS-unique files preserved: [list]

Numbering: plans 0001-NNNN, chronicles 0001-NNNN (no gaps)
Build: [PASS/FAIL/SKIPPED]

Ready to commit. Use /commit or `git commit` to finalize the merge.
```

---

## Edge Cases

- **No numbered doc conflicts:** Skip Phase 2 and 3, go straight to Phase 4.
- **No code conflicts:** Skip Phase 4.
- **Only one side renumbered:** Use that side's numbering directly.
- **Conflicting unique files at same number:** Shift the later-dated file to next available number.
- **Research file missing for a plan:** Note in summary, don't create one.
- **Lock file regeneration fails:** Report the error and let the user decide.
