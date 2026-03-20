# Phase 4: SOLUTION — GATE

**Cannot start without user-approved plan.** If you haven't received explicit approval, go back to Phase 2.

## STOP — Update Plan Document BEFORE Any Implementation

**Before spawning any implementer subagent, you MUST complete these steps first:**

1. **Update WORKFLOW STATE** in the plan file: set `Current Phase: 4 (Implementation)`, remove completed phases from `Phases remaining`
2. **Add `## Task Checklist`** section to the plan file with a numbered checklist derived from the plan's tasks:
   ```markdown
   ## Task Checklist
   - [ ] Task 1: [description from plan]
   - [ ] Task 2: [description from plan]
   ...
   ```
3. **Verify** — Read the plan file back to confirm both the WORKFLOW STATE update and the Task Checklist are persisted

**Do NOT spawn any implementer until the plan file has both the updated WORKFLOW STATE and the Task Checklist.** These survive context clearing and are the single source of truth for workflow progress.

---

## Task Dependency Analysis — BEFORE Choosing Execution Strategy

**Analyze file overlap to determine whether tasks can run in parallel.**

### Step 1: Build File-Touch Map

For each task in the checklist, identify ALL files it will create or modify:
- Read task descriptions in the plan (often list specific files/modules)
- Quick `Grep`/`Glob` to confirm file paths exist
- Consider transitive dependencies: if Task A moves a function, it also touches every file that imports that function

Write the map to the plan file:
```markdown
## File-Touch Map
- Task 1: src/api/routes.py, tests/test_routes.py
- Task 2: src/models/user.py, tests/test_user.py
- Task 3: src/api/routes.py, src/api/middleware.py
- Task 4: src/db/migrations/001.py
- Task 5: src/models/user.py, src/models/profile.py
```

### Step 2: Find Orthogonal Groups

Two tasks are **connected** if they share ANY file (even one). Find connected components:

```
Group A: Task 1, Task 3  (share src/api/routes.py)
Group B: Task 2, Task 5  (share src/models/user.py)
Group C: Task 4          (no shared files with any other task)
→ 3 orthogonal groups → max 3 agents
```

**Conservative rule:** When in doubt about whether two tasks share files, put them in the same group. False negatives (missing an overlap) cause merge conflicts. False positives (grouping too aggressively) just reduce parallelism — a safe tradeoff.

### Step 3: Choose Execution Strategy

| Condition | Strategy |
|-----------|----------|
| 1 group (all tasks share files) | **Single agent, no worktree** |
| N orthogonal groups, clean git state | **N parallel agents, each in worktree** |
| N orthogonal groups, dirty git state | Ask user: WIP commit → parallel, or fallback to single |
| 3 or fewer tasks total | **Single agent, no worktree** (parallelism overhead not worth it) |

---

## Single-Agent Mode (DEFAULT)

**Used when:** all tasks in one group, 3 or fewer tasks, or pre-flight check fails.

Spawn **one** `implementer` subagent via the Agent tool with ALL tasks. **No worktree isolation** — the agent works directly in the current working directory.

