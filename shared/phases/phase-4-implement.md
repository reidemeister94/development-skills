# Phase 4: SOLUTION — GATE

**Cannot start without user-approved plan.** No approval? Go back to Phase 2.

## STOP — Update Plan Document BEFORE Implementation

**Before spawning any implementer:**

1. **Update WORKFLOW STATE:** `Current Phase: 4 (Implementation)`, remove completed phases
2. **Add `## Task Checklist`:**
   ```markdown
   ## Task Checklist
   - [ ] Task 1: [description from plan]
   - [ ] Task 2: [description from plan]
   ```
3. **Verify** — Read plan file back to confirm both updates persisted

**Do NOT spawn any implementer until plan file has both WORKFLOW STATE and Task Checklist.**

---

## Task Dependency Analysis

### Step 1: Build File-Touch Map

For each task, identify ALL files it will create or modify. Consider transitive dependencies (moving a function touches every file importing it).

```markdown
## File-Touch Map
- Task 1: src/api/routes.py, tests/test_routes.py
- Task 2: src/models/user.py, tests/test_user.py
- Task 3: src/api/routes.py, src/api/middleware.py
```

### Step 2: Find Orthogonal Groups

Tasks sharing ANY file are **connected**. Find connected components:

```
Group A: Task 1, Task 3  (share src/api/routes.py)
Group B: Task 2, Task 5  (share src/models/user.py)
Group C: Task 4          (no overlap)
→ 3 orthogonal groups → max 3 agents
```

**When in doubt about overlap, group together.** False negatives cause merge conflicts; false positives just reduce parallelism.

### Step 3: Choose Strategy

| Condition | Strategy |
|-----------|----------|
| 1 group (all share files) | **Single agent, no worktree** |
| N groups, clean git | **N parallel agents in worktrees** |
| N groups, dirty git | Ask user: WIP commit → parallel, or single |
| 3 or fewer tasks | **Single agent, no worktree** |

---

## Single-Agent Mode (DEFAULT)

Spawn **one** `implementer` via Agent tool with ALL tasks. **No worktree** — works in current directory.

**Why no worktree by default:** Worktrees branch from HEAD, which may lack uncommitted plan/research files from Phases 1-3. In field testing, stale worktrees caused 100% unusable output.

**If fails:** `git checkout -- .` or `git stash` to clean up.

---

## Parallel-Agent Mode

**Only when:** 2+ orthogonal groups AND 4+ tasks AND pre-flight passes.

### Pre-Flight (MANDATORY)

```bash
git status --porcelain
```

**If dirty:** Report to user. Options: (a) WIP commit then parallel, (b) fall back to single.
**If clean:** Proceed.

### Spawn N Agents

One `implementer` per group. Pass `isolation: "worktree"`. Spawn ALL in a single message.

### After Completion

1. Check all results
2. Merge each worktree branch sequentially: `git merge <branch> --no-edit`
3. If merge conflict: STOP — file analysis missed overlap
4. Clean up worktrees
5. Consolidate plan file — verify all checklists and logs present
6. Run full test suite on merged result

---

## Context Package (all strategies)

Pass ONLY dynamic context to implementer:

1. **Task checklist** — tasks for THIS agent
2. **Plan context** — goals, constraints, architecture (summarized)
3. **Plan file path** — **ABSOLUTE**
4. **Research file path** — **ABSOLUTE** (from WORKFLOW STATE). Do NOT summarize — pass the path.
5. **Patterns file path(s)** — **ABSOLUTE**. Do NOT summarize — pass the path(s).
6. **Implementation rules** — language-specific (copy verbatim)
7. **Quality checklist** — language-specific items
8. **Verification criteria** — command, expected outcome, failure definition
9. **Isolation info** — "Running in [main directory / isolated worktree]. Use absolute paths."

## Observation Masking

**Keep verbose outputs off the main conversation:**
- Implementer writes reasoning to `## Implementation Log` on disk
- Summary tells what completed and what needs attention
- Full details always on disk — read plan file when needed
- Do NOT ask implementer to paste full test output in return message

## Execution Rules

- **Progress on disk:** Implementer marks checklist after each task. If it fails mid-way, you see what's done.
- **Questions returned:** Answer, then re-spawn with answers + remaining tasks.
- **Failure:** Read plan file checklist for completed tasks. Fix root cause, spawn new implementer for remaining.
- **Timeout/context exhausted:** Read `## Task Checklist` for `[x]` tasks. Spawn new implementer with remaining + "Tasks 1-N already done."

## After ALL Tasks Complete

1. **Verify plan file:** All tasks `[x]` with files, `## Implementation Log` exists
2. **Parallel mode:** Verify merges succeeded, worktrees cleaned
3. **Update chronicle** with discoveries from Implementation Log
4. **Update WORKFLOW STATE:** `Current Phase: 5 (Verification)`

**Gate:** State **"SOLUTION COMPLETE"**

## Expected Artifacts
- `## File-Touch Map` (if grouping performed)
- `## Task Checklist` with all `[x]` + affected files
- `## Implementation Log` with per-task reasoning
- WORKFLOW STATE: `Current Phase: 5 (Verification)`
- Chronicle updated with discoveries

**→ Run `/compact` now** — implementation is the heaviest phase. Then proceed to Phase 5.
