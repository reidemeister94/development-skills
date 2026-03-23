---
name: adr-list
description: "List and browse Architecture Decision Records. Use when asked to 'show all ADRs', 'list our architecture decisions', 'find the ADR about X', 'what decisions have we made about Y', or 'browse our decision records'."
user-invocable: true
argument-hint: "[optional: filter keyword]"
allowed-tools: Glob, Read, Bash
metadata:
  author: salvob41
  version: 1.0.1
  category: documentation
---

# ADR List — Browse Architecture Decision Records

**Announce:** "I'm using the adr-list skill to show architecture decisions."

---

## Step 1: Find ADRs

```bash
ls docs/decisions/ADR-*.md 2>/dev/null | sort
```

If no files found:
> "No ADRs found in `docs/decisions/`. Run `/adr` to document your first architectural decision."
Stop.

---

## Step 2: Read and Summarize

For each ADR file, read the first ~30 lines to extract:
- ADR number and title (from filename and H1)
- Status (the line immediately after the `## Status` heading)
- First sentence of the Decision section (the "what was decided" summary)

If `$ARGUMENTS` is provided, filter results to ADRs whose title or content contains the keyword.

---

## Step 3: Display

Show a clean table:

```
Architecture Decision Records — docs/decisions/
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  #     Status           Title
  ────  ───────────────  ──────────────────────────────────────────
  0001  ✓ Accepted       Use PostgreSQL as primary database
  0002  ✓ Implemented    Adopt hashicorp/go-retryablehttp for HTTP clients
  0003  ~ Proposed       Migrate authentication to JWT
  0004  ✗ Deprecated     Use Redis for session storage
  0005  ↪ Superseded     Use monolithic architecture

Total: 5 ADRs  (1 accepted, 1 implemented, 1 proposed, 1 deprecated, 1 superseded)
```

Status symbols:
- `✓ Accepted` — decision made, not yet fully deployed
- `✓ Implemented` — decision made and fully deployed
- `~ Proposed` — under discussion
- `✗ Deprecated` — no longer applies
- `↪ Superseded` — replaced by another ADR

---

## Step 4: Offer Actions

After displaying the list, say:
> "Run `/adr` to document a new decision, or `/adr-update ADR-NNNN` to change a decision's status."

If the user asked about a specific topic (filter was active), highlight the matching ADRs.