**Why no worktree by default:** Worktrees branch from HEAD, which may be behind the working directory state (uncommitted plan files, research files from Phases 1-3, or locally committed changes that haven't been pushed). A stale worktree means agents work on outdated code — in field testing, this caused 100% of implementer output to be unusable. Working directly in the main directory ensures the agent always sees the latest state.

**If implementation fails:** Use `git checkout -- .` or `git stash` to clean up.

The orchestrator curates a **single context package** for the implementer (see Context Package below).

---

## Parallel-Agent Mode

**Used ONLY when:** 2+ orthogonal groups identified AND 4+ tasks total AND pre-flight check passes.

### Pre-Flight Check (MANDATORY)

```bash
git status --porcelain
```

**If dirty (uncommitted changes exist):**
1. Report to user: "There are uncommitted changes. Parallel mode requires a clean working directory so worktrees start from the correct state."
2. Present options:
   - (a) Create a WIP commit to capture current state, then proceed with parallel
   - (b) Fall back to single-agent mode (no worktree)
3. If (a): `git add -A && git commit -m "wip: pre-implementation checkpoint"` — note this commit for squashing later
4. If (b): Use Single-Agent Mode

**If clean:** Proceed.

### Spawn N Agents

For each orthogonal group, spawn one `implementer` subagent:
- Pass `isolation: "worktree"` explicitly in the Agent tool call
- Pass ONLY that group's tasks (not all tasks)
- Each agent gets the full context package but a different task subset
- Spawn ALL agents **in a single message** (parallel execution)

```
Agent 1 (Group A): Tasks 1, 3 → isolation: "worktree"
Agent 2 (Group B): Tasks 2, 5 → isolation: "worktree"
Agent 3 (Group C): Task 4     → isolation: "worktree"
```

### After Parallel Agents Complete

1. **Check all agent results** — Did every agent complete successfully?
2. **Merge each worktree branch** sequentially into the current branch:
   ```bash
   git merge <worktree-branch-1> --no-edit
   git merge <worktree-branch-2> --no-edit
   ```
3. **If any merge conflict:** STOP. The file-touch analysis missed an overlap. Resolve manually or fall back to single-agent for remaining work.
4. **Clean up worktrees** after successful merges
5. **Consolidate the plan file** — Each agent updated the plan file (via absolute path). Verify all task checklists and implementation logs are present.
6. **Run full test suite** on the merged result to verify integration

---

## Context Package (applies to ALL strategies)

The implementer's agent definition contains stable rules (TDD discipline, anti-poisoning, observation management, verification honesty). The orchestrator passes ONLY dynamic, task-specific context:

1. **Task checklist** — the tasks assigned to THIS agent (numbered, with descriptions)
2. **Plan context** — goals, constraints, architecture decisions (summarized, not the full plan)
3. **Plan file path** — **ABSOLUTE** path to the plan file. Always use absolute paths regardless of isolation mode, so updates are visible to the orchestrator.
4. **Research file path** — **ABSOLUTE** path to `docs/plans/NNNN__research.md` (from WORKFLOW STATE `Research:` field). The implementer MUST read this. Do NOT summarize — pass the path.
5. **Patterns file path(s)** — **ABSOLUTE** path(s) to the language skill's `patterns.md`. Do NOT summarize — pass the path(s).
6. **Implementation rules** — language-specific rules from your skill (copy verbatim — short)
7. **Quality checklist** — language-specific items from your skill
8. **Verification criteria** — command to run, expected outcome, what constitutes failure
9. **Isolation info** — "You are running in [the main working directory / an isolated worktree]. Use absolute paths for all plan file operations."

**Task Checklist format** — the implementer updates the plan file after each task:
```markdown
## Task Checklist
- [x] Task 1: [description]
  Files: src/file.py:15-42, tests/test_file.py (new)
- [x] Task 2: [description]
  Files: src/api/routes.py:88-95
- [ ] Task 3: [description]
```

## Observation Masking

**Tool outputs consume 80%+ of tokens in agent trajectories.** Keep verbose outputs off the main conversation:
- The implementer writes all reasoning to the plan file's `## Implementation Log` (on disk, not in conversation)
- When the implementer returns, its summary tells you what completed and what needs attention. **The full details are always on disk in the plan file** — read it whenever you need specifics.
- Do NOT ask the implementer to paste full test output or file contents in its return message

## Execution Rules

- **Progress tracking on disk:** The implementer updates the plan file's checklist after each completed task (mark + affected files). If it fails mid-way, the main agent can see which tasks are done.
- **If implementer returns questions:** Answer them, then re-spawn with the answers and the remaining unchecked tasks.
- **If implementer fails:** Read the failure details and the plan file checklist to see what completed. Fix the root cause, then spawn a new implementer for the remaining unchecked tasks.
- **If implementer does not return** (timeout or context exhausted): Read the plan file's `## Task Checklist` to identify which tasks were marked `[x]`. Spawn a new implementer with: remaining unchecked tasks + "Tasks 1-N are already implemented — do NOT re-implement them" + the same context package.

## After ALL Tasks Complete

1. **Verify the plan file was updated** — Read the plan file and confirm:
   - `## Task Checklist` has all tasks marked `[x]` with affected files
   - `## Implementation Log` section exists with per-task reasoning
   If the implementer did not write the Implementation Log, extract it from the return summary and append it yourself.
2. **If parallel mode:** verify all merges succeeded and worktrees are cleaned up
3. **Update chronicle** with discoveries, unexpected challenges, and design decisions from the Implementation Log
4. **Update WORKFLOW STATE** in the plan file: set `Current Phase: 5 (Verification)`

**Gate:** State **"SOLUTION COMPLETE"**

## Expected Artifacts
- `## File-Touch Map` in plan file (if task grouping was performed)
- `## Task Checklist` in plan file with all tasks marked `[x]` + affected files
- `## Implementation Log` in plan file with per-task reasoning
- WORKFLOW STATE updated: `Current Phase: 5 (Verification)`
- Chronicle updated with discoveries (if chronicle exists)

**→ Run `/compact` now** — implementation is the heaviest phase and your context is likely bloated. Preserve: current phase (5), plan file path, research file path, chronicle path, language skill, verification commands. Then proceed to Phase 5. Read `phase-5-verify.md`.
