# Phase 3: CHRONICLE CREATION — GATE

**When in doubt, create the chronicle.** Cost: ~30 seconds. Cost of missing one: losing the WHY forever.

**Chronicle IS NEEDED when ANY apply:**
- New feature or endpoint
- Architectural change or new patterns
- Complex bug fix requiring investigation
- Breaking change or API modification
- Multi-file refactoring with design decisions
- Business logic where WHY isn't obvious
- Significant research or discovery

**Chronicle NOT NEEDED when ALL apply:**
- Single-line or trivial fix
- No new patterns or architectural decisions
- Change is self-evident from the diff
- No business context worth preserving

---

## If Chronicle IS Needed

**Announce:** "Creating chronicle to capture task context."

### Create the Chronicle File

1. `mkdir -p docs/chronicles/`
2. Find next number: `ls docs/chronicles/*.md 2>/dev/null | sort | tail -1` — increment (start at 0001)
3. Write using template below
4. Fill: User Requirements, Context, Objective (WHY), Project State (before), Affected Areas

**Naming:** `docs/chronicles/NNNN__YYYY-MM-DD__brief-description.md`

### Template

```markdown
# [Brief Title]

> Chronicle: NNNN__YYYY-MM-DD__brief-description.md
> Status: Draft | In Progress | Completed

## User Requirements (Complete)

[FULL user communication — requirements, constraints, preferences. Preserve ALL signal.]

## Context

[Background from research. Project state, technical context.]

**Key references:**
- `path/to/module/` - [why involved]

## Project State

**Before:** [State before work]
**After:** [Updated during finalization]

## Objective (The WHY)

[WHY this change. Business context, user needs, problems.]

## Affected Areas

| Area | Files/Modules | Impact |
|------|---------------|--------|
| [Component] | `path/` | [Change] |

## Discoveries & Insights

- **[Date]**: [Discovery or insight]

---

## CLAUDE.md Updates

### Updates to apply:

- [ ] `CLAUDE.md` - [What to add/update]
```

### Lifecycle

- **Phase 4:** Update Discoveries, record design decisions
- **Phase 7:** Align with final code, condense User Requirements, fill "After" state, set Completed, identify CLAUDE.md updates

**Gate:** State **"CHRONICLE INITIATED — [filename]"**

---

## If Chronicle NOT Needed

1. Update plan file WORKFLOW STATE: `Chronicle: NOT NEEDED — [reason]`
2. **Gate:** State **"CHRONICLE: NOT NEEDED — [reason]"**

## Expected Artifacts
- Chronicle file in `docs/chronicles/` (if needed), OR WORKFLOW STATE with `NOT NEEDED`
- WORKFLOW STATE: `Current Phase: 4`

**→ Proceed immediately to Phase 4. Read `phase-4-implement.md`.**
