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

## Single-Implementer Model — ONE implementer for ALL tasks

The main agent acts as a **thin orchestrator**. Spawn a **single** `implementer` subagent via the Task tool with ALL tasks from the checklist. The implementer reads the codebase once and implements all tasks sequentially in the same context — no redundant reads, no lossy context transfer between agents.

**Why one implementer:** Each task in a feature is connected. Spawning separate agents per task forces each to re-read the same research, patterns, and source files, and relies on lossy "prior task summaries" instead of direct memory. A single agent accumulates understanding naturally across tasks and the main context stays clean for follow-up questions.

The orchestrator curates a **single context package** for the implementer. The implementer's agent definition already contains stable rules (protocol, Red/Green TDD discipline, anti-poisoning checks, observation management, output format). The orchestrator passes ONLY dynamic, task-specific context:

1. **Full task checklist** — ALL tasks from the plan, numbered, with descriptions
2. **Plan context** — goals, constraints, architecture decisions (summarized, not the full plan)
3. **Plan file path** — the FULL path to the plan file. The implementer MUST update the checklist (mark `[x]` + affected files) after completing each task. This is the persistent progress tracker that survives context clearing.
4. **Research file path** — the FULL path to `docs/plans/NNNN__research.md` (from the plan's WORKFLOW STATE `Research:` field). The implementer MUST read this before coding — it contains web research findings, codebase analysis, alternatives evaluated, anti-patterns, and sources. Do NOT summarize or inline — pass the path so the implementer reads the original file.
5. **Patterns file path(s)** — the FULL path(s) to your language skill's `patterns.md` file(s). The implementer MUST read these before coding. Do NOT summarize or inline — pass the path(s) so the implementer reads the original file.
6. **Implementation rules** — the language-specific rules from your skill's "Implementation Rules" section (copy verbatim — these are short)
7. **Quality checklist** — the language-specific checklist items from your skill's "Quality Checklist" section
8. **Verification criteria** — command to run, expected outcome, what constitutes failure

**Task Checklist format** — the implementer updates the plan file after each task with affected files for artifact tracking:
```markdown
## Task Checklist
- [x] Task 1: [description]
  Files: src/file.py:15-42, tests/test_file.py (new)
- [x] Task 2: [description]
  Files: src/api/routes.py:88-95
- [ ] Task 3: [description]
```

## Execution Rules

- **One spawn:** Send ALL tasks to a single implementer. Do NOT spawn per-task agents.
- **Progress tracking on disk:** The implementer updates the plan file's checklist after each completed task (mark + affected files). If it fails mid-way, the main agent can see which tasks are done and which files were touched.
- **If implementer returns questions:** Answer them, then re-spawn (or resume) with the answers and the remaining unchecked tasks.
- **If implementer fails:** Read the failure details and the plan file checklist to see what completed. Fix the root cause, then spawn a new implementer for the remaining unchecked tasks (it will read the current file state from disk).
- **If implementer does not return** (timeout, crash, or context limit exhausted): Read the plan file's `## Task Checklist` to identify which tasks were marked `[x]`. The code on disk reflects all completed work. Spawn a new implementer with: remaining unchecked tasks + "Tasks 1-N are already implemented — do NOT re-implement them" + the same context package.
- **Recovery pattern:** On failure or timeout, the new implementer receives: remaining tasks + "Tasks 1-N are already implemented" + the current state of modified files. It does NOT need full re-context — the code on disk is the source of truth.

## After ALL Tasks Complete

1. **Verify the plan file was updated by the implementer** — Read the plan file and confirm:
   - `## Task Checklist` has all tasks marked `[x]` with affected files
   - `## Implementation Log` section exists with per-task reasoning (the implementer writes this)
   If the implementer did not write the Implementation Log, extract it from the implementer's return summary and append it to the plan file yourself.

2. **Update chronicle** with discoveries, unexpected challenges, and design decisions from the Implementation Log
3. **Update WORKFLOW STATE** in the plan file: set `Current Phase: 5 (Verification)`

**Gate:** State **"SOLUTION COMPLETE"**

## Expected Artifacts
- `## Task Checklist` in plan file with all tasks marked `[x]` + affected files
- `## Implementation Log` in plan file with per-task reasoning
- WORKFLOW STATE updated: `Current Phase: 5 (Verification)`
- Chronicle updated with discoveries (if chronicle exists)

**→ Run `/compact` now** — implementation is the heaviest phase and your context is likely bloated. Preserve: current phase (5), plan file path, research file path, chronicle path, language skill, verification commands. Then proceed to Phase 5. Read `phase-5-verify.md`.
