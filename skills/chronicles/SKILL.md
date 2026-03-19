---
name: chronicles
description: "Use when starting a new development task to capture context, or when finalizing a task to document discoveries and decisions."
---

# Chronicles

**Announce:** "I'm using the chronicles skill to capture task context."

## Chronicle Philosophy

A chronicle is a **project snapshot** -- it captures what happened at a specific moment in a project's life. Months later, a developer or model should be able to read a chronicle and understand:

- **What the user wanted** -- the full context of what was communicated, not a summary
- **Why decisions were made** -- business context, technical trade-offs, rejected alternatives
- **What was discovered** -- unexpected findings, gotchas, patterns identified
- **What changed** -- references to key code areas (not low-level diffs)
- **What state the project was in** -- before and after the work

Chronicles sit ABOVE code and plan documents in the abstraction hierarchy:

```
Code + Git = WHAT changed (low-level diffs, line-by-line)
Plan docs  = HOW it was implemented (tasks, approaches, file-level changes)
Chronicles = WHY it happened, WHAT the user communicated, PROJECT STATE (high-level)
```

**Capture everything the user communicated.** Do not filter or summarize the user's words during creation. Condense for readability during finalization, but preserve ALL intent and reasoning.

---

## Usage

### Within Development Workflow (Phase 3)

Read `shared/phases/phase-3-chronicle.md` for the full template, lifecycle, and creation instructions. That file is the authoritative source.

### Standalone Invocation

When invoked directly (outside the workflow):
1. Follow the same template from `shared/phases/phase-3-chronicle.md`
2. Create the chronicle file in `docs/chronicles/`
3. No workflow gates apply -- just create and fill the chronicle

---

## When Chronicle is NOT Needed

ALL of these must apply:
- Single-line or trivial fix (typo, obvious bug, string change)
- No new patterns or architectural decisions
- Change is self-evident from the code diff
- No business context worth preserving

If skipping, state: **"CHRONICLE: NOT NEEDED -- [brief reason]"**

---

## When Used with Brainstorming

1. Create chronicle to capture the exploration
2. Document different approaches considered and WHY each was accepted/rejected
3. If implementation follows, the chronicle becomes the foundation

---

## Principles

- **Capture the WHY** -- Code shows what changed, chronicles explain why
- **Capture the user's voice** -- What the user communicated is the most valuable signal
- **Higher level than code** -- Reference key areas, don't paste diffs
- **Project snapshot** -- A reader months later should understand the moment in time
- **Condense, don't lose** -- Summarize conversations for readability but preserve all intent
- **Reference, don't repeat** -- Point to code locations, don't paste code
- **Evolve continuously** -- Update as you learn, don't wait until the end
- **Promote insights** -- Valuable discoveries belong in CLAUDE.md for future sessions
