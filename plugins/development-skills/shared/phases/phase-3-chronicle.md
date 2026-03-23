# Phase 3: CHRONICLE CREATION — GATE

**When in doubt, create the chronicle.** The cost is ~30 seconds. The cost of a missing chronicle is losing the WHY behind a decision forever.

**Chronicle IS NEEDED when ANY of these apply:**
- New feature or endpoint added
- Architectural change or new patterns
- Complex bug fix requiring investigation
- Breaking change or API modification
- Multi-file refactoring with design decisions
- Business logic changes where WHY isn't obvious
- Significant research or discovery involved

**Chronicle is NOT NEEDED when ALL of these apply:**
- Single-line or trivial fix (typo, obvious bug, string change)
- No new patterns or architectural decisions
- Change is self-evident from the code diff
- No business context worth preserving

**Anti-rationalization:**

| Your thought | Reality |
|---|---|
| "Chronicle is just busywork" | Chronicles are the only record of WHY decisions were made. Code shows WHAT, plans show HOW. Without a chronicle, the WHY is lost in 3 months. |

---

## If Chronicle IS Needed

**Announce:** "Creating chronicle to capture task context."

### Create the Chronicle File

1. Run `mkdir -p docs/chronicles/` using Bash
2. Find next number: `ls docs/chronicles/*.md 2>/dev/null | sort | tail -1` — increment by 1 (start at 0001 if none exist)
3. Write file using the template below
4. Fill in: User Requirements (complete user communication), Context (condensed from research), Objective (the WHY), Project State (before), Affected Areas

**Naming:** `docs/chronicles/NNNN__YYYY-MM-DD__brief-description.md`

### Chronicle Template

```markdown
# [Brief Title]

> Chronicle: NNNN__YYYY-MM-DD__brief-description.md
> Status: Draft | In Progress | Completed

## User Requirements (Complete)

[Capture FULL user communication — requirements, constraints, preferences, context.
Preserve ALL signal. Condense for readability during finalization but never lose meaning.]

## Context

[Background from research. Project state, relevant technical context.]

**Key references:**
- `path/to/module/` - [why involved]

## Project State

**Before:** [State before this work]
**After:** [Updated during finalization]

## Objective (The WHY)

[WHY this change, not WHAT. Business context, user needs, problems.]

## Affected Areas

| Area | Files/Modules | Impact |
|------|---------------|--------|
| [Component] | `path/` | [High-level change] |

## Discoveries & Insights

[Updated throughout the task.]

- **[Date]**: [Discovery or insight]

---

## CLAUDE.md Updates

### Updates to apply:

- [ ] `CLAUDE.md` - [What to add/update]
```

### Chronicle Lifecycle

- **During Implementation (Phase 4):** Update Discoveries & Insights, record design decisions, unexpected challenges
- **During Finalization (Phase 7):** Align with final code, condense User Requirements, fill "After" state, set Status: Completed, identify CLAUDE.md updates

**Gate:** State **"CHRONICLE INITIATED — [filename]"**

---

## If Chronicle is NOT Needed

1. **Persist the decision:** Update the plan file's WORKFLOW STATE — set `Chronicle: NOT NEEDED — [reason]`. This survives context compaction so Phase 7 doesn't re-evaluate.
2. **Gate:** State **"CHRONICLE: NOT NEEDED — [reason covering all skip criteria above]"**

## Expected Artifacts
- Chronicle file in `docs/chronicles/` (if needed), OR
- WORKFLOW STATE updated with `Chronicle: NOT NEEDED — [reason]`
- WORKFLOW STATE updated: `Current Phase: 4`

**→ Proceed immediately to Phase 4. Read `phase-4-implement.md`.**
