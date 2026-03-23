---
name: adr-update
description: "Update the status of an Architecture Decision Record. Use when asked to 'accept this ADR', 'mark ADR-0003 as implemented', 'deprecate the old database decision', 'this ADR is superseded by ADR-0007', or 'update the status of ADR about X'."
user-invocable: true
argument-hint: "[ADR number or title]"
allowed-tools: Glob, Read, Edit, Bash, AskUserQuestion
metadata:
  author: salvob41
  version: 1.0.1
  category: documentation
---

# ADR Update — Change an ADR's Status

**Announce:** "I'm using the adr-update skill to update this ADR."

---

## Step 1: Find the Target ADR

If `$ARGUMENTS` specifies an ADR number or title keyword, find the matching file:

```bash
ls docs/decisions/ADR-*.md 2>/dev/null | sort
```

If `$ARGUMENTS` is empty or doesn't match, list all ADRs and ask:
> "Which ADR would you like to update? (provide number or title)"

Read the target ADR file to show its current state.

---

## Step 2: Ask What to Change

Use AskUserQuestion to ask:

> "What would you like to change about ADR-NNNN: [title]?"

Options:
1. **Accept** — Change status from Proposed → Accepted
2. **Mark as Implemented** — Change status to Implemented (decision fully deployed)
3. **Deprecate** — Mark as no longer applicable (add a brief reason)
4. **Supersede** — Mark as replaced by a newer ADR (which one?)
5. **Edit content** — Update context, consequences, implementation notes, or diagram
6. **Reopen** — Change status back to Proposed for re-evaluation

---

## Step 3: Apply the Change

### Status changes

Status lives in the `## Status` section. Replace the line after the heading:

**Accept:**
```
## Status
Accepted
```

**Mark as Implemented:**
```
## Status
Implemented
```

**Deprecate:**
```
## Status
Deprecated — [brief reason, e.g. "technology abandoned by vendor"]
```

**Supersede:**
```
## Status
Superseded by [ADR-NNNN: title of newer ADR]
```

If superseding, also update the newer ADR's References section to link back:
```
- Supersedes [ADR-NNNN: title of this ADR]
```

**Reopen:**
```
## Status
Proposed
```

### Content edits

Apply the user's requested edits directly. Show a diff of what changed before saving.

---

## Step 4: Confirm and Save

Show the changed lines and ask:
> "Here's what I'll change. Confirm?"

Apply edits using Edit tool after confirmation.

---

## Step 5: Done

```
Updated: docs/decisions/ADR-NNNN-title.md
Status: [old] → [new]
```
