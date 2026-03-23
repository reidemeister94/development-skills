---
name: adr
description: "Create or document an Architecture Decision Record. Use when making or documenting a significant technical decision — for example, 'document this architectural decision', 'create an ADR for X', 'we decided to use Y instead of Z', 'record this technology choice', or any decision about database schema, API design, authentication, project structure, or coding patterns with lasting consequences."
user-invocable: true
argument-hint: "[decision topic or description]"
allowed-tools: Glob, Read, Write, Edit, AskUserQuestion, Bash
metadata:
  author: salvob41
  version: 1.0.1
  category: documentation
---

# ADR — Create Architecture Decision Record

**Announce:** "I'm using the ADR skill to document this architectural decision."

---

## Step 1: Understand the Decision

Read `**/adr/references/decision-categories.md` (Glob) to know the right questions for the domain.

If `$ARGUMENTS` is provided, use it as starting context. Otherwise ask what decision to document.

Gather in one AskUserQuestion (skip what's already in `$ARGUMENTS`):
1. **What was decided?** (definitive: "We will use X")
2. **Why?** — the problem, constraint, or requirement that triggered this
3. **Alternatives rejected** — what else was evaluated and why it lost
4. **Trade-offs** — what gets harder or more constrained
5. **Status** — Proposed / Accepted / Implemented (default: Accepted)

---

## Step 2: Scan Existing ADRs

```bash
mkdir -p docs/decisions && ls docs/decisions/ADR-*.md 2>/dev/null | sort
```

- Next number = highest existing + 1 (start at 0001 if none).
- Check if any existing ADR is superseded by this one.

---

## Step 3: Generate the ADR

```markdown
# ADR-NNNN: [Verb-phrase title — e.g. "Use PostgreSQL as primary database"]

## Status
Accepted

## Context

[Problem, constraint, or situation that forced this decision. Concrete — reference actual
code, errors, or behaviours. Write for a new team member reading this 6 months from now.]

## Decision

[The decision, stated definitively. Include key reasoning inline. Use tables, code snippets,
or config examples when they help. Can be detailed — clarity beats brevity here.]

## Alternatives Considered

| Alternative | Reason Rejected |
|-------------|-----------------|
| Option A    | Why rejected    |

## Consequences

**Pros:**
- …

**Cons:**
- …

## Architecture / Flow

*(Add when the decision involves a pipeline, data flow, or component interaction.)*

```mermaid
flowchart LR
  A --> B
` ``

## Implementation Notes

*(Add when concrete details matter: code patterns, config values, migration steps, package names.)*

## Follow-ups

*(Open questions or future work spawned by this decision.)*

## References

*(Related ADRs, tickets, or docs.)*
```

Filename: `docs/decisions/ADR-NNNN-kebab-case-title.md`

---

## Step 4: Confirm and Save

Show the full ADR and ask for confirmation before writing the file.
If edits are requested, apply and ask again.

---

## Step 5: Handle Supersession

If this ADR supersedes an existing one, update the old file's Status:

```
## Status
Superseded by [ADR-NNNN: new title]
```

---

## Quality Rules

- **Definitive.** "We will use X" — not "we might consider X".
- **Concrete.** Reference files, error cases, config values — not vague generalities.
- **Honest trade-offs.** Every decision has cons. List them.
- **Verb-phrase title.** "Use PostgreSQL" not "PostgreSQL Decision".
- **Mermaid when relevant.** Any flow, pipeline, or component interaction gets a diagram.
- **Omit empty sections.** Don't include optional sections with placeholder text — only add them if there's real content.

## Examples

### Example 1: Document a technology choice
User says: "We decided to use PostgreSQL instead of MongoDB, create an ADR"
Actions: Gather context → draft ADR with options considered → record decision and rationale → save to docs/adr/
Result: ADR file created with decision, options, and consequences documented

### Example 2: Document an API design decision
User says: "Create an ADR for using REST over GraphQL"
Actions: Ask for context if needed → draft ADR → propose next status (proposed/accepted)
Result: ADR created and ready for team review
